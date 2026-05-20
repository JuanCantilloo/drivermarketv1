from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "Drivemarket"

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from app import app  # noqa: E402
