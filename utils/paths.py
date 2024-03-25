from pathlib import Path

UTILS_DIR = (Path(__file__) / '..').resolve()
ROOT_DIR = UTILS_DIR / '..'

RUNTIME_DIR = ROOT_DIR / '.runtime'
RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
