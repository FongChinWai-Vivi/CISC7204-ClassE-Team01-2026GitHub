#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point - run the cleaning chain in order and stop at the first failure.

    python scripts/data_cleaning/run_all.py

Step 1 inventories and gates the raw downloads, step 2 cleans the three module series,
step 3 builds the panels and checks them against the delivered files.  Each script exits
non-zero on a failed assertion, which stops the chain here.
"""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
STEPS = ["01_ingest.py", "02_clean_series.py", "03_panel_build.py"]


def main():
    for name in STEPS:
        script = HERE / name
        print("\n=== %s " % name + "=" * (60 - len(name)))
        rc = subprocess.call([sys.executable, str(script)])
        if rc != 0:
            print("\nSTOP: %s exited with %d - later steps were not run" % (name, rc))
            return rc
    print("\nAll steps passed.  Cleaned series and panels are in data_processed/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
