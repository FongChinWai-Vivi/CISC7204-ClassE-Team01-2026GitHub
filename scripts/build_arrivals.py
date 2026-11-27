#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_arrivals.py - rebuild the monthly visitor-arrivals series of the project.

This is the first link of the cleaning chain that used to exist only as a cell in
notebooks/pipeline.ipynb: data_processed/demand_monthly_arrivals.csv had no script
that could regenerate it from the repository alone.

Inputs (all read-only, all kept in this repository):
  data/dsec_timeseries/DSEC_KeyIndicator_27.json
        DSEC key indicator, monthly visitor arrivals ("Visitor arrivals", id 14023),
        2008-01 .. 2026-08.
  data/dsec_timeseries/DSEC_KeyIndicator_127.json
        DSEC key indicator, monthly same-day visitor arrivals
        ("Same-day visitor arrivals", id 14035), same coverage.
  data/dsec_timeseries/DSEC_KeyIndicator_28.json
        DSEC key indicator, year-on-year change of arrivals (percent, id 14023),
        same coverage; months with no published figure carry IndicatorValue null
        and the remark "No figure provided" (kept here as an empty cell).
  Dataset/DSEC_arrivals_2026_09_supplement.csv
        One row: the September 2026 arrivals figure published by DSEC on
        2026-10-22, which post-dates the JSON snapshots above. The same-day split
        and the year-on-year change of that month are not published in the
        snapshots, so those two columns stay empty for the appended row.

Output (overwritten after a snapshot):
  data_processed/demand_monthly_arrivals.csv
        225 rows, 2008-01 .. 2026-09, columns
        date, year, month, arrivals, same_day_arrivals, arrivals_yoy_pct,
        same_day_share_pct

Column rules, exactly as in the file of record:
  date                first day of the month, ISO 8601
  arrivals            IndicatorValue of id 14023
  same_day_arrivals   IndicatorValue of id 14035
  arrivals_yoy_pct    IndicatorValue of the year-on-year indicator (percent)
  same_day_share_pct  same_day_arrivals / arrivals * 100, full float precision

Run from the repository root:  python scripts/build_arrivals.py
Use --check to rebuild in memory and compare with the file on disk without
writing anything.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import sys

import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(REPO, "data_processed")
SERIES = os.path.join(REPO, "data", "dsec_timeseries")

OUT_NAME = "demand_monthly_arrivals.csv"
COLUMNS = [
    "date",
    "year",
    "month",
    "arrivals",
    "same_day_arrivals",
    "arrivals_yoy_pct",
    "same_day_share_pct",
]

# (file, output column) - the three key indicators the series is built from.
INDICATORS = [
    ("DSEC_KeyIndicator_27.json", "arrivals"),
    ("DSEC_KeyIndicator_127.json", "same_day_arrivals"),
    ("DSEC_KeyIndicator_28.json", "arrivals_yoy_pct"),
]

EXPECTED_ROWS = 225
EXPECTED_WINDOW = ("2008-01", "2026-09")


def load_indicator(fname: str) -> dict:
    """{(year, month): value} for one DSEC key-indicator JSON snapshot."""
    path = os.path.join(SERIES, fname)
    if not os.path.exists(path):
        raise SystemExit(f"missing DSEC snapshot: {path}")
    with open(path, encoding="utf-8") as fh:
        payload = json.load(fh)
    records = payload["Value"]["indicatorValues"][0]["dsecIndicatorData"]
    series = {}
    for rec in records:
        year, month = int(rec["Year"]), int(rec["PeriodID"])
        if not 1 <= month <= 12:
            raise SystemExit(f"{fname}: unexpected period {month} for {year}")
        series[(year, month)] = rec["IndicatorValue"]
    return series


def build_frame() -> pd.DataFrame:
    """Monthly arrivals frame, 2008-01 .. 2026-09."""
    series = {col: load_indicator(fname) for fname, col in INDICATORS}
    # The three snapshots must cover the same months, otherwise the merge below
    # would silently drop a column.
    keys = [set(series[col]) for _, col in INDICATORS]
    if len(set(map(frozenset, keys))) != 1:
        raise SystemExit("the three DSEC snapshots do not cover the same months")
    months = sorted(keys[0])

    frame = pd.DataFrame(
        {
            "year": [y for y, _ in months],
            "month": [m for _, m in months],
            **{col: [series[col][k] for k in months] for _, col in INDICATORS},
        }
    )
    frame["arrivals"] = pd.to_numeric(frame["arrivals"], errors="coerce").astype(float)
    frame["same_day_arrivals"] = pd.to_numeric(
        frame["same_day_arrivals"], errors="coerce"
    ).astype(float)
    frame["arrivals_yoy_pct"] = pd.to_numeric(
        frame["arrivals_yoy_pct"], errors="coerce"
    )
    if frame[["year", "month", "arrivals"]].isna().any().any():
        raise SystemExit("an arrivals month came back empty from the snapshots")
    # Same-day share: multiply before dividing, which is how the file of record was
    # produced (the other order differs in the last binary digit of 74 of the 225
    # rows, so the order is part of the definition, not an implementation detail).
    frame["same_day_share_pct"] = (
        frame["same_day_arrivals"] * 100 / frame["arrivals"]
    )

    # The September 2026 supplement, appended after the snapshot coverage.
    supp_path = os.path.join(REPO, "Dataset", "DSEC_arrivals_2026_09_supplement.csv")
    if os.path.exists(supp_path):
        supp = pd.read_csv(supp_path)
        supp = supp[["year", "month", "arrivals"]]
        frame = pd.concat([frame, supp], ignore_index=True)
        frame = frame.drop_duplicates(subset=["year", "month"], keep="last")

    frame = frame.sort_values(["year", "month"]).reset_index(drop=True)
    frame.insert(
        0,
        "date",
        pd.to_datetime(dict(year=frame["year"], month=frame["month"], day=1)).dt.strftime(
            "%Y-%m-%d"
        ),
    )
    frame = frame[COLUMNS]

    lo, hi = EXPECTED_WINDOW
    frame = frame[
        (frame["date"].str.slice(0, 7) >= lo) & (frame["date"].str.slice(0, 7) <= hi)
    ].reset_index(drop=True)
    if frame.shape[0] != EXPECTED_ROWS:
        raise SystemExit(
            f"arrivals series has {frame.shape[0]} rows, expected {EXPECTED_ROWS}"
        )
    return frame


def frame_equals(left: pd.DataFrame, right: pd.DataFrame) -> bool:
    """Cell-by-cell comparison that treats empty cells as equal."""
    for col in left.columns:
        a, b = left[col].reset_index(drop=True), right[col].reset_index(drop=True)
        if a.dtype.kind in "fi" and b.dtype.kind in "fi":
            af, bf = a.astype(float), b.astype(float)
            if not ((af.isna() & bf.isna()) | (af == bf)).all():
                return False
        elif not (a.astype(str) == b.astype(str)).all():
            return False
    return True


def md5_of(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare a rebuild with the file on disk, write nothing",
    )
    args = parser.parse_args()

    frame = build_frame()
    out = os.path.join(PROC, OUT_NAME)

    if args.check:
        if not os.path.exists(out):
            print(f"CHECK: {OUT_NAME} does not exist yet")
            return 1
        old = pd.read_csv(out)
        same_columns = list(old.columns) == list(frame.columns)
        same_shape = old.shape == frame.shape
        same_values = same_columns and same_shape and frame_equals(old, frame)
        print(f"rows rebuilt {frame.shape[0]} / on disk {old.shape[0]}")
        print(f"columns identical: {same_columns}; values identical: {same_values}")
        if same_values:
            print("CHECK: the file on disk is reproducible from the repository")
            return 0
        print("CHECK: the file on disk differs from the rebuild")
        return 1

    # Snapshot and hash before the first byte is written.
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(PROC, "_backup", stamp)
    before = ""
    if os.path.exists(out):
        before = md5_of(out)
        os.makedirs(bdir, exist_ok=True)
        shutil.copy2(out, os.path.join(bdir, OUT_NAME))
        print(f"existing file {OUT_NAME}: {os.path.getsize(out):,} B  {before}")
        print(f"backup -> {bdir}")
    else:
        print(f"{OUT_NAME} does not exist yet - first build")

    frame.to_csv(out, index=False, encoding="utf-8-sig", lineterminator="\r\n")
    after = md5_of(out)
    print(f"written      {OUT_NAME}: {os.path.getsize(out):,} B  {after}")
    print(f"rows {frame.shape[0]}, {frame['date'].iloc[0]} .. {frame['date'].iloc[-1]}")
    print(f"changed: {after != before}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
