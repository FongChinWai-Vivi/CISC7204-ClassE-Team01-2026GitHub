#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_hotel_tables.py - rebuild the three hotel tables read by the dashboard.

The dashboard reads three hotel tables that no script used to produce:

  Dashboard/data/hotel_occ_monthly_2023_2026.csv     45 rows, monthly occupancy rate
  Dashboard/data/hotel_guests_by_star_2023_2026.csv 180 rows, guests by hotel class
  Dashboard/data/hotel_occ_history_2014_2025.csv    153 rows, the long occupancy record
        (the file keeps the name it had when it stopped in 2025; the extract now
        covers 2014-01 .. 2026-09)

All three are published extracts of the DSEC hotel files that are already kept in
Dataset/, which is why the chain only ever needed a publication step and not a new
download:

  Dataset/hotel_occ_total_summary.csv            -> hotel_occ_monthly_2023_2026.csv
  Dataset/hotel_Arrival_byHotelStar_summary.csv  -> hotel_guests_by_star_2023_2026.csv
  Dataset/Hotel_occ_total.csv                    -> hotel_occ_history_2014_2025.csv

The build does not recompute any figure: it validates the source extract (header,
row count, month coverage, the "Total" rows, the hotel classes) and republishes the
rows verbatim, so the numbers the dashboard shows cannot drift from Dataset/. That
validation is also why the script is worth having: a truncated or re-sorted DSEC
export fails here instead of silently changing a chart.

Run from the repository root:
    python scripts/build_hotel_tables.py            # write the three tables
    python scripts/build_hotel_tables.py --check    # compare with the files on disk
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH_DATA = os.path.join(REPO, "Dashboard", "data")

# output name -> (source path, expected rows, expected header)
TABLES = {
    "hotel_occ_monthly_2023_2026.csv": (
        os.path.join(REPO, "Dataset", "hotel_occ_total_summary.csv"),
        45,
        ["Year", "Quarter", "Month", "Occupancy_rate"],
    ),
    "hotel_guests_by_star_2023_2026.csv": (
        os.path.join(REPO, "Dataset", "hotel_Arrival_byHotelStar_summary.csv"),
        180,
        ["Year", "Quarter", "Month", "Hotel_Establishments", "Number_of_guests"],
    ),
    "hotel_occ_history_2014_2025.csv": (
        os.path.join(REPO, "Dataset", "Hotel_occ_total.csv"),
        153,
        [
            "Year",
            "Quarter",
            "Month",
            "Hotel Establishments",
            "Occupancy rate",
            "Remark",
            "Difference",
            "Remark",
        ],
    ),
}

# The hotel classes the by-star table must carry, and the years the history must
# reach. DSEC publishes the 2- to 5-star classes; a missing class means a broken
# export. The history file keeps the name it had when it covered 2014-2025, but the
# extract has since been extended to 2026-09, so the range checked here is 2014-2026.
STAR_CLASSES = ["2-Star Hotels", "3-Star Hotels", "4-Star Hotels", "5-Star Hotels"]
HISTORY_RANGE = (2014, 2026)
MONTHLY_WINDOW = ("2023-01", "2026-09")


def read_rows(path: str) -> tuple[list[str], list[list[str]]]:
    """Header and data rows of a CSV, read as text.

    csv.reader is used on purpose: Dataset/Hotel_occ_total.csv repeats a column name
    ("Remark"), which pandas refuses to keep, and the table must stay byte-identical
    to the DSEC extract.
    """
    if not os.path.exists(path):
        raise SystemExit(f"missing source extract: {path}")
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = [row for row in csv.reader(fh) if row]
    if not rows:
        raise SystemExit(f"empty source extract: {path}")
    return rows[0], rows[1:]


def validate(name: str, header: list[str], rows: list[list[str]]) -> str:
    """Check one extract against the shape the dashboard depends on."""
    source, expected_rows, expected_header = TABLES[name]
    if header != expected_header:
        raise SystemExit(f"{name}: header changed: {header} != {expected_header}")
    if len(rows) != expected_rows:
        raise SystemExit(f"{name}: {len(rows)} data rows, expected {expected_rows}")
    for row in rows:
        if len(row) != len(header):
            raise SystemExit(f"{name}: ragged row {row}")

    if name == "hotel_occ_monthly_2023_2026.csv":
        months = [f"{int(r[0]):04d}-{int(r[2]):02d}" for r in rows]
        if months != sorted(months) or len(set(months)) != len(months):
            raise SystemExit(f"{name}: months are not strictly increasing")
        if (months[0], months[-1]) != MONTHLY_WINDOW:
            raise SystemExit(
                f"{name}: coverage {months[0]}..{months[-1]} != {MONTHLY_WINDOW}"
            )
        if any(not r[3].strip() for r in rows):
            raise SystemExit(f"{name}: empty occupancy rate")
        return f"{len(rows)} months, {months[0]} .. {months[-1]}"

    if name == "hotel_guests_by_star_2023_2026.csv":
        classes = sorted({r[3] for r in rows})
        if classes != STAR_CLASSES:
            raise SystemExit(f"{name}: hotel classes {classes} != {STAR_CLASSES}")
        months = sorted({f"{int(r[0]):04d}-{int(r[2]):02d}" for r in rows})
        if (months[0], months[-1]) != MONTHLY_WINDOW:
            raise SystemExit(
                f"{name}: coverage {months[0]}..{months[-1]} != {MONTHLY_WINDOW}"
            )
        if any(r[4].strip() in ("", "~") for r in rows):
            raise SystemExit(f"{name}: empty guest figure")
        return f"{len(rows)} rows, {len(classes)} classes, {months[0]} .. {months[-1]}"

    years = sorted({int(r[0]) for r in rows})
    if (years[0], years[-1]) != HISTORY_RANGE:
        raise SystemExit(f"{name}: years {years[0]}..{years[-1]} != {HISTORY_RANGE}")
    totals = [r for r in rows if r[3] == "Total"]
    if len(totals) != len(rows):
        raise SystemExit(
            f"{name}: {len(rows) - len(totals)} rows are not the 'Total' series"
        )
    if any(not r[4].strip() for r in rows):
        raise SystemExit(f"{name}: empty occupancy rate")
    return f"{len(rows)} months, {years[0]} .. {years[-1]}, all rows 'Total'"


def render(header: list[str], rows: list[list[str]]) -> str:
    """CSV text in the layout of the published tables: CRLF, one trailing newline."""
    import io

    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\r\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buf.getvalue()


def md5_of(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare with the files on disk, write nothing"
    )
    args = parser.parse_args()

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(DASH_DATA, "_backup", stamp)
    problems = 0
    for name in TABLES:
        header, rows = read_rows(TABLES[name][0])
        summary = validate(name, header, rows)
        text = render(header, rows)
        out = os.path.join(DASH_DATA, name)
        if args.check:
            if not os.path.exists(out):
                print(f"CHECK {name}: missing on disk")
                problems += 1
                continue
            same = open(out, encoding="utf-8-sig", newline="").read() == text
            print(f"CHECK {name}: {summary}; identical to disk = {same}")
            problems += 0 if same else 1
            continue

        before = ""
        if os.path.exists(out):
            before = md5_of(out)
            os.makedirs(bdir, exist_ok=True)
            shutil.copy2(out, os.path.join(bdir, name))
        with open(out, "w", encoding="utf-8-sig", newline="") as fh:
            fh.write(text)
        after = md5_of(out)
        print(f"{name}: {summary}")
        print(f"  {os.path.getsize(out):,} B  md5 {after}  "
              f"{'changed' if after != before else 'identical to the file before'}")
        if before:
            print(f"  previous file backed up to {bdir}")

    if args.check:
        if problems:
            print(f"CHECK: {problems} table(s) differ from the rebuild")
            return 1
        print("CHECK: all three hotel tables are reproducible from Dataset/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
