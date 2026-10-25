"""Strict configuration, resolved against the application directory."""
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parent
VIEW_IDS = ['headline', 'mechanism_bar', 'severity_scatter', 'diagnosis_stack', 'summary_table']
SCHEMA = {
    'dashboard': {'title': str, 'layout': str, 'available_views': list},
    'analysis': {'year': int},
    'defaults': {'mechanisms': list, 'severities': list, 'narrative_query': str},
    'data': {'prepared_path': str, 'provenance_path': str, 'diagnosis_lookup_path': str},
}


def read_config(path=ROOT / 'config.toml'):
    path = Path(path)
    try:
        with path.open('rb') as f:
            config = tomllib.load(f)
        if set(config) != set(SCHEMA):
            raise ValueError(f'sections must be exactly {list(SCHEMA)}')
        for section, fields in SCHEMA.items():
            if not isinstance(config[section], dict) or set(config[section]) != set(fields):
                raise ValueError(f'{section}: expected exactly {list(fields)}')
            for key, kind in fields.items():
                value = config[section][key]
                if type(value) is not kind:
                    raise ValueError(f'{section}.{key}: expected {kind.__name__}')
                if kind is str and section != 'defaults' and not value.strip():
                    raise ValueError(f'{section}.{key}: must be nonblank')
        if config['dashboard']['layout'] != 'wide':
            raise ValueError('dashboard.layout: must be wide')
        if config['dashboard']['available_views'] != VIEW_IDS:
            raise ValueError(f'dashboard.available_views: require exactly {VIEW_IDS} in that order')
        if config['analysis']['year'] not in (2023, 2024, 2025):
            raise ValueError('analysis.year: expected integer 2023, 2024, or 2025')
        if config['defaults'] != dict(mechanisms=[], severities=[], narrative_query=''):
            raise ValueError('defaults: require empty mechanisms/severities and blank narrative_query')
        return config
    except (OSError, ValueError, TypeError) as exc:
        raise ValueError(f'{path}: {exc}. Correct config.toml before starting.') from exc


def resolve_path(value):
    return (ROOT / value).resolve()
