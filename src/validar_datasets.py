"""Baixa e inspeciona dados oficiais; não treina modelos nem transforma o original."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
import io
import json
import platform
import importlib.metadata

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://cdn.jsdelivr.net/npm/vega-datasets@3.2.1/'
FILES = ['budget.json', 'cars.json', 'seattle-weather.csv', 'penguins.json', 'gapminder.json']


def save_new(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != content:
            raise FileExistsError(f'Arquivo existente diferente: {path}')
        return
    path.write_bytes(content)


def main():
    original = ROOT / 'PUCSP_CS_AI_11_AI_ML_RandomForest.ipynb'
    original_hash = hashlib.sha256(original.read_bytes()).hexdigest()
    metadata = urlopen(BASE + 'datapackage.json', timeout=60).read()
    save_new(ROOT / 'data/metadata/vega_datapackage_3.2.1.json', metadata)
    resources = json.loads(metadata)['resources']
    report = {'release': '3.2.1', 'python': platform.python_version(),
              'packages': {p: importlib.metadata.version(p) for p in
                           ['pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn']},
              'original_notebook_sha256': original_hash,
              'catalog': [{'name': r['name'], 'path': r['path']} for r in resources],
              'datasets': {}}
    for filename in FILES:
        url = BASE + 'data/' + filename
        raw = urlopen(url, timeout=60).read()
        resource = next(r for r in resources if r['path'] == filename)
        expected = resource.get('hash', '')
        actual = 'sha1:' + hashlib.sha1(raw).hexdigest()
        # O manifesto publicado pode conter hash desatualizado. Verificar bytes
        # contra o mesmo tag no repositório oficial, sem ocultar a divergência.
        github_url = 'https://raw.githubusercontent.com/vega/vega-datasets/v3.2.1/data/' + filename
        github_raw = urlopen(github_url, timeout=60).read()
        if raw != github_raw:
            raise ValueError(f'CDN e GitHub divergem: {filename}')
        folder = 'raw' if filename == 'budget.json' else 'alternatives'
        save_new(ROOT / 'data' / folder / filename, raw)
        df = (pd.DataFrame(json.loads(raw)) if filename.endswith('.json')
              else pd.read_csv(io.BytesIO(raw)))
        info = {'url': url, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                'catalog_hash_verified': actual == expected,
                'catalog_sha1': expected, 'download_sha1': actual,
                'github_url': github_url, 'github_bytes_identical': True,
                'rows': len(df), 'columns': len(df.columns),
                'dtypes': df.dtypes.astype(str).to_dict(),
                'nulls': df.isna().sum().astype(int).to_dict(),
                'blank_strings': {c: int(df[c].map(lambda v: isinstance(v, str) and not v.strip()).sum()) for c in df},
                'duplicate_rows': int(df.duplicated().sum()),
                'sources': resource.get('sources', []),
                'description': resource.get('description', '')}
        if filename == 'budget.json':
            years = [c for c in df if c.isdigit()]
            numeric = df[years + ['TQ']].apply(lambda col: pd.to_numeric(col.str.replace(',', '', regex=False), errors='coerce'))
            info['budget_checks'] = {
                'years': years,
                'numeric_conversion_failures': int((numeric.isna() & df[numeric.columns].notna()).sum().sum()),
                'zeros': int(numeric.eq(0).sum().sum()),
                'negative_values': int(numeric.lt(0).sum().sum()),
                'account_code_unique': int(df['Account code'].nunique()),
                'duplicate_account_code_rows': int(df['Account code'].duplicated().sum()),
                'nonzero_by_year': numeric.ne(0).sum().astype(int).to_dict(),
                'unit_and_actual_estimate_boundary': 'Require confirmation from primary documentation; not inferred from year labels.'}
        report['datasets'][filename] = info
        print(json.dumps({'file': filename, **info}, ensure_ascii=False))
    assert hashlib.sha256(original.read_bytes()).hexdigest() == original_hash
    out = ROOT / 'reports/validacao_datasets.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Notebook original preservado. Relatorio:', out)


if __name__ == '__main__':
    main()
