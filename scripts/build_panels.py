#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_panels.py - rebuild the three integrated panel files of the project from the
raw / intermediate files kept in this repository.

Inputs (all read-only):
  data/mgtodataplus/MacaoDistrictTourismData_{2023,2024,2025,2026}12|09_en.xlsx
        District x hour visitor headcount. Every monthly file of a year is a
        year-to-date file, so only the last file of each year is read
        (202312, 202412, 202512, 202609), otherwise the same month is counted
        up to four times.
  Dataset/Hotel_occ_total.csv            DSEC monthly occupancy rate (all hotels)
  Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv
        DSEC monthly total hotel guests and hotel room supply. DSEC publishes
        these two columns in the hotel survey tables; the export kept here is the
        one used by the report, because the original portal download is not
        stored in the repository.
  data_processed/demand_monthly_arrivals.csv
        DSEC monthly visitor arrivals (built from the DSEC key-indicator JSON
        snapshots in data/dsec_timeseries).
  Dataset/DSEC_arrivals_2026_09_supplement.csv
        One row: the September 2026 arrivals figure published by DSEC on
        2026-10-22, which post-dates the JSON snapshot used for the series above.
  Monthly_Bus_Database/bus_monthly_2020_2026.csv
        DSAT monthly bus statistics (daily average trips, buses in service).

Outputs (overwritten):
  data_processed/mgto_district_hour_master_2023_01_2026_09.csv   25,920 rows
  data_processed/monthly_panel_2023_01_2026_09.csv               45 rows
  data_processed/quarterly_panel_2023Q1_2026Q3.csv               15 rows

Run from the repository root:  python scripts/build_panels.py
"""
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
PROC = os.path.join(REPO, "data_processed")
MGTO = os.path.join(DATA, "mgtodataplus")

# Year-to-date files: the last published file of each year, which holds every
# month of that year exactly once.
YTD_FILES = [
    "MacaoDistrictTourismData_202312_en.xlsx",
    "MacaoDistrictTourismData_202412_en.xlsx",
    "MacaoDistrictTourismData_202512_en.xlsx",
    "MacaoDistrictTourismData_202609_en.xlsx",
]

WINDOW = ("2023-01", "2026-09")


def build_mgto_master() -> pd.DataFrame:
    """District x hour long table, de-duplicated over the year-to-date files."""
    frames = []
    for fname in YTD_FILES:
        path = os.path.join(MGTO, fname)
        raw = pd.read_excel(path, sheet_name="1", header=None)
        # The published sheet carries a two-row header; data rows start where the
        # year column becomes numeric.
        raw = raw[pd.to_numeric(raw[0], errors="coerce").notna()].copy()
        frames.append(
            pd.DataFrame(
                {
                    "year": pd.to_numeric(raw[0]).astype(int),
                    "month": pd.to_numeric(raw[1]).astype(int),
                    "hour": raw[2].astype(str).str.strip(),
                    "district": raw[5].astype(str).str.strip(),
                    "headcount": pd.to_numeric(raw[6], errors="coerce").astype(float),
                }
            )
        )
    master = (
        pd.concat(frames, ignore_index=True)
        .dropna(subset=["headcount"])
        .reset_index(drop=True)
    )

    months = master.groupby(["year", "month"]).size()
    if months.nunique() != 1:
        raise SystemExit("district-hour panel is not balanced across months")
    if len(months) != 45 or master.shape[0] != 45 * 576:
        raise SystemExit(
            f"unexpected district-hour size: {len(months)} months, "
            f"{master.shape[0]} rows"
        )
    return master


def build_monthly(master: pd.DataFrame) -> pd.DataFrame:
    """Monthly integrated panel: arrivals, three hotel series, four bus series,
    district headcount and the intensity ratio."""
    # --- arrivals -----------------------------------------------------------
    arr = pd.read_csv(
        os.path.join(PROC, "demand_monthly_arrivals.csv"), parse_dates=["date"]
    )
    arr = arr[["year", "month", "arrivals"]].rename(columns={"arrivals": "visitor_arrivals"})

    supp_path = os.path.join(REPO, "Dataset", "DSEC_arrivals_2026_09_supplement.csv")
    if os.path.exists(supp_path):
        supp = pd.read_csv(supp_path)
        supp = supp.rename(columns={"arrivals": "visitor_arrivals"})
        arr = pd.concat([arr, supp], ignore_index=True)
        arr = arr.drop_duplicates(subset=["year", "month"], keep="last")

    # --- hotel --------------------------------------------------------------
    occ = pd.read_csv(os.path.join(REPO, "Dataset", "Hotel_occ_total.csv"))
    occ = occ[occ["Hotel Establishments"].astype(str).str.strip() == "Total"]
    occ = occ[occ["Month"].notna()]
    occ = pd.DataFrame(
        {
            "year": occ["Year"].astype(int),
            "month": occ["Month"].astype(int),
            "hotel_occ_pct": pd.to_numeric(occ["Occupancy rate"], errors="coerce"),
        }
    )

    hr_path = os.path.join(REPO, "Dataset", "DSEC_hotel_guests_rooms_2023_01_2026_09.csv")
    hr = pd.read_csv(hr_path)
    hr["year"] = hr["month"].str.slice(0, 4).astype(int)
    hr["month"] = hr["month"].str.slice(5, 7).astype(int)
    hr = hr.rename(columns={"guests": "hotel_guests", "rooms": "hotel_rooms"})

    # --- bus ----------------------------------------------------------------
    bus = pd.read_csv(os.path.join(REPO, "Monthly_Bus_Database", "bus_monthly_2020_2026.csv"))
    bus = pd.DataFrame(
        {
            "year": bus["year"].astype(int),
            "month": bus["month_no"].astype(int),
            "bus_daily_avg_trips_wan": bus["daily_avg_trips_wan"],
            "bus_monthly_trips": bus["monthly_trips_est"],
            "buses_in_service": bus["buses_in_service"],
        }
    )

    # --- district hour total ------------------------------------------------
    dist = (
        master.groupby(["year", "month"])["headcount"]
        .sum()
        .reset_index()
        .rename(columns={"headcount": "mgto_district_headcount"})
    )

    panel = arr.merge(occ, on=["year", "month"], how="left")
    panel = panel.merge(hr, on=["year", "month"], how="left")
    panel = panel.merge(bus, on=["year", "month"], how="left")
    panel = panel.merge(dist, on=["year", "month"], how="left")

    panel["month"] = pd.to_datetime(
        dict(year=panel["year"], month=panel["month"], day=1)
    ).dt.strftime("%Y-%m")
    panel = panel.rename(columns={"month": "month_label"})
    panel["month_no"] = pd.to_datetime(panel["month_label"]).dt.month
    panel["quarter"] = (
        panel["year"].astype(str)
        + "Q"
        + pd.to_datetime(panel["month_label"]).dt.quarter.astype(str)
    )
    panel["bus_trips_per_arrival"] = (
        panel["bus_monthly_trips"] / panel["visitor_arrivals"]
    ).round(4)

    panel = panel[
        [
            "month_label",
            "year",
            "month_no",
            "quarter",
            "visitor_arrivals",
            "hotel_occ_pct",
            "hotel_guests",
            "hotel_rooms",
            "bus_daily_avg_trips_wan",
            "bus_monthly_trips",
            "buses_in_service",
            "mgto_district_headcount",
            "bus_trips_per_arrival",
        ]
    ].rename(columns={"month_label": "month"})
    panel = panel.sort_values(["year", "month_no"]).reset_index(drop=True)

    lo, hi = WINDOW
    panel = panel[(panel["month"] >= lo) & (panel["month"] <= hi)].reset_index(drop=True)
    if panel.shape[0] != 45:
        raise SystemExit(f"monthly panel has {panel.shape[0]} rows, expected 45")
    return panel


def build_quarterly(panel: pd.DataFrame) -> pd.DataFrame:
    """Quarterly roll-up of the monthly panel."""
    g = panel.groupby("quarter", sort=True)
    q = pd.DataFrame(
        {
            "months_in_data": g.size(),
            "visitor_arrivals_sum": g["visitor_arrivals"].sum(),
            "hotel_occ_avg_pct": g["hotel_occ_pct"].mean().round(1),
            "hotel_guests_sum": g["hotel_guests"].sum(),
            # integer truncation, as in the file of record (a quarter average of
            # room supply is a level, not a rounded count)
            "hotel_rooms_avg": g["hotel_rooms"].mean(),
            "bus_daily_avg_trips_wan_mean": g["bus_daily_avg_trips_wan"].mean().round(2),
            "bus_monthly_trips_sum": g["bus_monthly_trips"].sum(),
            "buses_in_service_max": g["buses_in_service"].max(),
            "mgto_district_headcount_sum": g["mgto_district_headcount"].sum(),
        }
    ).reset_index()

    for col in [
        "visitor_arrivals_sum",
        "hotel_guests_sum",
        "bus_monthly_trips_sum",
        "mgto_district_headcount_sum",
    ]:
        q[col] = q[col].astype("Int64")
    q["hotel_rooms_avg"] = np.trunc(q["hotel_rooms_avg"].to_numpy()).astype("int64")
    q["months_in_data"] = q["months_in_data"].astype(int)
    q["buses_in_service_max"] = q["buses_in_service_max"].astype(float)

    q["bus_trips_per_arrival"] = (
        q["bus_monthly_trips_sum"] / q["visitor_arrivals_sum"]
    ).round(4)
    q["district_hits_per_arrival"] = (
        q["mgto_district_headcount_sum"] / q["visitor_arrivals_sum"]
    ).round(4)
    return q


def main() -> int:
    master = build_mgto_master()
    master.to_csv(
        os.path.join(PROC, "mgto_district_hour_master_2023_01_2026_09.csv"),
        index=False,
        encoding="utf-8-sig",
        lineterminator="\r\n",
    )
    print(f"district-hour master : {master.shape[0]:,} rows "
          f"({master.groupby(['year','month']).ngroups} months x 576)")

    panel = build_monthly(master)
    panel.to_csv(
        os.path.join(PROC, "monthly_panel_2023_01_2026_09.csv"),
        index=False,
        encoding="utf-8-sig",
        lineterminator="\r\n",
    )
    missing = panel[["hotel_occ_pct", "hotel_guests", "hotel_rooms"]].isna().sum().sum()
    print(f"monthly panel        : {panel.shape[0]} rows, {panel['month'].min()} .. "
          f"{panel['month'].max()}, missing hotel cells = {missing}")

    q = build_quarterly(panel)
    q.to_csv(
        os.path.join(PROC, "quarterly_panel_2023Q1_2026Q3.csv"),
        index=False,
        encoding="utf-8-sig",
        lineterminator="\r\n",
    )
    print(f"quarterly panel      : {q.shape[0]} rows, {q['quarter'].iloc[0]} .. "
          f"{q['quarter'].iloc[-1]}")

    # Read-back checks quoted in the report.
    win = panel[(panel["month"] >= "2023-01") & (panel["month"] <= "2025-12")]
    win_q = q[(q["quarter"] >= "2023Q1") & (q["quarter"] <= "2025Q4")]
    r_mon = np.corrcoef(win["visitor_arrivals"], win["bus_monthly_trips"])[0, 1]
    r_qtr = np.corrcoef(win_q["visitor_arrivals_sum"], win_q["bus_monthly_trips_sum"])[0, 1]
    print(f"check r(monthly) 2023-01..2025-12 (n=36) = {r_mon:.3f}")
    print(f"check r(quarterly) 2023Q1..2025Q4 (n=12) = {r_qtr:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
