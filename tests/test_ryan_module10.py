"""Ryan's Module 10 tests; all injury records are invented."""
from pathlib import Path

import pandas as pd
import pytest

from contracts import ORIGINAL
from prepare_data import candidates, finalize


LOOKUP = Path(__file__).resolve().parents[1] / 'data/reference/neiss_code_lookup_2025.csv'


def invented_records():
    rows = []
    for case, date, weight in [
        ('RYAN-A', '2025-02-03', 10),
        ('RYAN-B', '2025-12-31', 20),
    ]:
        row = dict.fromkeys(ORIGINAL, '')
        row.update(
            CPSC_Case_Number=case, Treatment_Date=pd.Timestamp(date), Age=70,
            Product_1=3277, Product_2=0, Product_3=0, Weight=weight,
            Disposition=4, Diagnosis=57, Narrative_1='Fell while using treadmill',
            Stratum='S', PSU=1,
        )
        rows.append(row)
    return pd.DataFrame(rows, columns=ORIGINAL)


def small_source_validator(provenance, year):
    # Permit two invented records instead of official annual/sample row counts.
    assert year == 2025
    assert provenance['analysis_years'] == [2025]
    assert provenance['source_checks_passed'] is True
    assert provenance['source_files'][0]['row_count'] == 2
    assert provenance['source_files'][0]['column_count'] == 25


@pytest.mark.parametrize('file_format', ['xlsx', 'tsv'])
def test_annual_ingestion_preserves_dates_and_selects_year(tmp_path, file_format):
    frame = invented_records()
    source = tmp_path / f'annual.{file_format}'
    if file_format == 'xlsx':
        decoy = frame.copy()
        decoy['CPSC_Case_Number'] = ['DECOY-A', 'DECOY-B']
        decoy['Treatment_Date'] = pd.to_datetime(['2024-02-03', '2024-12-31'])
        with pd.ExcelWriter(source, engine='openpyxl') as workbook:
            decoy.to_excel(workbook, sheet_name='NEISS_2024', index=False)
            frame.to_excel(workbook, sheet_name='NEISS_2025', index=False)
            pd.read_csv(LOOKUP, dtype=str).to_excel(
                workbook, sheet_name='NEISS_FMT', index=False,
            )
    else:
        frame.to_csv(source, sep='\t', date_format='%m/%d/%Y', index=False)

    target = candidates(
        source, 2025, 'sample', tmp_path / 'out', LOOKUP,
        _source_validator=small_source_validator,
    )
    exported = pd.read_csv(target, dtype={'CPSC_Case_Number': str})
    # Compare by ID: output row order is not part of this test's contract.
    actual = exported.set_index('CPSC_Case_Number').sort_index()
    assert actual.index.tolist() == ['RYAN-A', 'RYAN-B']
    assert actual['Treatment_Date'].tolist() == ['2025-02-03', '2025-12-31']
    assert actual['treatment_year'].tolist() == [2025, 2025]


def test_finalize_rejects_changed_raw_source(tmp_path):
    frame = invented_records()
    source = tmp_path / 'raw.csv'
    frame.to_csv(source, date_format='%Y-%m-%d', index=False)
    output = tmp_path / 'out'
    target = candidates(
        source, 2025, 'sample', output, LOOKUP,
        _source_validator=small_source_validator,
    )
    review_path = output / 'treadmill_2025.reviews.csv'
    pd.DataFrame({
        'CPSC_Case_Number': ['RYAN-A', 'RYAN-B'],
        'treadmill_confirmed': [True, True],
        'injury_mechanism': ['Fall', 'Fall'],
        'reviewed': [True, True],
        'review_note': ['Reviewed invented fall', 'Reviewed invented fall'],
    }).to_csv(review_path, index=False)
    codebook = output / 'mechanism-codebook.md'
    evidence_path = output / 'treadmill_2025.source.json'
    unchanged = {p: p.read_bytes() for p in (target, review_path, evidence_path)}

    # A successful control proves these reviews and candidates are otherwise valid.
    control = finalize(
        target, review_path, codebook, tmp_path / 'control',
        _source_validator=small_source_validator,
    )
    assert control.is_file()

    frame.loc[0, 'Weight'] = 11
    frame.to_csv(source, date_format='%Y-%m-%d', index=False)
    with pytest.raises(ValueError, match='Raw source bytes changed'):
        finalize(
            target, review_path, codebook, output,
            _source_validator=small_source_validator,
        )
    assert not (output / 'treadmill_2025.csv').exists()
    assert not (output / 'treadmill_2025.provenance.json').exists()
    for path, original_bytes in unchanged.items():
        assert path.read_bytes() == original_bytes
