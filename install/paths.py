"""Immutable program files and writable per-user data, for source or release."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGED = (ROOT / "release.json").is_file()
DATA = Path.home() / "Library/Application Support/Splash" if PACKAGED else ROOT
MODELS = DATA / "models" if PACKAGED else ROOT / "install/models"
RUNTIME = DATA / "runtime" if PACKAGED else ROOT / "build/runtime"
# The interpreter running the launcher also runs the children it starts: a
# stock release starts it from its own python/bin/python3, while a bundle
# that supplies a shared interpreter starts it from that one. A source
# checkout keeps its own venv.
PYTHON = Path(sys.executable) if PACKAGED else ROOT / ".venv/bin/python"
BINARY = ROOT / ("engine/splash" if PACKAGED else "build/splash")
