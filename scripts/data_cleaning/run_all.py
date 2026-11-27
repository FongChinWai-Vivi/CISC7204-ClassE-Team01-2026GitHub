#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point - run the cleaning chain in order and stop at the first failure.

    python scripts/data_cleaning/run_all.py

Step 1 inventories and gates the raw downloads, step 2 cleans the three module series,
step 3 rebuilds the two series that used to exist only as notebook cells (the monthly
visitor arrivals and the three hotel tables), step 4 builds the panels and checks them
against the delivered files, and step 5 copies the panels into Dashboard/data and
verifies them by MD5.  Each script exits non-zero on a failed assertion, which stops
the chain here.

Which steps need the raw downloads again: only step 1 gates them, and steps 2-4 read
the intermediate files and the DSEC extracts kept under data/ and Dataset/.  The chain
can therefore be rebuilt from the repository alone, apart from the raw monthly bus and
DSEC downloads that 01_ingest.py checks (see scripts/data_cleaning/README.md).
"""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent

# (script, needs the raw downloads?) in execution order.  The two scripts added at
# step 3 pre-date the panels: the arrivals series and the hotel tables are inputs of
# the panel and dashboard stages, not outputs of them.
STEPS = [
    (HERE / "01_ingest.py", "raw downloads"),
    (HERE / "02_clean_series.py", "intermediate"),
    (SCRIPTS / "build_arrivals.py", "intermediate"),
    (SCRIPTS / "build_hotel_tables.py", "Dataset extracts"),
    (HERE / "03_panel_build.py", "intermediate"),
    (SCRIPTS / "sync_dashboard_data.py", "intermediate"),
]


def main():
    for script, source in STEPS:
        if not script.exists():
            print("\nSTOP: %s is missing - later steps were not run" % script.name)
            return 1
        print("\n=== %s " % script.name + "=" * (60 - len(script.name)))
        print("    reads: %s" % source)
        rc = subprocess.call([sys.executable, str(script)])
        if rc != 0:
            print("\nSTOP: %s exited with %d - later steps were not run" % (script.name, rc))
            return rc
    print("\nAll steps passed.  Cleaned series and panels are in data_processed/, "
          "and Dashboard/data matches them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
