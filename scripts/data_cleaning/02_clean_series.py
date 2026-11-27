#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Step 2 - clean the three module series.

Demand (DSEC arrivals, hotel occupancy, hotel guests and rooms) and supply (DSAT bus
statistics) are parsed, keyed on the month, cut to the analysis window 2023-01..2026-09
and written one file per module.  Every series is checked for completeness before it is
written: 45 months, no gap, plausible range.  A failed check stops the run.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
DP = REPO / "data_processed"
WINDOW = [f"{y}-{m:02d}" for y in (2023, 2024, 2025, 2026) for m in range(1, 13)][:45]


def month_key(year, month):
    return pd.Series(year).astype(int).astype(str) + "-" + pd.Series(month).astype(int).map("{:02d}".format)


def check(df, name, lo=None, col=None):
    if len(df) != 45:
        raise SystemExit("FAIL %s: expected 45 months, found %d" % (name, len(df)))
    if sorted(df["month"]) != WINDOW:
        raise SystemExit("FAIL %s: month window is not 2023-01..2026-09" % name)
    if col is not None:
        s = pd.to_numeric(df[col], errors="coerce")
        if s.isna().any():
            raise SystemExit("FAIL %s: %d missing values in %s" % (name, int(s.isna().sum()), col))
        if lo is not None and s.le(lo).any():
            raise SystemExit("FAIL %s: values at or below %s in %s" % (name, lo, col))
    print("  ok  %-14s %d months, %s..%s" % (name, len(df), df["month"].min(), df["month"].max()))


def main():
    # ---- arrivals: DSEC key indicator 27, plus the September 2026 release
    arr = pd.read_csv(DP / "demand_monthly_arrivals.csv")
    arr["month"] = month_key(arr["year"], arr["month"])
    arr = arr[arr["month"].isin(WINDOW)][["month", "arrivals", "same_day_arrivals"]].copy()
    arr["arrivals"] = pd.to_numeric(arr["arrivals"], errors="coerce")
    check(arr, "arrivals", lo=3e5, col="arrivals")
    arr.to_csv(DP / "clean_arrivals.csv", index=False)

    # ---- occupancy: DSEC monthly rate for all establishments
    occ = pd.read_csv(REPO / "Dataset" / "Hotel_occ_total.csv")
    occ = occ[occ["Month"].notna()].copy()
    occ["Year"] = pd.to_numeric(occ["Year"], errors="coerce").astype("Int64")
    occ["Month"] = pd.to_numeric(occ["Month"], errors="coerce").astype("Int64")
    if "Hotel Establishments" in occ.columns:
        total = occ[occ["Hotel Establishments"].astype(str).str.strip().str.lower() == "total"]
        if len(total):
            occ = total
    occ["month"] = month_key(occ["Year"], occ["Month"])
    occ = occ[occ["month"].isin(WINDOW)]
    occ = (occ.groupby("month", as_index=False)["Occupancy rate"].mean()
              .rename(columns={"Occupancy rate": "hotel_occ_pct"}))
    check(occ, "occupancy", col="hotel_occ_pct")
    if occ["hotel_occ_pct"].between(0, 100).all() is False:
        raise SystemExit("FAIL occupancy: rate outside 0-100 per cent")
    occ.to_csv(DP / "clean_occupancy.csv", index=False)

    # ---- hotel guests and guest rooms
    gr = pd.read_csv(REPO / "Dataset" / "DSEC_hotel_guests_rooms_2023_01_2026_09.csv")
    gr["month"] = gr["month"].astype(str)
    gr = gr[gr["month"].isin(WINDOW)][["month", "guests", "rooms"]].copy()
    check(gr, "guests_rooms", lo=0, col="guests")
    gr.to_csv(DP / "clean_guests_rooms.csv", index=False)

    # ---- bus supply: DSAT monthly statistics
    bus = pd.read_csv(REPO / "Monthly_Bus_Database" / "bus_monthly_2020_2026.csv")
    bus["month"] = month_key(bus["year"], bus["month_no"])
    bus = bus[bus["month"].isin(WINDOW)].copy()
    bus = bus.rename(columns={"daily_avg_trips_wan": "bus_daily_avg_trips_wan",
                              "monthly_trips_est": "bus_monthly_trips"})
    bus = bus[["month", "bus_daily_avg_trips_wan", "bus_monthly_trips", "buses_in_service"]]
    check(bus, "bus", lo=0, col="bus_monthly_trips")
    bus.to_csv(DP / "clean_bus.csv", index=False)

    print("PASS: three module series cleaned, 45 complete months each")
    return 0


if __name__ == "__main__":
    sys.exit(main())
