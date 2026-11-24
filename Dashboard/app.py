"""
CISC7204 Class E Team 01 - Macau visitor demand dashboard (Dash port).

This module is a 1:1 Dash rebuild of the static deliverable
``CISC7204_ClassE_Team01_Dashboard.html`` produced by ``build_dashboard.py``.
The static page ships 16 Plotly figures, 6 KPI cards and a small vanilla-JS
layer that links six controls (year / zone / district / map metric / play /
reset) to eight of those figures.  Here the original HTML body, CSS, Plotly
figures and JavaScript logic are all reproduced:

* page structure  -> parsed from the original <body> at export time
                     (``data/dash/body_template.html``),
* figures         -> the exact Plotly JSON found inside the static page
                     (``data/dash/figures.json``, transferred arrays decoded),
* linked behaviour -> the original ``app_logic.js`` formulas ported to Python
                     (filtered_rows / hour_profile / heat_from_rows / ...),
* styling          -> the original stylesheet (``assets/dashboard.css``).

The static HTML and ``build_dashboard.py`` are never modified.

Run
---
    python app.py            # http://127.0.0.1:8050
"""

from __future__ import annotations

import copy
import html as html_lib
import json
import math
import pathlib
from html.parser import HTMLParser

from dash import ALL, Dash, Input, Output, State, ctx, dcc, html, no_update

# --------------------------------------------------------------------------
# Paths and baked-in assets (produced once from the static HTML)
# --------------------------------------------------------------------------
BASE_DIR = pathlib.Path(__file__).resolve().parent
DASH_DATA = BASE_DIR / "data" / "dash"
PAYLOAD_PATH = DASH_DATA / "payload.json"
FIGURES_PATH = DASH_DATA / "figures.json"
BODY_PATH = DASH_DATA / "body_template.html"

MISSING_ASSETS = [
    str(p) for p in (PAYLOAD_PATH, FIGURES_PATH, BODY_PATH) if not p.exists()
]
if MISSING_ASSETS:
    raise SystemExit(
        "Missing Dash asset file(s):\n  "
        + "\n  ".join(MISSING_ASSETS)
        + "\nThey are extracted from the static dashboard, see README.md."
    )

PAYLOAD = json.loads(PAYLOAD_PATH.read_text(encoding="utf-8"))
FIGS = json.loads(FIGURES_PATH.read_text(encoding="utf-8"))
BODY_TEMPLATE = BODY_PATH.read_text(encoding="utf-8")

D = PAYLOAD["districts"]          # 24 districts: en/cn/zone/share/density/...
P = PAYLOAD["panel"]              # row-level panel: y / d / h / v
H = PAYLOAD["hotel"]              # monthly hotel series
KPI0 = PAYLOAD["kpi"]             # headline numbers used by the KPI cards
YEARS = PAYLOAD["years"]
ZONES = PAYLOAD["zones"]

EN2IDX = {d["en"]: i for i, d in enumerate(D)}
# Playback must emit the same value type as the Year dropdown options (ints),
# otherwise the closed dropdown cannot resolve its label and shows blank.
PLAY_SEQ = list(YEARS) if YEARS else [2023, 2024, 2025, 2026]

# Plotly config used by every figure on the static page (CONFIG in app_logic.js)
PLOTLY_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d", "toggleSpikelines"],
    "toImageButtonOptions": {"format": "png", "scale": 2},
}

SQRT_SCALE = [
    [0, "#F7FBFF"], [0.15, "#DEEBF7"], [0.35, "#9ECAE1"],
    [0.60, "#4292C6"], [0.82, "#08519C"], [1, "#08306B"],
]
RDBU = [[0, "#2166AC"], [0.5, "#F7F7F7"], [1, "#B2182B"]]

METRIC = {
    "share": {
        "key": "share", "ci": 9, "sqrt": True, "scale": SQRT_SCALE, "fmt": ".2f",
        "suffix": "%", "label": "Headcount share", "title": "Share of<br>city total (%)",
        "ticks": {
            "vals": [math.sqrt(v) for v in (1, 2, 5, 10, 20, 30, 44)],
            "text": ["1", "2", "5", "10", "20", "30", "44"],
        },
    },
    "density": {
        "key": "density", "ci": 5, "sqrt": False, "scale": "Viridis", "fmt": ",.0f",
        "suffix": "", "label": "Headcount per km\u00b2 per month",
        "title": "Headcount per<br>km\u00b2 per month", "ticks": None,
    },
    "delta": {
        "key": "delta", "ci": 6, "sqrt": False, "scale": RDBU, "fmt": "+.2f",
        "suffix": " pp", "label": "2026 share shift", "title": "2026 share<br>shift (pp)",
        "ticks": None,
    },
    "perdep": {
        "key": "perdep", "ci": 7, "sqrt": False, "scale": "OrRd", "fmt": ",.0f",
        "suffix": "", "label": "Headcount per departure",
        "title": "Headcount per<br>departure", "ticks": None,
    },
}

METRIC_OPTIONS = [
    {"label": "Headcount share of city total", "value": "share"},
    {"label": "Headcount per km\u00b2 per month", "value": "density"},
    {"label": "2026 share shift (pp)", "value": "delta"},
    {"label": "Headcount per departure", "value": "perdep"},
]
YEAR_OPTIONS = [{"label": "All years (2023-2026)", "value": "all"}] + [
    {"label": str(y), "value": y} for y in YEARS
]
ZONE_OPTIONS = [{"label": "All zones", "value": "all"}] + [
    {"label": z, "value": z} for z in ZONES
]
DISTRICT_OPTIONS = [{"label": "All districts", "value": "all"}] + [
    {"label": "%s (%s)" % (d["en"], d["cn"]), "value": i} for i, d in enumerate(D)
]

# Figures that respond to the linked filters, in page order.
LINKED_FIGS = ["f_hour", "f_heat", "f_map", "f_zone", "f_dep",
               "f_hocc", "f_hrel", "f_hstar"]


# --------------------------------------------------------------------------
# Ported logic (app_logic.js)
# --------------------------------------------------------------------------
def _as_year(year):
    if year in (None, "", "all"):
        return None
    try:
        return int(year)
    except (TypeError, ValueError):
        return None


def _as_district(district):
    if district in (None, "", "all"):
        return None
    try:
        return int(district)
    except (TypeError, ValueError):
        return None


def filtered_rows(year, zone, district):
    """Row indices of the demand panel inside the current filter."""
    y = _as_year(year)
    di = _as_district(district)
    p_year, p_dist, p_val = P["y"], P["d"], P["v"]
    out = []
    for i in range(len(p_val)):
        if y is not None and p_year[i] != y:
            continue
        if di is not None and p_dist[i] != di:
            continue
        if zone not in (None, "", "all") and D[p_dist[i]]["zone"] != zone:
            continue
        out.append(i)
    return out


def hour_profile(rows):
    """Hourly demand split in %, the red line of Fig 6."""
    buckets = [0.0] * 24
    total = 0.0
    hour, value = P["h"], P["v"]
    for i in rows:
        buckets[hour[i]] += value[i]
        total += value[i]
    if total <= 0:
        return buckets
    return [v / total * 100 for v in buckets]


def heat_from_rows(rows):
    """District x hour matrix of each district's own day (Fig 12)."""
    totals, grid = {}, {}
    disc, hour, value = P["d"], P["h"], P["v"]
    for i in rows:
        d = disc[i]
        hh = hour[i]
        totals[d] = totals.get(d, 0.0) + value[i]
        key = (d, hh)
        grid[key] = grid.get(key, 0.0) + value[i]
    dists = sorted(totals, key=lambda d: totals[d], reverse=True)
    y = [D[d]["en"] for d in dists]
    z = []
    for d in dists:
        t = totals[d] or 1
        z.append([round(grid.get((d, hh), 0.0) / t * 100, 3) for hh in range(24)])
    return y, z, dists


def scope_mask(zone, district):
    di = _as_district(district)
    mask = []
    for i, d in enumerate(D):
        if di is not None:
            mask.append(i == di)
        elif zone not in (None, "", "all"):
            mask.append(d["zone"] == zone)
        else:
            mask.append(True)
    return mask


def year_share(year):
    """Headcount share (%) of every district recomputed for the selected year."""
    y = _as_year(year)
    tot = [0.0] * len(D)
    allv = 0.0
    p_year, p_dist, p_val = P["y"], P["d"], P["v"]
    for i in range(len(p_val)):
        if y is not None and p_year[i] != y:
            continue
        tot[p_dist[i]] += p_val[i]
        allv += p_val[i]
    if allv <= 0:
        return [d["share"] for d in D]
    return [v / allv * 100 for v in tot]


def hhi_texts(year, zone, district):
    """Right-hand KPI card: concentration index of the districts in scope."""
    kpi_hhi = KPI0["hhi"]
    default_v = "{:,}".format(int(round(kpi_hhi)))
    default_s = "equivalent of %.2f equal districts \u00b7 top 3 = %.1f%%" % (
        10000 / kpi_hhi, KPI0["top3"]
    )
    is_default = (
        _as_year(year) is None
        and zone in (None, "", "all")
        and district in (None, "", "all")
    )
    if is_default:
        return default_v, default_s

    mask = scope_mask(zone, district)
    raw = [v if mask[i] else 0.0 for i, v in enumerate(year_share(year))]
    total = sum(raw)
    if not total > 0:
        return default_v, default_s
    pr = [v / total for v in raw]
    hhi = sum(p * p for p in pr) * 10000
    top3 = sum(sorted(pr, reverse=True)[:3]) * 100
    value = "{:,}".format(int(round(hhi)))
    sub = "equivalent of %.2f equal districts \u00b7 top 3 = %.1f%%" % (10000 / hhi, top3)
    if _as_year(year) is not None:
        sub += " \u00b7 %s only" % year
    return value, sub


def hover_template(metric_key):
    m = METRIC[metric_key]
    return (
        "<b>%{customdata[8]}</b> (%{location})<br>"
        + m["label"]
        + ": %{customdata["
        + str(m["ci"])
        + "]:"
        + m["fmt"]
        + "}"
        + m["suffix"]
        + "<br>Headcount share: %{customdata[9]:.2f}%"
        + "<br>Total headcount: %{customdata[0]:,.0f}"
        + "<br>Stops: %{customdata[1]}"
        + "<br>Weekday departures: %{customdata[4]:,.0f}"
        + "<br>Peak hour: %{customdata[2]}:00"
        + "<br>Night share (22:00-05:59): %{customdata[3]:.1f}%<extra></extra>"
    )


# --------------------------------------------------------------------------
# Figure rebuilds - same mutation the vanilla JS does with Plotly.restyle
# --------------------------------------------------------------------------
def _clone(fig_id):
    return copy.deepcopy(FIGS[fig_id])


def rebuild_hour(rows):
    fig = _clone("f_hour")
    if len(fig["data"]) > 1:
        fig["data"][1]["y"] = hour_profile(rows)
    return fig


def rebuild_heat(rows):
    fig = _clone("f_heat")
    y, z, _dists = heat_from_rows(rows)
    zmax = max([4.0] + [v for row in z for v in row]) if z else 4.0
    fig["data"] = [{
        "type": "heatmap",
        "z": z,
        "x": list(range(24)),
        "y": y,
        "colorscale": "YlOrRd",
        "zmin": 0,
        "zmax": round(zmax, 2),
        "colorbar": {
            "title": {"text": "% of that<br>district's day",
                      "font": {"size": 10, "color": "#0E2136"}},
            "tickfont": {"size": 10, "color": "#0E2136"},
            "thickness": 10,
            "len": 0.8,
        },
        "hovertemplate": "%{y}<br>%{x}:00<br>%{z:.2f}% of the district's headcount<extra></extra>",
    }]
    layout = fig["layout"]
    layout["margin"] = {"l": 150, "r": 10, "t": 10, "b": 44}
    layout["height"] = 470
    yaxis = dict(layout.get("yaxis") or {})
    yaxis["tickfont"] = {"size": 9, "color": "#0E2136"}
    yaxis["autorange"] = "reversed"
    layout["yaxis"] = yaxis
    return fig


def rebuild_map(year, zone, district, metric):
    fig = _clone("f_map")
    trace = fig["data"][0]
    m = METRIC.get(metric) or METRIC["share"]
    scope = scope_mask(zone, district)
    shares = year_share(year)

    if metric == "share":
        raw = list(shares)
    elif metric == "density":
        raw = [d["density"] * (shares[i] / d["share"]) if d["share"] > 0 else d["density"]
               for i, d in enumerate(D)]
    else:
        raw = [d[m["key"]] for d in D]

    z = []
    for i, v in enumerate(raw):
        if not scope[i]:
            z.append(None)
            continue
        z.append(math.sqrt(v) if m["sqrt"] else v)

    inside = [v for i, v in enumerate(raw) if scope[i]]
    ref = inside or raw
    mx = max(ref) if ref else 0
    ab = max([abs(v) for v in ref]) if ref else 0

    trace["z"] = z
    trace["colorscale"] = m["scale"]
    trace.setdefault("colorbar", {})
    trace["colorbar"].setdefault("title", {})
    trace["colorbar"]["title"]["text"] = m["title"]
    trace["hovertemplate"] = hover_template(metric if metric in METRIC else "share")
    trace["customdata"] = [
        [d["hits"], d["stops"], d["peak"], d["night"], d["wdep"], d["density"],
         d["delta"], d["perdep"], d["en"], round(shares[i], 3)]
        for i, d in enumerate(D)
    ]

    if metric == "delta":
        trace["zmin"] = -ab
        trace["zmax"] = ab
        trace["zmid"] = 0
        trace["colorbar"]["tickvals"] = None
        trace["colorbar"]["ticktext"] = None
    else:
        trace["zmin"] = 0
        trace["zmax"] = math.sqrt(mx) if m["sqrt"] else mx
        trace["zmid"] = None
        if m.get("ticks"):
            trace["colorbar"]["tickvals"] = m["ticks"]["vals"]
            trace["colorbar"]["ticktext"] = m["ticks"]["text"]
        else:
            trace["colorbar"]["tickvals"] = None
            trace["colorbar"]["ticktext"] = None
    return fig


def rebuild_zone_charts(year, zone, district):
    """Fig 8 / 9 dim the zones that are outside the current scope."""
    fig_zone = _clone("f_zone")
    fig_dep = _clone("f_dep")
    active = zone not in (None, "", "all") and district in (None, "", "all")
    target = zone
    opacity = [1 if (not active or z == target) else 0.15 for z in ZONES]
    for trace in fig_zone["data"]:
        trace.setdefault("marker", {})
        trace["marker"]["opacity"] = list(opacity)
    for trace in fig_dep["data"]:
        trace.setdefault("marker", {})
        trace["marker"]["opacity"] = list(opacity)
    return fig_zone, fig_dep


def rebuild_hotel(year):
    """Fig 3 / 4 / 5 follow the year selector only."""
    y_sel = _as_year(year)
    keep = [i for i in range(len(H["y"]))
            if y_sel is None or str(H["y"][i]) == str(y_sel)]
    x = [H["m"][i] for i in keep]

    f_occ = _clone("f_hocc")
    if len(f_occ["data"]) > 1:
        f_occ["data"][0]["x"] = x
        f_occ["data"][0]["y"] = [H["arr"][i] / 1e6 for i in keep]
        f_occ["data"][1]["x"] = x
        f_occ["data"][1]["y"] = [H["occ"][i] for i in keep]

    f_rel = _clone("f_hrel")
    for ti, yr in enumerate(H["years"]):
        if ti >= len(f_rel["data"]):
            break
        sel = [i for i in keep if H["y"][i] == yr]
        f_rel["data"][ti]["x"] = [H["occ"][i] for i in sel]
        f_rel["data"][ti]["y"] = [H["tpv"][i] for i in sel]
        f_rel["data"][ti]["customdata"] = [[H["m"][i]] for i in sel]

    f_star = _clone("f_hstar")
    for ti, cls in enumerate(H["cls"]):
        if ti >= len(f_star["data"]):
            break
        f_star["data"][ti]["x"] = x
        f_star["data"][ti]["y"] = [H["star"][cls][i] for i in keep]
    return f_occ, f_rel, f_star


# --------------------------------------------------------------------------
# One shot state computation (used both for the first paint and callbacks)
# --------------------------------------------------------------------------
def compute_view(year, zone, district, metric):
    year = "all" if year in (None, "") else year
    zone = "all" if zone in (None, "") else zone
    district = "all" if district in (None, "") else district
    metric = metric if metric in METRIC else "share"

    rows_ui = filtered_rows(year, zone, district)
    rows = rows_ui  # no legend highlight state is kept in the Dash port

    hour_fig = rebuild_hour(rows)
    heat_fig = rebuild_heat(rows)
    map_fig = rebuild_map(year, zone, district, metric)
    zone_fig, dep_fig = rebuild_zone_charts(year, zone, district)
    occ_fig, rel_fig, star_fig = rebuild_hotel(year)

    total = sum(P["v"][i] for i in rows_ui)
    grand = sum(P["v"])
    year_txt = "2023-2026" if year == "all" else str(year)
    if district == "all":
        dist_txt = "all 24 districts" if zone == "all" else "%s districts" % zone
    else:
        dist_txt = (D[int(district)].get("en") if int(district) < len(D) else str(district))
    n_dist = len({P["d"][i] for i in rows_ui})
    is_default = year == "all" and zone == "all" and district == "all"

    share_line = " %.2fM visitor headcount rows \u00b7 %.1f%% of the full panel \u00b7 %d district%s in scope" % (
        total / 1e6, (total / grand * 100 if grand else 0.0), n_dist, "" if n_dist == 1 else "s"
    )
    if district != "all" and int(district) < len(D):
        share_line += " \u00b7 share of city total %.2f%%" % D[int(district)]["share"]
    hint = ("No filter applied - showing the whole panel" if is_default
            else "Filter active \u2192 re-drawn: Fig 4, 5, 6, 8, 9, 10, 11, 12")

    scope_children = [
        html.B(year_txt), " \u00b7 ", html.B(dist_txt), html.Br(),
        share_line, html.Br(),
        html.Span(" " + hint, className="scopeHint"),
    ]

    chip_parts = []
    if not is_default:
        chip_parts = [year_txt]
        if zone != "all":
            chip_parts.append(zone)
        if district != "all" and int(district) < len(D):
            chip_parts.append(D[int(district)]["en"])
    chip_txt = " \u00b7 ".join(chip_parts)
    chip_style = {"display": "inline-block"} if chip_txt else {"display": "none"}

    hhi_v, hhi_s = hhi_texts(year, zone, district)
    heat_count = "%d row%s / %s" % (n_dist, "" if n_dist == 1 else "s", year_txt)

    return {
        "figures": {
            "f_hour": hour_fig,
            "f_heat": heat_fig,
            "f_map": map_fig,
            "f_zone": zone_fig,
            "f_dep": dep_fig,
            "f_hocc": occ_fig,
            "f_hrel": rel_fig,
            "f_hstar": star_fig,
        },
        "kpi_hhi_v": hhi_v,
        "kpi_hhi_s": hhi_s,
        "scope_children": scope_children,
        "chip_txt": chip_txt,
        "chip_style": chip_style,
        "heat_count": heat_count,
    }


INITIAL = compute_view("all", "all", "all", "share")
CHIP_COUNT = BODY_TEMPLATE.count('data-chip')


# --------------------------------------------------------------------------
# HTML body -> Dash components
# --------------------------------------------------------------------------
VOID_TAGS = {"br", "hr", "img", "input", "meta", "link", "source", "col"}
KEEP_ATTRS = {"className", "style", "id", "title", "htmlFor", "role", "href", "target"}

TAG_MAP = {
    "div": html.Div, "span": html.Span, "p": html.P, "b": html.B, "i": html.I,
    "em": html.Em, "strong": html.Strong, "small": html.Small, "code": html.Code,
    "h1": html.H1, "h2": html.H2, "h3": html.H3, "h4": html.H4, "h5": html.H5,
    "header": html.Header, "footer": html.Footer, "section": html.Section,
    "nav": html.Nav, "label": html.Label, "a": html.A, "ul": html.Ul, "ol": html.Ol,
    "li": html.Li, "br": html.Br, "hr": html.Hr, "sub": html.Sub, "sup": html.Sup,
    "table": html.Table, "thead": html.Thead, "tbody": html.Tbody,
    "tr": html.Tr, "td": html.Td, "th": html.Th, "button": html.Button,
}

_dropdown_values = {
    "selYear": lambda: "all",
    "selZone": lambda: "all",
    "selDistrict": lambda: "all",
    "selMetric": lambda: "share",
}
_dropdown_options = {
    "selYear": YEAR_OPTIONS,
    "selZone": ZONE_OPTIONS,
    "selDistrict": DISTRICT_OPTIONS,
    "selMetric": METRIC_OPTIONS,
}


def _generic_component(tag, attrs):
    cls = TAG_MAP.get(tag, html.Div)
    kwargs = {}
    for key, value in attrs.items():
        if key == "class":
            kwargs["className"] = value
        elif key == "for":
            kwargs["htmlFor"] = value
        elif key in KEEP_ATTRS:
            kwargs[key] = value
    if cls is html.Button:
        kwargs["n_clicks"] = 0
    return cls(**kwargs)


def _special_component(tag, attrs, chip_box):
    """Components that must become interactive Dash controls."""
    eid = attrs.get("id")
    if eid in _dropdown_values:
        return dcc.Dropdown(
            id=eid,
            options=_dropdown_options[eid],
            value=_dropdown_values[eid](),
            clearable=False,
            searchable=False,
            className="dash-dd",
        )
    if eid == "btnPlay":
        return html.Button("\u25b6 Play years", id="btnPlay", className="btn",
                           title=attrs.get("title", ""), n_clicks=0)
    if eid == "btnReset":
        return html.Button("Reset filters", id="btnReset", className="btn", n_clicks=0)
    if eid and eid.startswith("f_") and eid in FIGS:
        height = (FIGS[eid].get("layout") or {}).get("height") or 330
        return dcc.Graph(
            id=eid,
            figure=INITIAL["figures"].get(eid, FIGS[eid]),
            config=PLOTLY_CONFIG,
            className="plot",
            style={"height": "%dpx" % int(height), "width": "100%"},
            responsive=True,
        )
    if eid == "kpiHhiV":
        return html.Div(INITIAL["kpi_hhi_v"], id="kpiHhiV", className=attrs.get("class", "kpi-v"))
    if eid == "kpiHhiS":
        return html.Div(INITIAL["kpi_hhi_s"], id="kpiHhiS", className=attrs.get("class", ""))
    if eid == "hiChip":
        return html.Div("", id="hiChip", className=attrs.get("class", "chip"),
                        style={"display": "none"})
    if eid == "scopeText":
        return html.Div(INITIAL["scope_children"], id="scopeText",
                        className=attrs.get("class", "scope"))
    if eid == "heatCount":
        return html.Span(INITIAL["heat_count"], id="heatCount",
                         className=attrs.get("class", "chip"))
    if eid == "hoverChip":
        return html.Span("", id="hoverChip", className=attrs.get("class", "chip"),
                         style={"display": "none"})
    if "data-chip" in attrs:
        idx = chip_box[0]
        chip_box[0] += 1
        return html.Span("", id={"type": "chip", "index": idx},
                         className=attrs.get("class", "chip"),
                         style={"display": "none"})
    return None


def _prepare_body(markup):
    """Drop the <option> children of the native selects: Dash owns the options."""
    out = []
    pos = 0
    lower = markup.lower()
    while True:
        start = lower.find("<select", pos)
        if start < 0:
            out.append(markup[pos:])
            break
        out.append(markup[pos:start])
        open_end = lower.find(">", start) + 1
        close = lower.find("</select>", open_end)
        if close < 0:
            out.append(markup[start:])
            break
        out.append(markup[start:open_end])
        pos = close + len("</select>")
    return "".join(out)


class _BodyParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.roots = []
        self.stack = []
        self.chip_box = [0]

    def _add(self, node):
        if self.stack:
            self.stack[-1]["children"].append(node)
        else:
            self.roots.append(node)

    def handle_starttag(self, tag, attrs):
        ad = {k: (v if v is not None else "") for k, v in attrs}
        special = _special_component(tag, ad, self.chip_box)
        node = {"comp": special if special is not None else _generic_component(tag, ad),
                "children": [], "skip": special is not None, "tag": tag}
        self._add(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        ad = {k: (v if v is not None else "") for k, v in attrs}
        special = _special_component(tag, ad, self.chip_box)
        node = {"comp": special if special is not None else _generic_component(tag, ad),
                "children": [], "skip": True, "tag": tag}
        self._add(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data.strip():
            self._add({"comp": data, "children": [], "skip": True, "tag": "#text"})


def _finalize(node):
    comp = node["comp"]
    if node["skip"] or not node["children"]:
        return comp
    comp.children = [_finalize(child) for child in node["children"]]
    return comp


def _body_inner(markup):
    """Keep only what sits inside <body>: Dash owns <html> and <head>."""
    lower = markup.lower()
    start = lower.find("<body")
    if start < 0:
        return markup
    start = lower.find(">", start) + 1
    end = lower.rfind("</body>")
    return markup[start:end] if end > start else markup[start:]


def build_body():
    parser = _BodyParser()
    parser.feed(_prepare_body(_body_inner(BODY_TEMPLATE)))
    parser.close()
    return [_finalize(node) for node in parser.roots]


# --------------------------------------------------------------------------
# App
# --------------------------------------------------------------------------
PAGE_TITLE = (
    "Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, "
    "and Bus Ridership in Macao"
)

app = Dash(__name__, title=PAGE_TITLE, update_title=None)
server = app.server

# Dash's default index_string wraps the config/scripts in a <footer>, which adds
# ~43px of empty page below the layout. The static file has no such wrapper, so
# the shell is rebuilt without it to keep the page height identical.
app.index_string = (
    "<!DOCTYPE html>\n<html>\n<head>\n{%metas%}\n<title>{%title%}</title>\n"
    "{%favicon%}\n{%css%}\n</head>\n<body>\n{%app_entry%}\n{%config%}\n"
    "{%scripts%}\n{%renderer%}\n</body>\n</html>\n"
)
app.layout = html.Div(build_body(), id="page-root", style={"display": "contents"})


def no_change():
    return no_update


@app.callback(
    Output("f_hour", "figure"),
    Output("f_heat", "figure"),
    Output("f_map", "figure"),
    Output("f_zone", "figure"),
    Output("f_dep", "figure"),
    Output("f_hocc", "figure"),
    Output("f_hrel", "figure"),
    Output("f_hstar", "figure"),
    Output("kpiHhiV", "children"),
    Output("kpiHhiS", "children"),
    Output("scopeText", "children"),
    Output("hiChip", "children"),
    Output("hiChip", "style"),
    Output({"type": "chip", "index": ALL}, "children"),
    Output({"type": "chip", "index": ALL}, "style"),
    Output("heatCount", "children"),
    Input("selYear", "value"),
    Input("selZone", "value"),
    Input("selDistrict", "value"),
    Input("selMetric", "value"),
)
def update_linked(year, zone, district, metric):
    view = compute_view(year, zone, district, metric)
    figs = view["figures"]
    chips = [view["chip_txt"]] * CHIP_COUNT
    chip_styles = [view["chip_style"]] * CHIP_COUNT
    return (
        figs["f_hour"], figs["f_heat"], figs["f_map"], figs["f_zone"], figs["f_dep"],
        figs["f_hocc"], figs["f_hrel"], figs["f_hstar"],
        view["kpi_hhi_v"], view["kpi_hhi_s"], view["scope_children"],
        view["chip_txt"], view["chip_style"],
        chips, chip_styles,
        view["heat_count"],
    )


# ---- map <-> heatmap click selects that district -------------------------
@app.callback(
    Output("selDistrict", "value", allow_duplicate=True),
    Input("f_map", "clickData"),
    Input("f_heat", "clickData"),
    prevent_initial_call=True,
)
def pick_district(map_click, heat_click):
    if not ctx.triggered_id:
        return no_change()
    event = map_click if ctx.triggered_id == "f_map" else heat_click
    if not event or not event.get("points"):
        return no_change()
    point = event["points"][0]
    label = None
    custom = point.get("customdata")
    if isinstance(custom, list) and len(custom) >= 9:
        label = custom[8]
    if label is None and point.get("location") in EN2IDX:
        label = point["location"]
    if label is None and point.get("y") in EN2IDX:
        label = point["y"]
    if label in EN2IDX:
        return EN2IDX[label]
    return no_change()


# ---- zone charts select that zone ---------------------------------------
@app.callback(
    Output("selZone", "value", allow_duplicate=True),
    Output("selDistrict", "value", allow_duplicate=True),
    Input("f_zone", "clickData"),
    Input("f_dep", "clickData"),
    prevent_initial_call=True,
)
def pick_zone(zone_click, dep_click):
    event = zone_click if ctx.triggered_id == "f_zone" else dep_click
    if not event or not event.get("points"):
        return no_change(), no_change()
    point = event["points"][0]
    label = point.get("x")
    if label in ZONES:
        return label, "all"
    return no_change(), no_change()


# ---- year playback ------------------------------------------------------
@app.callback(
    Output("selYear", "value", allow_duplicate=True),
    Output("playTick", "disabled"),
    Output("btnPlay", "children"),
    Output("btnPlay", "className"),
    Input("btnPlay", "n_clicks"),
    Input("playTick", "n_intervals"),
    State("selYear", "value"),
    State("playTick", "disabled"),
    prevent_initial_call=True,
)
def drive_play(clicks, ticks, year, interval_disabled):
    trigger = ctx.triggered_id
    running = interval_disabled is False
    if trigger == "btnPlay":
        if not clicks:
            return no_change(), no_change(), no_change(), no_change()
        if running:
            return no_change(), True, "\u25b6 Play years", "btn"
        start = year if year in PLAY_SEQ else PLAY_SEQ[0]
        return start, False, "\u275a\u275a Pause", "btn on"
    if trigger == "playTick" and running and ticks:
        current = year
        idx = next((i for i, v in enumerate(PLAY_SEQ) if str(v) == str(current)), -1)
        return PLAY_SEQ[(idx + 1) % len(PLAY_SEQ)], no_change(), no_change(), no_change()
    return no_change(), no_change(), no_change(), no_change()


# ---- reset --------------------------------------------------------------
@app.callback(
    Output("selYear", "value", allow_duplicate=True),
    Output("selZone", "value", allow_duplicate=True),
    Output("selDistrict", "value", allow_duplicate=True),
    Output("selMetric", "value", allow_duplicate=True),
    Output("playTick", "disabled", allow_duplicate=True),
    Output("btnPlay", "children", allow_duplicate=True),
    Output("btnPlay", "className", allow_duplicate=True),
    Input("btnReset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_all(clicks):
    if not clicks:
        return (no_change(),) * 7
    return "all", "all", "all", "share", True, "\u25b6 Play years", "btn"




# The playback timer is appended after the replicated body markup so the parsed
# page keeps the exact element order of the static HTML.
app.layout.children.append(
    dcc.Interval(id="playTick", interval=1700, disabled=True, n_intervals=0)
)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
