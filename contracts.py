"""Shared validation and normalization; no UI, source I/O, or classifications."""
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ORIGINAL = 'CPSC_Case_Number Treatment_Date Age Sex Race Other_Race Hispanic Body_Part Diagnosis Other_Diagnosis Body_Part_2 Diagnosis_2 Other_Diagnosis_2 Disposition Location Fire_Involvement Product_1 Product_2 Product_3 Alcohol Drug Narrative_1 Stratum PSU Weight'.split()
DERIVED = ['adult_65_plus', 'has_product_3277', 'mentions_treadmill', 'treatment_year', 'is_severe', 'injury_mechanism']
LOOKUP = ['Format name', 'Starting value for format', 'Ending value for format', 'Format value label']
MECHANISMS = ['Repair/moving', 'Entering/exiting', 'Belt contact', 'Struck by equipment', 'Fall', 'Unknown/Unclassified']
SEVERE = {2, 4, 5, 8}
KNOWN = {0, 1, 2, 4, 5, 6, 8}
BASELINES = {2023: 338262, 2024: 361672, 2025: 410201}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def require_columns(data, columns):
    missing = set(columns) - set(data.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')


def integer_series(series, name, nullable=True):
    values = pd.to_numeric(series, errors='coerce')
    nonblank = series.notna() & series.astype('string').str.strip().ne('')
    bad = (nonblank & values.isna()) | (values.notna() & (~np.isfinite(values) | values.mod(1).ne(0)))
    if bad.any() or (not nullable and values.isna().any()):
        raise ValueError(f'{name}: invalid integer codes at rows {series.index[bad | values.isna()].tolist()[:10]}')
    return values.astype('Int64')


def booleans(series, name):
    parsed = series.astype('string').str.lower().map({'true': True, 'false': False})
    if parsed.isna().any():
        raise ValueError(f'{name}: require nonnull true/false Boolean values')
    return parsed.astype(bool)


def severity_display(disposition):
    return pd.Series(np.select([disposition.isin(SEVERE), disposition.isin(KNOWN)],
                              ['Severe', 'Other known disposition'], default='Unknown'), index=disposition.index)


def normalize_lookup(lookup):
    require_columns(lookup, LOOKUP)
    lookup = lookup[LOOKUP].copy()
    for col in LOOKUP:
        lookup[col] = lookup[col].astype('string').str.strip()
    diag = lookup['Format name'].eq('DIAG')
    keys = integer_series(lookup.loc[diag, LOOKUP[1]], 'DIAG lookup keys', nullable=False)
    if keys.duplicated().any():
        raise ValueError('DIAG lookup: duplicate keys; many-to-one join required')
    if lookup.loc[diag, LOOKUP[3]].isna().any() or lookup.loc[diag, LOOKUP[3]].eq('').any():
        raise ValueError('DIAG lookup: missing labels')
    lookup.loc[diag, LOOKUP[1]] = keys.astype('string')
    return lookup


def validate_visits(data, years, *, cohort=False, labels=None):
    """Return normalized copy, rejecting malformed rows rather than dropping them."""
    needed = ORIGINAL + DERIVED if cohort else ['CPSC_Case_Number', 'Treatment_Date', 'Weight', 'Disposition', 'Diagnosis', 'injury_mechanism', 'is_severe']
    require_columns(data, needed)
    frame = data.copy()
    ids = frame.CPSC_Case_Number.astype('string')
    if ids.isna().any() or ids.str.strip().eq('').any() or ids.duplicated().any():
        raise ValueError('CPSC_Case_Number: missing/duplicate visit IDs')
    frame['CPSC_Case_Number'] = ids
    dates = pd.to_datetime(frame.Treatment_Date, format='ISO8601', errors='coerce')
    if dates.isna().any() or not dates.dt.year.isin(years).all():
        raise ValueError('Treatment_Date: invalid dates or dates outside analysis_years')
    frame['Treatment_Date'] = dates
    weights = pd.to_numeric(frame.Weight, errors='coerce')
    if weights.isna().any() or not (np.isfinite(weights) & weights.gt(0)).all():
        raise ValueError('Weight: require finite positive survey weights')
    frame['Weight'] = weights.astype(float)
    for col in ['Disposition', 'Diagnosis']:
        frame[col] = integer_series(frame[col], col)
    frame['is_severe'] = booleans(frame.is_severe, 'is_severe')
    if not frame.is_severe.eq(frame.Disposition.isin(SEVERE)).all():
        raise ValueError('is_severe: inconsistent with Disposition mapping (2/4/5/8)')
    mechanisms = frame.injury_mechanism.astype('string')
    if mechanisms.isna().any() or mechanisms.str.strip().eq('').any():
        raise ValueError('injury_mechanism: missing/blank reviewed label')
    if labels is not None and not mechanisms.isin(labels).all():
        raise ValueError('injury_mechanism: label absent from approved codebook')
    if cohort:
        for col in ['Age', 'Product_1', 'Product_2', 'Product_3', 'treatment_year']:
            frame[col] = integer_series(frame[col], col, nullable=False)
        expected = {
            'adult_65_plus': frame.Age.between(65, 120),
            'has_product_3277': frame[['Product_1', 'Product_2', 'Product_3']].eq(3277).any(axis=1),
            'mentions_treadmill': frame.Narrative_1.astype('string').str.contains('TREADMILL', case=False, regex=False, na=False),
        }
        for col, flag in expected.items():
            frame[col] = booleans(frame[col], col)
            if not flag.all() or not frame[col].eq(flag).all():
                raise ValueError(f'{col}: inconsistent cohort eligibility')
        if not frame.treatment_year.eq(dates.dt.year).all():
            raise ValueError('treatment_year: must match Treatment_Date')
    return frame


def validate_source_evidence(provenance, year):
    if not isinstance(provenance, dict):
        raise ValueError('provenance: expected a JSON object')
    if type(provenance.get('schema_version')) is not int or provenance.get('schema_version') != 1 or provenance.get('analysis_years') != [year]:
        raise ValueError('provenance: schema_version/year mismatch')
    scope = provenance.get('source_scope')
    if scope not in ('full_annual', 'sample'):
        raise ValueError('provenance.source_scope: expected full_annual or sample')
    if provenance.get('source_checks_passed') is not True:
        raise ValueError('provenance: raw-source checks failed; verify official annual source')
    sources = provenance.get('source_files')
    if not isinstance(sources, list) or len(sources) != 1:
        raise ValueError('provenance.source_files: require exactly one source')
    source = sources[0]
    if not isinstance(source, dict):
        raise ValueError('provenance.source_files: expected a source object')
    for key in ['path', 'sha256', 'row_count', 'column_count', 'min_date', 'max_date']:
        if key not in source:
            raise ValueError(f'provenance.source_files: missing {key}')
    if not isinstance(source['path'], str) or not source['path'].strip():
        raise ValueError('provenance: missing source path')
    validate_digest(source['sha256'], 'source sha256')
    if type(source['row_count']) is not int or type(source['column_count']) is not int:
        raise ValueError('provenance: source counts must be integers')
    if scope == 'full_annual':
        if (source['row_count'], source['column_count'], source['min_date'], source['max_date']) != (BASELINES[year], 25, f'{year}-01-01', f'{year}-12-31'):
            raise ValueError('provenance: full annual baseline count/schema/date coverage mismatch; confirm official revision')
    else:
        if source['row_count'] not in (15000, 20000) or source['column_count'] != 25:
            raise ValueError('provenance: invalid documented sample shape')
        for key in ['min_date', 'max_date']:
            if pd.isna(pd.to_datetime(source[key], errors='coerce')):
                raise ValueError(f'provenance: invalid {key}')


def validate_digest(value, name):
    if not isinstance(value, str) or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError(f'{name}: require SHA-256 hex fingerprint')
