# Dashboard (Plotly Dash, aligned 1:1 with the static HTML)

## 1. Correspondence with the static HTML
| Asset | Path | Origin and role |
|---|---|---|
| Page skeleton | data/dash/body_template.html | Extracted from the body of the static HTML: header → sticky filterbar → 6 KPI cards → 16 chart cards → footer |
| Plotly JSON for the 16 charts | data/dash/figures.json (1.1 MB) | Extracted directly from the Plotly figures inlined in the static HTML; injected unchanged on the Dash first screen |
| Data required by the callbacks | data/dash/payload.json (639 KB) | Chinese/English names, zone, share and density for the 24 districts; district × month × hour panel rows; hotel series; KPI constants |
| Styling | assets/dashboard.css | Original CSS (--navy:#1B4965, --blue:#2E86AB, --sky:#62B6CB, --red:#EE6C4D, --gold:#F4A259, --green:#3E8914, --purple:#7B2CBF, --ink:#0E2136) |
| Structural baseline | preview/html_structure.json / preview/html_structure.md | Page-structure inventory |

On start-up, `app.py` reads the three JSON/HTML assets above and maps the body tags through TAG_MAP, so the DOM hierarchy, class names and copy match the static page. The 8 static charts are rendered on the first screen from the original JSON in figures.json; the 8 linked charts are recomputed server-side from the current filters.

### 1.1 Controls
| Control | Default | Role |
|---|---|---|
| selYear | Year | All years (2023-2026), 2023–2026 (5 items) |
| selZone | Zone | All zones, Macau Peninsula, Taipa & Cotai, Coloane (4 items) |
| selDistrict | District | All districts + 24 districts (25 items, values indexed 0-23) |
| selMetric | Map metric | Headcount share (%), Headcount per km² per month, 2026 share shift (pp), Headcount per departure (4 items) |
| btnPlay | ▶ Play years | — | Cycles 2023→2026 in step with dcc.Interval(1700 ms) |
| btnReset | Reset filters | — | Restores the 4 dropdowns and the playback state |

No control was added to or removed from the HTML; there is no month-range slider and no 24-district multi-select.

### 1.2 KPIs (6 cards, identical to the HTML)
| # | Text | Static or dynamic |
|---|---|---|
| 1 | 103.2M Visitor arrivals | Static |
| 2 | 42.5M Visitor-guests | Static |
| 3 | 9.96 → 5.83 Bus trips per visitor | Static |
| 4 | 2,229 District concentration (HHI) | **Dynamic** (kpiHhiV / kpiHhiS) |
| 5 | 85.7% Occupancy rate | Static |
| 6 | 0.51 Taipa & Cotai demand/supply | Static |

### 1.3 One-to-one mapping of the 16 charts
| fig id | Card span | HTML title | Trace composition | Height | Dash implementation |
|---|---|---|---|---|---|
| f_long | span12 | 1·Long-run monthly visitor arrivals, 2015-2026 | 3 scatter | 330 | Static JSON |
| f_month | span7 | 2·Arrivals and bus passenger trips, monthly | bar+scatter | 330 | Static JSON |
| f_quarter | span5 | 3·Bus trips per visitor, quarterly | bar+scatter | 330 | Static JSON |
| f_hocc | span7 | 4·Visitor arrivals and the hotel occupancy rate | bar+scatter | 356 | Dynamic |
| f_hrel | span5 | 5·Occupancy against bus trips per visitor | 4 scatter | 356 | Dynamic |
| f_hstar | span6 | 6·Who fills the rooms: hotel guests by hotel class | 4 bar | 356 | Dynamic |
| f_hhist | span6 | 7·The long occupancy record, 2014-2026 | 1 scatter | 356 | Static JSON |
| f_zone | span6 | 8·Supply-demand mismatch across the three zones | 3 bar | 330 | Dynamic + click linkage |
| f_dep | span6 | 9·Visitor headcount carried per scheduled departure | 1 bar | 330 | Dynamic + click linkage |
| f_hour | span12 | 10·Demand and scheduled supply by hour of day | 5 trace | 360 | Dynamic |
| f_map | span7 | 11·The 24 DSEC statistical districts | choropleth | 470 | Dynamic |
| f_heat | span5 | 12·District by hour-of-day profile | heatmap | 470 | Dynamic + row click linkage |
| f_season | span6 | 13·Seasonality of arrivals, 2023-2025 | 1 bar | 330 | Static JSON |
| f_golden | span6 | 14·Golden Week daily intensity | 5 scatter | 330 | Static JSON |
| f_shift_zone | span12 | 15·What shifted in 2026 | 1 bar | 300 | Static JSON |
| f_shift_hour | span12 | 15·What shifted in 2026 | 1 bar | 340 | Static JSON |

## 2. Dependencies and running the app
Environment: Windows 11, Python 3.11.8 (the interpreter the repository was last verified on), dash 4.5.1, plotly 7.2.0, pandas 3.1.1, numpy 2.4.6. Any interpreter that satisfies `requirements.txt` at the repository root works; the folder is run in place, so no machine path is hard-coded.

```powershell
cd Dashboard
python app.py
```

Then open http://127.0.0.1:8050. The entry call is `app.run(debug=False, host="127.0.0.1", port=8050)`:
- debug=False, so no second process is spawned;
- if port 8050 is already in use, stop the holder first with Stop-Process -Id <pid> (find it with Get-NetTCPConnection -LocalPort 8050);
- all paths resolve from `__file__`, so `python app.py` runs from any working directory;
- **no network access at run time**: plotly.js is served locally by Dash from `_/_dash-component-suites/plotly/package_data/plotly.min.js`, and the CSS comes from `assets/dashboard.css`.

## 3. Callback inventory (5)
| # | Callback | Outputs | Inputs |
|---|---|---|---|
| 1 | update_linked | f_hour, f_heat, f_map, f_zone, f_dep, f_hocc, f_hrel, f_hstar, kpiHhiV, kpiHhiS, scopeText, hiChip (children + style), the filter chips (children + style), heatCount, hourText, hourValue (18 outputs in total) | selYear.value, selZone.value, selDistrict.value, selMetric.value, selHour.value |
| 2 | pick_district | selDistrict.value | f_map.clickData, f_heat.clickData |
| 3 | pick_zone | selZone.value, selDistrict.value | f_zone.clickData, f_dep.clickData |
| 4 | drive_play | selYear.value, playTick.disabled, btnPlay.children, btnPlay.className | btnPlay.n_clicks, playTick.n_intervals |
| 5 | reset_all | the 4 dropdown values + playTick.disabled + btnPlay.children + btnPlay.className | btnReset.n_clicks |

Reused pure functions: filtered_rows, hour_profile, heat_from_rows, scope_mask, year_share, hhi_texts, rebuild_hour, rebuild_heat, rebuild_map, rebuild_zone_charts, rebuild_hotel, compute_view.

> Note: the entries in PLAY_SEQ must be int years. With the string "2025", the Dash dropdown finds no matching option, so the button keeps advancing while the year label renders blank - this was hit during integration testing and has been fixed.

## 4. Verification results
Both builds were captured with headless Chrome (CDP, 1600 px wide, captureBeyondViewport):
- Static HTML baseline: preview/html_reference.png (1600 × 5104)
- Dash running build: preview/dash_preview.png (1600 × 5104)
- Playback-state capture: preview/dash_play_state.png

| Check | Result |
|---|---|
| Page title | Identical in both builds (Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao) |
| Full-page size | Both 1600 × 5104, aligned pixel by pixel |
| Full-page pixel difference (grayscale threshold 24) | **0.263%** |
| 16 charts: bounding boxes / axis titles / trace counts | All identical |
| Static charts (8) | Taken directly from the Plotly JSON inlined in the HTML, 0.00% difference |
| Linked charts | f_long 0.50%, f_month 0.78%, f_hocc 0.59%, f_hrel 0.25%, f_hstar 0.52%, f_zone 0.57%, f_hour 0.79%, f_golden 0.65% |
| Year switch | Selecting 2024 makes scopeText read 2024 · all 24 districts 33.74M ... | the 3 hotel charts and the map are recomputed |
| Zone click linkage | Clicking the first bar of f_zone sets selZone to Macau Peninsula and scopeText to 2023-2026 · Macau Peninsula districts 58.14M ... | |
| District filter | Selecting Cotai gives HHI 10,000 (a single district, equivalent to 1.00 districts) |
| Play cycle | On click the button becomes ❚❚ Pause and the year label advances 2023→2024→2025 step by step; clicking again pauses |
| Reset | All 4 dropdowns return to All and the page returns to its initial state (height back to 5104) |
| External dependencies | No cdn.plot.ly / unpkg / jsdelivr reference in the HTML; plotly.js loads locally |

### Residual differences (known)
1. The 8 linked charts differ by 0.25%–0.79% at legend text and curve edges, at anti-aliasing level (same JSON structure, same font family, different sub-pixel rendering);
2. In the playback state the page is 5109 px tall (5 px more than the default state), because the button label toggles between ▶ Play years and ❚❚ Pause and the text width inside the filterbar changes the line wrap;
3. In the static build f_golden / f_season / f_hour / f_shift_hour are computed in the browser by JS; in Dash they are rebuilt server-side from payload.json. The values match what the HTML shows on the first screen, but they no longer come from the same browser-side code path.

## 5. Known limitations
- Development server: app.run() is the Flask/Werkzeug dev server, with no WSGI/HTTPS configuration; local use only.
- No caching: every filter change recomputes 8 charts and serialises the whole response; the payload.json panel is stored row-compressed (four columns y/d/h/v) but there is no dcc.Store-level cache.
- Start-up cost: about 1.8 MB of JSON (payload + figures) is read at import time and the body template is parsed, giving a cold start of about 3–5 s.
- State lives in the browser: a refresh returns to the default All/All/All/share and no session is persisted.
- Map granularity: 24 DSEC statistical-district polygons with no street-level detail; the colour scale uses fixed bins per metric.
- No automated tests: verification was a one-off headless Chrome script plus pixel comparison, and the script is not shipped with the repository.
- Encoding: all files are UTF-8; on a legacy Windows code page, console output of Chinese district names may be garbled, while the browser rendering is correct.

*This README describes the rewritten Dash build (app.py, 863 lines, 5 callbacks, 4 dropdowns + 2 buttons, 16 charts, 6 KPI cards), which matches the static HTML chart by chart.*
*(AI-generated content, for reference only.)*
