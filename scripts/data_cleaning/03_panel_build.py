#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Step 3 - build the panels and check them against the delivered files.

Merges the three cleaned module series on the month key, folds the district x hour table
into a monthly district head-count, and writes the analysis panel.  It then compares the
result with the delivered panel, series by series, and stops if any series disagrees.
The district x hour table itself is produced in the pipeline notebook (section 2) because
the 45 bilingual MGTO workbooks have an irregular header depth; this script does not
re-extract it, it re-derives its monthly total and checks the grid is complete, so a
silent change in that step fails here.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DP = REPO / "data_processed"
DELIVERED = DP / "monthly_panel_2023_01_2026_09.csv"
DISTRICT_HOUR = DP / "demand_district_hour_panel_2023_2026.csv"


def main():
    # ---- district x hour grid: 24 districts x 24 hours x 45 months
    dh = pd.read_csv(DISTRICT_HOUR)
    dh["month"] = (dh["year"].astype(int).astype(str) + "-"
                   + dh["month"].astype(int).map("{:02d}".format))
    n_dis, n_hour, n_mon = dh["district_en"].nunique(), dh["hour"].nunique(), dh["month"].nunique()
    expect = n_dis * n_hour * n_mon
    if len(dh) != expect:
        raise SystemExit("FAIL district-hour grid: %d rows, expected %d x %d x %d = %d"
                         % (len(dh), n_dis, n_hour, n_mon, expect))
    print("  ok  district-hour grid %d districts x %d hours x %d months = %d rows"
          % (n_dis, n_hour, n_mon, len(dh)))
    head = dh.groupby("month", as_index=False)["headcount"].sum() \
             .rename(columns={"headcount": "mgto_district_headcount"})

    # ---- merge the modules on the month key
    arr = pd.read_csv(DP / "clean_arrivals.csv")
    occ = pd.read_csv(DP / "clean_occupancy.csv")
    gr = pd.read_csv(DP / "clean_guests_rooms.csv")
    bus = pd.read_csv(DP / "clean_bus.csv")

    panel = (arr.merge(occ, on="month", how="outer")
                .merge(gr, on="month", how="outer")
                .merge(bus, on="month", how="outer")
                .merge(head, on="month", how="outer")
                .sort_values("month").reset_index(drop=True))
    panel = panel.rename(columns={"arrivals": "visitor_arrivals",
                                  "guests": "hotel_guests",
                                  "rooms": "hotel_rooms"})
    panel["year"] = panel["month"].str[:4].astype(int)
    panel["month_no"] = panel["month"].str[5:].astype(int)
    panel["quarter"] = panel["year"].astype(str) + "Q" + (((panel["month_no"] - 1) // 3) + 1).astype(str)
    panel["bus_trips_per_arrival"] = (panel["bus_monthly_trips"] / panel["visitor_arrivals"]).round(4)

    keep = ["month", "year", "month_no", "quarter", "visitor_arrivals", "hotel_occ_pct", "hotel_guests",
            "hotel_rooms", "bus_daily_avg_trips_wan", "bus_monthly_trips", "buses_in_service",
            "mgto_district_headcount", "bus_trips_per_arrival"]
    panel = panel[keep]
    if len(panel) != 45:
        raise SystemExit("FAIL panel: expected 45 rows, found %d" % len(panel))

    out = DP / "clean_panel_rebuilt.csv"
    panel.to_csv(out, index=False)

    # ---- compare with the delivered panel
    if not DELIVERED.exists():
        print("WARN: delivered panel not found, rebuilt panel written without a comparison")
        return 0
    ref = pd.read_csv(DELIVERED).sort_values("month").reset_index(drop=True)
    worst, failed = 0.0, []
    print("  series                max relative difference")
    for col in keep[4:]:
        a = pd.to_numeric(panel[col], errors="coerce")
        b = pd.to_numeric(ref[col], errors="coerce")
        denom = b.abs().replace(0, np.nan)
        rel = float(((a - b).abs() / denom).max())
        flag = ""
        if rel > 0.005:
            flag = "  <-- CHECK"
            failed.append((col, rel))
        worst = max(worst, rel)
        print("  %-20s %10.2e%s" % (col, rel, flag))

    if failed:
        print("FAIL: rebuilt panel disagrees with the delivered panel in %d series: %s"
              % (len(failed), ", ".join(c for c, _ in failed)))
        return 1
    print("PASS: panel rebuilt, 45 rows, every series within 0.5%% of the delivered panel "
          "(worst %.2e)" % worst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
