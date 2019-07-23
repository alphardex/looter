"""
用来自动生成这篇README.md
"""
from pathlib import Path
Path('README.md').write_text('\n'.join([*['# Examples\n'], *[f"- [{str(py)[:-3]}]({str(py)}): {open(py, encoding='utf-8').readlines()[1]}" for py in Path('.').glob('*.py')]]), encoding='utf-8')