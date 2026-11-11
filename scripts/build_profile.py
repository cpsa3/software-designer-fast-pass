#!/usr/bin/env python3
"""Convenience wrapper to run build_profile.py from the repository root or scripts/."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET_SCRIPT = REPO_ROOT / "01-shared-core" / "05-error-vault" / "_tools" / "build_profile.py"

if __name__ == "__main__":
    result = subprocess.run([sys.executable, str(TARGET_SCRIPT)] + sys.argv[1:])
    sys.exit(result.returncode)
