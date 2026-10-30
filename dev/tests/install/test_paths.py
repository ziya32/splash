"""The interpreter a release's launcher runs its children on."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from install import paths

PATHS_SOURCE = Path(paths.__file__)


def _load_packaged_paths(root: Path):
    """The same module, beside a release.json, as a packaged release has it."""
    (root / "install").mkdir()
    shutil.copy2(PATHS_SOURCE, root / "install" / "paths.py")
    (root / "release.json").write_text("{}\n", encoding="utf-8")
    spec = importlib.util.spec_from_file_location(
        "packaged_paths", root / "install" / "paths.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PathsTests(unittest.TestCase):
    def test_a_packaged_runtime_runs_its_children_on_its_own_interpreter(self):
        """A release supplied with an interpreter uses that one for its children.

        ``install/launcher.py`` starts both the model preparation and the
        server with ``paths.PYTHON``. A release launched from the app's shared
        interpreter must therefore hand that same interpreter to its children,
        not a python path inside the release that the app does not carry.
        """
        with tempfile.TemporaryDirectory() as temporary:
            packaged = _load_packaged_paths(Path(temporary))
            self.assertTrue(packaged.PACKAGED)
            self.assertEqual(packaged.PYTHON, Path(sys.executable))

    def test_a_source_checkout_keeps_its_venv(self):
        self.assertFalse(paths.PACKAGED)
        self.assertEqual(paths.PYTHON, paths.ROOT / ".venv" / "bin" / "python")
