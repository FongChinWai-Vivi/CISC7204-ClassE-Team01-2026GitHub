# -*- coding: utf-8 -*-
"""
CISC7204 Class E Team 01 - Interactive Dashboard builder
========================================================
Reads the cleaned panels committed in the team GitHub repository
(FongChinWai-Vivi/CISC7204-ClassE-Team01-2026GitHub, folder data_processed/)
and writes ONE self-contained, offline HTML dashboard:

    CISC7204_ClassE_Team01_Dashboard.html

No server, no network, no Python needed to open the result - plotly.js is
inlined and every number is computed from the CSVs in data/ at build time.

Run:
    C:\\Users\\lenovo\\anaconda3\\python.exe build_dashboard.py
"""

import json
import math
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT_HTML = os.path.join(HERE, "CISC7204_ClassE_Team01_Dashboard.html")
PLOTLY_JS = os.path.join(HERE, "plotly.min.js")

# ----------------------------------------------------------------------------
# Palette - team colour style (same family as figures/fig1..fig16)
# ----------------------------------------------------------------------------
C = {
    "navy": "#1B4965",
    "blue": "#2E86AB",
    "sky": "#62B6CB",
    "red": "#EE6C4D",
    "gold": "#F4A259",
    "green": "#3E8914",
    "purple": "#7B2CBF",
    "grey": "#8D99AE",
    "ink": "#12263A",
    "muted": "#374B61",
    "line": "#E1E8F0",
}
ZONE_COLOR = {
    "Macau Peninsula": C["blue"],
    "Taipa & Cotai": C["red"],
    "Coloane": C["green"],
}
FONT = dict(family="Segoe UI, Inter, Helvetica, Arial, sans-serif", size=12.5, color=C["ink"])
# every tick label is drawn at this weight/colour so the axes never look washed out
TICKFONT = dict(size=11.5, color="#0E2136", family="Segoe UI, Inter, Helvetica, Arial, sans-serif")


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA, name))


def style(fig, height=340, legend=True, margin=(58, 18, 40, 52), **kw):
    """Apply the house style to a figure."""
    if "showlegend" in kw:
        legend = kw.pop("showlegend")
    fig.update_layout(
        template="plotly_white",
        font=FONT,
        height=height,
        margin=dict(l=margin[0], r=margin[1], t=margin[2], b=margin[3]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white", bordercolor=C["line"],
                        font=dict(size=12.5, color="#0B1A2B")),
        showlegend=legend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                    font=dict(size=11.5, color="#0E2136")),
        **kw,
    )
    fig.update_xaxes(showgrid=False, linecolor=C["line"], zeroline=False, tickfont=TICKFONT)
    fig.update_yaxes(gridcolor=C["line"], zeroline=False, tickfont=TICKFONT)
    return fig


# ----------------------------------------------------------------------------
# 1. Load the panels
# ----------------------------------------------------------------------------
arrivals_long = load("demand_monthly_arrivals.csv")
monthly = load("monthly_panel_2023_01_2026_09.csv")
quarterly = load("quarterly_panel_2023Q1_2026Q3.csv")
zone_match = load("match_zone_supply_demand.csv")
hour_match = load("match_hourly_profile.csv")
district_metrics = load("district_map_metrics.csv")
season = load("monthly_seasonality_index.csv")
shift_zone = load("optional_2026_zone_shift.csv")
shift_hour = load("optional_2026_hour_shift.csv")
golden = load("demand_goldenweek_daily.csv")
annual = load("annual_alignment_2018_2026.csv")
# hotel block - copied from Dataset/ of the team repository on GitHub
hotel_occ = load("hotel_occ_monthly_2023_2026.csv")          # Dataset/hotel_occ_total_summary.csv
hotel_star = load("hotel_guests_by_star_2023_2026.csv")      # Dataset/hotel_Arrival_byHotelStar_summary.csv
hotel_hist = load("hotel_occ_history_2014_2025.csv")         # Dataset/Hotel_occ_total.csv

with open(os.path.join(DATA, "macau_stats_zones.geojson"), encoding="utf-8") as fh:
    GEO = json.load(fh)

panel = load("demand_district_hour_panel_2023_2026.csv")

# ----------------------------------------------------------------------------
# 2. Derived statistics (nothing below is hard-coded)
# ----------------------------------------------------------------------------
WIN = monthly[(monthly.year >= 2023) & (monthly.year <= 2025)]          # 36-month estimation window
win_arrivals = float(WIN.visitor_arrivals.sum())
win_guests = float(WIN.hotel_guests.sum())
win_bus = float(WIN.bus_monthly_trips.sum())
r_month = float(np.corrcoef(WIN.visitor_arrivals, WIN.bus_monthly_trips)[0, 1])

q_all = quarterly.dropna(subset=["bus_trips_per_arrival"])
q_first, q_last = q_all.iloc[0], q_all.iloc[-1]
_win = quarterly[quarterly.quarter == "2025Q4"]
q_win_last = _win.iloc[0] if len(_win) else q_all.iloc[-1]
# headline ratio is reported on the 36-month window: 2023Q1 -> 2025Q4
trip_drop_pct = (q_win_last.bus_trips_per_arrival / q_first.bus_trips_per_arrival - 1) * 100

share = district_metrics.share_total_pct / 100.0
hhi = float((share ** 2).sum() * 10000)
top3_share = float(district_metrics.share_total_pct.nlargest(3).sum())

covai = zone_match[zone_match.zone == "Taipa & Cotai"].iloc[0]
peninsula = zone_match[zone_match.zone == "Macau Peninsula"].iloc[0]
coloane = zone_match[zone_match.zone == "Coloane"].iloc[0]

# ----------------------------------------------------------------------------
# 3. Figure 1 - long-run monthly arrivals, 2015-2026
# ----------------------------------------------------------------------------
al = arrivals_long[arrivals_long.year >= 2015].copy()
al["dt"] = pd.to_datetime(al.date)


def year_slice(df, lo, hi):
    return df[(df.year >= lo) & (df.year <= hi)]


pre = year_slice(al, 2015, 2019)
pand = year_slice(al, 2020, 2022)
post = year_slice(al, 2023, 2026)

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=pre["dt"], y=pre.arrivals / 1e6, mode="lines", name="2015-2019 (pre-pandemic)",
                          line=dict(color=C["navy"], width=2.4),
                          hovertemplate="%{x|%b %Y}<br>%{y:.2f}M arrivals<extra></extra>"))
fig1.add_trace(go.Scatter(x=pand["dt"], y=pand.arrivals / 1e6, mode="lines", name="2020-2022 (pandemic, red dashed)",
                          line=dict(color=C["red"], width=2.2, dash="dash"),
                          hovertemplate="%{x|%b %Y}<br>%{y:.3f}M arrivals<extra></extra>"))
fig1.add_trace(go.Scatter(x=post["dt"], y=post.arrivals / 1e6, mode="lines+markers", name="2023-2026 (recovery)",
                          line=dict(color=C["blue"], width=2.6), marker=dict(size=4),
                          hovertemplate="%{x|%b %Y}<br>%{y:.2f}M arrivals<extra></extra>"))
fig1.add_vrect(x0="2023-01-01", x1="2025-12-31", fillcolor=C["gold"], opacity=0.16, line_width=0,
               annotation_text="36-month estimation window", annotation_position="top left",
               annotation_font_size=11, annotation_font_color="#2C3E55")
fig1.add_annotation(x="2019-08-01", y=3.6, text="2019 peak &asymp; 3.28M / month",
                    showarrow=True, arrowhead=2, ax=-10, ay=-32, font=dict(size=11, color=C["navy"]))
low = al[al.year == 2020].arrivals.min()
low_row = al[al.arrivals == low].iloc[0]
fig1.add_annotation(x=low_row["dt"], y=low / 1e6, text="Apr 2020: {:,.0f} arrivals".format(low),
                    showarrow=True, arrowhead=2, ax=30, ay=-38, font=dict(size=11, color=C["red"]))
fig1.update_yaxes(title="Visitor arrivals (million / month)")
style(fig1, height=330, margin=(58, 18, 30, 52))
fig1.update_layout(legend=dict(orientation="h", y=1.12, x=0))

# ----------------------------------------------------------------------------
# 4. Figure 2 - arrivals vs bus trips, monthly, 2023-01..2026-09
# ----------------------------------------------------------------------------
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=monthly.month, y=monthly.visitor_arrivals / 1e6, name="Visitor arrivals (M, left)",
                      marker_color=C["sky"], opacity=0.85,
                      hovertemplate="%{x}<br>%{y:.2f}M arrivals<extra></extra>"))
fig2.add_trace(go.Scatter(x=monthly.month, y=monthly.bus_monthly_trips / 1e6, name="Bus passenger trips (M, right)",
                          yaxis="y2", mode="lines+markers",
                          line=dict(color=C["navy"], width=2.6), marker=dict(size=5),
                          hovertemplate="%{x}<br>%{y:.1f}M trips<extra></extra>"))
fig2.add_trace(go.Scatter(x=monthly.month, y=monthly.bus_trips_per_arrival, name="Trips per visitor (right)",
                          yaxis="y2", mode="lines", visible="legendonly",
                          line=dict(color=C["red"], width=2, dash="dot"),
                          hovertemplate="%{x}<br>%{y:.2f} trips / visitor<extra></extra>"))
fig2.add_vrect(x0="2025-09-30", x1="2026-09-30", fillcolor=C["grey"], opacity=0.10, line_width=0,
               annotation_text="2026 (partial)", annotation_position="top right", annotation_font_size=10)
fig2.update_yaxes(title="Visitor arrivals (million)", range=[0, monthly.visitor_arrivals.max() / 1e6 * 1.18])
fig2.update_layout(
    yaxis2=dict(title="Bus passenger trips (million)", overlaying="y", side="right",
                showgrid=False, tickfont=TICKFONT),
    margin=dict(l=58, r=58, t=30, b=40),
)
style(fig2, height=330, margin=(58, 58, 30, 40))
fig2.add_annotation(x=0.02, y=0.06, xref="paper", yref="paper", showarrow=False,
                    text="Pearson r = {:.3f} (n = {} months, 2023-01 to 2025-12)".format(r_month, len(WIN)),
                    font=dict(size=11, color="#2C3E55"), align="left")

# ----------------------------------------------------------------------------
# 5. Figure 3 - bus trips per visitor by quarter
# ----------------------------------------------------------------------------
fig3 = go.Figure()
in_win = q_all.quarter <= "2025Q4"
fig3.add_trace(go.Bar(x=q_all.quarter, y=q_all.bus_trips_per_arrival, name="Bus trips per visitor",
                      marker_color=[C["blue"] if w else C["grey"] for w in in_win],
                      hovertemplate="%{x}<br>%{y:.2f} trips / visitor<extra></extra>"))
fig3.add_trace(go.Scatter(x=q_all.quarter, y=q_all.bus_trips_per_arrival, mode="lines+markers",
                          line=dict(color=C["navy"], width=2), marker=dict(size=5), showlegend=False,
                          hoverinfo="skip"))
fig3.add_annotation(x="2025Q4", y=q_win_last.bus_trips_per_arrival,
                    text="{:.2f} &rarr; {:.2f} ({:+.0f}%)<br>2023Q1 &rarr; 2025Q4".format(
                        q_first.bus_trips_per_arrival, q_win_last.bus_trips_per_arrival, trip_drop_pct),
                    showarrow=True, arrowhead=2, ax=-58, ay=26, font=dict(size=11, color=C["red"]))
fig3.update_yaxes(title="Bus trips per visitor")
style(fig3, height=330, showlegend=False, margin=(58, 18, 30, 46))
fig3.update_layout(legend=dict(orientation="h", y=1.1))

# ----------------------------------------------------------------------------
# 6. Figure 4 - three-zone supply / demand mismatch
# ----------------------------------------------------------------------------
zone_order = ["Macau Peninsula", "Taipa & Cotai", "Coloane"]
zm = zone_match.set_index("zone").loc[zone_order].reset_index()
fig4 = go.Figure()
for col, label, color in [
    ("demand_share_pct", "Visitor demand", C["red"]),
    ("departures_share_pct", "Scheduled departures", C["blue"]),
    ("stops_share_pct", "Bus stops", C["sky"]),
]:
    fig4.add_trace(go.Bar(x=zm.zone, y=zm[col], name=label, marker_color=color,
                          text=["{:.1f}%".format(v) for v in zm[col]], textposition="outside",
                          textfont=dict(size=11.5, color="#0E2136"),
                          hovertemplate="%{x}<br>" + label + ": %{y:.2f}%<extra></extra>"))
fig4.update_yaxes(title="Share of city total (%)", range=[0, 80])
fig4.update_layout(barmode="group", bargap=0.28, bargroupgap=0.08)
style(fig4, height=330, margin=(58, 18, 30, 46))

# ----------------------------------------------------------------------------
# 7. Figure 5 - demand carried per scheduled departure
# ----------------------------------------------------------------------------
fig5 = go.Figure()
fig5.add_trace(go.Bar(
    y=zm.zone, x=zm.demand_per_departure, orientation="h",
    marker_color=[ZONE_COLOR[z] for z in zm.zone],
    text=["{:,.0f}".format(v) for v in zm.demand_per_departure], textposition="outside",
    textfont=dict(size=12.5, color="#0E2136"),
    customdata=zm[["supply_demand_ratio", "daily_bus_departures", "gap_index"]].values,
    hovertemplate=("%{y}<br>%{x:,.0f} visitor headcount per departure"
                   "<br>Supply / demand ratio: %{customdata[0]:.3f}"
                   "<br>Daily departures: %{customdata[1]:,.0f}"
                   "<br>Gap index: %{customdata[2]:+.2f} pp<extra></extra>"),
))
fig5.update_xaxes(title="Visitor headcount per scheduled departure (2026 H1)", range=[0, 250])
fig5.update_yaxes(autorange="reversed")
style(fig5, height=330, showlegend=False, margin=(120, 40, 30, 46))

# ----------------------------------------------------------------------------
# 8. Figure 6 - hour-of-day demand vs scheduled supply
# ----------------------------------------------------------------------------
h = hour_match.copy()
fig6 = go.Figure()
fig6.add_trace(go.Scatter(x=h.hour, y=h.demand_share_pct, mode="lines", name="Visitor demand share (all periods)",
                          line=dict(color=C["grey"], width=2, dash="dot"),
                          hovertemplate="%{x}:00<br>%{y:.2f}% of daily demand<extra></extra>"))
fig6.add_trace(go.Scatter(x=h.hour, y=h.demand_share_pct, mode="lines", name="Visitor demand share (filtered)",
                          line=dict(color=C["red"], width=3),
                          hovertemplate="%{x}:00<br>%{y:.2f}% of daily demand<extra></extra>"))
fig6.add_trace(go.Scatter(x=h.hour, y=h.supply_share_weekday_pct, mode="lines", name="Scheduled departures (weekday)",
                          line=dict(color=C["blue"], width=2.6),
                          hovertemplate="%{x}:00<br>%{y:.2f}% of daily departures<extra></extra>"))
fig6.add_trace(go.Scatter(x=h.hour, y=h.supply_share_weekend_pct, mode="lines",
                          name="Scheduled departures (weekend)", visible="legendonly",
                          line=dict(color=C["sky"], width=2.2, dash="dash"),
                          hovertemplate="%{x}:00<br>%{y:.2f}% of daily departures<extra></extra>"))
fig6.add_trace(go.Bar(x=h.hour, y=h.gap_weekday_pp, name="Gap vs weekday supply (pp)", yaxis="y2",
                      marker_color=[C["red"] if v < 0 else C["green"] for v in h.gap_weekday_pp],
                      opacity=0.35,
                      hovertemplate="%{x}:00<br>%{y:+.2f} pp (supply &minus; demand)<extra></extra>"))
night = h[h.hour.isin([0, 1, 2, 3, 4, 5])]
fig6.add_annotation(x=2.5, y=h.demand_share_pct.iloc[0] * 1.02,
                    text="00:00-05:59: {:.1f}% of demand vs {:.1f}% of weekday departures".format(
                        night.demand_share_pct.sum(), night.supply_share_weekday_pct.sum()),
                    showarrow=False, font=dict(size=11, color="#2C3E55"))
fig6.update_xaxes(title="Hour of day", dtick=2)
fig6.update_yaxes(title="Share of daily total (%)")
fig6.update_layout(yaxis2=dict(title="Gap (percentage points)", overlaying="y", side="right",
                               showgrid=False, range=[-8, 8], tickfont=TICKFONT),
                   margin=dict(l=58, r=58, t=30, b=46))
style(fig6, height=360, margin=(58, 58, 30, 46))

# ----------------------------------------------------------------------------
# 9. Figure 7 - 24-district choropleth (metric switched in the browser)
# ----------------------------------------------------------------------------
dm = district_metrics.copy()
en_map = panel[["district_cn", "district_en"]].drop_duplicates().set_index("district_cn")["district_en"]
dm["district_en"] = dm.district_cn.map(en_map).fillna(dm.district_cn)
dm = dm.sort_values("share_total_pct", ascending=False)

metric_defs = {
    "share": dict(col="share_total_pct", title="Headcount share of city total (%)", scale="Blues", fmt=".2f"),
    "density": dict(col="hits_per_km2_month", title="Headcount per km&sup2; per month", scale="Viridis", fmt=",.0f"),
    "delta": dict(col="delta_pp", title="2026 share shift (percentage points)", scale="RdBu", fmt="+.2f"),
    "perdep": dict(col="hits_per_departure", title="Headcount per scheduled departure", scale="OrRd", fmt=",.0f"),
}

customdata = dm[["hits_total", "stops", "peak_hour", "night_share_pct", "weekday_departures",
                 "hits_per_km2_month", "delta_pp", "hits_per_departure", "district_en",
                 "share_total_pct"]].values

fig7 = go.Figure(go.Choropleth(
    geojson=GEO,
    featureidkey="properties.district_cn",
    locations=dm.district_cn,
    # sqrt scale: the share distribution is extremely skewed (Cotai alone holds 44%),
    # a linear scale would paint 20 of the 24 districts the same pale colour
    z=np.sqrt(dm.share_total_pct.values),
    colorscale=[[0, "#F7FBFF"], [0.15, "#DEEBF7"], [0.35, "#9ECAE1"],
                [0.60, "#4292C6"], [0.82, "#08519C"], [1, "#08306B"]],
    marker_line_color="white",
    marker_line_width=1.0,
    zmin=0, zmax=math.sqrt(float(dm.share_total_pct.max())),
    colorbar=dict(
        title=dict(text="Share of<br>city total (%)", font=dict(size=11, color="#0E2136")), tickfont=TICKFONT, thickness=12, len=0.72,
        tickvals=[math.sqrt(v) for v in (1, 2, 5, 10, 20, 30, 44)],
        ticktext=["1", "2", "5", "10", "20", "30", "44"],
    ),
    customdata=customdata,
    hovertemplate=("<b>%{customdata[8]}</b> (%{location})<br>"
                   "Headcount share: %{customdata[9]:.2f}%<br>"
                   "Total headcount: %{customdata[0]:,.0f}<br>"
                   "Stops: %{customdata[1]}<br>"
                   "Weekday departures: %{customdata[4]:,.0f}<br>"
                   "Peak hour: %{customdata[2]}:00<br>"
                   "Night share (22:00-05:59): %{customdata[3]:.1f}%<extra></extra>"),
))
fig7.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
fig7.update_layout(
    height=470,
    margin=dict(l=6, r=6, t=6, b=6),
    paper_bgcolor="rgba(0,0,0,0)",
    font=FONT,
    hoverlabel=dict(bgcolor="white", bordercolor=C["line"],
                        font=dict(size=12.5, color="#0B1A2B")),
)
fig7.update_layout(dragmode="pan")

# ----------------------------------------------------------------------------
# 10. Figure 8 - district x hour heatmap (rebuilt in the browser on filter)
# ----------------------------------------------------------------------------
pivot = (panel.groupby(["district_cn", "district_en", "hour"]).headcount.sum()
         .reset_index())
tot = pivot.groupby("district_cn").headcount.sum()
pivot["share"] = pivot.apply(lambda r: r.headcount / tot[r.district_cn] * 100, axis=1)
order = tot.sort_values(ascending=False).index.tolist()
heat_z = [[0] * 24 for _ in order]
for _, row in pivot.iterrows():
    heat_z[order.index(row.district_cn)][int(row.hour)] = row.share
heat_y = [en_map.get(c, c) for c in order]

fig8 = go.Figure(go.Heatmap(
    z=heat_z, x=list(range(24)), y=heat_y, colorscale="YlOrRd", zmin=0, zmax=8,
    colorbar=dict(title=dict(text="% of that<br>district's day", font=dict(size=10, color="#0E2136")), tickfont=dict(size=10, color="#0E2136"), thickness=10, len=0.8),
    hovertemplate="%{y}<br>%{x}:00<br>%{z:.2f}% of the district's headcount<extra></extra>",
))
fig8.update_xaxes(title="Hour of day", dtick=3, showgrid=False)
fig8.update_yaxes(autorange="reversed", tickfont=TICKFONT, showgrid=False)
fig8.update_layout(height=470, margin=dict(l=150, r=10, t=10, b=44), paper_bgcolor="rgba(0,0,0,0)",
                   font=FONT, hoverlabel=dict(bgcolor="white", bordercolor=C["line"],
                     font=dict(size=11.5, color="#0B1A2B")))

# ----------------------------------------------------------------------------
# 11. Figure 9 - seasonality index
# ----------------------------------------------------------------------------
sf = season.copy()
fig9 = go.Figure()
fig9.add_trace(go.Bar(x=sf.month_no, y=sf.season_index_arrivals, name="Seasonal index (2023-2025 mean = 100)",
                      marker_color=[C["red"] if f == "peak" else C["sky"] for f in sf.peak_flag],
                      hovertemplate="Month %{x}<br>index %{y:.2f}<extra></extra>"))
fig9.add_hline(y=100, line=dict(color=C["navy"], width=1.4, dash="dash"),
               annotation_text="annual mean", annotation_position="right",
               annotation_font_size=10)
fig9.update_xaxes(title="Month of year", dtick=1)
fig9.update_yaxes(title="Seasonal index", range=[80, 120])
style(fig9, height=330, showlegend=False, margin=(58, 18, 30, 46))

# ----------------------------------------------------------------------------
# 12. Figure 10 - 2026 shift, zone and hour
# ----------------------------------------------------------------------------
fig10 = go.Figure()
fig10.add_trace(go.Bar(x=shift_zone.zone, y=shift_zone.delta_pp, name="Zone share shift (pp)",
                       marker_color=[C["red"] if v < 0 else C["green"] for v in shift_zone.delta_pp],
                       text=["{:+.2f}".format(v) for v in shift_zone.delta_pp], textposition="outside",
                       textfont=dict(size=11.5, color="#0E2136"),
                       hovertemplate="%{x}<br>%{y:+.2f} pp vs 2023-2025 baseline<extra></extra>"))
fig10.update_xaxes(title="Zone")
fig10.update_yaxes(title="Share shift, 2026 vs baseline (pp)", range=[-2.6, 2.9])
fig10.update_traces(cliponaxis=False)
style(fig10, height=300, showlegend=False, margin=(58, 22, 30, 46))

fig11 = go.Figure()
sh = shift_hour.copy()
fig11.add_trace(go.Bar(x=sh.hour, y=sh.delta_pp, name="Hour share shift (pp)",
                       marker_color=[C["red"] if v < 0 else C["green"] for v in sh.delta_pp],
                       hovertemplate="%{x}:00<br>%{y:+.3f} pp vs 2023-2025 baseline<extra></extra>"))
fig11.update_xaxes(title="Hour of day", dtick=3)
fig11.update_yaxes(title="Share shift (pp)")
fig11.update_traces(cliponaxis=False)
style(fig11, height=340, showlegend=False, margin=(58, 22, 30, 46))

# ----------------------------------------------------------------------------
# 13. Figure 12 - Golden Week daily intensity
# ----------------------------------------------------------------------------
gw = golden[golden.gw == "1st October Golden Week"]
gfig = go.Figure()
gw_years = [2019, 2023, 2024, 2025]
palette = [C["grey"], C["sky"], C["blue"], C["navy"]]
for yr, col in zip(gw_years, palette):
    d = gw[gw.year == yr].sort_values("day_index")
    if len(d):
        gfig.add_trace(go.Scatter(x=d.day_index, y=d.ratio_vs_month_avg, mode="lines+markers", name=str(yr),
                                  line=dict(color=col, width=2.2), marker=dict(size=6),
                                  customdata=d[["date", "arrivals"]].values,
                                  hovertemplate="%{customdata[0]}<br>%{y:.2f}&times; the month average"
                                                "<br>%{customdata[1]:,.0f} arrivals<extra></extra>"))
spr = golden[(golden.gw == "Spring Festival Golden Week") & (golden.year == 2026)].sort_values("day_index")
if len(spr):
    gfig.add_trace(go.Scatter(x=spr.day_index, y=spr.ratio_vs_month_avg, mode="lines+markers",
                              name="2026 Spring Festival (partial year)", line=dict(color=C["gold"], width=2.4, dash="dot"),
                              marker=dict(size=6),
                              customdata=spr[["date", "arrivals"]].values,
                              hovertemplate="%{customdata[0]}<br>%{y:.2f}&times; the month average"
                                            "<br>%{customdata[1]:,.0f} arrivals<extra></extra>"))
gfig.add_hline(y=1.0, line=dict(color="#2C3E55", width=1.2, dash="dash"),
               annotation_text="monthly average", annotation_position="right", annotation_font_size=10)
gfig.update_xaxes(title="Day of Golden Week", dtick=1)
gfig.update_yaxes(title="Daily arrivals / month average")
style(gfig, height=330, margin=(58, 18, 30, 46))
gfig.update_layout(legend=dict(orientation="h", y=1.14, x=0))

# ----------------------------------------------------------------------------
# 13b. Hotel block - the third leg of the title argument
#      (visitor arrivals -> hotel occupancy -> bus ridership)
#      source files: Dataset/hotel_occ_total_summary.csv,
#                    Dataset/hotel_Arrival_byHotelStar_summary.csv,
#                    Dataset/Hotel_occ_total.csv
# ----------------------------------------------------------------------------
ho = hotel_occ.copy()
ho["dt"] = pd.to_datetime(dict(year=ho.Year.astype(int), month=ho.Month.astype(int), day=1))
ho["ym"] = ho.dt.dt.strftime("%Y-%m")

hm = monthly[["month", "year", "visitor_arrivals", "hotel_guests", "hotel_rooms",
              "bus_monthly_trips", "bus_trips_per_arrival"]].merge(
    ho[["ym", "Occupancy_rate"]], left_on="month", right_on="ym", how="left").rename(
    columns={"Occupancy_rate": "occ"})

hm_win = hm[hm.year.between(2023, 2025)].dropna(subset=["occ"])
occ_win_mean = float(hm_win.occ.mean())
_hp = hm.dropna(subset=["occ"])
_peak = _hp.loc[_hp.occ.idxmax()]
occ_peak = float(_peak.occ)
occ_peak_ym = str(_peak.month)
r_occ_arr = float(np.corrcoef(hm_win.occ, hm_win.visitor_arrivals)[0, 1])
r_occ_bus = float(np.corrcoef(hm_win.occ, hm_win.bus_monthly_trips)[0, 1])
r_occ_tpv = float(np.corrcoef(hm_win.occ, hm_win.bus_trips_per_arrival)[0, 1])
_occ_23 = float(hm[hm.year == 2023].occ.mean())
_occ_26 = float(hm[hm.year == 2026].occ.mean())

st = hotel_star.copy()
st["dt"] = pd.to_datetime(dict(year=st.Year.astype(int), month=st.Month.astype(int), day=1))
st["ym"] = st.dt.dt.strftime("%Y-%m")
st["cls"] = st.Hotel_Establishments.str.replace(" Hotels", "", regex=False)
STAR_ORDER = ["2-Star", "3-Star", "4-Star", "5-Star"]
STAR_COLOR = {"2-Star": C["sky"], "3-Star": C["blue"], "4-Star": C["navy"], "5-Star": C["gold"]}
star_by_ym = {c: st[st.cls == c].set_index("ym").Number_of_guests.reindex(hm.month).fillna(0.0)
              for c in STAR_ORDER}
star_total = float(sum(star_by_ym[c].sum() for c in STAR_ORDER))
five_share = float(star_by_ym["5-Star"].sum() / max(star_total, 1.0) * 100)
five_share_23 = float(star_by_ym["5-Star"][hm.year.values == 2023].sum() /
                      max(sum(star_by_ym[c][hm.year.values == 2023].sum() for c in STAR_ORDER), 1.0) * 100)
five_share_26 = float(star_by_ym["5-Star"][hm.year.values == 2026].sum() /
                      max(sum(star_by_ym[c][hm.year.values == 2026].sum() for c in STAR_ORDER), 1.0) * 100)

hh = hotel_hist.rename(columns={"Hotel Establishments": "establishment",
                               "Occupancy rate": "occ", "Remark": "remark1",
                               "Remark.1": "remark2"})[["Year", "Month", "occ"]]
hh = hh.rename(columns={"Year": "year", "Month": "month"}).dropna()
hh["year"] = hh.year.astype(int)
hh["month"] = hh.month.astype(int)
hh["dt"] = pd.to_datetime(dict(year=hh.year, month=hh.month, day=1))
hh = hh.sort_values("dt")
occ_2019 = float(hh.loc[hh.year == 2019, "occ"].mean())
occ_2025 = float(hh.loc[hh.year == 2025, "occ"].mean())

# --- Figure 3 - monthly arrivals against the hotel occupancy rate ---
figH1 = go.Figure()
figH1.add_trace(go.Bar(x=list(hm.month), y=list(hm.visitor_arrivals / 1e6),
                       name="Visitor arrivals (million, left)",
                       marker=dict(color=C["sky"], line=dict(width=0)), opacity=0.92,
                       hovertemplate="%{x}<br>%{y:.2f}M visitor arrivals<extra></extra>"))
figH1.add_trace(go.Scatter(x=list(hm.month), y=list(hm.occ), name="Hotel occupancy rate (%, right)",
                           yaxis="y2", mode="lines+markers",
                           line=dict(color=C["red"], width=2.6), marker=dict(size=6, color=C["red"]),
                           hovertemplate="%{x}<br>%{y:.1f}% hotel occupancy<extra></extra>"))
figH1.add_vrect(x0="2025-09-30", x1="2026-09-30", fillcolor=C["grey"], opacity=0.10, line_width=0,
                annotation_text="2026 partial", annotation_position="top right", annotation_font_size=10)
figH1.add_annotation(x=0.015, y=0.96, xref="paper", yref="paper", showarrow=False, xanchor="left",
                     text="arrivals vs occupancy: r = {:.2f}".format(r_occ_arr),
                     font=dict(size=11.5, color="#0E2136"), bgcolor="rgba(255,255,255,.74)")
figH1.update_yaxes(title="Visitor arrivals (million)",
                   range=[0, float(hm.visitor_arrivals.max()) / 1e6 * 1.22])
figH1.update_layout(yaxis2=dict(title="Hotel occupancy rate (%)", overlaying="y", side="right",
                                range=[40, 100], showgrid=False, tickfont=TICKFONT))
style(figH1, height=356, margin=(58, 26, 40, 52))

# --- Figure 4 - who fills the rooms: guests by hotel class ---
figH3 = go.Figure()
for c in STAR_ORDER:
    figH3.add_trace(go.Bar(x=list(hm.month), y=[float(v) for v in star_by_ym[c]],
                           name=c + " hotels", marker=dict(color=STAR_COLOR[c], line=dict(width=0)),
                           hovertemplate="%{x}<br>%{y:,.0f} hotel guests<extra></extra>"))
figH3.update_layout(barmode="stack", bargap=0.22)
figH3.update_yaxes(title="Hotel guests per month")
figH3.add_annotation(x=0.015, y=0.96, xref="paper", yref="paper", showarrow=False, xanchor="left",
                     text="5-star share: {:.1f}% in 2023 &rarr; {:.1f}% in 2026".format(
                         five_share_23, five_share_26),
                     font=dict(size=11.5, color="#0E2136"), bgcolor="rgba(255,255,255,.74)")
style(figH3, height=356, margin=(58, 26, 40, 52))

# --- Figure 5 - occupancy against the ridership intensity, one series per year ---
figH2 = go.Figure()
YEAR_COLOR = {2023: C["sky"], 2024: C["blue"], 2025: C["navy"], 2026: C["gold"]}
for yr in sorted(int(v) for v in hm.year.unique()):
    s = hm[(hm.year == yr)].dropna(subset=["occ"])
    figH2.add_trace(go.Scatter(
        x=[float(v) for v in s.occ], y=[float(v) for v in s.bus_trips_per_arrival],
        mode="markers", name=str(yr),
        marker=dict(size=8.5, color=YEAR_COLOR.get(yr, C["grey"]), line=dict(width=1, color="white")),
        customdata=[[m] for m in s.month],
        hovertemplate="%{customdata[0]}<br>%{x:.1f}% occupancy"
                      "<br>%{y:.2f} bus trips per visitor<extra></extra>"))
figH2.update_xaxes(title="Hotel occupancy rate (%)")
figH2.update_yaxes(title="Bus trips per visitor")
figH2.add_annotation(x=0.015, y=0.96, xref="paper", yref="paper", showarrow=False, xanchor="left",
                     text="occupancy vs trips per visitor: r = {:.2f}".format(r_occ_tpv),
                     font=dict(size=11.5, color="#0E2136"), bgcolor="rgba(255,255,255,.74)")
style(figH2, height=356, margin=(58, 26, 40, 52))

# --- Figure 6 - the long occupancy record, 2014-2026 ---
figH4 = go.Figure()
figH4.add_trace(go.Scatter(x=list(hh.dt), y=list(hh.occ), mode="lines", name="Hotel occupancy rate",
                           line=dict(color=C["navy"], width=2.3),
                           hovertemplate="%{x|%Y-%m}<br>%{y:.1f}% occupancy<extra></extra>"))
figH4.add_vrect(x0="2020-02-01", x1="2023-01-01", fillcolor=C["red"], opacity=0.10, line_width=0,
                annotation_text="pandemic years", annotation_position="top left", annotation_font_size=10)
figH4.add_hline(y=occ_2019, line=dict(color=C["gold"], width=1.7, dash="dash"),
                annotation_text="2019 mean {:.1f}%".format(occ_2019),
                annotation_position="bottom right", annotation_font_size=10)
figH4.update_yaxes(title="Occupancy rate (%)", range=[0, 100])
style(figH4, height=356, margin=(58, 26, 40, 52), showlegend=False)

hotel_payload = dict(
    m=list(hm.month),
    y=[int(v) for v in hm.year],
    arr=[float(v) for v in hm.visitor_arrivals],
    occ=[None if pd.isna(v) else float(v) for v in hm.occ],
    tpv=[float(v) for v in hm.bus_trips_per_arrival],
    bus=[float(v) for v in hm.bus_monthly_trips],
    star={c: [float(v) for v in star_by_ym[c]] for c in STAR_ORDER},
    cls=STAR_ORDER,
    years=sorted(int(v) for v in hm.year.unique()),
)

# ----------------------------------------------------------------------------
# 14. Browser payload (compact arrays for the linked views)
# ----------------------------------------------------------------------------
dist_list = dm[["district_cn", "district_en", "zone", "share_total_pct", "hits_per_km2_month",
                "delta_pp", "hits_per_departure", "stops", "peak_hour", "night_share_pct",
                "weekday_departures", "hits_total"]].copy()
dist_index = {cn: i for i, cn in enumerate(dist_list.district_cn)}

payload = {
    "districts": [
        dict(cn=r.district_cn, en=r.district_en, zone=r.zone, share=float(r.share_total_pct),
             density=float(r.hits_per_km2_month), delta=float(r.delta_pp),
             perdep=float(r.hits_per_departure), stops=int(r.stops), peak=int(r.peak_hour),
             night=float(r.night_share_pct), wdep=float(r.weekday_departures),
             hits=float(r.hits_total))
        for r in dist_list.itertuples()
    ],
    "years": sorted(int(y) for y in panel.year.unique()),
    "zones": zone_order,
    "panel": {
        "y": panel.year.astype(int).tolist(),
        "m": panel.month.astype(int).tolist(),
        "h": panel.hour.astype(int).tolist(),
        "d": [dist_index[c] for c in panel.district_cn],
        "v": [float(x) for x in panel.headcount],
    },
    "kpi": dict(
        arrivals=win_arrivals, guests=win_guests, bus=win_bus, r=r_month,
        trips_first=float(q_first.bus_trips_per_arrival), trips_last=float(q_win_last.bus_trips_per_arrival),
        trip_drop=trip_drop_pct, hhi=hhi, top3=top3_share,
        cotai_ratio=float(covai.supply_demand_ratio), cotai_perdep=float(covai.demand_per_departure),
        pen_ratio=float(peninsula.supply_demand_ratio), col_ratio=float(coloane.supply_demand_ratio),
        months=int(len(WIN)), quarters=int(len(q_all)),
    ),
    "zoneMatch": zm.to_dict(orient="list"),
    "hourMatch": h.to_dict(orient="list"),
    "hotel": hotel_payload,
}

FIGS = {
    "f_long": json.loads(fig1.to_json()),
    "f_month": json.loads(fig2.to_json()),
    "f_quarter": json.loads(fig3.to_json()),
    "f_zone": json.loads(fig4.to_json()),
    "f_dep": json.loads(fig5.to_json()),
    "f_hour": json.loads(fig6.to_json()),
    "f_map": json.loads(fig7.to_json()),
    "f_heat": json.loads(fig8.to_json()),
    "f_season": json.loads(fig9.to_json()),
    "f_shift_zone": json.loads(fig10.to_json()),
    "f_shift_hour": json.loads(fig11.to_json()),
    "f_golden": json.loads(gfig.to_json()),
    "f_hocc": json.loads(figH1.to_json()),
    "f_hstar": json.loads(figH3.to_json()),
    "f_hrel": json.loads(figH2.to_json()),
    "f_hhist": json.loads(figH4.to_json()),
}

KPI_HTML = """
      <div class="kpi"><div class="kpi-v">{arrivals:.1f}M</div><div class="kpi-l">Visitor arrivals</div>
        <div class="kpi-s">{months}-month window, 2023-01 to 2025-12</div></div>
      <div class="kpi"><div class="kpi-v">{guests:.1f}M</div><div class="kpi-l">Hotel guests</div>
        <div class="kpi-s">same {months}-month window</div></div>
      <div class="kpi"><div class="kpi-v">{trips_first:.2f} &rarr; {trips_last:.2f}</div><div class="kpi-l">Bus trips per visitor</div>
        <div class="kpi-s">{trip_drop:+.0f}% from 2023Q1 to 2025Q4</div></div>
      <div class="kpi"><div class="kpi-v" id="kpiHhiV">{hhi:,.0f}</div><div class="kpi-l">District concentration (HHI)</div>
        <div class="kpi-s" id="kpiHhiS">equivalent of {hhi_eq:.2f} equal districts &middot; top 3 = {top3:.1f}%</div></div>
      <div class="kpi"><div class="kpi-v">{occ_avg:.1f}%</div><div class="kpi-l">Hotel occupancy rate</div>
        <div class="kpi-s">{months}-month mean &middot; peak {occ_peak:.1f}% in {occ_peak_ym}</div></div>
      <div class="kpi"><div class="kpi-v">{cotai:.2f}</div><div class="kpi-l">Taipa &amp; Cotai supply/demand ratio</div>
        <div class="kpi-s">vs {pen:.2f} on the Peninsula &middot; {perdep:,.0f} headcount per departure</div></div>
""".format(
    arrivals=win_arrivals / 1e6, guests=win_guests / 1e6, months=len(WIN),
    trips_first=q_first.bus_trips_per_arrival, trips_last=float(q_win_last.bus_trips_per_arrival), trip_drop=trip_drop_pct,
    hhi=hhi, hhi_eq=10000 / hhi, top3=top3_share, cotai=covai.supply_demand_ratio,
    pen=peninsula.supply_demand_ratio, perdep=covai.demand_per_departure,
    occ_avg=occ_win_mean, occ_peak=occ_peak, occ_peak_ym=occ_peak_ym,
)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao</title>
<style>
  :root{
    --navy:#1B4965; --blue:#2E86AB; --sky:#62B6CB; --red:#EE6C4D; --gold:#F4A259;
    --green:#3E8914; --purple:#7B2CBF; --ink:#0E2136; --muted:#374B61;
    --bg:#EDF1F6; --card:#FFFFFF; --line:#E1E8F0;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
       font-family:"Segoe UI",Inter,Helvetica,Arial,sans-serif;font-size:14px;line-height:1.45}
  .wrap{max-width:1680px;margin:0 auto;padding:0 22px 34px}
  header{background:linear-gradient(115deg,#123047 0%,#1B4965 42%,#2E86AB 100%);color:#fff;
         margin:0 -22px 20px;padding:26px 30px 22px;border-radius:0 0 20px 20px;
         box-shadow:0 8px 24px rgba(18,38,58,.18)}
  header .tag{display:inline-block;font-size:11px;letter-spacing:.14em;text-transform:uppercase;
              background:rgba(255,255,255,.16);padding:4px 10px;border-radius:999px;margin-bottom:10px}
  header h1{margin:0 0 6px;font-size:26px;font-weight:700;letter-spacing:-.01em}
  header p{margin:0;font-size:13px;color:#CFE3EE;max-width:1080px}
  header .pills{margin-top:12px;display:flex;flex-wrap:wrap;gap:8px}
  header .pill{font-size:11.5px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);
               padding:4px 10px;border-radius:999px;color:#EAF4FA}
  .filterbar{position:sticky;top:0;z-index:40;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);
             border:1px solid var(--line);border-radius:14px;padding:12px 16px;margin-bottom:18px;
             display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end;
             box-shadow:0 4px 16px rgba(18,38,58,.07)}
  .field{display:flex;flex-direction:column;gap:4px}
  .field label{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#2C3E55;font-weight:700}
  select{appearance:none;border:1px solid var(--line);background:#fff;border-radius:9px;padding:7px 30px 7px 11px;
         font-size:13px;color:var(--ink);font-family:inherit;cursor:pointer;min-width:170px;
         background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'><path d='M2 4l4 4 4-4' fill='none' stroke='%235B6B7C' stroke-width='1.6'/></svg>");
         background-repeat:no-repeat;background-position:right 10px center}
  select:focus{outline:2px solid var(--sky);outline-offset:1px}
  .btn{border:1px solid var(--line);background:#fff;border-radius:9px;padding:8px 14px;font-size:13px;
       font-family:inherit;cursor:pointer;color:var(--ink);transition:.15s}
  .btn:hover{background:#F3F7FB;border-color:var(--sky)}
  .btn.primary{background:var(--navy);color:#fff;border-color:var(--navy)}
  .btn.primary:hover{background:#154056}
  .btn.on{background:var(--navy);color:#fff;border-color:var(--navy)}
  .btn.on:hover{background:#154056}
  body.playing .filterbar{border-color:var(--sky);box-shadow:0 4px 16px rgba(46,134,193,.20)}
  .scope{margin-left:auto;font-size:12px;color:var(--muted);text-align:right;max-width:430px}
  .scope b{color:var(--ink)}
  .kpis{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:12px;margin-bottom:12px}
  .kpi{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;
       box-shadow:0 2px 10px rgba(18,38,58,.05);position:relative;overflow:hidden}
  .kpi:before{content:"";position:absolute;inset:0 auto 0 0;width:4px;background:var(--blue)}
  .kpi:nth-child(2):before{background:var(--sky)} .kpi:nth-child(3):before{background:var(--red)}
  .kpi:nth-child(4):before{background:var(--gold)} .kpi:nth-child(5):before{background:var(--purple)}
  .kpi:nth-child(6):before{background:var(--green)}
  .kpi-v{font-size:24px;font-weight:700;letter-spacing:-.02em;color:var(--navy)}
  .kpi-l{font-size:12.5px;font-weight:600;margin-top:2px}
  .kpi-s{font-size:11.5px;color:var(--muted);margin-top:4px;font-weight:500}
  .grid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:12px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 14px 8px;display:flex;flex-direction:column;
        box-shadow:0 2px 10px rgba(18,38,58,.05);min-width:0}
  .card h3{margin:0 0 2px;font-size:14.5px;font-weight:700;letter-spacing:-.01em}
  .card .sub{margin:0 0 8px;font-size:12px;color:var(--muted);font-weight:500}
  .card .head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .card .head select{min-width:210px;font-size:12px;padding:5px 26px 5px 9px}
  .plot{width:100%}
 .card>.plot:last-child{margin-top:auto}
    .scopeHint{color:#44556A;font-size:11.5px}
    .chip{display:inline-block;margin-left:8px;padding:2px 9px;border-radius:11px;background:#eef3fa;
          color:#28486F;font-size:11px;font-weight:700;vertical-align:middle;letter-spacing:.2px}
  .span12{grid-column:span 12}.span7{grid-column:span 7}.span6{grid-column:span 6}
  .span5{grid-column:span 5}.span4{grid-column:span 4}.span8{grid-column:span 8}
  .legend .legendtext, .legend text{fill:#0E2136;font-weight:600}
  .note{font-size:11.5px;color:var(--muted);margin:2px 2px 6px}
  .legendtip{font-size:11.5px;color:#33465C;background:#F7FAFD;border:1px dashed var(--line);
             border-radius:8px;padding:6px 9px;margin:6px 2px 8px}
  footer{margin-top:26px;border-top:1px solid var(--line);padding-top:16px;font-size:12px;color:var(--muted)}
  footer b{color:var(--ink)}
  @media (max-width:1180px){
    .kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
    .span7,.span5,.span6,.span8,.span4,.span12{grid-column:span 12}
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="tag">CISC7204 Data Science and Data Visualization &middot; Class E &middot; Team 01</div>
    <h1>Visualizing the Relationship Between Visitor Arrivals,<br/>Hotel Occupancy, and Bus Ridership in Macao</h1>
    <p>Interactive companion to the team report. Visitor arrivals, hotel occupancy and public-bus ridership
       are put on one screen so the supply-demand mismatch can be read at three grains - city, zone and the
       24 DSEC statistical districts - and at two time grains, the month and the hour of day.</p>
    <div class="pills">
      <span class="pill">Data window: 2023-01 to 2026-09 (2026 partial) &middot; hotel occupancy history from 2014</span>
      <span class="pill">Estimation window: 36 months, 2023-01 to 2025-12</span>
      <span class="pill">Sources: MGTO Data Plus &middot; DSEC &middot; DSAT</span>
      <span class="pill">Click a district on the map, a row in the heatmap or a bar to filter &middot; hover to preview &middot; arrow keys step the year &middot; Play cycles 2023-2026 &middot; click a legend item to highlight it across every chart</span>
    </div>
  </header>

  <div class="filterbar">
    <div class="field"><label for="selYear">Year</label><select id="selYear"></select></div>
    <div class="field"><label for="selZone">Zone</label><select id="selZone"></select></div>
    <div class="field"><label for="selDistrict">District</label><select id="selDistrict"></select></div>
    <div class="field"><label for="btnPlay">Auto-cycle</label><button class="btn" id="btnPlay" title="Animate the year filter">&#9654; Play years</button></div>
    <div class="field"><label>&nbsp;</label><button class="btn" id="btnReset">Reset filters</button></div>
    <div class="chip" id="hiChip" style="display:none"></div>
    <div class="scope" id="scopeText"></div>
  </div>

  <section class="kpis">__KPI__</section>

  <section class="grid">
    <div class="card span12">
      <h3>1 &middot; Long-run monthly visitor arrivals, 2015-2026</h3>
      <p class="sub">Pandemic years are drawn in red and cannot be read as normal demand; the shaded band is the 36-month estimation window used in every correlation reported below.</p>
      <div id="f_long" class="plot"></div>
    </div>

    <div class="card span7">
      <h3>2 &middot; Arrivals and bus passenger trips, monthly</h3>
      <p class="sub">Arrivals recover year by year, but the ridership line on the right axis does not keep pace - the coupling weakens as the market grows.</p>
      <div id="f_month" class="plot"></div>
    </div>

    <div class="card span5">
      <h3>3 &middot; Bus trips per visitor, quarterly</h3>
      <p class="sub">The headline ratio falls every quarter: each visitor is served by fewer scheduled trips than the quarter before.</p>
      <div id="f_quarter" class="plot"></div>
    </div>

    <div class="card span7">
      <h3>4 &middot; Visitor arrivals and the hotel occupancy rate<span class="chip" data-chip="1"></span></h3>
      <p class="sub">Rooms fill as the city fills: the occupancy rate on the right axis tracks visitor arrivals on the left, month by month, so the hotel stock is doing the work of absorbing the crowd.</p>
      <div id="f_hocc" class="plot"></div>
    </div>

    <div class="card span5">
      <h3>5 &middot; Occupancy against bus trips per visitor<span class="chip" data-chip="1"></span></h3>
      <p class="sub">Each point is one month and the colour is the year. Occupancy pushes to the right across 2023-2026 while ridership per visitor slides down: the rooms fill up, but the bus network does not carry proportionally more.</p>
      <div id="f_hrel" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>6 &middot; Who fills the rooms: hotel guests by hotel class<span class="chip" data-chip="1"></span></h3>
      <p class="sub">Monthly guest counts split by hotel star rating, straight from the DSEC hotel survey. The 5-star tier dominates the stack, so capacity that ignores it is capacity aimed at a minority of the hotel base.</p>
      <div id="f_hstar" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>7 &middot; The long occupancy record, 2014-2026</h3>
      <p class="sub">The full DSEC monthly occupancy series: the pandemic collapse, the 2023-2026 climb, and how far the market now sits above the 2019 mean before the buses are planned for it.</p>
      <div id="f_hhist" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>8 &middot; Supply-demand mismatch across the three zones<span class="chip" data-chip="1"></span></h3>
      <p class="sub">Demand share is compared with the share of scheduled departures and of bus stops. A zone where the demand bar is taller than the supply bars is under-supplied.</p>
      <div id="f_zone" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>9 &middot; Visitor headcount carried per scheduled departure<span class="chip" data-chip="1"></span></h3>
      <p class="sub">The cleanest single measure of load: how many visitor-hours of demand sit behind each scheduled departure in the zone. Hover for the supply/demand ratio.</p>
      <div id="f_dep" class="plot"></div>
    </div>

    <div class="card span12">
      <h3>10 &middot; Demand and scheduled supply by hour of day<span class="chip" id="hoverChip" style="display:none"></span><span class="chip" data-chip="1"></span></h3>
      <p class="sub">The red line is the visitor demand share for the current filter; the blue line is the scheduled departure share. Bars are the gap in percentage points - red bars are hours where demand runs ahead of supply.</p>
      <div id="f_hour" class="plot"></div>
    </div>

    <div class="card span7">
      <h3>11 &middot; The 24 DSEC statistical districts<span class="chip" data-chip="1"></span></h3>
      <div class="head">
        <p class="sub">The Year / Zone / District filters above drive this map (colours are recomputed for the selected year); pick a Zone or a district with the top filters to spotlight it. Click a district here to filter views 8, 9, 10 and 12.</p>
        <select id="selMetric">
          <option value="share">Headcount share (%)</option>
          <option value="density">Headcount per km&sup2; per month</option>
          <option value="delta">2026 share shift (pp)</option>
          <option value="perdep">Headcount per departure</option>
        </select>
      </div>
      <div id="f_map" class="plot"></div>
    </div>

    <div class="card span5">
      <h3>12 &middot; District by hour-of-day profile<span class="chip" id="heatCount"></span><span class="chip" data-chip="1"></span></h3>
      <p class="sub">Each row is rescaled to that district's own daily total, so a small district and Cotai can be read side by side. Click a row to filter.</p>
      <div id="f_heat" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>13 &middot; Seasonality of arrivals, 2023-2025</h3>
      <p class="sub">Index on the 2023-2025 monthly mean; red bars are the flagged peak months. Capacity planning that ignores this shape under-supplies the peaks.</p>
      <div id="f_season" class="plot"></div>
    </div>

    <div class="card span6">
      <h3>14 &middot; Golden Week daily intensity</h3>
      <p class="sub">Daily arrivals inside the 1st October Golden Week expressed as a multiple of that month's average day. The shape of the peak is what the bus schedule has to absorb.</p>
      <div id="f_golden" class="plot"></div>
    </div>

    <div class="card span12">
      <h3>15 &middot; What shifted in 2026</h3>
      <p class="sub">2026 year-to-date against the 2023-2025 baseline: the demand keeps tilting towards Cotai, and the hour-of-day shape barely moves.</p>
      <div id="f_shift_zone" class="plot"></div>
      <div id="f_shift_hour" class="plot"></div>
    </div>
  </section>

  <footer>
    <b>How to read this dashboard.</b> Every figure is computed at build time from the cleaned panels in
    <code>data/</code>, which are the files committed in
    <code>data_processed/</code> of FongChinWai-Vivi/CISC7204-ClassE-Team01-2026GitHub.
    Headcount is a stock summed over the panel (2023-01 to 2026-09) and is comparable between districts, never
    across publications. Density is the only column comparable across district sizes. Supply is stop-level
    scheduled departures; stops outside the 24 polygons are excluded, not snapped.
    Demand-side sources: MGTO Macao Tourism Data Plus (district x hour), DSEC visitor arrivals, hotel
    occupancy and hotel guests. Supply-side sources: DSAT monthly and quarterly ridership and timetable
    releases, data.gov.mo public bus route and stop export. 2026 is partial in every view that shows it.<br/>
    Hotel block: <code>hotel_occ_monthly_2023_2026.csv</code>,
    <code>hotel_guests_by_star_2023_2026.csv</code> and <code>hotel_occ_history_2014_2025.csv</code>, copied
    from <code>Dataset/</code> of the same team repository (hotel occupancy total, guests by hotel class and
    the long 2014-2026 occupancy record).<br/>
    Built with Plotly.js inside a single offline HTML file - no server and no network connection required.
  </footer>
</div>

<script>__PLOTLYJS__</script>
<script>
const PAYLOAD = __PAYLOAD__;
const FIGS = __FIGS__;
const CONFIG = {responsive:true, displaylogo:false,
  modeBarButtonsToRemove:["select2d","lasso2d","autoScale2d","toggleSpikelines"],
  toImageButtonOptions:{format:"png", filename:"cisc7204-team01-chart", scale:2}};

const D = PAYLOAD.districts;
const P = PAYLOAD.panel;
const el = id => document.getElementById(id);

// ---------------- filter state ----------------
const state = {year:"all", zone:"all", district:"all", metric:"share", supply:"weekday"};

function fillSelects(){
  const y = el("selYear");
  y.innerHTML = '<option value="all">All years (2023-2026)</option>' +
    PAYLOAD.years.map(v=>`<option value="${v}">${v}${v===2026?" (partial)":""}</option>`).join("");
  const z = el("selZone");
  z.innerHTML = '<option value="all">All zones</option>' +
    PAYLOAD.zones.map(v=>`<option value="${v}">${v}</option>`).join("");
  const d = el("selDistrict");
  d.innerHTML = '<option value="all">All 24 districts</option>' +
    D.map((x,i)=>`<option value="${i}">${x.en} (${x.cn})</option>`).join("");
}

function filteredRows(skipYear){
  const y = (skipYear || state.year==="all") ? null : +state.year;
  const di = state.district==="all" ? null : +state.district;
  const out = [];
  for(let i=0;i<P.v.length;i++){
    if(y!==null && P.y[i]!==y) continue;
    if(di!==null && P.d[i]!==di) continue;
    if(state.zone!=="all" && D[P.d[i]].zone!==state.zone) continue;
    out.push(i);
  }
  return out;
}

// ---------------- linked views ----------------
function hourProfile(rows){
  const h = new Array(24).fill(0);
  let tot = 0;
  for(const i of rows){ h[P.h[i]] += P.v[i]; tot += P.v[i]; }
  return tot>0 ? h.map(v=>v/tot*100) : h;
}

function heatFromRows(rows){
  const totals = new Map(), grid = new Map();
  for(const i of rows){
    const d = P.d[i], hh = P.h[i];
    totals.set(d, (totals.get(d)||0) + P.v[i]);
    const k = d+"|"+hh;
    grid.set(k, (grid.get(k)||0) + P.v[i]);
  }
  const dists = [...totals.keys()].sort((a,b)=>totals.get(b)-totals.get(a));
  const y = dists.map(d=>D[d].en);
  const z = dists.map(d=>{
    const t = totals.get(d)||1;
    return Array.from({length:24},(_,hh)=>+(((grid.get(d+"|"+hh)||0)/t*100).toFixed(3)));
  });
  return {y, z, dists};
}

// hotel block: the four hotel charts follow the year selector only. They are monthly views,
// so a year selection re-slices their x axis instead of leaving a stale full-range figure on screen.
function refreshHotel(){
  const H = PAYLOAD.hotel;
  if(!H || !H.m) return;
  const keep = H.y.map(function(v, i){
    return (state.year === "all" || String(v) === String(state.year)) ? i : -1;
  }).filter(function(i){ return i >= 0; });
  const x = keep.map(function(i){ return H.m[i]; });
  const pick = function(key){ return keep.map(function(i){ return H[key][i]; }); };

  // fig 3 - arrivals bars on the left axis, occupancy line on the right axis
  Plotly.restyle("f_hocc", {x:[x, x], y:[pick("arr").map(function(v){ return v / 1e6; }), pick("occ")]}, [0, 1]);

  // fig 4 - one marker per month, one trace per year (trace order = H.years)
  H.years.forEach(function(yr, ti){
    const sel = keep.filter(function(i){ return H.y[i] === yr; });
    Plotly.restyle("f_hrel", {
      x:[sel.map(function(i){ return H.occ[i]; })],
      y:[sel.map(function(i){ return H.tpv[i]; })],
      customdata:[sel.map(function(i){ return [H.m[i]]; })]
    }, [ti]);
  });

  // fig 5 - hotel guests by class (trace order = H.cls)
  const xs = [], ys = [];
  H.cls.forEach(function(c){
    xs.push(x);
    ys.push(keep.map(function(i){ return H.star[c][i]; }));
  });
  Plotly.restyle("f_hstar", {x:xs, y:ys}, H.cls.map(function(_, i){ return i; }));
}

function refreshLinked(){
  const rowsUI = filteredRows();
  refreshHotel();
  // a legend highlight is a view-layer selection: it narrows the hour curve and the heatmap rows
  // without touching the year / zone / district filters themselves, and a highlighted year
  // overrides the year selector instead of intersecting with it (otherwise the curve goes empty)
  const rows = HI.kind === "year" ? filteredRows(true) : rowsUI;
  const rowsHi = hiScopedRows(rows);
  const share = hourProfile(rowsHi);
  Plotly.restyle("f_hour", {y:[share]}, [1]);

  const heat = heatFromRows(rowsHi);
  const zmax = Math.max(4, ...heat.z.flat());
  Plotly.react("f_heat", [{
    type:"heatmap", z:heat.z, x:Array.from({length:24},(_,i)=>i), y:heat.y,
    colorscale:"YlOrRd", zmin:0, zmax:+zmax.toFixed(2),
    colorbar:{title:{text:"% of that<br>district's day", font:{size:10, color:"#0E2136"}}, tickfont:{size:10, color:"#0E2136"}, thickness:10, len:0.8},
    hovertemplate:"%{y}<br>%{x}:00<br>%{z:.2f}% of the district's headcount<extra></extra>"
  }], Object.assign({}, FIGS.f_heat.layout, {
    margin:{l:150,r:10,t:10,b:44}, height:470,
    yaxis:Object.assign({}, FIGS.f_heat.layout.yaxis, {tickfont:{size:9, color:"#0E2136"}, autorange:"reversed"})
  }), CONFIG);

  const total = rowsUI.reduce((s,i)=>s+P.v[i],0);
  const all = P.v.reduce((a,b)=>a+b,0);
  const yearTxt = state.year==="all" ? "2023-2026" : state.year;
  const distTxt = state.district==="all" ? (state.zone==="all"?"all 24 districts":state.zone+" districts")
                                         : ((D[+state.district] || {}).en || String(state.district));
  const nDist = new Set(rowsUI.map(i=>P.d[i])).size;
  const isDefault = state.year==="all" && state.zone==="all" && state.district==="all";
  el("scopeText").innerHTML = `<b>${yearTxt}</b> &middot; <b>${distTxt}</b><br>
     ${(total/1e6).toFixed(2)}M visitor headcount rows &middot; ${(total/all*100).toFixed(1)}% of the full panel
     &middot; ${nDist} district${nDist===1?"":"s"} in scope
     ${state.district!=="all" ? "&middot; share of city total "+D[+state.district].share.toFixed(2)+"%":""}
     <br><span class="scopeHint">${isDefault ? "No filter applied - showing the whole panel"
        : "Filter active &rarr; re-drawn: Fig 4, 5, 6, 8, 9, 10, 11, 12"}</span>`;

  applyMap();
  highlightZone();
  el("f_heat").__rows = rows.length;
  el("heatCount").textContent = nDist + " row" + (nDist===1?"":"s") + " / " + yearTxt;

  // echo the active filter on every card the filter touches, so a small numeric
  // change is still obviously a response to the click
  const chipTxt = isDefault ? "" : [yearTxt,
      state.zone!=="all" ? state.zone : null,
      state.district!=="all" ? D[+state.district].en : null].filter(Boolean).join(" \u00B7 ");
  document.querySelectorAll('.chip[data-chip]').forEach(c=>{
    c.textContent = chipTxt;
    c.style.display = chipTxt ? "inline-block" : "none";
  });
  updateHHI();
  bindHeatHover();
  applyHighlight();
}

// ---------------- map metric switch ----------------
const SQRT_SCALE = [[0,"#F7FBFF"],[0.15,"#DEEBF7"],[0.35,"#9ECAE1"],[0.60,"#4292C6"],
                    [0.82,"#08519C"],[1,"#08306B"]];
const RDBU = [[0,"#2166AC"],[0.5,"#F7F7F7"],[1,"#B2182B"]];
const METRIC = {
  share:  {key:"share",  ci:9, sqrt:true,  scale:SQRT_SCALE, fmt:".2f",  suffix:"%",
           label:"Headcount share", title:"Share of<br>city total (%)",
           ticks:{vals:[1,2,5,10,20,30,44].map(v=>Math.sqrt(v)), text:["1","2","5","10","20","30","44"]}},
  density:{key:"density",ci:5, scale:"Viridis", fmt:",.0f", suffix:"",
           label:"Headcount per km\u00B2 per month", title:"Headcount per<br>km\u00B2 per month"},
  delta:  {key:"delta",  ci:6, scale:RDBU, fmt:"+.2f", suffix:" pp",
           label:"2026 share shift", title:"2026 share<br>shift (pp)"},
  perdep: {key:"perdep", ci:7, scale:"OrRd", fmt:",.0f", suffix:"",
           label:"Headcount per departure", title:"Headcount per<br>departure"}
};

function hoverTemplate(m){
  return "<b>%{customdata[8]}</b> (%{location})<br>" +
         m.label + ": %{customdata[" + m.ci + "]:" + m.fmt + "}" + m.suffix +
         "<br>Headcount share: %{customdata[9]:.2f}%" +
         "<br>Total headcount: %{customdata[0]:,.0f}" +
         "<br>Stops: %{customdata[1]}<br>Weekday departures: %{customdata[4]:,.0f}" +
         "<br>Peak hour: %{customdata[2]}:00" +
         "<br>Night share (22:00-05:59): %{customdata[3]:.1f}%<extra></extra>";
}

// ---- helpers shared by every linked view ----
function scopeMask(){
  const di = state.district==="all" ? null : +state.district;
  return D.map((x,i)=>{
    if(di!==null) return i===di;
    if(state.zone!=="all") return x.zone===state.zone;
    return true;
  });
}

// headcount share (%) of each district recomputed for the selected year
function yearShare(){
  // a legend highlight on a year re-shades the map for that year even when the filter says "all"
  const y = HI.kind === "year" ? +HI.name : (state.year==="all" ? null : +state.year);
  const tot = new Array(D.length).fill(0);
  let all = 0;
  for(let i=0;i<P.v.length;i++){
    if(y!==null && P.y[i]!==y) continue;
    tot[P.d[i]] += P.v[i]; all += P.v[i];
  }
  return all>0 ? tot.map(v=>v/all*100) : D.map(x=>x.share);
}

function applyMap(){
  const m = METRIC[state.metric];
  const scope = scopeMask();
  // legend highlight wins on the map: the clicked zone stays lit, every other polygon goes to basemap grey
  if(HI.kind === "zone"){
    D.forEach(function(x, i){ if(x.zone !== HI.name) scope[i] = false; });
  }
  const shares = yearShare();
  let raw;
  if(state.metric==="share") raw = shares.slice();
  else if(state.metric==="density") raw = D.map((x,i)=> x.share>0 ? x.density*(shares[i]/x.share) : x.density);
  else raw = D.map(x=>x[m.key]);

  // districts outside the current zone / district filter are drawn as null -> plain basemap grey
  const z = raw.map((v,i)=> scope[i] ? (m.sqrt?Math.sqrt(v):v) : null);
  const ins = raw.filter((v,i)=>scope[i]);
  const pick = a => a.length ? a : raw;
  const mx = Math.max(...pick(ins));
  const ab = Math.max(...pick(ins).map(Math.abs));

  const update = {
    z:[z],
    colorscale:[m.scale],
    "colorbar.title.text":[m.title],
    hovertemplate:[hoverTemplate(m)],
    customdata:[D.map((x,i)=>[x.hits, x.stops, x.peak, x.night, x.wdep, x.density,
                              x.delta, x.perdep, x.en, +shares[i].toFixed(3)])]
  };
  if(state.metric==="delta"){
    update.zmin=[-ab]; update.zmax=[ab]; update.zmid=[0];
    update["colorbar.tickvals"]=[null]; update["colorbar.ticktext"]=[null];
  } else if(m.sqrt){
    update.zmin=[0]; update.zmax=[Math.sqrt(mx)]; update.zmid=[null];
    update["colorbar.tickvals"]=[m.ticks.vals]; update["colorbar.ticktext"]=[m.ticks.text];
  } else {
    update.zmin=[0]; update.zmax=[mx]; update.zmid=[null];
    update["colorbar.tickvals"]=[null]; update["colorbar.ticktext"]=[null];
  }
  Plotly.restyle("f_map", update, [0]);
}

// keep only the selected zone loud in the two zone-level charts
function highlightZone(){
  const zs = PAYLOAD.zones || [];
  const hiZ = HI.kind === "zone" ? HI.name : null;
  const target = hiZ || state.zone;
  const active = (state.zone!=="all" && state.district==="all") || !!hiZ;
  const op = zs.map(z => (!active || z===target) ? 1 : 0.15);
  Plotly.restyle("f_zone", {"marker.opacity":[op, op, op]});
  Plotly.restyle("f_dep", {"marker.opacity":[op]});
}

// a filter click at the top of the page would otherwise change charts that are off-screen
function revealLinked(){
  const box = document.getElementById("f_hour");
  if(!box) return;
  const card = box.closest(".card") || box;
  const r = card.getBoundingClientRect();
  if(r.top < 0 || r.top > window.innerHeight * 0.55){
    card.scrollIntoView({behavior:"smooth", block:"start"});
  }
}

// ---------------- year playback ----------------
const PLAY_SEQ = ["2023","2024","2025","2026"];
let playTimer = null;

function setYear(v){
  state.year = v;
  el("selYear").value = v;
  refreshLinked();
}

function stepYear(delta){
  const opts = ["all"].concat(PLAY_SEQ);
  const cur = Math.max(0, opts.indexOf(state.year));
  setYear(opts[(cur + delta + opts.length) % opts.length]);
  revealLinked();
}

function stopPlay(){
  if(playTimer){ clearInterval(playTimer); playTimer = null; }
  const b = el("btnPlay");
  if(b){ b.innerHTML = "&#9654; Play years"; b.classList.remove("on"); }
  document.body.classList.remove("playing");
}

function togglePlay(){
  if(playTimer){ stopPlay(); return; }
  let k = PLAY_SEQ.indexOf(state.year);
  if(k < 0) k = 0;
  setYear(PLAY_SEQ[k]);
  const b = el("btnPlay");
  b.innerHTML = "&#10074;&#10074; Pause"; b.classList.add("on");
  document.body.classList.add("playing");
  playTimer = setInterval(function(){ k = (k + 1) % PLAY_SEQ.length; setYear(PLAY_SEQ[k]); }, 1700);
}

// hovering the map or a heatmap row previews that district's hourly curve in view 6
function districtHourShare(idx){
  const y = state.year === "all" ? null : +state.year;
  const h = new Array(24).fill(0);
  let tot = 0;
  for(let i = 0; i < P.v.length; i++){
    if(P.d[i] !== idx) continue;
    if(y !== null && P.y[i] !== y) continue;
    h[P.h[i]] += P.v[i]; tot += P.v[i];
  }
  return tot > 0 ? h.map(function(v){ return v / tot * 100; }) : null;
}

function previewHour(idx){
  const sh = districtHourShare(idx);
  if(!sh) return;
  Plotly.restyle("f_hour", {y:[sh]}, [1]);
  const c = el("hoverChip");
  if(c){ c.textContent = "hover preview \u00B7 " + D[idx].en; c.style.display = "inline-block"; }
}

function endPreview(){
  Plotly.restyle("f_hour", {y:[hourProfile(filteredRows())]}, [1]);
  const c = el("hoverChip");
  if(c){ c.style.display = "none"; c.textContent = ""; }
}

// f_heat is rebuilt by Plotly.react on every filter, so its hover hooks are re-attached
function bindHeatHover(){
  const gd = el("f_heat");
  if(!gd || typeof gd.on !== "function") return;
  try{
    if(gd.removeAllListeners){
      gd.removeAllListeners("plotly_hover");
      gd.removeAllListeners("plotly_unhover");
    }
  }catch(e){}
  gd.on("plotly_hover", function(ev){ const i = D.findIndex(function(x){ return x.en === ev.points[0].y; }); if(i >= 0) previewHour(i); });
  gd.on("plotly_unhover", endPreview);
}

// ---------------- cross-chart highlight: click any legend item, every chart follows ----------------
const HI = {kind:null, name:null};
const HI_CHARTS = ["f_long","f_month","f_quarter","f_zone","f_dep","f_hour","f_map","f_heat",
                   "f_season","f_shift_zone","f_shift_hour","f_golden",
                   "f_hocc","f_hstar","f_hrel","f_hhist"];
const YEAR_ONLY = ["f_long","f_month","f_quarter","f_season","f_shift_zone","f_shift_hour","f_golden","f_hrel"];

function yearOfName(n){ const m = /(20\d\d)/.exec(String(n || "")); return m ? +m[1] : null; }

// a legend entry can name a year, a zone or a side of the argument; the last one is matched by
// keyword so a click on "Visitor demand" in one chart lights up every demand series in the others
const CONCEPT_RULES = [
  ["ratio",  /gap|per visitor|per departure|trips per|ratio|index|share shift/i],
  ["demand", /demand|arrival|visitor|occupancy|hotel/i],
  ["supply", /departure|supply|bus passenger trips|bus trips|bus stop|scheduled/i]
];
const CONCEPT_LABEL = {demand:"demand side", supply:"supply side", ratio:"ratio / gap"};

function conceptOf(name){
  const n = String(name || "");
  for(let i = 0; i < CONCEPT_RULES.length; i++){
    if(CONCEPT_RULES[i][1].test(n)) return CONCEPT_RULES[i][0];
  }
  return null;
}

function fadeByConcept(c){
  HI_CHARTS.forEach(function(id){
    if(id === "f_map" || id === "f_heat") return;      // these two carry no clickable legend
    const gd = el(id);
    if(!gd || !gd.data || !gd.data.length) return;
    if(!gd.data.some(function(t){ return conceptOf(t.name) === c; })) return;
    Plotly.restyle(id, "opacity", gd.data.map(function(t){
      const k = conceptOf(t.name);
      return (k === null || k === c) ? 1 : 0.12;
    }));
  });
}

function hiRows(){
  if(!HI.kind) return null;
  const out = [];
  for(let i = 0; i < P.v.length; i++){
    if(HI.kind === "zone" && String(D[P.d[i]].zone) !== String(HI.name)) continue;
    if(HI.kind === "year" && String(P.y[i]) !== String(HI.name)) continue;
    out.push(i);
  }
  return out;
}

function hiScopedRows(base){
  if(!HI.kind) return base;
  const keep = new Set(hiRows() || []);
  return base.filter(function(i){ return keep.has(i); });
}

const OP0 = {};

function snapOpacity(){
  HI_CHARTS.forEach(function(id){
    const gd = el(id);
    if(gd && gd.data) OP0[id] = gd.data.map(function(t){ return t.opacity === undefined ? 1 : t.opacity; });
  });
}

function resetFade(ids){
  (ids || HI_CHARTS).forEach(function(id){
    if(id === "f_map" || id === "f_heat") return;
    const gd = el(id);
    if(!gd || !gd.data || !OP0[id]) return;
    const cur = gd.data.map(function(t){ return t.opacity === undefined ? 1 : t.opacity; });
    if(cur.length === OP0[id].length && cur.every(function(v, i){ return v === OP0[id][i]; })) return;
    Plotly.restyle(id, "opacity", OP0[id]);
  });
}

function applyHighlight(){
  const chip = el("hiChip");
  if(!HI.kind){
    resetFade();
    if(chip){ chip.style.display = "none"; chip.textContent = ""; }
    document.body.classList.remove("highlighting");
    scheduleLegendPaint();
    return;
  }
  document.body.classList.add("highlighting");
  const tag = HI.kind === "year" ? " (year)" : HI.kind === "zone" ? " (zone)" : "";
  if(chip){
    chip.textContent = "highlight \u00B7 " +
      (HI.kind === "concept" ? CONCEPT_LABEL[HI.name] : HI.name) + tag +
      " \u00B7 click again or press Esc to clear";
    chip.style.display = "inline-block";
  }
  resetFade();
  if(HI.kind === "concept"){ fadeByConcept(HI.name); scheduleLegendPaint(); return; }
  if(HI.kind !== "year"){ scheduleLegendPaint(); return; }
  YEAR_ONLY.forEach(function(id){
    const gd = el(id);
    if(!gd || !gd.data) return;
    const hit = gd.data.some(function(t){ return yearOfName(t.name) === +HI.name; });
    if(!hit) return;      // this chart has no series for that year - leave it alone
    Plotly.restyle(id, "opacity", gd.data.map(function(t){
      const y = yearOfName(t.name);
      return (y === null) ? 1 : (y === +HI.name ? 1 : 0.12);
    }));
  });
  scheduleLegendPaint();
}

// the legend is the control surface, so a faded trace keeps a readable label:
// the swatch dims with the series, the text keeps its dark ink and weight
function paintLegend(){
  HI_CHARTS.forEach(function(id){
    const gd = el(id);
    if(!gd || !gd.data) return;
    const rows = gd.querySelectorAll(".legend g.traces");
    Array.prototype.forEach.call(rows, function(row){
      const t = row.querySelector(".legendtext");
      if(!t) return;
      const label = String(row.getAttribute("data-unformatted") || t.textContent || "").trim();
      const op = parseFloat(row.style.opacity || "1");
      const tr = (gd.data || []).filter(function(d){ return String(d.name || "").trim() === label; })[0];
      const trOp = tr && tr.opacity !== undefined ? +tr.opacity : 1;
      const faded = (op < 0.5) || (trOp < 0.5);
      t.style.fill = faded ? "#3D5064" : "#0E2136";
      t.style.fontWeight = faded ? "600" : "700";
      t.style.fontSize = faded ? "11.2px" : "11.5px";
    });
  });
}
function scheduleLegendPaint(){
  paintLegend();
  requestAnimationFrame(paintLegend);
  setTimeout(paintLegend, 140);
  setTimeout(paintLegend, 420);
}

function toggleHighlight(name){
  if(!name) return;
  let kind = null, val = null;
  if((PAYLOAD.zones || []).indexOf(name) >= 0){ kind = "zone"; val = name; }
  else {
    const y = yearOfName(name);
    if(y){ kind = "year"; val = y; }
    else {
      const c = conceptOf(name);
      if(c){ kind = "concept"; val = c; }     // "Visitor demand" / "Scheduled departures" / "Gap ..."
    }
  }
  if(!kind) return;
  if(HI.kind === kind && HI.name === val){ HI.kind = null; HI.name = null; }
  else { HI.kind = kind; HI.name = val; }
  refreshLinked();
}

// the click highlights instead of hiding, so the default legend toggle is suppressed
function bindLegendHighlight(){
  HI_CHARTS.forEach(function(id){
    const gd = el(id);
    if(!gd) return;
    if(gd.on && !gd.__hiPlot){ gd.__hiPlot = true; gd.on("plotly_afterplot", paintLegend); }
    const lg = gd.querySelector(".legend");
    if(!lg || lg.__hiBound) return;
    lg.__hiBound = true;
    // capture phase: the click is taken before plotly can toggle the trace off
    lg.addEventListener("click", function(e){
      let node = e.target;
      while(node && node !== lg && !(node.classList && node.classList.contains("traces"))) node = node.parentNode;
      if(!node || node === lg) return;
      const txt = node.getAttribute("data-unformatted") ||
                  ((node.querySelector(".legendtext") || node).textContent || "");
      e.stopPropagation();
      e.preventDefault();
      toggleHighlight(String(txt).trim());
    }, true);
  });
}

function pickDistrict(idx){
  if(!(idx >= 0) || idx >= D.length) return;
  el("selDistrict").value = String(idx);
  state.district = String(idx);
  state.zone = "all"; el("selZone").value = "all";
  stopPlay();
  refreshLinked(); revealLinked();
}

function pickZone(z){
  if((PAYLOAD.zones || []).indexOf(z) < 0) return;
  el("selZone").value = z;
  state.zone = z;
  state.district = "all"; el("selDistrict").value = "all";
  stopPlay();
  refreshLinked(); revealLinked();
}

function resetAll(){
  stopPlay();
  state.year = "all"; state.zone = "all"; state.district = "all";
  el("selYear").value = "all"; el("selZone").value = "all"; el("selDistrict").value = "all";
  HI.kind = null; HI.name = null;
  refreshLinked();
}

// the HHI card follows the current scope instead of staying frozen at the full-window value
const KPI0 = { v: (el("kpiHhiV") || {}).innerHTML, s: (el("kpiHhiS") || {}).innerHTML };
function updateHHI(){
  const vEl = el("kpiHhiV"), sEl = el("kpiHhiS");
  if(!vEl) return;
  const isDefault = state.year === "all" && state.zone === "all" && state.district === "all";
  if(isDefault){ vEl.innerHTML = KPI0.v; if(sEl) sEl.innerHTML = KPI0.s; return; }
  const scope = scopeMask();
  const raw = yearShare().map(function(v,i){ return scope[i] ? v : 0; });
  const tot = raw.reduce(function(a,b){ return a + b; }, 0);
  if(!(tot > 0)) return;
  const pr = raw.map(function(v){ return v / tot; });
  const hhi = pr.reduce(function(a,b){ return a + b * b; }, 0) * 10000;
  const top3 = pr.slice().sort(function(a,b){ return b - a; }).slice(0,3).reduce(function(a,b){ return a + b; }, 0) * 100;
  vEl.innerHTML = Math.round(hhi).toLocaleString("en-US");
  if(sEl) sEl.innerHTML = "equivalent of " + (10000 / hhi).toFixed(2) + " equal districts &middot; top 3 = " +
    top3.toFixed(1) + "%" + (state.year !== "all" ? " &middot; " + state.year + " only" : "");
}

// ---------------- wiring ----------------
function draw(){
  Plotly.newPlot("f_long", FIGS.f_long.data, FIGS.f_long.layout, CONFIG);
  Plotly.newPlot("f_month", FIGS.f_month.data, FIGS.f_month.layout, CONFIG);
  Plotly.newPlot("f_quarter", FIGS.f_quarter.data, FIGS.f_quarter.layout, CONFIG);
  Plotly.newPlot("f_zone", FIGS.f_zone.data, FIGS.f_zone.layout, CONFIG);
  Plotly.newPlot("f_dep", FIGS.f_dep.data, FIGS.f_dep.layout, CONFIG);
  Plotly.newPlot("f_hour", FIGS.f_hour.data, FIGS.f_hour.layout, CONFIG);
  Plotly.newPlot("f_map", FIGS.f_map.data, FIGS.f_map.layout, CONFIG);
  Plotly.newPlot("f_heat", FIGS.f_heat.data, FIGS.f_heat.layout, CONFIG);
  Plotly.newPlot("f_season", FIGS.f_season.data, FIGS.f_season.layout, CONFIG);
  Plotly.newPlot("f_shift_zone", FIGS.f_shift_zone.data, FIGS.f_shift_zone.layout, CONFIG);
  Plotly.newPlot("f_shift_hour", FIGS.f_shift_hour.data, FIGS.f_shift_hour.layout, CONFIG);
  Plotly.newPlot("f_golden", FIGS.f_golden.data, FIGS.f_golden.layout, CONFIG);
  Plotly.newPlot("f_hocc", FIGS.f_hocc.data, FIGS.f_hocc.layout, CONFIG);
  Plotly.newPlot("f_hrel", FIGS.f_hrel.data, FIGS.f_hrel.layout, CONFIG);
  Plotly.newPlot("f_hstar", FIGS.f_hstar.data, FIGS.f_hstar.layout, CONFIG);
  Plotly.newPlot("f_hhist", FIGS.f_hhist.data, FIGS.f_hhist.layout, CONFIG);

  el("f_map").on("plotly_click", ev => {
    const idx = D.findIndex(x=>x.cn===ev.points[0].location);
    if(idx>=0) pickDistrict(idx);
  });
  el("f_heat").on("plotly_click", ev => {
    const idx = D.findIndex(x=>x.en===ev.points[0].y);
    if(idx>=0) pickDistrict(idx);
  });
  // view 4: click a zone bar to zoom every linked view into that zone
  el("f_zone").on("plotly_click", ev => {
    const z = ev.points[0].x;
    if((PAYLOAD.zones || []).indexOf(z) >= 0) pickZone(z);
  });
  // view 5 bars are zones too, so they drive the zone filter
  el("f_dep").on("plotly_click", ev => {
    const z = ev.points[0].y;
    if((PAYLOAD.zones || []).indexOf(z) >= 0) pickZone(z);
  });
  // hovering the map previews the district hour curve in view 6
  el("f_map").on("plotly_hover", ev => {
    const idx = D.findIndex(x=>x.cn===ev.points[0].location);
    if(idx>=0) previewHour(idx);
  });
  el("f_map").on("plotly_unhover", endPreview);
  refreshLinked();
  snapOpacity();
  bindLegendHighlight();
}

el("selYear").addEventListener("change", e=>{ stopPlay(); setYear(e.target.value); revealLinked(); });
el("selZone").addEventListener("change", e=>{
  stopPlay();
  state.zone = e.target.value;
  if(state.zone!=="all" && state.district!=="all" && D[+state.district].zone!==state.zone){
    state.district="all"; el("selDistrict").value="all";
  }
  refreshLinked(); revealLinked();
});
el("selDistrict").addEventListener("change", e=>{
  stopPlay();
  state.district = e.target.value;
  if(state.district!=="all"){ state.zone="all"; el("selZone").value="all"; }
  refreshLinked(); revealLinked();
});
el("selMetric").addEventListener("change", e=>{ state.metric = e.target.value; applyMap(); });
el("btnReset").addEventListener("click", resetAll);
el("btnPlay").addEventListener("click", togglePlay);
document.addEventListener("keydown", e=>{
  const t = e.target && e.target.tagName;
  if(t === "SELECT" || t === "INPUT" || t === "TEXTAREA") return;
  if(e.key === "ArrowRight" || e.key === "ArrowLeft"){
    stepYear(e.key === "ArrowRight" ? 1 : -1);
    e.preventDefault();
  } else if(e.key === "Escape"){
    resetAll();
  }
});

fillSelects();
draw();
window.addEventListener("resize", ()=>Object.keys(FIGS).forEach(k=>{ if(el(k)) Plotly.Plots.resize(el(k)); }));
</script>
</body>
</html>
"""


def main() -> None:
    with open(PLOTLY_JS, encoding="utf-8") as fh:
        plotly_js = fh.read()

    # hover template for the map needs two extra customdata columns (share, en)
    html = HTML
    html = html.replace("__KPI__", KPI_HTML)
    html = html.replace("__PAYLOAD__", json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__FIGS__", json.dumps(FIGS, ensure_ascii=False, separators=(",", ":")))
    html = html.replace("__PLOTLYJS__", plotly_js)

    with open(OUT_HTML, "w", encoding="utf-8") as fh:
        fh.write(html)

    size_mb = os.path.getsize(OUT_HTML) / 1024 / 1024
    print("written:", OUT_HTML)
    print("size   : %.2f MB" % size_mb)
    print("panel rows: %d | districts: %d" % (len(panel), len(dist_list)))
    print("KPI: arrivals %.1fM guests %.1fM r %.3f trips/visitor %.2f->%.2f (%+.1f%%) HHI %.0f"
          % (win_arrivals / 1e6, win_guests / 1e6, r_month, q_first.bus_trips_per_arrival,
             q_win_last.bus_trips_per_arrival, trip_drop_pct, hhi))


if __name__ == "__main__":
    main()


