from pathlib import Path
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from tests.support import fixture_app
from tests.conftest import ROOT
from configuration import read_config


def metrics(at):
    return [item.value for item in at.metric]


def test_initial_and_full_filter_reset_cycle():
    at = AppTest.from_function(fixture_app, default_timeout=20).run()
    assert not at.exception
    assert metrics(at) == ['120','5','41.7%']
    assert len(at.get('plotly_chart')) == 3 and len(at.dataframe) == 1
    assert at.multiselect[0].value == [] and at.multiselect[1].value == [] and at.text_input[0].value == ''
    at.multiselect[0].set_value(['Fall']).run()
    assert metrics(at) == ['40','2','25.0%']
    at.multiselect[1].set_value(['Severe']).run()
    at.text_input[0].set_value('belt').run()
    assert metrics(at) == ['10','1','100.0%']
    at.button[0].click().run()
    assert metrics(at) == ['120','5','41.7%']
    at.multiselect[1].set_value(['Severe']).run()
    assert metrics(at) == ['50','3','100.0%']
    assert any('both numerator and denominator' in item.value for item in at.info)
    at.button[0].click().run()
    at.text_input[0].set_value('belt').run()
    assert metrics(at) == ['30','2','100.0%']
    at.text_input[0].set_value('no match whatsoever').run()
    assert metrics(at) == ['0','0','N/A']
    assert at.dataframe[0].value.empty
    assert any('No records match' in item.value for item in at.info)
    assert at.multiselect[0].options == ['Contact','Fall','Unknown/Unclassified']
    at.button[0].click().run()
    assert metrics(at) == ['120','5','41.7%']
    assert not at.exception


def test_real_default_missing_data():
    at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=20).run()
    assert not at.exception
    assert not at.metric
    assert 'Dashboard data unavailable' in at.error[0].value


@pytest.mark.parametrize('change', [
    ('year = 2025','year = "2025"'), ('year = 2025','year = true'),
    ('layout = "wide"','layout = "centered"'), ('narrative_query = ""','narrative_query = "belt"'),
    ('mechanisms = []','mechanisms = ["Fall"]'), ('severities = []','severities = ["Severe"]'),
    ('"headline", "mechanism_bar"','"mechanism_bar", "headline"'),
    ('"severity_scatter"','"headline"'), ('"severity_scatter"','"bogus"'),
    ('"severity_scatter", ',''), ('year = 2025','year = 2025\nunknown = 3'),
])
def test_configuration_errors(tmp_path, change):
    path = tmp_path / 'config.toml'
    path.write_text((ROOT / 'config.toml').read_text().replace(*change))
    with pytest.raises(ValueError, match='config.toml'):
        read_config(path)


def test_cache_and_invalidation(tmp_path, monkeypatch):
    import app
    calls = []
    def counted(*args):
        calls.append(args)
        return {'ok':len(calls)}
    monkeypatch.setattr(app.loader, 'load_dashboard_data', counted)
    paths = [tmp_path / name for name in ['prepared.csv','provenance.json','lookup.csv']]
    for p in paths: p.write_text('a')
    app.cached_load.clear()
    for _ in range(4):
        assert app.cached_load(app.file_fingerprints(paths),2025,1) == {'ok':1}
    assert len(calls) == 1
    paths[0].write_text('changed bytes')
    assert app.cached_load(app.file_fingerprints(paths),2025,1) == {'ok':2}
    assert len(calls) == 2
    app.cached_load.clear()


def test_empty_cohort_and_sample():
    def empty_app():
        from app import main
        from tests.support import fixture_loader
        def empty():
            loaded = fixture_loader()
            loaded['data'] = loaded['data'].iloc[:0]
            return loaded
        main(_test_loader=empty)
    at = AppTest.from_function(empty_app, default_timeout=20).run()
    assert not at.exception
    assert metrics(at) == ['0','0','N/A']
    assert any('No prepared treadmill cases' in item.value for item in at.info)
    def sample_app():
        from app import main
        from tests.support import fixture_loader
        def sample():
            loaded = fixture_loader()
            loaded['provenance']['source_scope'] = 'sample'
            return loaded
        main(_test_loader=sample)
    at = AppTest.from_function(sample_app, default_timeout=20).run()
    assert not at.exception and not at.metric and not at.get('plotly_chart')
    assert any('Full annual NEISS data required' in item.value for item in at.info)


def test_cache_through_widget_reruns_and_failed_refresh(monkeypatch):
    import app
    from tests.support import fixture_loader
    calls = []
    revision = [1]
    def counted(*args):
        calls.append(args)
        if revision[0] == 3:
            raise ValueError('inconsistent derived flag')
        return fixture_loader()
    monkeypatch.setattr(app.loader,'load_dashboard_data',counted)
    monkeypatch.setattr(app,'file_fingerprints',lambda paths: tuple((str(p), revision[0],1) for p in paths))
    app.cached_load.clear()
    at = AppTest.from_string('from app import main\nmain()\n', default_timeout=20).run()
    assert metrics(at) == ['120','5','41.7%'] and len(calls) == 1
    at.multiselect[0].set_value(['Fall']).run()
    at.text_input[0].set_value('belt').run()
    at.button[0].click().run()
    assert len(calls) == 1
    revision[0] = 2
    at.run()
    assert len(calls) == 2
    revision[0] = 3
    at.run()
    assert not at.metric and not at.get('plotly_chart')
    assert 'Prepared data validation failed' in at.error[0].value
    app.cached_load.clear()


def test_configuration_stops_before_loader(tmp_path):
    path = tmp_path/'bad.toml'
    path.write_text((ROOT/'config.toml').read_text().replace('year = 2025', 'year = "2025"'))
    source = f"from app import main\ndef forbidden():\n    raise AssertionError('loader was called')\nmain({str(path)!r}, _test_loader=forbidden)\n"
    at = AppTest.from_string(source, default_timeout=20).run()
    assert not at.exception and not at.metric and not at.multiselect
    assert 'Configuration error' in at.error[0].value
