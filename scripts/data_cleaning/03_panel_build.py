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

Scope of the comparison, read this before trusting a PASS: the delivered panel and the
rebuilt panel are both derived from the same intermediate artefacts in data_processed/,
so the series-by-series check below proves that the aggregation is *repeatable*, not that
the upstream extraction is correct.  mgto_district_headcount is a self-reference - both
sides are a monthly sum of demand_district_hour_panel_2023_2026.csv - and it therefore
cannot validate that extraction.  The upstream artefacts that no script rebuilds yet
(demand_monthly_arrivals.csv, analysis_dataset_master*.csv and the three hotel tables) are
outside the reach of this check as well; see scripts/data_cleaning/README.md.
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
        print("FAIL: delivered panel %s is missing, so the rebuilt panel cannot be verified"
              % DELIVERED.name)
        print("      the rebuilt panel was written to %s for inspection" % out.name)
        return 1
    ref = pd.read_csv(DELIVERED).sort_values("month").reset_index(drop=True)
    worst, failed = 0.0, []
    print("  series                max relative difference")
    for col in keep[4:]:
        a = pd.to_numeric(panel[col], errors="coerce")
        b = pd.to_numeric(ref[col], errors="coerce")
        if len(a) != len(b):
            failed.append((col, "length %d vs %d" % (len(a), len(b))))
            print("  %-20s %10s  <-- CHECK (row count differs)" % (col, "n/a"))
            continue
        both_na = a.isna() & b.isna()
        cmp = ~both_na
        if not cmp.any():
            failed.append((col, "every value is missing on both sides"))
            print("  %-20s %10s  <-- CHECK (all values missing)" % (col, "n/a"))
            continue
        # a value present on one side only is a disagreement, not something to skip over
        one_side = a[cmp].isna() ^ b[cmp].isna()
        if one_side.any():
            failed.append((col, "%d rows missing on one side" % int(one_side.sum())))
            print("  %-20s %10s  <-- CHECK (%d rows missing on one side)"
                  % (col, "n/a", int(one_side.sum())))
            continue
        diff = (a[cmp] - b[cmp]).abs()
        denom = b[cmp].abs()
        zero_base = denom == 0
        if zero_base.any():
            # relative difference is undefined on a zero baseline: require exact equality
            if not bool((diff[zero_base] == 0).all()):
                failed.append((col, "non-zero value where the delivered panel is 0"))
                print("  %-20s %10s  <-- CHECK (zero baseline)" % (col, "n/a"))
                continue
        rel_series = diff[~zero_base] / denom[~zero_base]
        rel = float(rel_series.max()) if len(rel_series) else 0.0
        if np.isnan(rel):
            # an undefined relative difference must fail, never fall through to PASS
            failed.append((col, "relative difference is undefined (NaN)"))
            print("  %-20s %10s  <-- CHECK (undefined, NaN)" % (col, "n/a"))
            continue
        flag = ""
        if rel > 0.005:
            flag = "  <-- CHECK"
            failed.append((col, "max relative difference %.2e" % rel))
        worst = max(worst, rel)
        print("  %-20s %10.2e%s" % (col, rel, flag))

    if failed:
        print("FAIL: rebuilt panel disagrees with the delivered panel in %d series:"
              % len(failed))
        for col, why in failed:
            print("  %-20s %s" % (col, why))
        return 1
    print("PASS: panel rebuilt, 45 rows, every series within 0.5%% of the delivered panel "
          "(worst %.2e)" % worst)
    print("NOTE: this PASS covers repeatability of the aggregation only. "
          "mgto_district_headcount is a self-reference - both sides are a monthly sum of "
          "demand_district_hour_panel_2023_2026.csv - so it says nothing about the MGTO "
          "extraction behind that panel. The arrivals series and the three hotel tables are "
          "rebuilt by build_arrivals.py and build_hotel_tables.py, not here.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
