"""Validate explicit human workbook decisions and export a NEW review CSV.

Default is validation only. Never edits candidates, the workbook, or the original
review template. No approval or reviewed flag is inferred from AI recommendations.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

FIELDS = ['CPSC_Case_Number', 'treadmill_confirmed', 'injury_mechanism', 'reviewed', 'review_note']
POLICY_ID = 'injury-focused-2025-proposed-v2'


def text(value):
    return '' if value is None else str(value).strip()


def explicit_true(value):
    return value is True or (isinstance(value, str) and value.strip().lower() == 'true')


def unique_by_id(rows, name):
    result = {}
    for row in rows:
        case = text(row.get('CPSC_Case_Number'))
        if not case or case in result:
            raise ValueError(f'{name}: missing or duplicate case ID {case!r}')
        result[case] = row
    return result


def approved_labels(codebook):
    body = Path(codebook).read_text(encoding='utf-8')
    if body.splitlines()[0].strip() != 'Version: 1.0':
        raise ValueError('Approved codebook version 1.0 required')
    labels = [line.split('|')[1].strip().strip('`') for line in body.splitlines() if line.startswith('| `')]
    if len(labels) != 6 or len(set(labels)) != 6:
        raise ValueError('Expected six distinct approved mechanism labels')
    return set(labels)


def review_values(workbook):
    """Use the focused human input form, keeping the earlier AI sheet immutable.

    Older workbooks remain readable. Conflicting legacy approvals or edits to
    source AI fields fail loudly rather than silently accepting another tab.
    """
    original = list(workbook['Approval review'].values)
    if 'Human review' not in workbook.sheetnames:
        return original
    current = list(workbook['Human review'].values)
    def records(values):
        headers = list(values[0])
        if len(set(headers)) != len(headers):
            raise ValueError('Duplicate review column headers')
        return [dict(zip(headers,row)) for row in values[1:] if any(v is not None for v in row)]
    old = unique_by_id(records(original),'Original AI audit')
    new = unique_by_id(records(current),'Human review')
    if set(old) != set(new):
        raise ValueError('Human review IDs must match the original AI audit exactly')
    human = ['human_approval','human_inclusion','human_mechanism','human_reviewed','reviewer','human_review_note','human_resolution']
    for case, row in new.items():
        if any(text(old[case].get(k)) for k in human):
            raise ValueError(f'{case}: conflicting legacy human entries; use Human review only and reconcile the prior record explicitly')
        for key in ['Narrative_1','recommended_inclusion','recommended_mechanism','taxonomy_gap','requires_adjudication','reviewed']:
            if row.get(key) != old[case].get(key):
                raise ValueError(f'{case}: source AI field {key} changed; use human correction fields')
    return current


def read_approval_workbook(path):
    from openpyxl import load_workbook
    with Path(path).open('rb') as stream:
        workbook = load_workbook(stream, read_only=True, data_only=False)
        try:
            if not {'Approval review', 'Policy'}.issubset(set(workbook.sheetnames)):
                raise ValueError('Approval review and Policy sheets are required')
            values = review_values(workbook)
            headers = list(values[0])
            if len(set(headers)) != len(headers):
                raise ValueError('Duplicate workbook column headers')
            required = {'CPSC_Case_Number','Narrative_1','recommended_inclusion','recommended_mechanism',
                        'human_approval','human_inclusion','human_mechanism','human_reviewed','reviewer',
                        'human_review_note','human_resolution','requires_adjudication'}
            if not required.issubset(headers):
                raise ValueError('Missing required approval columns')
            rows = [dict(zip(headers,row)) for row in values[1:] if any(v is not None for v in row)]
            policy = {text(row[0]):row[1] for row in workbook['Policy'].iter_rows(min_row=1,max_row=9,values_only=True)}
            return rows, policy
        finally:
            workbook.close()


def validate_approvals(candidates, decisions, policy, labels, candidate_digest):
    if any(isinstance(v,str) and v.lstrip().startswith('=') for v in policy.values()):
        raise ValueError('Formulas cannot stand in for policy approval or identity')
    if policy.get('policy_id') != POLICY_ID or text(policy.get('codebook_version')) != '1.0':
        raise ValueError('Policy identity or codebook version mismatch')
    if policy.get('candidate_sha256') != candidate_digest:
        raise ValueError('Candidate SHA-256 mismatch; review the original matching export')
    if not explicit_true(policy.get('policy_approved_by_human')) or not text(policy.get('policy_approver')):
        raise ValueError('Explicit human policy approval and named approver required')
    if not explicit_true(policy.get('mapping_accepted_by_human')) or not text(policy.get('policy_note')):
        raise ValueError('Human acceptance and explanation of inclusion-to-treadmill_confirmed mapping required')
    source = unique_by_id(candidates,'Candidates')
    reviews = unique_by_id(decisions,'Approvals')
    if not source or set(source) != set(reviews):
        raise ValueError('Approval case IDs must match all candidate IDs exactly')
    output = []
    for case, candidate in source.items():
        row = reviews[case]
        if row.get('Narrative_1') != candidate['Narrative_1']:
            raise ValueError(f'{case}: original narrative changed')
        for key in ['human_approval','human_inclusion','human_mechanism','human_reviewed','reviewer',
                    'human_review_note','human_resolution']:
            if isinstance(row.get(key),str) and row[key].startswith('='):
                raise ValueError(f'{case}: formulas cannot stand in for human decisions')
        approval = text(row.get('human_approval'))
        if approval not in {'Approve','Correct'}:
            raise ValueError(f'{case}: missing approval or deferred case')
        if not explicit_true(row.get('human_reviewed')) or not text(row.get('reviewer')):
            raise ValueError(f'{case}: explicit human_reviewed=True and reviewer name required')
        proposal = text(row.get('recommended_inclusion'))
        proposed_mechanism = text(row.get('recommended_mechanism'))
        if proposal not in {'Include','Exclude','Unresolved'} or proposed_mechanism not in labels:
            raise ValueError(f'{case}: invalid recommendation or mechanism')
        supplied_mechanism = text(row.get('human_mechanism'))
        if supplied_mechanism and supplied_mechanism not in labels:
            raise ValueError(f'{case}: invalid human mechanism')
        supplied_decision = text(row.get('human_inclusion'))
        if approval == 'Approve':
            if proposal == 'Unresolved':
                raise ValueError(f'{case}: unresolved proposal requires explicit human correction')
            if supplied_decision and supplied_decision != proposal:
                raise ValueError(f'{case}: conflicting human decision; use Correct')
            if supplied_mechanism and supplied_mechanism != proposed_mechanism:
                raise ValueError(f'{case}: conflicting human mechanism; use Correct')
            decision, mechanism = proposal, proposed_mechanism
        else:
            decision, mechanism = supplied_decision, supplied_mechanism
            if decision not in {'Include','Exclude'}:
                raise ValueError(f'{case}: human correction must resolve inclusion')
            if decision == 'Include' and mechanism not in labels:
                raise ValueError(f'{case}: included correction needs an approved mechanism')
        if row.get('requires_adjudication') not in (True,False,'True','False','true','false'):
            raise ValueError(f'{case}: invalid adjudication flag')
        if explicit_true(row.get('taxonomy_gap')) and decision == 'Include' and not text(row.get('human_resolution')):
            raise ValueError(f'{case}: taxonomy gap requires an explicit human_resolution explaining the approved codebook mapping')
        note = text(row.get('human_review_note'))
        resolution = text(row.get('human_resolution'))
        if (decision == 'Exclude' or approval == 'Correct') and not note:
            raise ValueError(f'{case}: exclusion/correction requires a human review note')
        if (explicit_true(row.get('requires_adjudication')) or proposal == 'Unresolved') and not (note or resolution):
            raise ValueError(f'{case}: unresolved issue needs a human resolution explanation')
        if decision == 'Include' and mechanism not in labels:
            raise ValueError(f'{case}: invalid included mechanism')
        # Copy only the explicit human verification above; never infer it from AI or approval.
        human_reviewed = 'True' if explicit_true(row['human_reviewed']) else 'False'
        audit_note = f"Human reviewer: {text(row['reviewer'])}; action: {approval}."
        if note: audit_note += ' ' + note
        if resolution: audit_note += ' Resolution: ' + resolution
        output.append(dict(CPSC_Case_Number=case,treadmill_confirmed='True' if decision=='Include' else 'False',
                           injury_mechanism=mechanism if decision=='Include' else '',
                           reviewed=human_reviewed,review_note=audit_note))
    return output


def read_csv(path):
    with Path(path).open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        return list(reader),reader.fieldnames


def export_new_csv(path, rows, forbidden_paths):
    path=Path(path)
    if path.resolve() in {Path(p).resolve() for p in forbidden_paths}:
        raise ValueError('Output may not replace any input or the original review template')
    if path.suffix.lower() != '.csv':
        raise ValueError('Output must be a new .csv file')
    # Exclusive create: do not overwrite an existing output, even if validation succeeded.
    with path.open('x',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS)
        writer.writeheader();writer.writerows(rows)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['workbook','candidates','template','codebook']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--confirm-human-verification',action='store_true',
                        help='Use only after genuine human verification; does not fill any approval fields')
    args=parser.parse_args(argv)
    candidates,_=read_csv(args.candidates)
    template,fields=read_csv(args.template)
    if fields != FIELDS or set(unique_by_id(template,'Template')) != set(unique_by_id(candidates,'Candidates')):
        raise ValueError('Original review template schema/IDs do not match candidates')
    rows,policy=read_approval_workbook(args.workbook)
    validated=validate_approvals(candidates,rows,policy,approved_labels(args.codebook),hashlib.sha256(args.candidates.read_bytes()).hexdigest())
    counts=dict(total=len(validated),included=sum(r['treadmill_confirmed']=='True' for r in validated),
                excluded=sum(r['treadmill_confirmed']=='False' for r in validated))
    if args.output:
        if not args.confirm_human_verification:
            raise ValueError('Writing requires --confirm-human-verification after genuine human review')
        export_new_csv(args.output,validated,[args.workbook,args.candidates,args.template,args.codebook])
        print(json.dumps(dict(status='new_human_verified_csv_written',output=str(args.output),**counts)))
    else:
        print(json.dumps(dict(status='validation_only_no_files_written',**counts)))
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (ValueError,OSError,KeyError) as exc:
        print(f'Review transfer rejected: {exc}',file=sys.stderr)
        raise SystemExit(2)
