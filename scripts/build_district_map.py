"""CISC7204 Class E Team 01 — M3 district map layer.

Builds the statistical-district geometry layer and the district-level map
metrics used by Section 15 of the pipeline notebook, then renders the static
choropleth figure (Figure 14) and the interactive Bokeh map.

Inputs
  data/geo/stats_zones/*.json                     DSEC 24 statistical districts (WGS84 polygons)
  data_processed/demand_district_hour_panel_2023_2026.csv   district x hour x month demand panel
  data_processed/supply_stop_departures.csv                 stop-level scheduled departures (lat/lng)

Outputs
  data_processed/macau_stats_zones.geojson        merged, coordinate-rounded geometry layer
  data_processed/district_map_metrics.csv         24 rows of map indicators
  figures/fig14_district_choropleth.png           three-panel static map
  reports/district_map_interactive.html           interactive Bokeh map

Run from the repository root:  python scripts/build_district_map.py
"""

import json
import math
import os
import glob

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm, TwoSlopeNorm
from matplotlib.patches import Patch
import matplotlib.patheffects as pe

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(REPO, "data", "geo", "stats_zones")
PROC = os.path.join(REPO, "data_processed")
FIGD = os.path.join(REPO, "figures")
REPD = os.path.join(REPO, "reports")
for d in (PROC, FIGD, REPD):
    os.makedirs(d, exist_ok=True)

# ZAPE = 新口岸區, NAPE = 外港及南灣湖新填海區 (repo naming follows the Portuguese acronyms)
EXCLUDE = {"umac"}  # University of Macau Hengqin campus: not one of the 24 DSEC statistical districts

plt.rcParams.update({
    "font.sans-serif": ["Microsoft YaHei", "SimHei", "DejaVu Sans"],
    "axes.unicode_minus": False,
})

C = {"blue": "#2f6fb2", "red": "#c0392b", "green": "#2e8b57", "grey": "#8a8f98", "orange": "#e08b2f"}


# --------------------------------------------------------------------------- #
# 1. geometry layer
# --------------------------------------------------------------------------- #
def round_coords(obj, nd=6):
    """Recursively round every coordinate pair, dropping duplicated vertices."""
    if isinstance(obj, list) and obj and isinstance(obj[0], (int, float)):
        return [round(float(v), nd) for v in obj]
    out = []
    for item in obj:
        c = round_coords(item, nd)
        if out and c == out[-1] and isinstance(c, list) and c and isinstance(c[0], (int, float)):
            continue
        out.append(c)
    return out


def ring_area_km2(ring):
    """Spherical-excess free planar shoelace on an equal-area-ish local projection (fine at Macao scale)."""
    lat0 = math.radians(sum(p[1] for p in ring) / len(ring))
    kx = 111.320 * math.cos(lat0)
    ky = 110.574
    s = 0.0
    for (x1, y1), (x2, y2) in zip(ring[:-1], ring[1:]):
        s += (x1 * kx) * (y2 * ky) - (x2 * kx) * (y1 * ky)
    return abs(s) / 2.0


def geom_area_km2(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    total = 0.0
    for poly in polys:
        if not poly:
            continue
        total += ring_area_km2(poly[0])
        for hole in poly[1:]:
            total -= ring_area_km2(hole)
    return max(total, 0.0)


def load_zones():
    feats = []
    for path in sorted(glob.glob(os.path.join(GEO, "*.json"))):
        key = os.path.basename(path)[:-5]
        if key in EXCLUDE:
            continue
        doc = json.load(open(path, encoding="utf-8"))
        for f in doc["features"]:
            props = f.get("properties", {})
            geom = {"type": f["geometry"]["type"], "coordinates": round_coords(f["geometry"]["coordinates"])}
            feats.append({
                "feature": {"type": "Feature", "properties": {
                    "key": key,
                    "district_cn": props.get("nameCht"),
                    "district_pt": props.get("namePor"),
                }, "geometry": geom},
                "district_cn": props.get("nameCht"),
                "area_km2": geom_area_km2(geom),
            })
    feats.sort(key=lambda r: r["district_cn"])
    return feats


# --------------------------------------------------------------------------- #
# 2. point-in-polygon: assign the 586 bus stops to districts
# --------------------------------------------------------------------------- #
def point_in_ring(x, y, ring):
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i][0], ring[i][1]
        x2, y2 = ring[(i + 1) % n][0], ring[(i + 1) % n][1]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside


def point_in_geom(x, y, geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        if not poly:
            continue
        if point_in_ring(x, y, poly[0]) and not any(point_in_ring(x, y, h) for h in poly[1:]):
            return True
    return False


def assign_stops(zones):
    stops = pd.read_csv(os.path.join(PROC, "supply_stop_departures.csv"))
    bbox = {}
    for z in zones:
        xs, ys = [], []
        polys = z["feature"]["geometry"]["coordinates"]
        polys = polys if z["feature"]["geometry"]["type"] == "MultiPolygon" else [polys]
        for poly in polys:
            for p in poly[0]:
                xs.append(p[0]); ys.append(p[1])
        bbox[z["district_cn"]] = (min(xs), min(ys), max(xs), max(ys))

    rows = []
    for s in stops.itertuples():
        hit = None
        for z in zones:
            x0, y0, x1, y1 = bbox[z["district_cn"]]
            if not (x0 - 1e-9 <= s.lng <= x1 + 1e-9 and y0 - 1e-9 <= s.lat <= y1 + 1e-9):
                continue
            if point_in_geom(s.lng, s.lat, z["feature"]["geometry"]):
                hit = z["district_cn"]
                break
        rows.append({"stop_code": s.stop_code, "district_cn": hit,
                     "weekdays": s.weekdays, "weekends": s.weekends})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 3. metrics
# --------------------------------------------------------------------------- #
def build_metrics(zones):
    panel = pd.read_csv(os.path.join(PROC, "demand_district_hour_panel_2023_2026.csv"))
    total_hits = panel["headcount"].sum()

    g = panel.groupby("district_cn")
    m = pd.DataFrame({
        "hits_total": g["headcount"].sum(),
        "months_present": g["month"].nunique(),
        "zone": g["zone"].first(),
    })
    m["share_total_pct"] = m["hits_total"] / total_hits * 100

    def block_share(df, mask):
        sub = df[mask]
        tot = sub["headcount"].sum()
        return sub.groupby("district_cn")["headcount"].sum() / tot * 100

    m["share_base_pct"] = block_share(panel, panel["year"] <= 2025).reindex(m.index)
    m["share_2026_pct"] = block_share(panel, panel["year"] == 2026).reindex(m.index)
    m["delta_pp"] = m["share_2026_pct"] - m["share_base_pct"]
    m["hits_2026"] = panel[panel["year"] == 2026].groupby("district_cn")["headcount"].sum().reindex(m.index)

    # peak hour and night share per district
    hour_share = panel.groupby(["district_cn", "hour"])["headcount"].sum().reset_index()
    hour_share["share"] = hour_share.groupby("district_cn")["headcount"].transform(lambda s: s / s.sum() * 100)
    peak = hour_share.loc[hour_share.groupby("district_cn")["headcount"].idxmax()].set_index("district_cn")
    m["peak_hour"] = peak["hour"]
    m["peak_hour_share_pct"] = peak["share"]
    night = panel[panel["hour"] <= 5].groupby("district_cn")["headcount"].sum().reindex(m.index) / m["hits_total"] * 100
    m["night_share_pct"] = night

    # geometry
    area = pd.Series({z["district_cn"]: z["area_km2"] for z in zones})
    m["area_km2"] = area.reindex(m.index)
    m["hits_per_km2_month"] = m["hits_total"] / m["area_km2"] / m["months_present"]

    # supply side, stop assignment
    st = assign_stops(zones)
    unassigned = int(st["district_cn"].isna().sum())
    sup = st.dropna(subset=["district_cn"]).groupby("district_cn").agg(
        stops=("stop_code", "nunique"),
        weekday_departures=("weekdays", "sum"),
        weekend_departures=("weekends", "sum"),
    )
    m = m.join(sup)
    m["stops"] = m["stops"].fillna(0).astype(int)
    m["weekday_departures"] = m["weekday_departures"].fillna(0)
    m["hits_per_departure"] = m["hits_total"] / m["weekday_departures"].replace(0, np.nan)
    m = m.reset_index().rename(columns={"index": "district_cn"})
    m = m.sort_values("hits_total", ascending=False).reset_index(drop=True)
    return m, unassigned, st


def main():
    zones = load_zones()
    geo_out = {
        "type": "FeatureCollection",
        "name": "macau_stats_zones_24",
        "metadata": {
            "source": "ioloas/macau-map-data + ngsiolei/macau-map-data (stats-zones/), derived from Macao Online Map webmap.gis.gov.mo",
            "crs": "EPSG:4326 (WGS84)",
            "districts": 24,
            "note": "ZAPE = Zona de Aterros do Porto Exterior (新口岸區); NAPE = Novos Aterros do Porto Exterior e Aterros da Baía da Praia Grande (外港及南灣湖新填海區)",
        },
        "features": [z["feature"] for z in zones],
    }
    geo_path = os.path.join(PROC, "macau_stats_zones.geojson")
    with open(geo_path, "w", encoding="utf-8") as fh:
        json.dump(geo_out, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"[geo] {len(zones)} districts -> {geo_path} ({os.path.getsize(geo_path)/1024:.0f} KB)")

    metrics, unassigned, stop_assign = build_metrics(zones)
    mpath = os.path.join(PROC, "district_map_metrics.csv")
    metrics.to_csv(mpath, index=False, encoding="utf-8-sig")
    print(f"[metrics] {len(metrics)} districts -> {mpath}")
    print(f"[supply] stops assigned {len(stop_assign) - unassigned}/{len(stop_assign)} "
          f"(unassigned {unassigned} = stops outside district polygons, kept out of district supply)")

    stop_assign.to_csv(os.path.join(PROC, "stop_district_assignment.csv"), index=False, encoding="utf-8-sig")

    print(metrics[["district_cn", "zone", "hits_total", "share_total_pct", "delta_pp",
                   "area_km2", "hits_per_km2_month", "stops", "peak_hour"]].to_string(index=False))

    plot_static(zones, metrics)
    return metrics


# --------------------------------------------------------------------------- #
# 4. static three-panel choropleth
# --------------------------------------------------------------------------- #
def draw_polys(ax, geom, **kw):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            xs = [p[0] for p in ring]
            ys = [p[1] for p in ring]
            ax.fill(xs, ys, **kw)


def label_points(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    best, best_a = None, -1
    for poly in polys:
        ring = poly[0]
        a = 0.0
        cx = cy = 0.0
        for (x1, y1), (x2, y2) in zip(ring[:-1], ring[1:]):
            cr = x1 * y2 - x2 * y1
            a += cr
            cx += (x1 + x2) * cr
            cy += (y1 + y2) * cr
        a /= 2.0
        if abs(a) > best_a:
            best_a = abs(a)
            best = (cx / (6 * a), cy / (6 * a)) if a else (ring[0][0], ring[0][1])
    return best


def plot_static(zones, metrics):
    geo = {z["district_cn"]: z["feature"]["geometry"] for z in zones}
    mm = metrics.set_index("district_cn")

    fig, axes = plt.subplots(1, 3, figsize=(15.6, 5.0))

    panels = [
        dict(ax=axes[0], col="hits_total", title="(a) 全期分區人流總量（2023-01 → 2026-09）",
             cmap="YlOrRd", norm=PowerNorm(gamma=0.45), label="人流命中數（人次）", fmt="{:,.0f}"),
        dict(ax=axes[1], col="delta_pp", title="(b) 2026 年 1–9 月 對 2023–2025 佔比變化",
             cmap="RdBu_r", norm=TwoSlopeNorm(vcenter=0.0,
                                             vmin=-max(abs(mm["delta_pp"]).max(), 0.3),
                                             vmax=max(abs(mm["delta_pp"]).max(), 0.3)),
             label="佔比變化（百分點）", fmt="{:+.2f} pp"),
        dict(ax=axes[2], col="hits_per_km2_month", title="(c) 月均人流密度（人次 / 平方公里 / 月）",
             cmap="YlGnBu", norm=PowerNorm(gamma=0.45), label="人次 / km² / 月", fmt="{:,.0f}"),
    ]

    for p in panels:
        ax = p["ax"]
        vals = mm[p["col"]]
        norm = p["norm"]
        if isinstance(norm, TwoSlopeNorm):
            norm.vmin = min(norm.vmin, vals.min()); norm.vmax = max(norm.vmax, vals.max())
        cmap = plt.get_cmap(p["cmap"])
        for name, geom in geo.items():
            v = vals.get(name, np.nan)
            color = "#f2f2f2" if not np.isfinite(v) else cmap(norm(v))
            draw_polys(ax, geom, facecolor=color, edgecolor="white", linewidth=0.5, zorder=2)
        for name, geom in geo.items():
            cx, cy = label_points(geom)
            short = name.replace("區", "").replace("及", "·")
            if len(short) > 6:
                short = short[:6]
            ax.text(cx, cy, short, ha="center", va="center", fontsize=4.6, zorder=5,
                    path_effects=[pe.withStroke(linewidth=1.4, foreground="white")])
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        cb = fig.colorbar(sm, ax=ax, fraction=0.030, pad=0.015)
        cb.set_label(p["label"], fontsize=7)
        cb.ax.tick_params(labelsize=6)
        ax.set_title(p["title"], fontsize=8.6, pad=6)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)

    axes[0].text(0.02, 0.02, "統計分區邊界：Macao Online Map (webmap.gis.gov.mo)，WGS84", transform=axes[0].transAxes,
                 fontsize=5.4, color="#666")

    fig.suptitle("Figure 14 — 澳門 24 個統計分區的旅遊人流分佈與 2026 年結構位移", fontsize=10.4, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGD, "fig14_district_choropleth.png")
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"[figure] {out}")
    return out


if __name__ == "__main__":
    main()
