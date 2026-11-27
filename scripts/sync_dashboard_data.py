#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sync_dashboard_data.py - copy the cleaned panels into Dashboard/data and verify them.

Dashboard/build_dashboard.py reads its inputs from Dashboard/data/, while the chain
writes into data_processed/. Nothing used to keep the two folders in step, so a
panel could be rebuilt and the dashboard could keep the previous numbers without a
single warning. This script is that missing link: it compares the MD5 of every pair
and only copies when the two sides differ, then re-hashes the copies to prove that
what the dashboard will read is what the chain just produced.

Files that are not produced by the chain (the three hotel tables built by
build_hotel_tables.py, and the Dash app assets in Dashboard/data/dash/) are not
touched here.

Run from the repository root:
    python scripts/sync_dashboard_data.py           # copy the panels that differ
    python scripts/sync_dashboard_data.py --check   # compare only, write nothing
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "data_processed")
DST = os.path.join(REPO, "Dashboard", "data")

# One entry per file the dashboard reads from the chain. Kept explicit rather than
# globbed, so a panel that disappears is a failure here instead of a silently
# shorter dashboard.
PANELS = [
    "annual_alignment_2018_2026.csv",
    "annual_hour_profile.csv",
    "annual_month_profile.csv",
    "annual_summary_2023_2026.csv",
    "demand_district_hour_panel_2023_2026.csv",
    "demand_goldenweek_daily.csv",
    "demand_monthly_arrivals.csv",
    "district_map_metrics.csv",
    "match_hourly_profile.csv",
    "match_zone_supply_demand.csv",
    "monthly_detail_2023_01_2026_09.csv",
    "monthly_panel_2023_01_2026_09.csv",
    "monthly_seasonality_index.csv",
    "optional_2026_hour_shift.csv",
    "optional_2026_zone_shift.csv",
    "quarterly_panel_2023Q1_2026Q3.csv",
    "zone_month_share.csv",
    # map layer used by the choropleth
    "macau_stats_zones.geojson",
]

# Produced by build_hotel_tables.py from Dataset/, not by the chain.
NOT_SYNCED = [
    "hotel_occ_monthly_2023_2026.csv",
    "hotel_guests_by_star_2023_2026.csv",
    "hotel_occ_history_2014_2025.csv",
]


def md5_of(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare only, write nothing"
    )
    args = parser.parse_args()

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(DST, "_backup", stamp)

    missing = [name for name in PANELS if not os.path.exists(os.path.join(SRC, name))]
    if missing:
        print("missing in data_processed (nothing has been copied):")
        for name in missing:
            print(f"  {name}")
        print("build the panels first: python scripts/build_panels.py")
        return 1

    stale = copied = 0
    print(f"{'file':<45}{'status':<10}md5")
    for name in PANELS:
        s, d = os.path.join(SRC, name), os.path.join(DST, name)
        src_md5 = md5_of(s)
        dst_md5 = md5_of(d) if os.path.exists(d) else ""
        if src_md5 == dst_md5:
            print(f"{name:<45}{'in sync':<10}{src_md5}")
            continue
        stale += 1
        if args.check:
            state = "differs" if dst_md5 else "absent"
            print(f"{name:<45}{state:<10}{src_md5} (dashboard has {dst_md5 or '-'})")
            continue
        os.makedirs(DST, exist_ok=True)
        if dst_md5:
            os.makedirs(bdir, exist_ok=True)
            shutil.copy2(d, os.path.join(bdir, name))
        shutil.copy2(s, d)
        if md5_of(d) != src_md5:
            print(f"{name:<45}{'FAILED':<10}copy does not match the source")
            return 1
        copied += 1
        print(f"{name:<45}{'copied':<10}{src_md5}")

    for name in NOT_SYNCED:
        note = "built by build_hotel_tables.py from Dataset/"
        state = "" if os.path.exists(os.path.join(DST, name)) else "missing"
        print(f"{name:<45}{state or 'present':<10}{note}")

    print(f"\n{len(PANELS)} panels checked, {stale} out of sync, {copied} copied")
    if copied:
        print(f"previous dashboard copies backed up to {bdir}")
    if args.check and stale:
        print("CHECK: Dashboard/data is not in step with data_processed")
        return 1
    if args.check:
        print("CHECK: Dashboard/data matches data_processed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
