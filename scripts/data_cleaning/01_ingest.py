#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Step 1 - inventory and gate the raw downloads.

Reads nothing into the analysis; it records what is on disk and stops if a source is
missing or if a row count differs from the delivered one.  Run from anywhere.
"""
from pathlib import Path
import sys
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "data_processed" / "clean_inventory.csv"

MGTO_GLOB = "data/mgtodataplus/MacaoDistrictTourismData_*.xlsx"
MGTO_EXPECTED = 45

SINGLE = [
    ("Demand", "data/dsec_timeseries/DSEC_KeyIndicator_27.json", "DSEC monthly visitor arrivals"),
    ("Demand", "data/dsec_timeseries/DSEC_KeyIndicator_127.json", "DSEC same-day visitor arrivals"),
    ("Demand", "Dataset/DSEC_arrivals_2026_09_supplement.csv", "DSEC September 2026 release"),
    ("Demand", "Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv", "DSEC hotel guests and rooms"),
    ("Demand", "Dataset/Hotel_occ_total.csv", "DSEC hotel occupancy rate, monthly"),
    ("Supply", "Monthly_Bus_Database/bus_monthly_2020_2026.csv", "DSAT monthly bus statistics"),
]

PANELS = [
    ("Panel", "data_processed/demand_monthly_arrivals.csv", 225),
    ("Panel", "data_processed/demand_district_hour_panel_2023_2026.csv", 25920),
    ("Panel", "data_processed/monthly_panel_2023_01_2026_09.csv", 45),
]


def main():
    rows, problems = [], []

    workbooks = sorted(REPO.glob(MGTO_GLOB))
    rows.append({"group": "Demand", "file": MGTO_GLOB, "rows": len(workbooks),
                 "columns": "workbook", "role": "MGTO district x hour workbooks, year-to-date"})
    if len(workbooks) != MGTO_EXPECTED:
        problems.append("%s: expected %d workbooks, found %d" % (MGTO_GLOB, MGTO_EXPECTED, len(workbooks)))

    for group, rel, role in SINGLE:
        p = REPO / rel
        if not p.exists():
            problems.append("%s is missing" % rel)
            rows.append({"group": group, "file": rel, "rows": 0, "columns": "", "role": role})
            continue
        if p.suffix.lower() == ".csv":
            df = pd.read_csv(p)
            rows.append({"group": group, "file": rel, "rows": len(df),
                         "columns": "|".join(map(str, df.columns)), "role": role})
        else:
            rows.append({"group": group, "file": rel, "rows": 1, "columns": "json",
                         "role": role})

    for group, rel, expected in PANELS:
        p = REPO / rel
        if not p.exists():
            problems.append("%s is missing (run the earlier steps first)" % rel)
            rows.append({"group": group, "file": rel, "rows": 0, "columns": "", "role": "delivered panel"})
            continue
        df = pd.read_csv(p)
        rows.append({"group": group, "file": rel, "rows": len(df),
                     "columns": "|".join(map(str, df.columns)), "role": "delivered panel"})
        if len(df) != expected:
            problems.append("%s: expected %d rows, found %d" % (rel, expected, len(df)))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("inventory written ->", OUT.relative_to(REPO), "(%d sources)" % len(rows))

    if problems:
        print("FAILED:")
        for msg in problems:
            print("  -", msg)
        return 1
    print("PASS: every source is present and the delivered panels have the expected row counts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
