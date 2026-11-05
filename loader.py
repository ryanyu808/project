"""Validated prepared-artifact loading. Never opens raw annual files."""
import json
from pathlib import Path
import pandas as pd
from contracts import (sha256, normalize_lookup, validate_visits, validate_source_evidence,
                       validate_digest, MECHANISMS, CODEBOOK_VERSION)

LOADER_VERSION = 2


def _load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year, *, source_validator=validate_source_evidence, labels=MECHANISMS):
    prepared_path, provenance_path, diagnosis_lookup_path = map(Path, (prepared_path, provenance_path, diagnosis_lookup_path))
    try:
        provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
        source_validator(provenance, analysis_year)
        for name in ['prepared_sha256', 'review_sha256', 'codebook_sha256']:
            validate_digest(provenance.get(name), f'provenance.{name}')
        if provenance.get('review_complete') is not True or provenance.get('codebook_version') != CODEBOOK_VERSION:
            raise ValueError('provenance: complete human review and codebook_version ' + CODEBOOK_VERSION + ' required')
        count = provenance.get('prepared_row_count')
        reviewed = provenance.get('reviewed_candidate_count')
        if type(count) is not int or type(reviewed) is not int or count < 0 or reviewed < count:
            raise ValueError('provenance: invalid prepared/reviewed counts')
        from codebook import CODEBOOK_PATH, read_codebook
        read_codebook(CODEBOOK_PATH)
        if sha256(CODEBOOK_PATH) != provenance['codebook_sha256']:
            raise ValueError('codebook_sha256 mismatch; use the reviewed matching taxonomy')
        if 'diagnosis_lookup_sha256' in provenance:
            validate_digest(provenance['diagnosis_lookup_sha256'], 'diagnosis_lookup_sha256')
            if sha256(diagnosis_lookup_path) != provenance['diagnosis_lookup_sha256']:
                raise ValueError('diagnosis_lookup_sha256 mismatch')
        if sha256(prepared_path) != provenance['prepared_sha256']:
            raise ValueError('prepared_sha256 mismatch; rebuild the matching artifact/provenance pair')
        data = pd.read_csv(prepared_path, dtype={'CPSC_Case_Number': 'string'}, keep_default_na=False, na_values=[''])
        if len(data) != count:
            raise ValueError('prepared_row_count does not match CSV')
        data = validate_visits(data, [analysis_year], cohort=True, labels=labels)
        lookup = normalize_lookup(pd.read_csv(diagnosis_lookup_path, dtype=str))
        metadata = {
            'available_treatment_years': provenance['analysis_years'],
            'age_min': int(data.Age.min()) if len(data) else None,
            'age_max': int(data.Age.max()) if len(data) else None,
            'prepared_record_count': len(data),
            'record_counts_by_year': {analysis_year: len(data)},
            'record_counts_by_mechanism': {k: int(v) for k, v in data.injury_mechanism.value_counts().items()},
        }
        return dict(data=data, diagnosis_lookup=lookup, provenance=provenance, metadata=metadata)
    except FileNotFoundError:
        raise
    except (ValueError, TypeError, KeyError) as exc:
        raise ValueError(f'{prepared_path} / {provenance_path} / {diagnosis_lookup_path}: {exc}. Rebuild/validate prepared artifacts offline.') from exc


def load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year):
    return _load_dashboard_data(prepared_path, provenance_path, diagnosis_lookup_path, analysis_year)
