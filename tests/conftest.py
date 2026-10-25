from pathlib import Path
import pandas as pd
import pytest
from contracts import ORIGINAL

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def lookup():
    return pd.read_csv(ROOT / 'data/reference/neiss_code_lookup_2025.csv', dtype=str)


def fixture_data():
    rows = []
    for case, mechanism, weight, disposition, diagnosis, narrative in [
        ('A', 'Fall', 10, 4, 57, 'FELL from treadmill belt'),
        ('B', 'Fall', 30, 1, 53, 'Tripped beside treadmill'),
        ('C', 'Contact', 20, 2, 57, 'Hand caught in BELT'),
        ('D', 'Contact', 40, 9, None, None),
        ('E', 'Unknown/Unclassified', 20, 5, 71, None),
    ]:
        row = dict.fromkeys(ORIGINAL, None)
        row.update(CPSC_Case_Number=case, Treatment_Date=pd.Timestamp('2025-01-01'), Age=70,
                   Product_1=3277, Product_2=0, Product_3=0, Weight=weight, Disposition=disposition,
                   Diagnosis=diagnosis, Narrative_1=narrative, Stratum='S', PSU=1,
                   injury_mechanism=mechanism, is_severe=disposition in (2,4,5,8),
                   adult_65_plus=True, has_product_3277=True, mentions_treadmill=True, treatment_year=2025)
        rows.append(row)
    return pd.DataFrame(rows)


@pytest.fixture
def visits():
    return fixture_data()


@pytest.fixture
def context():
    return dict(analysis_years=[2025], source_scope='test_fixture', filter_description='all')
