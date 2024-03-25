import tempfile
import shutil
from pathlib import Path
from contextlib import contextmanager

from utils.paths import RUNTIME_DIR


@contextmanager
def tmp_datafolder():
    tmpdir = tempfile.mkdtemp(dir=str(RUNTIME_DIR.resolve()))
    try:
        yield Path(tmpdir)
    finally:
        shutil.rmtree(tmpdir)
