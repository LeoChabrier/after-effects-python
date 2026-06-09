import os
from pathlib import Path

SCRIPTS_DIR = Path(os.environ.get('APPDATA', Path.home())) / 'after-effects-python' / 'scripts'
