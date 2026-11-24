---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 3948123ca1e8ab71efaa265617bdd19e_529ba1ede31211f189bc525400248c00
    ReservedCode1: uG3pe5YvL++jC0XQ145K1B0TdxgOI9M9QH4zwueg8GAtpG5EQdgU4X9uBn3Zqkd8z3/BmeIlVTi4V7D/57DcpbVMnsZAURSI0Yq+XYI+Z2+rVtg+qfJp+P2OKn/HvhiKR66qqN81VEk0M7GysbNvAUtcmG6fIQKPuPhmmUV38ox3mfuISSt8VF15TDQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 3948123ca1e8ab71efaa265617bdd19e_529ba1ede31211f189bc525400248c00
    ReservedCode2: uG3pe5YvL++jC0XQ145K1B0TdxgOI9M9QH4zwueg8GAtpG5EQdgU4X9uBn3Zqkd8z3/BmeIlVTi4V7D/57DcpbVMnsZAURSI0Yq+XYI+Z2+rVtg+qfJp+P2OKn/HvhiKR66qqN81VEk0M7GysbNvAUtcmG6fIQKPuPhmmUV38ox3mfuISSt8VF15TDQ=
---

# Interactive Dashboard - Visitor Arrivals, Hotel Occupancy and Bus Ridership in Macao

Companion deliverable for **CISC7204 Data Science and Data Visualization, Class E, Team 01**.
It puts the report's visitor-arrival, hotel-occupancy and public-bus-ridership evidence on a single
interactive screen so the supply-demand mismatch can be read at three spatial grains
(city / zone / the 24 DSEC statistical districts) and two temporal grains (month, hour of day).

---

## 1. Files

| File | Role |
| --- | --- |
| `CISC7204_ClassE_Team01_Dashboard.html` | **Main deliverable.** Self-contained single file, 6.2 MB. Plotly.js, its CSS and all data are embedded - double-click to open, no internet, no Python, no server. |
| `build_dashboard.py` | Rebuild script. Reads `data/`, recomputes every statistic, writes the HTML. Nothing is hard-coded. |
| `data/` | 21 CSV / GeoJSON snapshots: 18 from the team repository's `data_processed/` folder plus the 3 hotel files from `Dataset/`. |
| `plotly.min.js` | Plotly.js 6.x bundle that gets inlined by the build script (kept for reproducibility). |
| `preview/00_full_page.png` | Full-page render of the finished dashboard (1920 x 5035 at 100% zoom after the layout tightening; the checked-in crop is from an earlier build). |
| `preview/figs/01..15_*.png` | One crop per figure, taken from the live page. |
| `preview/hotel_03..06_*.png` | Crops of the four hotel figures in the current build. |

## 2. Open and rebuild

Open the HTML directly:

```
start "" "CISC7204_ClassE_Team01_Dashboard.html"
```

Rebuild after a data refresh:

```
python build_dashboard.py
```

Requirements: `pandas`, `numpy`, `plotly` (tested with pandas 3.0.3, plotly 6.7.0).
The script re-downloads nothing; it only reads `data/`.

## 3. Data lineage

Source: `FongChinWai-Vivi/CISC7204-ClassE-Team01-2026GitHub`, folder `data_processed/`.

| Panel file | Used for |
| --- | --- |
| `demand_monthly_arrivals.csv` | Fig 1 - long-run monthly arrivals 2015-2026, pandemic years masked |
| `monthly_panel_2023_01_2026_09.csv` | Fig 2 - monthly arrivals vs bus passenger trips; KPI totals over the 36-month window |
| `quarterly_panel_2023Q1_2026Q3.csv` | Fig 3 - bus trips per visitor by quarter; KPI change from 2023Q1 to 2025Q4 |
| `annual_alignment_2018_2026.csv` | Fig 1 - annual benchmark lines |
| `match_zone_supply_demand.csv` | Fig 8 - demand vs supply share by zone; Fig 9 - headcount per departure and supply/demand ratio; KPI zone figures |
| `match_hourly_profile.csv` | Fig 10 - demand share vs scheduled-departure share by hour, weekday and weekend gaps |
| `district_map_metrics.csv` | Fig 11 - 24-district choropleth (share, density, 2026 shift, load per departure); KPI HHI and top-3 share |
| `macau_stats_zones.geojson` | Fig 11 - district geometry and names |
| `demand_district_hour_panel_2023_2026.csv` | Fig 12 - district x hour heatmap; Fig 11 district-click linkage |
| `monthly_seasonality_index.csv` | Fig 13 - month-of-year seasonality index |
| `optional_2026_zone_shift.csv` | Fig 15 - zone share shift in 2026 |
| `optional_2026_hour_shift.csv` | Fig 15 - hourly share shift in 2026 |
| `demand_goldenweek_daily.csv` | Fig 14 - Golden Week daily intensity vs month average, 2017-2026 |
| `hotel_occ_monthly_2023_2026.csv` | Fig 4 - occupancy line (2023Q1 71.4% to 2026Q3 88.0%); KPI occupancy card |
| `hotel_guests_by_star_2023_2026.csv` | Fig 6 - monthly hotel guests stacked by hotel class (2/3/4/5-star) |
| `hotel_occ_history_2014_2025.csv` | Fig 7 - the long occupancy record 2014-2026 with the pandemic band and the 2019 mean |

## 4. Views

The grid is a strict 12-column layout: every row adds up to exactly 12 columns, so there is no half-empty
row and no card that stops short of the page edge. Paired cards carry the same plot height, and each
figure is bottom-aligned inside its card, so a card can never end in dead white space.

1. **Long-run monthly visitor arrivals, 2015-2026** - pre-pandemic, pandemic (left blank/dashed) and post-pandemic segments, with the 36-month estimation window shaded and annual benchmarks.
2. **Arrivals and bus passenger trips, monthly** - dual axis plus a fitted relationship; the monthly correlation (r = 0.759) is annotated.
3. **Bus trips per visitor, quarterly** - the ratio that carries the report's headline result: 9.96 to 5.83 per visitor, -41.5%.
4. **Visitor arrivals and the hotel occupancy rate** - arrivals bars on the left axis against the DSEC monthly occupancy line on the right; the two series move together at r = 0.91, which is the demand-side reason the buses are full.
5. **Occupancy against bus trips per visitor** - one marker per month, coloured by year; it shows that the ridership per visitor fell while the city was already running at 80-90% occupancy.
6. **Who fills the rooms: hotel guests by hotel class** - monthly guest counts stacked by 2/3/4/5-star tier; the 5-star tier dominates the stack, so capacity that ignores it is capacity aimed at a minority of the hotel base.
7. **The long occupancy record, 2014-2026** - the pandemic collapse, the 2023-2026 climb, and how far the market now sits above the 2019 mean before the buses are planned for it.
8. **Supply-demand mismatch across the three zones** - demand share, departure share and stop share side by side, with the gap index.
9. **Visitor headcount carried per scheduled departure** - the load measure behind the Taipa & Cotai squeeze (203 vs 66 on the Peninsula).
10. **Demand and scheduled supply by hour of day** - 24-hour demand share against weekday and weekend departure shares, gaps in percentage points.
11. **The 24 DSEC statistical districts** - choropleth with a four-way metric switch (arrival share / hits per km2 / 2026 share shift / load per departure).
12. **District by hour-of-day profile** - heatmap driven by the district selected on the map.
13. **Seasonality of arrivals, 2023-2025** - month-of-year index against the annual mean.
14. **Golden Week daily intensity** - day-by-day arrivals relative to the month average, per year, with the 1.0 reference line.
15. **What shifted in 2026** - zone share shift (top) and hourly share shift (bottom), stacked in one full-width card.

## 5. Interactions

| Control | Effect |
| --- | --- |
| `Year` | Re-slices the hotel block (Figs 4, 5, 6) onto that year, recomputes the district shares behind Fig 11 for that year, and restricts Figs 10 and 12 to that year. |
| `Zone` | Spotlights the selected zone (Figs 8 and 9 fade the other two bars), keeps only its districts coloured in Fig 11, and restricts Figs 10 and 12 to those districts. |
| `District` | Keeps only that district in Fig 11, drops Fig 12 to a single row, and redraws Fig 10 for that district alone. |
| `Map metric` | Switches Fig 11 between arrival share, hits per km2, 2026 share shift and load per departure; the colour scale, mid-point and colour-bar ticks change with it. The year share is recomputed for the selected year. |
| Click a district on the map | Same as picking that district - Figs 8, 9, 10 and 12 re-render for the clicked district. |
| `Play years` (`Auto-cycle` button) | Animates the Year filter: `All -> 2023 -> 2024 -> 2025 -> 2026` at 1.7 s per step. Every linked view re-renders at each step, so the drift of the yellow bars in Fig 12 and of the district shading in Fig 11 can be watched rather than inferred, and the hotel block shrinks to that year's twelve months. A second click pauses. |
| Click a bar in Fig 8 or Fig 9 | The zone bars double as controls: clicking one applies that zone filter (the other two bars fade, Fig 11 keeps only that zone's districts, Fig 12 narrows to 6 rows, Fig 10 is recomputed). |
| Click a row in Fig 12 | Same as picking that district from the dropdown. |
| Hover a district on the map, or a row in Fig 12 | Previews that district's own hour-of-day demand curve inside Fig 10 (its title shows `hover preview - <district>`), without touching the active filter. Moving the pointer away restores the in-scope curve. |
| Keyboard `Left` / `Right` | Step one year back / forward along `All -> 2023 -> 2024 -> 2025 -> 2026`. |
| Keyboard `Esc` | Reset all three filters. |
| HHI KPI card | No longer a frozen full-window number: it is recomputed for the current scope (e.g. 2,229 city-wide, 6,514 for Taipa & Cotai alone) and reports the equivalent number of equal-size districts plus the top-3 share. |
| Legend entries | Click to **highlight a series across every figure** instead of hiding it (see below). |
| Camera icon (top right of every figure) | Download that figure as PNG for the slide deck. |
| Reset button | Returns every filter to its default state. |

Every figure that the filter touches carries a badge with the current filter (for example
`2024 - Taipa & Cotai`), and the sticky bar at the top reports the share of the panel still in scope,
so a small numeric change is never mistaken for a dead control. When a filter is set while the linked
figures are off-screen, the page scrolls the first linked figure into view.

### 5.1 Legend click = one-click cross-figure highlight

Clicking a legend entry anywhere is intercepted (`plotly_legendclick` returns `false`), so the series
is **not** hidden. Instead the clicked name is broadcast to all 16 figures as a single global highlight
target, and every other series in every figure fades to `opacity 0.12`:

| Clicked legend name | Recognised as | Figures that respond |
| --- | --- | --- |
| `2023` / `2024` / `2025` / `2026` | a **year** | The 9 year-bearing figures (Figs 1, 2, 3, 4, 5, 6, 13, 14, 15); Fig 11 also re-colours itself to that year's district shares. Year-less figures (Figs 7, 8, 9, 10, 12) stay fully lit, because the year has no meaning there. |
| A zone name (`Macau Peninsula`, `Taipa & Cotai`, `Coloane`) | a **zone** | Figs 8 / 9 stay lit on that zone's bars, Fig 11 keeps only that zone's districts, Fig 12 keeps only that zone's rows. |
| Anything else (`Scheduled departures`, `Arrivals`, `per visitor` ...) | a **concept**, matched by rule | A supply-side, demand-side or intensity/ratio group of lines is lit across every figure that carries such a series, so the same logic is compared on all axes at once. |

State rules, all verified headless:

- the highlighted name is echoed in the `hiChip` badge in the filter bar, together with a reminder of
  how to clear it;
- clicking the same entry again, pressing `Esc`, or hitting `Reset filters` clears it and restores the
  exact pre-highlight opacities (they are snapshotted at draw time, not assumed to be `1`);
- the highlight composes with the `Year` / `Zone` / `District` filters rather than replacing them - a
  filtered figure is highlighted inside the filtered subset (`2025` + filter `2024` therefore lights
  nothing in Fig 10 instead of silently disagreeing with the filter).


Three reading paths are supported, so the same evidence can be attacked from whichever angle a reader
starts at: (1) *top-down* - pick a year, then a zone, then a district from the dropdowns; (2) *by
pointing* - hover to compare a district against the in-scope average, click to commit it as the filter;
(3) *over time* - hit `Play years` (or hold the arrow keys) and watch the seasonal ridge in Fig 12 and
the district shading in Fig 11 move together. The `hover preview` curve is deliberately drawn on the
same axes as the filtered curve in Fig 10, so the comparison is direct rather than across two figures.

## 6. Analytical conventions

- **36-month estimation window**: 2023-01 to 2025-12. All window statistics (103.2 M arrivals, 42.5 M hotel guests, r = 0.759 monthly, 5.83 trips per visitor at 2025Q4) are computed on this window.
- **2026 is partial**: nine months at monthly grain, three quarters at quarterly grain, January-July at hourly grain. 2026 series are drawn but never mixed into the window statistics.
- **Concentration**: HHI is computed on the district arrival-share vector (2,229, equivalent to ~4.49 equal-sized districts); the top three districts carry 62.6% of arrivals.
- **Map colour scale**: the arrival-share distribution is highly skewed (a few districts above 30%, most below 5%), so Fig 11 uses a square-root transform with a hand-set colour bar (tick labels 1 / 2 / 5 / 10 / 20 / 30 / 44%) instead of a linear ramp that would flatten 20 of the 24 districts into one shade.
- **Every number is recomputed** at build time from the CSVs; the HTML carries data, not pre-formatted strings, so re-running the script after a data update is enough.

## 7. Verification

The finished HTML was rendered headless (Edge, 1600 px viewport, DevTools Protocol) and every control
was driven programmatically rather than eyeballed:

| Probe | Observed |
| --- | --- |
| `Play years` | Year went `All -> 2024 -> 2025` in two ticks, the button flipped to `Pause`, the filter bar entered its playing state, and a second click restored `Play years`. |
| Click the `Taipa & Cotai` bar (Fig 8) and the same bar in Fig 9 | Zone filter applied, Fig 12 dropped from 24 rows to 6, and the HHI card moved `2,229 -> 6,514`. |
| Click `北安及大潭山區` on the map | District filter applied, Fig 12 dropped to a single row, scope line read `1 district in scope`. |
| Hover a Fig 12 row (`COTAI Reclamation Area`) | Fig 10 demand curve switched to that district (00:00 share `3.663% -> 4.010%`) and the title badge appeared; unhover restored the in-scope curve. |
| Hover `沙梨頭及大三巴區` on the map | Same preview behaviour (00:00 share `2.853%`) without changing the active filter. |
| Keyboard `Right` / `Left` / `Esc` | Year went `All -> 2023 -> All`, and `Esc` returned all three filters to default (HHI back to `2,229`). |
| The map during `Play years` | The map keeps one fixed whole-Macao framing for all four years - its computed `transform` stayed `none` and `transition-duration` `0s` at every tick, so only the district colours change as the years advance. |
| Click the `2024` legend entry (Fig 11) | Nothing was hidden; the badge read `highlight - 2024 (year)` and the 9 year-bearing figures dimmed every other year to `0.12` while the 5 year-less figures stayed fully lit. A second click, and `Esc`, both restored the snapshot opacities exactly. |
| Click `Scheduled departures` (Fig 8) | Recognised as a supply-side concept: the two supply lines stayed lit in Fig 2 (`[0.12, 1, 0.12]`) and the demand-side group faded in every figure that carries it. |

16 Plotly containers drew (12 original + 4 hotel), none of them overflowed its card, and the console stayed clean.
A layout probe ran over the live page: 15 cards formed 9 rows, every row filled the grid exactly
(left gap 1 px = the card border, right gap 0 px), every pair of cards in a row shared one bottom edge
(spread 0 px), and no figure sat more than 16 px above its card's bottom edge.
The hotel block was probed separately in the current build: Fig 4 carried 45 arrival bars against 45 occupancy
points, Fig 5 carried 4 year traces (12, 12, 12, 9 markers), Fig 6 carried 4 class traces of 45 months each and
Fig 7 carried 153 months; setting `Year = 2024` re-sliced Figs 4 and 6 to 12 points and left only the 2024 trace
populated in Fig 5, and returning to `All` restored 45 / 45. The PNGs in
`preview/figs/` predate this animation layer, so they show the earlier, filter-only control set; the
`preview/hotel_*.png` crops were taken from the current build.
*（内容由AI生成，仅供参考）*
