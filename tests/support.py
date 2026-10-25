"""Explicitly isolated UI fixture; never loaded from production config."""
import pandas as pd
from tests.conftest import fixture_data, ROOT


def fixture_loader():
    return dict(data=fixture_data(), diagnosis_lookup=pd.read_csv(ROOT / 'data/reference/neiss_code_lookup_2025.csv',dtype=str),
                provenance=dict(analysis_years=[2025],source_scope='test_fixture'), metadata={})


def fixture_app():
    from app import main
    from tests.support import fixture_loader
    main(_test_loader=fixture_loader)
