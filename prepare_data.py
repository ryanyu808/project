"""Offline candidate export and gated finalization. Never imported by the page."""
import argparse
import json
import os
from pathlib import Path
import tempfile
import pandas as pd
from configuration import ROOT
from contracts import (ORIGINAL, DERIVED, MECHANISMS, SEVERE, BASELINES, sha256,
                       require_columns, integer_series, booleans, normalize_lookup,
                       validate_visits, validate_source_evidence)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def codebook_text():
    # Copy the approved definitions verbatim from the supplied specification.
    prompt = (ROOT / 'one-shot-prompt.md').read_text(encoding='utf-8')
    lines = prompt.splitlines()
    rows = [line for line in lines if any(line.startswith(f'| {i} | `') for i in range(1, 7))]
    result = ['Version: 1.0', '', '| injury_mechanism | definition | overlap_rule |', '|---|---|---|']
    for row in rows:
        cells = row.split('|')[2:-1]
        result.append('|' + '|'.join(cells) + '|')
    return '\n'.join(result) + '\n'


def ensure_docs(output):
    book = output / 'mechanism-codebook.md'
    expected = codebook_text()
    if book.exists() and book.read_text(encoding='utf-8') != expected:
        raise ValueError(f'{book}: differs from approved Version: 1.0 codebook')
    book.write_text(expected, encoding='utf-8')
    (output / 'README.md').write_text('''# Prepared treadmill cohort

One row is one ED visit. The original 25 fields and narratives are retained.
`adult_65_plus`: age integer years 65–120 (not age 0 or infant-month codes).
`has_product_3277`: code 3277 in any of Product_1/2/3.
`mentions_treadmill`: case-insensitive literal TREADMILL in Narrative_1.
All three flags must be true. `treatment_year` comes from Treatment_Date.
`is_severe`: disposition 2/4/5/8, false for other or missing outcomes.
`injury_mechanism`: human-reviewed, mutually exclusive Version: 1.0 codebook label.
Unknown/Unclassified is a reviewed unclear mechanism, never unfinished review.
Primary Diagnosis alone is used in composition. Secondary blanks are retained.
XLSX dates use the explicit NEISS_year sheet; annual TSV dates are MM/DD/YYYY;
sample dates are ISO. CSV outputs use ISO dates and explicit true/false flags.

Candidate, blank review, source evidence and quality files are audit artifacts,
ignored by git and never read by the dashboard. Preserve them locally. Candidate
SHA-256 binds finalization to the export. Final CSV/provenance bind the runtime
cohort. No estimates may be published until every candidate is human-reviewed.
The complete lookup is copied unchanged to ../reference/ and comes from the
dataset repository's complete 2025 four-column reference, not a sampled lookup.
''', encoding='utf-8')


def candidates(source, year, source_scope, output_dir, lookup=None, *, _source_validator=None):
    source, output = Path(source), Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    quality_path = output / f'treadmill_{year}.quality.json'
    quality = {'year': year, 'source': str(source), 'exceptions': []}
    try:
        is_xlsx = source.suffix.lower() == '.xlsx'
        if is_xlsx:
            data = pd.read_excel(source, sheet_name=f'NEISS_{year}', engine='openpyxl', dtype={'CPSC_Case_Number': 'string'}, keep_default_na=False, na_values=[''])
            reference = pd.read_excel(source, sheet_name='NEISS_FMT', engine='openpyxl', dtype=str)
        else:
            data = pd.read_csv(source, sep='\t' if source.suffix.lower() == '.tsv' else ',', dtype={'CPSC_Case_Number': 'string'}, keep_default_na=False, na_values=[''], low_memory=False)
            reference = pd.read_csv(lookup or ROOT / 'data/reference/neiss_code_lookup_2025.csv', dtype=str)
        normalized_reference = normalize_lookup(reference)
        if is_xlsx:
            complete = normalize_lookup(pd.read_csv(ROOT / 'data/reference/neiss_code_lookup_2025.csv', dtype=str))
            def relevant_labels(table):
                table = table.loc[table['Format name'].isin(['DIAG', 'DISP', 'PROD'])].copy()
                table['_code'] = pd.to_numeric(table['Starting value for format'], errors='coerce')
                table = table.loc[table['Format name'].ne('PROD') | table['_code'].eq(3277)]
                if table.duplicated(['Format name', '_code']).any():
                    raise ValueError('Relevant lookup keys must be unique by format and code')
                return {(r['Format name'], int(r['_code'])): r['Format value label'] for _, r in table.iterrows()}
            annual_labels, supplied_labels = relevant_labels(normalized_reference), relevant_labels(complete)
            quality['lookup_discrepancies_vs_2025'] = [dict(format=k[0], code=k[1], annual=annual_labels.get(k), reference_2025=supplied_labels.get(k))
                for k in sorted(set(annual_labels) | set(supplied_labels)) if annual_labels.get(k) != supplied_labels.get(k)]
        quality.update(source_row_count=len(data), source_column_count=len(data.columns),
                       source_columns=list(data.columns), missingness={c: int(v) for c, v in data.isna().sum().items()},
                       duplicate_ids=int(data.CPSC_Case_Number.duplicated().sum()) if 'CPSC_Case_Number' in data else None)
        if list(data.columns) != ORIGINAL:
            raise ValueError('Source schema differs from original 25 columns; confirm official source revision')
        dates = pd.to_datetime(data.Treatment_Date, format='%m/%d/%Y' if source.suffix.lower() == '.tsv' else ('%Y-%m-%d' if not is_xlsx else None), errors='coerce')
        weights = pd.to_numeric(data.Weight, errors='coerce')
        import numpy as np
        bad = {
            'invalid_dates': dates.isna(),
            'invalid_ids': data.CPSC_Case_Number.isna() | data.CPSC_Case_Number.str.strip().eq('') | data.CPSC_Case_Number.duplicated(keep=False),
            'invalid_weights': weights.isna() | ~np.isfinite(weights) | weights.le(0),
        }
        for name, mask in bad.items():
            quality[name] = int(mask.sum())
            quality['exceptions'].extend({'check': name, 'source_row': int(i) + 2, 'id': str(data.loc[i, 'CPSC_Case_Number'])} for i in data.index[mask])
        if any(mask.any() for mask in bad.values()):
            raise ValueError('Structural source failure: invalid dates/IDs/weights; see quality exceptions')
        evidence = {
            'schema_version': 1, 'analysis_years': [year], 'source_scope': source_scope,
            'source_checks_passed': True,
            'source_files': [{'path': str(source), 'sha256': sha256(source), 'row_count': len(data), 'column_count': len(data.columns),
                              'min_date': dates.min().date().isoformat(), 'max_date': dates.max().date().isoformat()}],
        }
        (_source_validator or validate_source_evidence)(evidence, year)
        quality['date_coverage'] = [evidence['source_files'][0]['min_date'], evidence['source_files'][0]['max_date']]
        cleaned = data.copy()
        cleaned['Treatment_Date'] = dates
        cleaned['Weight'] = weights
        for col in ['Age', 'Product_1', 'Product_2', 'Product_3', 'Disposition', 'Diagnosis']:
            cleaned[col] = integer_series(cleaned[col], col, nullable=col not in ['Age', 'Product_1', 'Product_2', 'Product_3'])
        cleaned['adult_65_plus'] = cleaned.Age.between(65, 120)
        cleaned['has_product_3277'] = cleaned[['Product_1', 'Product_2', 'Product_3']].eq(3277).any(axis=1)
        cleaned['mentions_treadmill'] = cleaned.Narrative_1.astype('string').str.contains('TREADMILL', case=False, regex=False, na=False)
        cleaned['treatment_year'] = dates.dt.year
        cleaned['is_severe'] = cleaned.Disposition.isin(SEVERE)
        mask = cleaned.adult_65_plus & cleaned.has_product_3277 & cleaned.mentions_treadmill & cleaned.treatment_year.eq(year)
        cohort = cleaned.loc[mask].copy()
        # Do not invent labels or represent machine suggestions as completed review.
        target = output / f'treadmill_{year}.candidates.csv'
        review_path = output / f'treadmill_{year}.reviews.csv'
        if target.exists() or review_path.exists():
            raise ValueError('Candidate/review output already exists; use a new output directory to preserve review work')
        cohort.to_csv(target, index=False, date_format='%Y-%m-%d')
        reviews = pd.DataFrame({'CPSC_Case_Number': cohort.CPSC_Case_Number, 'treadmill_confirmed': '', 'injury_mechanism': '', 'reviewed': False, 'review_note': ''})
        reviews.to_csv(review_path, index=False)
        evidence.update(candidate_sha256=sha256(target), candidate_row_count=len(cohort), lookup_sha256=sha256(lookup or ROOT / 'data/reference/neiss_code_lookup_2025.csv') if not is_xlsx else None,
                        lookup_verification='Annual NEISS_FMT used' if is_xlsx else 'Complete 2025 reference supplied by dataset repository; no separate annual NEISS_FMT comparison available for TSV')
        write_json(output / f'treadmill_{year}.source.json', evidence)
        quality.update(age_eligible_count=int(cleaned.adult_65_plus.sum()),
                       age_product_count=int((cleaned.adult_65_plus & cleaned.has_product_3277).sum()),
                       candidate_count=len(cohort), review_status='pending', retained_count=None, reviewed_excluded_count=None)
        ensure_docs(output)
        return target
    except Exception as exc:
        quality['error'] = str(exc)
        raise
    finally:
        write_json(quality_path, quality)


def finalize(candidate_path, review_path, codebook_path, output_dir, *, _source_validator=None, _labels=None):
    candidate_path, review_path, codebook_path, output = map(Path, (candidate_path, review_path, codebook_path, output_dir))
    output.mkdir(parents=True, exist_ok=True)
    stem = candidate_path.name.replace('.candidates.csv', '')
    evidence = json.loads(candidate_path.with_name(stem + '.source.json').read_text(encoding='utf-8'))
    year = evidence['analysis_years'][0]
    quality_path = candidate_path.with_name(stem + '.quality.json')
    quality = json.loads(quality_path.read_text(encoding='utf-8'))
    try:
        (_source_validator or validate_source_evidence)(evidence, year)
        raw_source = Path(evidence['source_files'][0]['path'])
        if sha256(raw_source) != evidence['source_files'][0]['sha256']:
            raise ValueError('Raw source bytes changed since candidate export; restore source and re-export')
        if sha256(candidate_path) != evidence['candidate_sha256']:
            raise ValueError('Candidate bytes changed since export; re-export and review again')
        if codebook_path.read_text(encoding='utf-8') != codebook_text() and _labels is None:
            raise ValueError('Codebook differs from approved Version: 1.0 definitions')
        labels = _labels or MECHANISMS
        cohort = pd.read_csv(candidate_path, dtype={'CPSC_Case_Number': 'string'}, keep_default_na=False, na_values=[''])
        reviews = pd.read_csv(review_path, dtype={'CPSC_Case_Number': 'string'}, keep_default_na=False)
        require_columns(reviews, ['CPSC_Case_Number', 'treadmill_confirmed', 'injury_mechanism', 'reviewed', 'review_note'])
        if len(cohort) != evidence['candidate_row_count'] or cohort.CPSC_Case_Number.duplicated().any() or reviews.CPSC_Case_Number.duplicated().any() or reviews.CPSC_Case_Number.eq('').any():
            raise ValueError('Candidate/review IDs must be unique; candidate count must match export')
        if set(cohort.CPSC_Case_Number) != set(reviews.CPSC_Case_Number):
            raise ValueError('Candidate/review ID sets differ; every candidate requires exactly one review')
        if not booleans(reviews.reviewed, 'reviewed').all():
            raise ValueError('Human review pending: every candidate requires reviewed=true')
        reviews['treadmill_confirmed'] = booleans(reviews.treadmill_confirmed, 'treadmill_confirmed')
        keep = reviews.treadmill_confirmed
        if not reviews.loc[keep, 'injury_mechanism'].isin(labels).all():
            raise ValueError('Retained review injury_mechanism absent from approved codebook')
        if reviews.loc[~keep, 'review_note'].str.strip().eq('').any():
            raise ValueError('Excluded review requires a review_note reason')
        joined = cohort.merge(reviews[['CPSC_Case_Number', 'treadmill_confirmed', 'injury_mechanism']], on='CPSC_Case_Number', validate='one_to_one')
        # Validate even excluded candidates for tampered structural fields.
        joined.loc[~joined.treadmill_confirmed, 'injury_mechanism'] = labels[-1]
        validate_visits(joined, [year], cohort=True, labels=labels)
        final = joined.loc[joined.treadmill_confirmed, ORIGINAL + DERIVED].copy()
        quality.update(review_status='complete', reviewed_candidate_count=len(reviews), retained_count=len(final), reviewed_excluded_count=int((~keep).sum()),
                       review_exclusions=reviews.loc[~keep, ['CPSC_Case_Number', 'review_note']].to_dict('records'))
        provenance = {key: evidence[key] for key in ['schema_version', 'analysis_years', 'source_scope', 'source_checks_passed', 'source_files']}
        provenance.update(prepared_row_count=len(final), review_complete=True, reviewed_candidate_count=len(reviews), codebook_version='1.0',
                          review_sha256=sha256(review_path), codebook_sha256=sha256(codebook_path))
        # Stage both files before publishing; digest validation catches interrupted pair replacement.
        with tempfile.TemporaryDirectory(dir=output) as temporary:
            staged = Path(temporary) / (stem + '.csv')
            final.to_csv(staged, index=False, date_format='%Y-%m-%d')
            provenance['prepared_sha256'] = sha256(staged)
            staged_prov = Path(temporary) / (stem + '.provenance.json')
            write_json(staged_prov, provenance)
            os.replace(staged, output / staged.name)
            os.replace(staged_prov, output / staged_prov.name)
        write_json(output / (stem + '.quality.json'), quality)
        return output / (stem + '.csv')
    except Exception as exc:
        quality['finalization_error'] = str(exc)
        write_json(quality_path, quality)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='phase', required=True)
    export = commands.add_parser('candidates')
    export.add_argument('--source', required=True)
    export.add_argument('--year', type=int, choices=BASELINES, required=True)
    export.add_argument('--source-scope', choices=['full_annual', 'sample'], required=True)
    export.add_argument('--lookup', default='data/reference/neiss_code_lookup_2025.csv')
    export.add_argument('--output-dir', default='data/prepared')
    finish = commands.add_parser('finalize')
    for arg in ['candidates', 'reviews', 'codebook', 'output-dir']:
        finish.add_argument('--' + arg, required=True)
    args = vars(parser.parse_args())
    phase = args.pop('phase')
    for key in ['source', 'lookup', 'output_dir', 'candidates', 'reviews', 'codebook']:
        if key in args:
            args[key] = ROOT / args[key]
    try:
        if phase == 'candidates':
            print(candidates(**args))
        else:
            print(finalize(args['candidates'], args['reviews'], args['codebook'], args['output_dir']))
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f'Preparation failed: {exc}\n')


if __name__ == '__main__':
    main()
