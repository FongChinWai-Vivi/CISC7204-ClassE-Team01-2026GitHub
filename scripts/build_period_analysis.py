"""Build the month / quarter / year analysis layers and the optional analysis blocks.

Reads only committed files in ``data_processed/`` and writes the extra tables used by
section 14 of ``notebooks/cisc7204_pipeline_M3_vivi.ipynb`` (period detail) and by the
supplementary analysis note in ``reports/``.

Every table carries the grain in its name so the notebook never has to re-derive a join.

run:  python scripts/build_period_analysis.py
"""
import os

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(REPO, "data_processed")

PANEL = pd.read_csv(os.path.join(PROC, "monthly_panel_2023_01_2026_09.csv"))
QTR = pd.read_csv(os.path.join(PROC, "quarterly_panel_2023Q1_2026Q3.csv"))
ARR = pd.read_csv(os.path.join(PROC, "demand_monthly_arrivals.csv"))
DH = pd.read_csv(os.path.join(PROC, "demand_district_hour_panel_2023_2026.csv"))
ZONE = pd.read_csv(os.path.join(PROC, "match_zone_supply_demand.csv"))
HOUR = pd.read_csv(os.path.join(PROC, "match_hourly_profile.csv"))
ANN = pd.read_csv(os.path.join(PROC, "match_annual_alignment.csv"))
EVT = pd.read_csv(os.path.join(PROC, "match_event_crowding.csv"))
EVTS = pd.read_csv(os.path.join(PROC, "match_event_segment_crowding.csv"))
GWY = pd.read_csv(os.path.join(PROC, "demand_goldenweek_daily.csv"))
GATE = pd.read_csv(os.path.join(PROC, "match_gateways.csv"))
SHUT = pd.read_csv(os.path.join(PROC, "supply_shuttle_quarterly.csv"))
OFFI = pd.read_csv(os.path.join(PROC, "supply_official_series.csv"))

OUT = {}


def save(df, name, note=""):
    df.to_csv(os.path.join(PROC, name), index=False, encoding="utf-8-sig")
    OUT[name] = (df.shape, note)


# ---------------------------------------------------------------- 1. monthly detail
m = PANEL.copy()
m["month"] = pd.to_datetime(m["month"])
m = m.sort_values("month").reset_index(drop=True)

# year-on-year from the long 2008-2026 arrivals series (panel starts 2023, so the 2023
# row is compared with the pandemic trough and is flagged as such)
_long = ARR.copy()
_long["ym"] = pd.to_datetime(dict(year=_long["year"], month=_long["month"], day=1))
_long = _long.sort_values("ym").set_index("ym")["arrivals"]
m["arrivals_yoy_pct"] = (m["visitor_arrivals"] / m["month"].map(
    lambda d: _long.get(d - pd.DateOffset(years=1), np.nan)) - 1) * 100
m["arrivals_mom_pct"] = m["visitor_arrivals"].pct_change() * 100
m["arrivals_ma3"] = m["visitor_arrivals"].rolling(3, min_periods=1).mean()
m["bus_trips_per_arrival_ma3"] = m["bus_trips_per_arrival"].rolling(3, min_periods=1).mean()
m["hotel_occ_yoy_pp"] = m["hotel_occ_pct"] - m["hotel_occ_pct"].shift(12)
# the panel carries the district-hour total but not the ratio (it is a quarterly column),
# so the monthly click-per-arrival ratio is derived here to keep both grains comparable
m["district_hits_per_arrival"] = (m["mgto_district_headcount"] / m["visitor_arrivals"]).round(4)

# seasonality on the three complete years (2023-2025); 2026 is a partial year
_base = m[m["year"].between(2023, 2025)]
_idx = (_base.groupby("month_no")["visitor_arrivals"].mean()
        / _base["visitor_arrivals"].mean() * 100).round(2)
m["season_index_arrivals"] = m["month_no"].map(_idx)

# share-of-year, rank within year, and distance from the 3-month moving peak
m["arrivals_share_of_year_pct"] = (m["visitor_arrivals"]
                                   / m.groupby("year")["visitor_arrivals"].transform("sum") * 100).round(3)
m["rank_in_year"] = m.groupby("year")["visitor_arrivals"].rank(ascending=False).astype(int)
m["months_in_year"] = m.groupby("year")["month"].transform("size")

MON_COLS = ["year", "month_no", "months_in_year", "visitor_arrivals", "arrivals_yoy_pct",
            "arrivals_mom_pct", "arrivals_ma3", "arrivals_share_of_year_pct", "rank_in_year",
            "season_index_arrivals", "hotel_occ_pct", "hotel_occ_yoy_pp", "hotel_guests",
            "hotel_rooms", "bus_daily_avg_trips_wan", "bus_monthly_trips", "buses_in_service",
            "bus_trips_per_arrival", "bus_trips_per_arrival_ma3",
            "mgto_district_headcount", "district_hits_per_arrival"]
mon = m[MON_COLS + ["month", "quarter"]].copy()
mon[MON_COLS] = mon[MON_COLS].astype(float).round(4)
mon["month"] = mon["month"].dt.strftime("%Y-%m")
mon = mon[["month"] + MON_COLS]
save(mon, "monthly_detail_2023_01_2026_09.csv", "45 rows: every monthly indicator plus YoY, MoM, 3-month MA, seasonal index")

# seasonality index table with the per-year shape behind it
seas = pd.DataFrame({"month_no": range(1, 13)})
seas["season_index_arrivals"] = seas["month_no"].map(_idx)
piv = _base.pivot_table(index="month_no", columns="year", values="visitor_arrivals", aggfunc="mean")
for y in piv.columns:
    seas[f"mean_arrivals_{y}"] = seas["month_no"].map(piv[y]).round(0)
seas["mean_arrivals_2023_2025"] = (seas["month_no"].map(
    _base.groupby("month_no")["visitor_arrivals"].mean())).round(0)
seas["peak_flag"] = np.where(seas["season_index_arrivals"] >= 105, "peak",
                             np.where(seas["season_index_arrivals"] <= 95, "trough", "neutral"))
save(seas, "monthly_seasonality_index.csv", "12 rows: month-of-year index vs the 2023-2025 mean")

# month x zone share (45 x 3)
z = (DH.groupby(["year", "month", "zone"])["headcount"].sum().reset_index())
z["total"] = z.groupby(["year", "month"])["headcount"].transform("sum")
z["share_pct"] = (z["headcount"] / z["total"] * 100).round(3)
z["month"] = pd.to_datetime(dict(year=z["year"], month=z["month"], day=1)).dt.strftime("%Y-%m")
zs = z.pivot_table(index="month", columns="zone", values="share_pct").reset_index()
zs["total_headcount"] = z.groupby("month")["total"].first().values
save(zs, "zone_month_share.csv", "45 rows: monthly headcount share of the three zones")

# ---------------------------------------------------------------- 2. quarterly detail
q = QTR.copy()
q["order"] = q["quarter"].str.slice(0, 4).astype(int) * 10 + q["quarter"].str.slice(5).astype(int)
q = q.sort_values("order").reset_index(drop=True)
q["arrivals_qoq_pct"] = q["visitor_arrivals_sum"].pct_change() * 100
q["arrivals_yoy_pct"] = (q["visitor_arrivals_sum"]
                         / q["visitor_arrivals_sum"].shift(4) - 1) * 100
q["trips_per_arrival_qoq_pct"] = q["bus_trips_per_arrival"].pct_change() * 100
q["arrivals_per_month"] = (q["visitor_arrivals_sum"] / q["months_in_data"]).round(0)
q["arrivals_annualised"] = (q["arrivals_per_month"] * 12).round(0)
q["hotel_guests_per_room"] = (q["hotel_guests_sum"] / q["months_in_data"] / q["hotel_rooms_avg"]).round(3)
q["quarter_of_year"] = q["quarter"].str.slice(5).astype(int)
q["year"] = q["quarter"].str.slice(0, 4).astype(int)
q["partial"] = np.where(q["months_in_data"] < 3, "partial", "full")
q = q.drop(columns=["order"])
save(q, "quarterly_detail_2023Q1_2026Q3.csv", "15 rows: quarterly panel plus QoQ, YoY, annualised arrivals, guests per room")

# ---------------------------------------------------------------- 3. annual layer
# anchor years complete; 2026 is Jan-Sep and is shown both raw and scaled to 12 months
long_year = ARR.groupby("year")["arrivals"].sum().rename("dsec_arrivals_full_year")
a = ANN.copy()
a = a.merge(long_year, left_on="year", right_on="year", how="left")

y2026_partial = m.loc[m["year"] == 2026, "visitor_arrivals"].sum()
y2025_same = m.loc[(m["year"] == 2025) & (m["month_no"] <= 9), "visitor_arrivals"].sum()
scale_2026 = float(ANN.loc[ANN["year"] == 2025, "visitor_arrivals"].iloc[0]) / y2025_same * y2026_partial
a = pd.concat([a, pd.DataFrame([{
    "year": 2026, "bus_passenger_trips": np.nan, "visitor_arrivals": y2026_partial,
    "trips_per_visitor": np.nan, "bus_trips_yoy_pct": np.nan, "arrivals_yoy_pct": np.nan,
    "dsec_arrivals_full_year": np.nan}])], ignore_index=True)
a["months_in_data"] = np.where(a["year"] == 2026, 9, 12)
a.loc[a["year"] == 2026, "arrivals_annualised_est"] = round(scale_2026, 0)

# district-hour context per year (demand side is complete for the hour layer)
yr_zone = DH.groupby(["year", "zone"])["headcount"].sum().unstack().fillna(0)
yr_zone_share = (yr_zone.div(yr_zone.sum(axis=1), axis=0) * 100).round(3)
yr_zone_share["total_headcount"] = yr_zone.sum(axis=1).round(0)
yr_zone_share["months"] = DH.groupby("year")["month"].nunique()
yr_zone_share = yr_zone_share.reset_index()
save(yr_zone_share, "annual_zone_share.csv", "year x zone: headcount share and months covered")

yr_hour = DH.groupby(["year", "hour"])["headcount"].sum().unstack()
yr_hour_share = (yr_hour.div(yr_hour.sum(axis=1), axis=0) * 100).round(3)
yr_hour_share = yr_hour_share.reset_index()
save(yr_hour_share, "annual_hour_profile.csv", "year x hour: share of the annual district-hour headcount")

# month-of-year shape per year, from the 2008-2026 arrivals series
mp = ARR.pivot_table(index="year", columns="month", values="arrivals", aggfunc="sum")
mp_share = (mp.div(mp.sum(axis=1), axis=0) * 100).round(3).reset_index()
save(mp_share, "annual_month_profile.csv", "year x month: share of that year's arrivals")

# annual roll-up of the three years the hour layer covers completely
ann_full = yr_zone_share.merge(PANEL.groupby("year").agg(
    months=("month", "nunique"),
    arrivals_sum=("visitor_arrivals", "sum"),
    occ_avg=("hotel_occ_pct", "mean"),
    bus_trips_sum=("bus_monthly_trips", "sum"),
    trips_per_arrival=("bus_trips_per_arrival", "mean")).reset_index(), on="year", how="left", suffixes=("", "_panel"))
ann_full["arrivals_per_month"] = (ann_full["arrivals_sum"] / ann_full["months"]).round(0)
save(a.round(4), "annual_alignment_2018_2026.csv", "year: bus passenger trips vs arrivals, with 2026 partial and annualised estimate")
save(ann_full.round(3), "annual_summary_2023_2026.csv", "year: panel roll-up joined with zone shares")

# ---------------------------------------------------------------- 4. optional blocks
# 4a event crowding: route x phase, plus the segment tail
ev = EVT.copy()
piv2 = ev.pivot_table(index="route", columns="phase", values="crowded_share")
if {"Grand Prix", "Normal week"}.issubset(piv2.columns):
    delta = (piv2["Grand Prix"] - piv2["Normal week"]).dropna().round(2)
    ev = ev.merge(delta.rename("gp_minus_normal_pp").reset_index(), on="route", how="left")
else:
    ev["gp_minus_normal_pp"] = np.nan
ev.to_csv(os.path.join(PROC, "optional_event_crowding_summary.csv"), index=False, encoding="utf-8-sig")
OUT["optional_event_crowding_summary.csv"] = (ev.shape, "route x phase crowding, Grand Prix vs normal week")

seg = EVTS.copy()
seg = seg.sort_values(["crowded_share", "obs"], ascending=False)
save(seg.head(20), "optional_event_segment_crowding_top20.csv", "20 most crowded route segments during the Grand Prix")

# 4b gateway configuration
g = GATE.copy()
g["departures_per_stop"] = (g["daily_departures"] / g["stops"]).round(1)
g["share_of_gateway_departures_pct"] = (g["daily_departures"] / g["daily_departures"].sum() * 100).round(2)
g = g.sort_values("daily_departures", ascending=False)
save(g, "optional_gateways_summary.csv", "7 border / terminal gateways: stops, routes, daily departures")

# 4c shuttle channel per quarter
s = SHUT.copy()
s = s[s["departures"].notna()].copy()
s["riders_per_departure"] = np.where(s["departures"] > 0,
                                     (s["ridership"] / s["departures"]).round(2), np.nan)
s["order"] = s["year"].astype(int) * 10 + s["quarter"].str.slice(1).astype(int)
s = s.sort_values("order").drop(columns=["order"])
save(s, "optional_shuttle_quarterly.csv", "hotel / point-to-point shuttle departures and ridership by quarter")

# 4d golden week: peak multiplier against the month average
gw = GWY.copy()
gw["gw_short"] = np.where(gw["gw"].str.startswith("Spring"), "CNY", "Oct1")
gw["phase"] = np.where(gw["month_baseline_daily"] > 0,
                       (gw["arrivals"] / gw["month_baseline_daily"]).round(3), np.nan)
gws = (gw.groupby(["year", "gw_short"])
       .agg(days=("day_index", "nunique"),
            arrivals_total=("arrivals", "sum"),
            arrivals_mean=("arrivals", "mean"),
            ratio_mean=("ratio_vs_month_avg", "mean"),
            ratio_max=("ratio_vs_month_avg", "max"),
            baseline_daily=("month_baseline_daily", "first"))
       .round(3).reset_index())
gws["arrivals_mean"] = gws["arrivals_mean"].round(0)
gws["baseline_daily"] = gws["baseline_daily"].round(0)
peak = gw.loc[gw.groupby(["year", "gw_short"])["arrivals"].idxmax(),
              ["year", "gw_short", "date", "arrivals"]].rename(
    columns={"date": "peak_day", "arrivals": "peak_day_arrivals"})
gws = gws.merge(peak, on=["year", "gw_short"], how="left")
save(gws, "optional_goldenweek_summary.csv", "golden week: total, mean, peak multiplier vs the month average, peak day")

# 4e 2026 snapshot against the 2023-2025 baseline
base = DH[DH["year"].between(2023, 2025)]
b_zone = (base.groupby("zone")["headcount"].sum() / base["headcount"].sum() * 100).round(2)
b_hour = (base.groupby("hour")["headcount"].sum() / base["headcount"].sum() * 100).round(3)
y26 = DH[DH["year"] == 2026]
s_zone = (y26.groupby("zone")["headcount"].sum() / y26["headcount"].sum() * 100).round(2)
s_hour = (y26.groupby("hour")["headcount"].sum() / y26["headcount"].sum() * 100).round(3)
zshift = pd.DataFrame({"zone": b_zone.index,
                       "share_2023_2025_pct": b_zone.values,
                       "share_2026_jan_sep_pct": s_zone.reindex(b_zone.index).values})
zshift["delta_pp"] = (zshift["share_2026_jan_sep_pct"] - zshift["share_2023_2025_pct"]).round(2)
hshift = pd.DataFrame({"hour": b_hour.index,
                       "share_2023_2025_pct": b_hour.values,
                       "share_2026_jan_sep_pct": s_hour.reindex(b_hour.index).values})
hshift["delta_pp"] = (hshift["share_2026_jan_sep_pct"] - hshift["share_2023_2025_pct"]).round(3)
save(zshift, "optional_2026_zone_shift.csv", "zone share, 2023-2025 baseline vs 2026 Jan-Sep")
save(hshift, "optional_2026_hour_shift.csv", "hour-of-day share, 2023-2025 baseline vs 2026 Jan-Sep")

# ---------------------------------------------------------------- 5. print an audit
print("=" * 78)
for k, (shape, note) in OUT.items():
    print(f"{k:48s} {str(shape):12s} {note}")
print("=" * 78)


def r(x, y):
    return np.corrcoef(x, y)[0, 1]


w = m[(m["month"] >= "2023-01-01") & (m["month"] <= "2025-12-01")]
print("\nmonthly r(arrivals, bus trips) 2023-01..2025-12 :", round(r(w["visitor_arrivals"], w["bus_monthly_trips"]), 3), "n =", len(w))
print("monthly r(arrivals, trips per visitor)          :", round(r(w["visitor_arrivals"], w["bus_trips_per_arrival"]), 3))
print("quarterly r(arrivals, passenger trips)          :", round(r(q["visitor_arrivals_sum"], q["bus_monthly_trips_sum"]), 3), "n =", len(q))
for yv in sorted(w["year"].unique()):
    s2 = w[w["year"] == yv]
    print(f"  by year {yv} (n = {len(s2)}): r =", round(r(s2["visitor_arrivals"], s2["bus_monthly_trips"]), 3))
print("\nslope of trips per visitor on month index:",
      round(np.polyfit(np.arange(len(m)), m["bus_trips_per_arrival"], 1)[0], 4), "per month")
print("seasonal index extreme months:", seas.loc[seas['season_index_arrivals'].idxmax(), 'month_no'],
      "/", seas.loc[seas['season_index_arrivals'].idxmin(), 'month_no'])
print("\nannual alignment:\n", a.to_string(index=False))
print("\nzone shift 2026 vs baseline:\n", zshift.to_string(index=False))
print("\ngolden week:\n", gws.to_string(index=False))
print("\nevent crowding:\n", ev.to_string(index=False))
print("\ngateways:\n", g.to_string(index=False))
