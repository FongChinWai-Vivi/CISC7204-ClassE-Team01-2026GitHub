---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5480d5b254a487a11b77a101419fe1ce_3042286fe8ed11f1a20652540072b1e8
    ReservedCode1: TAZ8THZmL3GawPN4qgBzwHEmDNAVm66RDKEPUSnL8MBvn33VG6XWzYOFL5IpRSZW2CWiN0bigOgpLiua25fAqs83tjjZHhwFGhDB6ivhk7uSK4GP6XKQU43rPLXx79Hkx4o157kslcb1/A8qmfdqXCSriPaDF+A25Iq1l4G1wn2nQToC4arAih+fPO0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5480d5b254a487a11b77a101419fe1ce_3042286fe8ed11f1a20652540072b1e8
    ReservedCode2: TAZ8THZmL3GawPN4qgBzwHEmDNAVm66RDKEPUSnL8MBvn33VG6XWzYOFL5IpRSZW2CWiN0bigOgpLiua25fAqs83tjjZHhwFGhDB6ivhk7uSK4GP6XKQU43rPLXx79Hkx4o157kslcb1/A8qmfdqXCSriPaDF+A25Iq1l4G1wn2nQToC4arAih+fPO0=
---

# CISC7204 Class E Team 01 — Project Inventory (Step 0, read-only)

- Generated: 2026-11-26. Explored by static reading only: no notebook or dashboard was executed, no file outside `_temp/` was created, modified or deleted.
- Root: `C:\Users\user\Documents\cisc7204\Project\Github\CISC7204-ClassE-Team01-2026GitHub` (437 files, ≈168.3 MB incl. working tree only; `.git`, `__pycache__`, `.ipynb_checkpoints`, virtualenvs excluded from tree counts but noted where present).
- Draft analysed: `Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx`.
- Evidence rule: every row cites the file it came from. `UNKNOWN` = not determinable from the repository. Student IDs are not reproduced (stated as "present"); no e-mail addresses or secrets are printed.

---

## 1. Folder tree (≤4 levels, sizes for >1 MB)

```
CISC7204-ClassE-Team01-2026GitHub/
├─ .gitignore                                   (ignores temp/, .ipynb_checkpoints/, extension/, __pycache__)
├─ README.md                                    0.02 MB — project guide, key numbers, data sources
├─ Group_dataset_Visitor.py                     0.00 MB — market-level same-day/overnight cleaner
├─ CISC7204-Assgn02-Pair06-RevisedProjectProposal.docx.docx   0.02 MB  (earlier course deliverable, other pair)
├─ CISC7204-Assgn02-Pair08-ProposalVerification.ipynb         0.84 MB  (other pair)
├─ CISC7204-Assgn02-Pair08-RevisedProjectProposal_b98…ea.docx  0.98 MB  (other pair)
├─ CISC7204-Assgn02-Pair10-RevisedProjectProposal.docx         0.43 MB  (other pair)
├─ cisc7204-Class_E-Team_01_WorkPlan01.docx / .pdf             0.02 / 0.14 MB
├─ cisc7204-Class_E-Team_01-WorkPlan02.docx / .pdf             0.03 / 0.29 MB
├─ .vscode/                        1 file  0.0 MB
├─ Dashboard/                     60 files 21.4 MB
│  ├─ CISC7204_ClassE_Team01_Dashboard.html     6.13 MB  (>1 MB, self-contained product)
│  ├─ plotly.min.js                             4.62 MB  (>1 MB, vendored lib)
│  ├─ app.py (31.5 KB) · build_dashboard.py (80.7 KB) · README.md · README_Dashboard.md
│  ├─ assets/                      2 files 0.0 MB  (dashboard.css, dash_overrides.css)
│  ├─ data/                       24 files 4.5 MB
│  │  ├─ dash/                     3 files 1.7 MB  (payload.json, figures.json 1.07 MB, body_template.html)
│  │  └─ 18 CSV + macau_stats_zones.geojson      (mirror of data_processed/, see §1.3)
│  └─ preview/                    28 files 6.0 MB  (full-page + per-figure screenshots)
│     └─ figs/                    16 files 0.5 MB
├─ Data cleaning/                  0 files 0.0 MB  (EMPTY folder)
├─ Dataset/                       13 files 0.1 MB  (raw DSEC/MGTO extracts, untouched)
├─ Monthly_Bus_Database/          32 files 9.3 MB
│  ├─ bus_monthly_2020_2026.csv, bus_annual_reference_2011_2025.csv,
│  │  bus_monthly_by_operator_2026.csv, bus_monthly.sqlite, source_index.csv, README.md
│  └─ raw_pdfs/                   26 files 9.2 MB  (DSAT monthly statistics PDFs)
├─ Proposal/                       4 files 2.1 MB
│  ├─ CISC7204_ClassE_Team01_Proposal.docx 0.67 MB (same byte size as the FinalReport.docx — see §1.3)
│  ├─ CISC7204_ClassE_Team01_Proposal.pdf  0.78 MB
│  └─ Project report/              2 files 0.7 MB  (FinalReport.docx 0.67 MB + _temp/)
├─ cisc7204-Class_E-Team_01_Photos/  11 files 7.2 MB  (group photos, incl. one 5.65 MB JPEG)
├─ data/                         194 files 32.3 MB
│  ├─ mgtodataplus/               45 files 17.5 MB  (MacaoDistrictTourismData_*.xlsx, 2023-01..2026-09)
│  ├─ data.gov.mo_bus_route_shp/  11 files  8.3 MB  (BUS_ROUTE_SEQ.xls 5.62 MB >1 MB)
│  ├─ geo/                        26 files  4.2 MB  (stats_zones JSON)
│  ├─ github_macau-bus-data/      93 files  0.9 MB  (routes.json, stops.json, route-schedule/)
│  ├─ dsec_timeseries/             3 files  0.2 MB  (KeyIndicator_27/127/28 JSON)
│  ├─ gov_mo_datasets/             9 files  0.3 MB  (tidy district×hour xlsx)
│  └─ mopubbus/                    7 files  0.9 MB  (AP1/3 trip records, weather_types.csv)
├─ data_processed/                49 files 18.4 MB  (all derived panels; 47 CSV + 3 GeoJSON + 1 SQLite)
│  ├─ macau_visitor_transport.sqlite            6.68 MB  (>1 MB, table analysis_master 25,920 rows)
│  ├─ analysis_dataset_master.csv               4.34 MB  (>1 MB)
│  ├─ demand_district_hour_panel_2023_2026.csv  1.92 MB  (>1 MB)
│  ├─ mgto_district_hour_master_2023_01_2026_09.csv 1.92 MB (>1 MB)
│  └─ 45 further CSVs + 2 GeoJSON (see §2)
├─ figures/                       16 files 2.8 MB  (fig1..fig14 PNG + archive/ 2 legacy PNG)
├─ minutes/                        1 file  0.1 MB  (1st meeting minutes PDF only)
├─ notebooks/                     37 files 12.6 MB
│  ├─ cisc7204_pipeline_M3_vivi.ipynb                    3.82 MB  (>1 MB)
│  ├─ CISC7204_ClassE_Team01_Visualization_lucas_pending test.ipynb 2.30 MB (>1 MB)
│  ├─ CISC7204_ClassE_Team01_Visualization_updated.ipynb 2.16 MB  (>1 MB)
│  ├─ cisc7204_proposal_figures_colour.ipynb             0.02 MB
│  ├─ Cross_check_and_pending_revisions.md               0.01 MB
│  ├─ .ipynb_checkpoints/          4 files 8.2 MB  (stale autosaves of the same notebooks)
│  └─ figures/                    32 files 4.3 MB  (16 PNG + 16 grayscale twins)
├─ reports/                        3 files 1.0 MB  (data_dictionary.md, data_coverage_audit_2026-11-04.md,
│                                                   district_map_interactive.html 0.95 MB)
├─ scripts/                        3 files 0.0 MB  (build_panels.py, build_period_analysis.py, build_district_map.py)
└─ video/                          2 files 50.4 MB
   ├─ …Team Project Introductory Video.mp4   44.23 MB  (>1 MB, largest file in repo)
   └─ …Team Project Introductory Video ppt.pptx 6.21 MB  (>1 MB)
```

### 1.3 Large / duplicate-looking files

| Path | Size | Flag / evidence |
|---|---|---|
| `video\…Introductory Video.mp4` | 44.23 MB | largest asset; video deliverable, not reusable in the report |
| `dashboard\CISC7204_ClassE_Team01_Dashboard.html` | 6.13 MB | self-contained (plotly.js inlined) — the only offline-runnable dashboard artefact |
| `data_processed\macau_visitor_transport.sqlite` | 6.68 MB | one table duplicating `analysis_dataset_master.csv` (25,920 rows) — duplicate content, different container |
| `Proposal\CISC7204_ClassE_Team01_Proposal.docx` vs `Proposal\Project report\…FinalReport.docx` | both 705,834 bytes | byte-size identical → suspected duplicate, cannot confirm without diff (read-only, not modified) |
| `data_processed\demand_district_hour_panel_2023_2026.csv` vs `…mgto_district_hour_master_2023_01_2026_09.csv` | both 2,016,276 bytes | identical size and columns → suspected duplicate under two names (README lists both) |
| 18 CSVs + `macau_stats_zones.geojson` in `Dashboard\data\` | same names, same sizes as `data_processed\` | mirror copies for the dashboard bundle |
| `notebooks\.ipynb_checkpoints\` (4 files, 8.2 MB) | ≈ copies of the 3 notebooks + 1 | stale autosaves, ignored by `.gitignore` but present on disk |
| `figures\archive\legacy_fig1…png`, `legacy_fig2…png` | 0.9 MB | superseded figure versions |

---

## 2. Datasets

Granularity abbreviations: M = monthly, Q = quarterly, D = daily, DH = district × hour (monthly average per hour slot), S = stop-level, Y = yearly.
"Stated source" is quoted from `README.md`, `data_processed\dataset_inventory.csv`, `data_processed\phase1_usability_verdict.csv` or the draft `…FinalReport.docx` §3.

| # | Path | Format | Rows | Key columns | Date range | Gran. | Stated source | Used by |
|---|---|---|---|---|---|---|---|---|
| D1 | `data_processed\monthly_panel_2023_01_2026_09.csv` | CSV | 45 | month, visitor_arrivals, hotel_occ_pct, hotel_guests, hotel_rooms, bus_daily_avg_trips_wan, bus_monthly_trips, buses_in_service, mgto_district_headcount, bus_trips_per_arrival | 2023-01 … 2026-09 | M | merged DSEC + MGTO + DSAT (README) | pipeline §6/§14, Visualization_updated §2–§11, proposal_figures, build_dashboard |
| D2 | `data_processed\quarterly_panel_2023Q1_2026Q3.csv` | CSV | 15 | quarter, visitor_arrivals_sum, hotel_occ_avg_pct, bus_monthly_trips_sum, bus_trips_per_arrival, district_hits_per_arrival | 2023Q1 … 2026Q3 | Q | roll-up of D1 (pipeline §14) | pipeline §14, proposal_figures fig4, dashboard |
| D3 | `data_processed\demand_monthly_arrivals.csv` | CSV | 225 | date, arrivals, same_day_arrivals, arrivals_yoy_pct, same_day_share_pct | 2008-01 … 2026-09 | M | DSEC Key Indicator 27/127/28 (dataset_inventory.csv) | pipeline, Visualization_updated, proposal_figures (fig1) |
| D4 | `data_processed\demand_district_hour_panel_2023_2026.csv` | CSV | 25,920 | year, month, period ("00:00"), district_cn, district_en, headcount, hour, zone | 2023-01 … 2026-09 (45 months) | DH | MGTO Data+ 45 monthly XLSX (README) | pipeline §7–§9, Visualization_updated fig 10–12, dashboard heat/map |
| D5 | `data_processed\mgto_district_hour_master_2023_01_2026_09.csv` | CSV | 25,920 | same schema as D4 | 2023-01 … 2026-09 | DH | derived from `data\mgtodataplus\` | pipeline §3.2 |
| D6 | `data_processed\analysis_dataset_master.csv` | CSV | 25,920 | year, month, hour, period, district_cn/en, zone, headcount, headcount_share_of_month, month_arrivals_per_district_hour, visitor_arrivals, hotel_occ_pct, bus_monthly_trips, daily_bus_departures, supply_demand_ratio | 2023 … 2026 | DH | join of D1 + D4 + supply (pipeline §13) | Visualization_updated §2+, SQLite copy |
| D7 | `data_processed\match_zone_supply_demand.csv` | CSV | 3 | zone, demand_share_pct, departures_share_pct, stops_share_pct, supply_demand_ratio, gap_index | 2026-01…07 window | zone | DSAT GTFS departures + D4 2026 | pipeline §7, fig2, docx Figure 2 |
| D8 | `data_processed\match_hourly_profile.csv` | CSV | 24 | hour, demand_share_pct, supply_share_weekday_pct, supply_share_weekend_pct, gap_*_pp | 2026-01…07 window | hour | as D7 | pipeline §8, fig3, docx Figure 3 |
| D9 | `data_processed\district_map_metrics.csv` | CSV | 24 | district_cn, hits_total, share_total_pct, share_2026_pct, delta_pp, peak_hour, night_share_pct, area_km2, hits_per_km2_month, stops, weekday/weekend_departures, hits_per_departure | 2023-12 & 2026 | district | D4 + D7 + polygon areas | choropleth fig14, dashboard map |
| D10 | `data_processed\annual_summary_2023_2026.csv` | CSV | 4 | year, zone shares, total_headcount, months, arrivals_sum, occ_avg, bus_trips_sum, trips_per_arrival | 2023–2026 | Y | roll-up of D1/D4 | dashboard, README annual block |
| D11 | `data_processed\monthly_detail_2023_01_2026_09.csv` | CSV | 45 | 22 cols incl. arrivals_yoy_pct, arrivals_mom_pct, ma3, season_index, hotel_occ_yoy_pp, ranks | 2023-01 … 2026-09 | M | roll-up of D1/D3 | Visualization_updated, dashboard |
| D12 | `data_processed\monthly_seasonality_index.csv` | CSV | 12 | month_no, season_index_arrivals, mean_arrivals_2023…2025, peak_flag | 2023–2025 base | M (of year) | D1 | fig8, dashboard seasonality |
| D13 | `Dataset\DSEC_hotel_guests_rooms_2023_01_2026_09.csv` | CSV | 45 | month, guests, rooms | 2023-01 … 2026-09 | M | DSEC hotel survey (draft §3.3) | D1 build |
| D14 | `Dataset\Hotel_occ_total.csv` | CSV | 153 | Year, Quarter, Month, Hotel Establishments, Occupancy rate, Difference, Remark ×2 | 2014-01 … 2026-09 | M | DSEC / "Macao Tourism Data Plus" (draft §3.3) | D1, `hotel_occ_history_2014_2025.csv` |
| D15 | `Dataset\Visitors_Arrival_byArrivalPoint.csv` | CSV | 153 | Year, Quarter, Month, Source Markets, Modes of Transport, Transport, Total, Remark ×2 | 2014-01 … 2026-09 | M | DSEC (draft §3.1) | context only |
| D16 | `Dataset\Visitors_Arrival_byOnday_Overnight_{CN,HK,KR,TW}.csv` | CSV | 153 each | Year, Quarter, Month, Source Markets, SameDay, OverNight, Remark ×2 each | CN/HK/TW 2014-…, KR 2023-01 … | M | DSEC (draft §3.2) | D3, market mix fig9 |
| D17 | `Dataset\visitors_2023_2026_by_market_summary.csv` | CSV | 180 | Year, Quarter, Month, Market, SameDay, OverNight | 2023-01 … 2026-09 | M | derived from D16 | Visualization_updated §15, fig9 |
| D18 | `Monthly_Bus_Database\bus_monthly_2020_2026.csv` | CSV | 81 | month, daily_avg_trips_wan, monthly_trips_est, buses_in_service, bus_stops, trips_per_bus_per_day, visitor_arrivals, trips_per_arrival, dsat_minfu/tcm_daily_wan, source | 2020-01 … 2026-09 | M | "DSAT quarterly statistics PDF" (column `source`) | D1 build (M3 module) |
| D19 | `Monthly_Bus_Database\bus_monthly.sqlite` | SQLite | 1 table, 15 rows | annual_reference(year, official_total_trips_yi, official_daily_avg_wan, …) | 2011–2025 | Y | DSAT annual | cross-check only |
| D20 | `data_processed\supply_stops.csv` | CSV | 586 | code, nameCht, namePor, parentCode, lat, lng, zone, stop_code, n_routes, n_records | snapshot 2026 | S | `data\github_macau-bus-data` (draft §3.7) | D7/D8 supply side |
| D21 | `data_processed\stop_district_assignment.csv` | CSV | 586 | stop_code, district_cn, weekdays, weekends (scheduled departures) | snapshot 2026 | S | timetable headways (920 windows) | D7/D9 |
| D22 | `data_processed\macau_stats_zones.geojson` | GeoJSON | 24 features (Polygon) | key, district_cn, district_pt | n/a | polygon | `data\geo\stats_zones\*.json` | fig14, dashboard map |
| D23 | `data_processed\macau_districts_official_26.geojson` / `macau_map_layer_26.geojson` | GeoJSON | 26 / 26 features | zone, district_cn, district_pt, district_en, (has_data, area_km2, context_note) | n/a | polygon | official 26-district layer | map layer |
| D24 | `data\mgtodataplus\MacaoDistrictTourismData_{202312,202412,202512,202609}_en.xlsx` | XLSX | 45 files (YTD snapshots) | district × hour × month headcount | 2023-01 … 2026-09 | DH | MGTO Data+ (README) | D4 build (YTD de-duplication) |
| D25 | `data\dsec_timeseries\DSEC_KeyIndicator_{27,127,28}.json` | JSON | 3 files | monthly arrivals, same-day arrivals, YoY | 2008-01 … 2026-08 | M | DSEC (dataset_inventory.csv) | D3 build |
| D26 | `data\mopubbus\*.csv` | CSV | 1,292–6,712 rows / file | AP1 & 3 trip records, crowd level, traffic condition, weather_types.csv (16 rows) | Grand Prix vs normal weeks | trip | MOPubBus (phase1 verdict) | pipeline §10 event view only |
| D27 | `data\data.gov.mo_bus_route_shp\…\BUS_ROUTE_SEQ.xls` | XLS | 5.62 MB | route/stop sequence inventory | snapshot | route-stop | data.gov.mo (phase1 verdict) | cross-check only |

### 2.1 Sample rows (verbatim, 3 rows each)

`D1 monthly_panel_2023_01_2026_09.csv`
```
month,year,month_no,quarter,visitor_arrivals,hotel_occ_pct,hotel_guests,hotel_rooms,bus_daily_avg_trips_wan,bus_monthly_trips,buses_in_service,mgto_district_headcount,bus_trips_per_arrival
2023-01,2023,1,2023Q1,1397748.0,71.4,847762.0,38549.0,46.52,14421200.0,1211.0,1847696.0,10.3175
2023-02,2023,2,2023Q1,1593743.0,76.1,879831.0,38839.0,59.15,16562000.0,1241.0,2102137.0,10.3919
2023-03,2023,3,2023Q1,1956867.0,77.1,977787.0,38995.0,59.1,18321000.0,1144.0,1928217.0,9.3624
```
`D2 quarterly_panel_2023Q1_2026Q3.csv`
```
quarter,months_in_data,visitor_arrivals_sum,hotel_occ_avg_pct,hotel_guests_sum,hotel_rooms_avg,bus_daily_avg_trips_wan_mean,bus_monthly_trips_sum,buses_in_service_max,mgto_district_headcount_sum,bus_trips_per_arrival,district_hits_per_arrival
2023Q1,3,4948358,74.9,2705380,38794,54.92,49304200,1241.0,5878050,9.9637,1.1879
2023Q2,3,6697519,80.7,3338976,42942,58.27,53028700,1144.0,6935830,7.9177,1.0356
2023Q3,3,8282291,85.4,3749426,44753,60.06,55252000,1064.0,8233061,6.6711,0.9941
```
`D3 demand_monthly_arrivals.csv`
```
date,year,month,arrivals,same_day_arrivals,arrivals_yoy_pct,same_day_share_pct
2008-01-01,2008,1,1900592.0,1030413.0,,54.21537078973288
2008-02-01,2008,2,2000243.0,1080446.0,,54.01573708794381
2008-03-01,2008,3,2135523.0,1173683.0,,54.959979358686375
```
`D4 demand_district_hour_panel_2023_2026.csv`
```
year,month,period,district_cn,district_en,headcount,hour,zone
2023,12,00:00,新橋區,Barca,1031,0,Macau Peninsula
2023,12,00:00,中區,Baixa de Macau,5906,0,Macau Peninsula
2023,12,00:00,氹仔中心區,Baixa da Taipa,3192,0,Taipa & Cotai
```
`D7 match_zone_supply_demand.csv`
```
zone,demand_share_pct,departures_share_pct,stops_share_pct,visitor_headcount_2026H1,daily_bus_departures,demand_per_departure,supply_demand_ratio,gap_index
Macau Peninsula,42.23,66.42,59.9,10225946,154853.0,66.036,1.573,24.19
Taipa & Cotai,56.1,28.68,30.55,13585057,66865.0,203.171,0.511,-27.42
Coloane,1.67,4.91,9.56,403413,11437.0,35.273,2.94,3.24
```
`D8 match_hourly_profile.csv`
```
hour,demand_share_pct,supply_share_weekday_pct,supply_share_weekend_pct,gap_weekday_pp,gap_weekend_pp
0,3.625,1.726,1.776,-1.899,-1.849
1,3.361,0.388,0.404,-2.973,-2.957
2,3.337,0.271,0.284,-3.066,-3.053
```
`D9 district_map_metrics.csv` (first 12 of 19 columns shown)
```
district_cn,hits_total,months_present,zone,share_total_pct,share_base_pct,share_2026_pct,delta_pp,hits_2026,peak_hour,peak_hour_share_pct,night_share_pct
路氹填海區,59053202,12,Taipa & Cotai,43.96015298554358,43.73096620887155,44.70410804404047,0.9731418351689172,14143116,17,5.015228471438348,23.082211528512882
新口岸區,13165289,12,Macau Peninsula,9.800452794056689,10.118068124438052,8.769452947012681,-1.348615177425371,2774407,14,4.686991679407873,24.14712658415626
外港及南灣湖新填海區,11648017,12,Macau Peninsula,8.670971123601602,8.459956845185003,9.355937080724628,0.8959802355396249,2959954,16,5.97973886885639,20.54433814785813
```
`D10 annual_summary_2023_2026.csv`
```
year,Coloane,Macau Peninsula,Taipa & Cotai,total_headcount,months,months_panel,arrivals_sum,occ_avg,bus_trips_sum,trips_per_arrival,arrivals_per_month
2023,1.406,43.315,55.278,28906800,12,12,28213003.0,81.208,214206400.0,7.896,2351084.0
2024,1.431,43.75,54.819,33743835,12,12,34928650.0,86.35,228663800.0,6.614,2910721.0
2025,1.601,43.911,54.488,40045669,12,12,40069360.0,89.433,232120300.0,5.845,3339113.0
```
`D12 monthly_seasonality_index.csv`
```
month_no,season_index_arrivals,mean_arrivals_2023,mean_arrivals_2024,mean_arrivals_2025,mean_arrivals_2023_2025,peak_flag
1,91.92,1397748.0,2861609.0,3646561.0,2635306.0,trough
2,93.41,1593743.0,3293564.0,3147184.0,2678164.0,trough
3,90.06,1956867.0,2720584.0,3068920.0,2582124.0,trough
```
`D14 Hotel_occ_total.csv` (raw; note duplicated "Remark" header)
```
Year,Quarter,Month,Hotel Establishments,Occupancy rate,Remark,Difference,Remark
2014,,1,Total,80.90,,-2.60,
2014,,2,Total,91.50,,15.30,
2014,,3,Total,88.20,,9.00,
```
`D15 Visitors_Arrival_byArrivalPoint.csv`
```
Year,Quarter,Month,Source Markets,Modes of Transport,Transport,Total,Remark,Total Year of Year Changes,Remark
2014,,1,Total,The Border Gate,By Land,1288072,,9.400000000000000,
2014,,2,Total,The Border Gate,By Land,1196015,,8.800000000000000,
2014,,3,Total,The Border Gate,By Land,1278567,,12.500000000000000,
```
`D16 Visitors_Arrival_byOnday_Overnight_CN.csv`
```
Year,Quarter,Month,Source Markets,SameDay,Remark,SameDay Year of Year Changes,Remark,OverNight,Remark,OverNight Year of Year Changes,Remark
2014,,1,Chinese mainland,925306,,21.10,,763971,,7.60,
2014,,2,Chinese mainland,922031,,13.40,,792745,,14.00,
2014,,3,Chinese mainland,938530,,26.50,,830878,,20.50,
```
`D18 bus_monthly_2020_2026.csv`
```
month,year,month_no,days_in_month,daily_avg_trips_wan,daily_avg_trips,monthly_trips_est,buses_in_service,bus_stops,trips_per_bus_per_day,visitor_arrivals,same_day_arrivals,trips_per_arrival,dsat_minfu_daily_wan,dsat_tcm_daily_wan,source
2020-01,2020,1,31,55.38,553800,17167800,910,415,608.6,2850465,1530832,6.023,,,DSAT quarterly statistics PDF 2020Q4
2020-02,2020,2,29,21.16,211600,6136400,910,415,232.5,156394,81090,39.237,,,DSAT quarterly statistics PDF 2020Q4
2020-03,2020,3,31,31.67,316700,9817700,910,416,348.0,212311,86415,46.242,,,DSAT quarterly statistics PDF 2020Q4
```
`D20 supply_stops.csv`
```
code,nameCht,namePor,parentCode,lat,lng,zone,stop_code,n_routes,n_route_dir,n_records,nn_dist_m
M1_2,關閘總站,PORTAS DO CERCO / TERMINAL,M1,22.215002,113.549331,Macau Peninsula,M1_2,1,2,2,8.684770946514938
M1_4,關閘總站,PORTAS DO CERCO / TERMINAL,M1,22.215016,113.549248,Macau Peninsula,M1_4,1,1,1,8.684770946514938
M1_5,關閘總站,PORTAS DO CERCO / TERMINAL,M1,22.215159,113.54923,Macau Peninsula,M1_5,1,2,2,16.008472519880147
```
`D21 stop_district_assignment.csv`
```
stop_code,district_cn,weekdays,weekends
C650_1,路氹填海區,191.77142857142852,184.53910533910533
C651_1,路氹填海區,191.77142857142852,184.53910533910533
C652_1,路環區,488.67636749215694,437.6433854468799
```

### 2.2 Missing / odd values, units, language

- **Units.** `bus_daily_avg_trips_wan` and `daily_avg_trips_wan` = 10 000 trips/day (the `wan` suffix is the only hint; not documented in `data_dictionary.md`). `headcount` in D4/D5/D6 = visitor head-count **averaged over the month for that hour slot** (`phase1_usability_verdict.csv`: "monthly averages per hour slot, so intra-month events are smoothed"). `*_share_pct` = share of daily/city total; `hits_per_km2_month` = head-count per km² per month; `weekdays`/`weekends` in D21 = scheduled departures, not ridership.
- **Missing values.** D1 `buses_in_service` is empty for exactly 2026-04…2026-09 (6 cells), consistent with draft §3.4 "buses in service to Mar 2026". D3 `arrivals_yoy_pct` empty for the first 12 months (2008, no prior year). D11 `hotel_occ_yoy_pp` empty for 2023 (no 2022 base). D6 has no nulls. `qa_report.csv`: 0 duplicate months, 0 missing months, 0 negative head-count, `hotel series completeness 45/45`, `bus series completeness 45/45`, `arrivals outliers |z|>3 = 0`.
- **Odd values / caveats.** `qa_report.csv` records `district headcount share of arrivals (2025) = 99.9 %` and itself warns "hour-level indicator is a sample of total arrivals, not the total" — the district panel and the DSEC arrival total are two different measurement systems and must not be presented as one population. D10 2025 `total_headcount` 40,045,669 vs `arrivals_sum` 40,069,360 (Δ = 23,691) — not equal, unexplained. D7 `demand_share_pct` for Coloane is 1.67 % while `README.md` and the draft quote 1.7 %; Taipa & Cotai `departures_share_pct` 28.68 in the file vs 28.7 in the draft (rounding only, but the report must pick one).
- **Internal contradiction.** `data_processed\phase1_usability_verdict.csv` labels MGTO district × hour as "(43 months)" while `qa_report.csv`, `dataset_inventory.csv` and D4 all say 45 months / 2023-01…2026-09. One of the two statements is stale.
- **Column-name language.** Derived tables are English `snake_case` except `district_cn` / `nameCht` (Chinese) and `district_en` / `namePor` (Latin). Raw `Dataset\*.csv` are English headers copied from DSEC but carry structural defects: duplicated `Remark` columns (two columns with the same name), `Quarter` always blank, `Month` as a bare integer with no year tie-in, numeric noise such as `9.400000000000000`, and source-market series with different start dates (CN/HK/TW from 2014, KR only from 2023-01) so any 2014–2022 market mix chart is impossible for KR.
- **Date coverage mismatch.** Draft §3.3 says occupancy covers "45 months Jan 2023–Sep 2026" while §5 success criteria demand "36 monthly / 12 quarterly rows"; the delivered panels are 45 months / 15 quarters. This is a documentation conflict, not a data error (README explains the extension).

---

## 3. Notebooks

All four notebooks were read statically (JSON cell scan). None was executed. Cell indices below are 0-based positions in the notebook's `cells` array.

### 3.1 `notebooks\cisc7204_pipeline_M3_vivi.ipynb` (81 cells, 40 code cells, **40 with stored outputs**)

- Kernel metadata: Python 3.12.3, kernel `python3` (no display name recorded).
- Section headings (markdown): 0 environment/paths · 1 raw data inventory & availability · 2 DSEC arrivals cleaning · 3 MGTO district×hour cleaning (3.1 year-to-date de-duplication, 3.2 panel vs 2026 snapshot) · 4 golden-week daily arrivals · 5 supply side: stops/routes/timetable (5.1 stop coordinates & macro-zone, 5.2 per-hour service from 920 timetable windows, 5.3 official supply series) · 6 monthly/quarterly panel integration & QA · 7 zone-level supply–demand match · 8 hour match · 9 gateway match · 10 Grand Prix / MOPubBus event view · 11 annual alignment · 12 charts (15) · 13 export of analysis dataset / SQLite / manifest · 14 period analysis (monthly, quarterly, annual, 14.4 optional blocks, 14.5 three-layer consistency) · 15 spatial layer, 24 statistical districts, fig 14 · 16 "what this run establishes" · 17 duplicates.
- Imports: `IPython.display`, `bokeh.*`, `glob`, `io`, `json`, `math`, `matplotlib.*`, `numpy`, `os`, `pandas`, `re`, `sqlite3`, `textwrap`, `warnings`, `zipfile`.
- Inputs: `data\mgtodataplus\*.xlsx`, `data\dsec_timeseries\*.json`, `data\github_macau-bus-data\{routes,stops}.json` + `route-schedule\*`, `Dataset\DSEC_hotel_guests_rooms_*.csv`, `Dataset\Hotel_occ_total.csv`, `Monthly_Bus_Database\bus_monthly_2020_2026.csv`, plus already-built `data_processed\*.csv`.
- Ordered cleaning/merging steps (as coded): (1) read and inventory every raw file; (2) DSEC arrivals: strip thousands separators/footnotes, `to_datetime`, monthly index 2008-01…2026-09, add same-day share; (3) MGTO: 45 year-to-date XLSX files de-duplicated to one file per year, district names mapped CN→EN and to three macro-zones, 24 districts × 24 hours asserted as a 576-cell balanced grid per month (45×576 = 25,920); (4) golden-week daily extraction (Chinese New Year / 1 Oct weeks); (5) supply: stop coordinates cleaned, stops assigned to macro-zone, headway ranges converted to departures per hour at the **midpoint**, stop→district assignment by distance; (6) monthly panel assembly + QA report (row/duplicate/missing assertions); (7) zone and hour share matching; (8) annual alignment against official totals; (9) export CSV + SQLite + manifest; (10) period roll-ups.
- Charts (file → title → type → x/y → aggregation → axis/colour notes):
  - `fig1_general_trend.png` "Arrivals per month, 2015-2026" · line · x = date (`YearLocator`, `%Y`), y = arrivals ÷ 10⁶ · monthly total, no aggregation · `ylim(0, 5.2)` (zero baseline), blue solid = non-pandemic, red dashed = pandemic years, grey band 2020-01…2022-12 α 0.18, orange band 2023-01…2025-12 α 0.16, legend lower right.
  - `fig2_zone_mismatch.png` "Where visitors are, and where the buses are" · grouped bars · x = 3 zones, y = share of city total (%) · three series `demand_share_pct`, `departures_share_pct`, `stops_share_pct` (blue/orange/purple), bar labels, `ylim(0, 78)` (non-zero baseline is fine; three different denominators are not).
  - `fig3_hourly_profile.png` "Hourly demand and supply profiles" · 3 lines + `fill_between` · x = hour 0–23, y = share of daily total (%) · demand (red), weekday supply (green), weekend supply (sky, dashed) · purple band 21.5–23.5 h, annotation "Evening demand with almost no service", `xlim(-0.5, 23.5)`, x ticks every 2 h.
  - `fig4_correlation.png` · two panels · (a) "Monthly, n = 36" scatter + OLS line, x = arrivals ÷ 10⁶, y = bus trips ÷ 10⁶, r printed in-panel; (b) "Quarterly, n = 12 quarters" bars, y = `bus_trips_per_visitor`, `ylim(0, 14.2)`, annotation "ridership per visitor falls by roughly 40 %".
  - `fig5_district_hour_heatmap.png` "Ten busiest districts by hour, 2023-2025" · `imshow` heat-map · x = hour, y = district (wrapped labels), colour = share (%).
  - `fig6_workplan.png` "Delivery plan on the four-week timeline" · horizontal bar / Gantt · x = weeks W1–W4, y = task, bar colour = owner, `Patch` legend.
  - `fig7_monthly_dashboard.png` (2×2 panels (a) arrivals M, (b) bus trips per visitor, (c) occupancy %, (d) district-hour head-count per arrival), `fig8_seasonality.png`, `fig9_quarterly_evolution.png`, `fig10_annual_alignment.png`, `fig11_zone_month_share.png`, `fig12_optional_blocks.png`, `fig13_2026_shift.png`, `fig14_district_choropleth.png` (choropleth over 24 districts).
- Outputs saved in notebook: yes, all 40 code cells carry stored outputs (no "not executed" state found). Files written: 23 CSVs into `data_processed\` (`analysis_dataset_master.csv`, `dataset_inventory.csv`, `demand_district_hour_2026.csv`, `demand_district_hour_panel_2023_2026.csv`, `demand_goldenweek_daily.csv`, `demand_monthly_arrivals.csv`, `match_annual_alignment.csv`, `match_event_crowding.csv`, `match_event_segment_crowding.csv`, `match_gateways.csv`, `match_hourly_profile.csv`, `match_zone_supply_demand.csv`, `mgto_district_hour_master_2023_01_2026_09.csv`, `monthly_panel_2023_01_2026_09.csv`, `output_manifest.csv`, `qa_report.csv`, `quarterly_panel_2023Q1_2026Q3.csv`, `supply_departures_route_hour.csv`, `supply_official_series.csv`, `supply_routes.csv`, `supply_shuttle_quarterly.csv`, `supply_stop_departures.csv`, `supply_stops.csv`), `data_processed\macau_visitor_transport.sqlite`, and figures into `figures\`.
- Hard-coded absolute paths: **none in this notebook** — paths are derived from the current working directory (if the directory basename is `notebooks`, its parent; otherwise cwd), which makes it the most portable notebook.
- Key printed numbers (with cell index): cell 28 hourly Pearson r demand vs supply **weekday 0.524 / weekend 0.548**; cell 34 annual bus trips vs annual arrivals **r = 0.952**; cell 79 "Headline findings": 2025 arrivals **40,069,360**, 2026 Jan–Sep **32,181,272** (9 months), Taipa & Cotai **56.10 %** of district-hour head-count vs Peninsula **42.23 %**, lowest zone supply/demand ratio **0.511** (Taipa & Cotai), one 6.05 km² district holds **43.96 %** of head-count, cross-district elasticity **0.348**, monthly r(arrivals, bus trips) 2023-01…2025-12 = **0.759 (n = 36)**, trips per visitor down **≈40 %** (r = −0.798 vs time). The same cell states these are associational, not causal.

### 3.2 `notebooks\CISC7204_ClassE_Team01_Visualization_updated.ipynb` (43 cells, 25 code cells, **25 with stored outputs**)

- Kernel metadata: Python 3.12.3, kernel `cisc7204_base`.
- Section headings: 1 environment/paths/palette · 2 data audit gate (structural) · 3 audit gate (unit reconciliation, roll-up identity) · 4 distributional overview (n = 36) · 5 Figure 1 long-run arrivals · 6 RQ1 arrivals/occupancy co-movement · 7 RQ1 numbers · 8 Figure 3 per-visitor bus intensity · 9 H1–H3 correlation / scatter / partial · 10 RQ2 seasonal pattern + 2026 out-of-sample · 11 T8 distribution diagnostics · 12 Figure 10 district-hour demand vs departures 2026 · 13 Figure 11 hourly mismatch weekday/weekend · 14 Figure 12 district×hour heat-map with Chinese labels · 15 supplementary views (market mix / lag / regression) · 16 quality gate (colour-blind, grayscale, export register) · 17 closing checks.
- Imports: `IPython.display`, `PIL`, `dash`, `matplotlib` (+ dates, patches, pyplot, ticker), `numpy`, `os`, `pandas`, `pathlib`, `scipy`, `seaborn`, `statsmodels.api`, `statsmodels.stats.stattools`, `warnings`.
- Inputs: 12 CSVs from `data_processed\` (`analysis_dataset_master.csv`, `demand_district_hour_2026.csv`, `demand_monthly_arrivals.csv`, `district_map_metrics.csv`, `match_hourly_profile.csv`, `match_zone_supply_demand.csv`, `monthly_detail_2023_01_2026_09.csv`, `monthly_panel_2023_01_2026_09.csv`, `monthly_seasonality_index.csv`, `qa_report.csv`, `quarterly_detail_2023Q1_2026Q3.csv`, `quarterly_panel_2023Q1_2026Q3.csv`) + 2 from `Dataset\` (`visitors_2023_2026_by_market_summary.csv`, `visitors_2023_2026_summary.csv`).
- Ordered steps: path resolution by upward search for a folder containing `data_processed` → structural audit gate → unit/roll-up identity gate (`monthly → quarterly` sums) → distributional diagnostics → 16 figures → colour-blind + grayscale export → closing arithmetic checks. No row-level cleaning of raw files happens here; it consumes the pipeline outputs.
- Charts (16 PNG + 16 `_gray` twins written to `notebooks\figures\`), with axis/encoding notes that matter for the report:
  - `fig01_arrivals_longrun.png` (cell 4) "Figure 1. Arrivals collapsed 2020-2022 and only rebuilt by 2025; shaded band = estimation…" · line · `ylim(0, max)` zero-based, reference lines, legend.
  - `fig02_rq1_coupling.png` (cell 5) two-panel: Panel A arrivals vs occupancy **on a twin y-axis (`twinx`)**; Panel B the same series as **z-scores** — Panel B is the honest version, Panel A is the classic dual-axis risk.
  - `fig04_intensity_decline.png` (cell 8 is the correlation matrix) — the intensity decline chart uses `axhline` references.
  - `fig_h1_correlation_matrix.png` (cell 8) "Figure 4. Correlation matrix of the core series, 2023-01 to 2025-12 (n = 36)" · heat-map of Pearson r.
  - `fig05_seasonality_2026.png` (cell 12) Panel A recurring shape with Spearman vs 2023-2025 printed in title; Panel B seasonality index comparison, `fill_between`, reference lines.
  - `fig07_2026_level_vs_base.png` (cell 14) "Figure 8. Each 2026 month relative to the same month in 2023-2025…" · **index chart with the y-axis starting at `min(series) − 100`-style offset, i.e. a deliberately truncated, index-based axis (100 = base)**; acceptable only if the base is labelled on the axis.
  - `fig08_distribution_diagnostics.png` (cell 15) Panel A density, Panel B ECDF (2026 placed in-sample, `ylim 0–1.02`), Panel C QQ plot.
  - `fig02_zone_mismatch.png` (cell 16) Panel A grouped shares, Panel B ratio (`ylim 0–78`, reference line at 1, legend).
  - `fig05b_district_hour_heatmap.png` (cell 18) "Figure 12. When the ten busiest districts are busy: share of the day" · heat-map, Chinese district labels.
  - `fig10_lag_crosscorrelation.png` (cell 20) lags −3…+3 bars with reference line, `ylim 0–1.02`.
  - `fig11_regression_diagnostics.png` (cell 21) residuals vs fitted, QQ.
  - `fig12_dashboard_preview.png` (cell 22) "Panel 1 — arrivals (left) and occupancy (right)…" **three panels, two of them with `twinx` (two y-axes) inside one screenshot** — a preview image, not a report figure.
  - Also `fig06_quarter_profile.png`, `fig09_market_waffle.png`.
- Outputs saved in notebook: yes (25/25 code cells have outputs). Files written: 16 PNGs + 16 `_gray.png` into `notebooks\figures\`.
- Hard-coded absolute paths: **none** (`pathlib` + upward search).
- Key printed numbers (cell 20): H1 arrivals~bus trips **r = 0.759, p = 8.23e-08, 95 % CI [0.51, 0.87]**; H2 arrivals~occupancy **r = 0.913, p = 7.81e-15, CI [0.83, 0.96]**; overnight~occupancy **0.861 (p = 1.55e-11)** vs same-day~occupancy **0.891 (p = 3.18e-13)**; overnight~hotel guests **0.921** vs same-day **0.694**; occupancy~bus raw **0.741**, **partial | arrivals r = 0.179, p = 2.96e-01**; per-year sensitivity H2/H1: 2023 0.904/0.818, 2024 0.744/0.254, 2025 0.814/0.625, 2023-2025 0.913/0.759.

### 3.3 `notebooks\CISC7204_ClassE_Team01_Visualization_lucas_pending test.ipynb` (43 cells, 25 code cells, **25 with outputs**)

- Python 3.14.6, kernel `cisc7204_base`.
- Same 17-section skeleton, same imports, same 14 input CSVs, same 16 output figures as §3.2 — it is a near-duplicate variant of the `_updated` notebook (file name says "pending test").
- Differences that matter: figure captions are numbered differently (`Figure H1. Correlation matrix…`, `Figure 3. Demand peaks…`, `Figure 5. When each district is busy…`, `Figure 7…`), whereas `_updated` calls the same charts Figure 4 / 11 / 12 / 5. Two numbering schemes for the same charts → the report's "Figure N" references can silently point to different charts.
- Hard-coded absolute paths: none. Key printed numbers (cell 20): "Occupancy ~ bus trips: r = 0.741 (raw)", "Occupancy ~ bus trips | arrivals: r = 0.179 (partial, p = 2.96e-01)", conclusion text "the occupancy-ridership link is largely explained by demand scale".
- Which of the two is authoritative: **UNKNOWN** from the repository (`notebooks\Cross_check_and_pending_revisions.md` names `_updated` as the cross-checked version, so `_updated` is the better candidate).

### 3.4 `notebooks\cisc7204_proposal_figures_colour.ipynb` (15 cells)

- Python 3.14.6, kernel `python3`. Title: "CISC7204 Class E Team 01 - Proposal figures (colour version)".
- Imports: `os`, `numpy`, `pandas`, `matplotlib` (+ dates, pyplot), `Patch`, `LinearSegmentedColormap`; `matplotlib.use("Agg")`, DejaVu Sans, figure/save dpi 200, Okabe-Ito palette.
- Inputs: `data_processed\monthly_panel_2023_01_2026_09.csv`, `demand_monthly_arrivals.csv`, `quarterly_panel_2023Q1_2026Q3.csv`, `match_zone_supply_demand.csv`, `match_hourly_profile.csv`, `demand_district_hour_panel_2023_2026.csv`.
- Charts: fig1 general trend, fig2 zone mismatch, fig3 hourly profile, fig4 correlation (2 panels), fig5 district-hour heat-map, fig6 workplan — the six images embedded in the draft report (§7.9).
- Hard-coded absolute paths: **yes, breaks on any copy** — `REPO = r"C:\Users\07viv\Desktop\CISC7204-Team01"`, `D = REPO\data_processed`, `OUT = REPO\figures`.
- Window constants `WIN_START = "2023-01-01"`, `WIN_END = "2025-12-01"` — the 36-month core window is hard-coded here, while the exported panel runs to 2026-09.

---

## 4. Dashboard

| Item | Finding | Evidence |
|---|---|---|
| Technology | Two artefacts: (a) one **self-contained static HTML** with inlined `plotly.min.js`; (b) a **Dash** port that rebuilds the same page from pre-baked JSON | `Dashboard\build_dashboard.py` docstring; `Dashboard\app.py` docstring |
| Entry files | `Dashboard\CISC7204_ClassE_Team01_Dashboard.html` (open directly), `Dashboard\app.py` (Dash server), `Dashboard\build_dashboard.py` (regenerates the HTML) | files exist |
| Launch command found | `python app.py  # http://127.0.0.1:8050`, and `app.run(debug=False, host="127.0.0.1", port=8050)`; README gives `& "C:\Users\07viv\anaconda3\python.exe" app.py`; builder docstring gives `C:\Users\lenovo\anaconda3\python.exe build_dashboard.py`; `README_Dashboard.md` gives `python build_dashboard.py` | `app.py`, `README.md`, `build_dashboard.py`, `README_Dashboard.md` |
| Required libs/versions | `dash`, `plotly`, `pandas`, `numpy`; README states dash 4.4.1, plotly 5.22.0, pandas 2.2.2, numpy 1.26.4 on Windows 11 / Python 3.12.3. No `requirements.txt` anywhere | `README.md` dashboard section |
| Pages/tabs | Single page, no `dcc.Tab`; layout is a 1:1 port of the static page: 16 Plotly figures + 6 KPI cards | `app.py` (1 `dcc.Graph`, 5 callbacks) |
| Filters/controls | Year (`selYear`), Zone (`selZone`), District (`selDistrict`), map metric (Head-count share / Head-count per km² per month / 2026 share shift / Head-count per departure), Auto-cycle (`btnPlay`), Reset (`btnReset`). **No hour slider** — although the draft promises one | `build_dashboard.py` control ids; draft §4 T9 |
| Charts | 16: long-run arrivals, monthly, quarterly, zone, departures, hourly, district map, heat-map, seasonality, 2026 zone shift, 2026 hour shift, golden week, hotel occupancy history, hotel occupancy vs intensity, guests by star, arrivals-vs-occupancy | `build_dashboard.py` ids `f_long f_month f_quarter f_zone f_dep f_hour f_map f_heat f_season f_shift_zone f_shift_hour f_golden f_hhist f_hrel f_hstar …` |
| Datasets read | `build_dashboard.py` reads **15 CSVs** from `Dashboard\data\` (`annual_alignment_2018_2026`, `demand_district_hour_panel_2023_2026`, `demand_goldenweek_daily`, `demand_monthly_arrivals`, `district_map_metrics`, `hotel_guests_by_star_2023_2026`, `hotel_occ_history_2014_2025`, `hotel_occ_monthly_2023_2026`, `match_hourly_profile`, `match_zone_supply_demand`, `monthly_panel_2023_01_2026_09`, `monthly_seasonality_index`, `optional_2026_hour_shift`, `optional_2026_zone_shift`, `quarterly_panel_2023Q1_2026Q3`); `app.py` reads only `data\dash\payload.json`, `figures.json`, `body_template.html` (no CSV at runtime) | both files |
| Runnable here? (static judgement, nothing executed) | **HTML: yes** — no server, no network, no Python (plotly.js inlined, 4.62 MB). **Dash app: no, not on this machine** — the agent interpreter is Python 3.11.8 with **no** `pandas / numpy / matplotlib / plotly / dash / scipy / statsmodels` installed, and no dependency file exists to install them from; also `dash 4.4.1` would have to be pinned manually | `python -c import …` probe; `app.py` imports |

---

## 5. Existing images / screenshots

| Path | What it shows | Likely source | Size / resolution | Usable in report |
|---|---|---|---|---|
| `figures\fig1_general_trend.png` | arrivals 2015–2026 with pandemic band | pipeline §12 | 1570×676, 118 KB | yes (already in draft) |
| `figures\fig2_zone_mismatch.png` | zone demand vs departures vs stops shares | pipeline §12 | 1242×614, 63 KB | yes (in draft) |
| `figures\fig3_hourly_profile.png` | hourly demand vs weekday/weekend supply | pipeline §12 | 1288×665, 111 KB | yes (in draft) |
| `figures\fig4_correlation.png` | monthly scatter + quarterly trips-per-visitor | pipeline §12 | 1905×625, 122 KB | yes (in draft) |
| `figures\fig5_district_hour_heatmap.png` | 10 busiest districts × hour | pipeline §12 | 1623×834, 99 KB | yes (in draft) |
| `figures\fig6_workplan.png` | 4-week Gantt of deliverables | pipeline §12 | 2113×654, 110 KB | **questionable** — a plan chart inside a results report |
| `figures\fig7…fig13` | monthly dashboard panels, seasonality, quarterly evolution, annual alignment, zone-month share, optional blocks, 2026 shift | pipeline §12 | 1865–1983 × 586–1186 | yes, candidates |
| `figures\fig14_district_choropleth.png` | 24-district choropleth | pipeline §15 | 2724×995, 382 KB | yes, candidate |
| `figures\archive\legacy_fig1…png`, `legacy_fig2…png` | superseded versions | older runs | not measured | no (archive) |
| `notebooks\figures\fig01…fig12 + fig_h1/_h2` (16) | newer 200-dpi versions of 16 charts, each with a `_gray.png` twin | Visualization_updated / lucas | 1792–2672 × 788–1673 | **yes — higher quality than the figures embedded in the draft, and colour-blind checked** |
| `Dashboard\preview\00_full_page.png` | whole dashboard page | app / static HTML | 1600×3893, 611 KB | yes (method screenshot) |
| `Dashboard\preview\00_full_page_compact.png` | compact whole page | static HTML | 1600×4228, **1.6 MB** | yes but large |
| `Dashboard\preview\01_filtered_year2024_taipa.png` | filtered state (2024, Taipa) | static HTML | 1600×3896, 600 KB | yes (proves filters work) |
| `Dashboard\preview\dash_play_state.png`, `dash_preview.png`, `html_reference.png` | Dash vs static comparison | app.py | 1600×5104–5109, ≈0.8 MB each | one is enough |
| `Dashboard\preview\hotel_03…06*.png` | hotel section close-ups | dashboard | 1005–1403 × 713–726 | optional |
| `Dashboard\preview\figs\` (16) | per-figure crops incl. filtered pairs | dashboard | 639–1560 × 212–567 | optional |
| `cisc7204-Class_E-Team_01_Photos\…GroupPhotos.jpg` | team photo | camera | 5.65 MB | no (not evidence) |
| `Proposal\Project report\…FinalReport.docx` `word/media\image1.png` | 381×359 raster, no matching file in repo | UNKNOWN (likely institutional mark) | 381×359, 77 KB | UNKNOWN |

---

## 6. Environment

- **No dependency declaration exists**: no `requirements.txt`, `environment.yml`, `pyproject.toml`, `setup.py`, `Pipfile` in the repository (verified by full file listing).
- Python / kernels actually recorded in notebook metadata: `cisc7204_pipeline_M3_vivi.ipynb` → 3.12.3 (`python3`); `…Visualization_updated.ipynb` → 3.12.3 (`cisc7204_base`); `…Visualization_lucas_pending test.ipynb` → 3.14.6 (`cisc7204_base`); `cisc7204_proposal_figures_colour.ipynb` → 3.14.6 (`python3`).
- README instructions: `python scripts/build_panels.py`; "Requirements: Python 3.11 or newer" plus `pandas`, `numpy`, `matplotlib`, `seaborn`; dashboard section adds dash 4.4.1 / plotly 5.22.0 / pandas 2.2.2 / numpy 1.26.4 and the hard-coded interpreter `C:\Users\07viv\anaconda3\python.exe`.
- Version claims in the draft (§4) — "Python 3.11, pandas 3.1, Matplotlib 3.11" — are **not supported** by anything in the folder (notebook metadata says 3.12.3 / 3.14.6; README says pandas 2.2.2). Treat as UNKNOWN/incorrect until the team confirms.
- This machine (agent interpreter): Python 3.11.8; `pandas`, `numpy`, `matplotlib`, `plotly`, `dash`, `seaborn`, `scipy`, `statsmodels`, `openpyxl`, `PIL` all **missing** → nothing Python-based in this repo can be re-run here without installing a stack.

---

## 7. Draft report analysis — `Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx`

### 7.1 Meta
- `docProps\app.xml`: **Pages = 14**, Words = 4,580, Characters = 26,109, Paragraphs = 61, Application = Microsoft Office Word, TotalTime = 25 min. Body word count measured from `document.xml` ≈ 4,077.
- Tables = 12, inline drawings = **7** (`word/media\image1…image4, image6…image8`; `image5` absent).
- Cover page: **present**. Table of contents: **absent** (`TOC field present: False`).

### 7.2 Heading structure (levels as styled, not as intended)

| Section | Words | Paras | Tables | Level in file |
|---|---|---|---|---|
| Cover | 48 | 16 | 1 | none |
| 1. Project Title and Research Question | 694 | 21 | 0 | one level (`pStyle=1`), sub-titles are bold runs |
| 2. Project Purpose | 176 | 15 | 0 | same |
| 3. Data Context | 837 | 24 | 3 | same |
| 4. Project Tasks and Deliverables | 1,333 | 36 | 3 | same |
| 5. Success Criteria | 188 | 8 | 1 | same |
| 6. Team Collaboration | 141 | 13 | 2 | same |
| 7. Timeline | 225 | 8 | 2 | same |
| GenAI Use Statement | 132 | 1 | 0 | same |
| References | 274 | 15 | 0 | same |
| **Total** | **≈4,048** | | **12** | |

- Only one real heading level exists: `styles.xml` defines **no Heading 1/2/3**; the nine section titles share a single custom style object (`style=1`, 10.5 pt Times New Roman bold). Consequence: no navigation pane, no automatic TOC, and "3.1 / 3.2 …" sub-titles are indistinguishable from body text at the XML level. For a 50-page final report this must be rebuilt.

### 7.3 Typography observed
- Times New Roman throughout; cover: 18 pt (36 half-points) for University / Faculty / Course lines, 14 pt for "Team Project Proposal", 20 pt for the project title, 10.5 pt for group name and body; body list style `a0` (57 paragraphs), plain body 100 paragraphs with no style.

### 7.4 Team members and roles (exactly as written; IDs marked "present")
| Name | Roles written in §6 | Data-module duty written in §6 |
|---|---|---|
| SONG ZHUOXI | Team Coordinator; Project Tracker (with KONG KIN MENG); Project Analyst | M1 Visitor arrivals — support |
| KONG KIN MENG | Project Tracker; Project Analyst; Project Developer | M1 Visitor arrivals — lead; master-dataset validation |
| FONG HIO LAM | Scribe; Project Developer; Liaison support | M3 Bus ridership — support |
| XIAN QILAN | Liaison; Project Analyst; Scribe support | M2 Hotel occupancy — support; Interpretation — lead |
| FONG CHIN WAI | Project Analyst; Project Developer; Quality Reviewer support | M3 Bus ridership — lead; master dataset pipeline; dashboard; Section G owner |
| KUAN CHI KIT | Project Analyst; Quality Reviewer | M2 Hotel occupancy — lead; relationship analysis; Team Reporter |

Student IDs: **present** in the cover table (not reproduced here). No e-mail addresses are printed in this inventory.

### 7.5 Goals, schedule, tasks, division of work (summary)
- **Question.** RQ1 — do monthly visitor arrivals, hotel occupancy and bus ridership move together in 2023–2025 (§1); RQ2 — how do the four seasons differ (§1). Hypotheses H1 arrivals↔bus positive, H2 arrivals↔occupancy positive and stronger for overnight visitors, H3 occupancy↔bus still related after controlling arrivals.
- **Data plan (§3).** 3.1 arrivals by source market (raw), 3.2 same-day/overnight (cleaned 2008-01…2026-08), 3.3 occupancy (45 months 2023-01…2026-09), 3.4 bus ridership (45 months, daily trips to 2026-09, buses in service to 2026-03), 3.5 optional room supply, 3.6 MGTO district×hour (25,920 rows, 24 districts × 24 h × 45 months), 3.7 DSAT GTFS stop-level departures (586 stop records).
- **Tasks T1–T10 (§4).** T1 cleaning; T2 master monthly dataset; T3 EDA; T4 Figure 1 long-run context; T5 RQ1 twin-axis; T6 H1–H3 correlation; T7 RQ2 seasonality; T8 overnight/same-day distributions; T9 Plotly Dash dashboard; T10 report, slides, review.
- **Schedule (§7).** Four weeks, 5 Nov → 3 Dec 2026; W1 cleaning M1/M2/M3, W2 merge + EDA + annual context, W3 twin-axis/heat-map/Pearson/partial/box/KDE/dashboard, W4 report + rehearsal + QC; meetings 9/16/23/30 Nov and 3 Dec; the course deadline (5 Dec 2026, 23:00) is treated as a 2-day buffer.
- **Division of work.** By module lead/support (§7.4 table) plus section ownership (Section G = FONG CHIN WAI, Section I = XIAN QILAN).
- **Stated figures in the draft that match the files**: 2023Q1 4.95 M arrivals / 74.9 % / 549 k trips per day / 9.96 trips per visitor — matches `quarterly_panel_2023Q1_2026Q3.csv`; Taipa & Cotai 56.1 % head-count vs 28.7 % departures, ratio 0.51 — matches `match_zone_supply_demand.csv` (28.68 → 28.7); Peninsula 66.4 % / 42.2 % / 1.57; Coloane ratio 2.94 with 1.7 %; 00:00–05:59 = 20.2 % of demand vs 3.6 % of weekday departures — matches `match_hourly_profile.csv` (3.584 %); H1 r = 0.917 (Q) / 0.759 (M), H2 0.913, H3 partial 0.179 (p = 0.296) — matches `Visualization_updated` cell 20.

### 7.6 Claims / deliverables in the draft with NO matching evidence in the folder

| Claim in draft | Evidence status |
|---|---|
| "5 meeting minutes" (§4 deliverable; §7 schedule of 5 meetings) | **only 1** file: `minutes\CISC7204-Class_E-Team_01_1st_Meeting_Minutes(3).pdf` → 4 meetings unrecorded |
| "presentation slides" (§4 deliverable) | no slide deck for the report presentation exists; the only PPTX is `video\…Introductory Video ppt.pptx` (a video deck) → **UNKNOWN** whether it doubles as the deliverable |
| Dashboard "shared time axis, district filter, **hour slider**" (§4 T9) | actual dashboard has Year / Zone / District / map-metric / auto-cycle / reset; **no hour slider** (`app.py`, `build_dashboard.py`) |
| Dashboard "opens from local CSV in 5 s, no network" (§5 acceptance test) | the HTML is self-contained (passes "no network"), but `app.py` reads baked **JSON**, not CSV (`app.py`) |
| "Python 3.11, pandas 3.1, Matplotlib 3.11" (§4) | no dependency file; notebook metadata 3.12.3 / 3.14.6; README says pandas 2.2.2 |
| "36 monthly / 12 quarterly rows" (§5 success criteria) | files contain 45 months / 15 quarters (extension documented in README, not in the criteria) |
| Figure references | the draft embeds `figures\fig1…fig6` (pipeline outputs) and **none** of the 16 newer `notebooks\figures\figNN` charts; the newer notebook numbers the same charts differently (§3.3) |
| "at least 7 APA 7 sources" (§5) | 14 reference entries listed; in-text citation format not verifiable from the text extraction |
| GenAI statement (§GenAI) | states Perplexity was used for drafting and an AI assistant for Figures 1–6 plotting code; consistent with the folder (no contradicting evidence) |

### 7.7 Embedded images in the draft (byte-identical to `figures\`)
| docx media | Resolution | KB | Matching repo file |
|---|---|---|---|
| `image2.png` | 1570×676 | 117 | `figures\fig1_general_trend.png` (118 KB) |
| `image3.png` | 1242×614 | 62 | `figures\fig2_zone_mismatch.png` (63 KB) |
| `image8.png` | 1288×665 | 110 | `figures\fig3_hourly_profile.png` (111 KB) |
| `image4.png` | 1905×625 | 121 | `figures\fig4_correlation.png` (122 KB) — note `fig13_2026_shift.png` has the same pixel size, distinguished by file size |
| `image6.png` | 1623×834 | 98 | `figures\fig5_district_hour_heatmap.png` (99 KB) |
| `image7.png` | 2113×654 | 110 | `figures\fig6_workplan.png` (110 KB) |
| `image1.png` | 381×359 | 77 | no match in repo → **UNKNOWN** |

---

## 8. Git evidence (read-only: `git log`, `git status` only; nothing staged, committed, checked out or reset)

- Branch: `main` (tracked by `origin/main`). Commit count: **19**. Commit date range: **2026-11-04 → 2026-11-24**.
- Contributors by author-name string (names only, no e-mails):

| Author string | Commits | Distinct files touched | Main areas touched |
|---|---|---|---|
| `chin wai fong` | 9 | 492 | `data\` (194, incl. legacy `PreliminaryProject_Pair_*` folder that no longer exists in the working tree), `Monthly_Bus_Database\` (32), `data_processed\` (31), `figures\`, photos |
| `Kong Kin Meng` | 6 | 88 | `notebooks\` (73), `Dataset\` (12), `Proposal\` |
| `Fong Chin Wai` | 2 | 98 | `notebooks\` (36), `data_processed\` (30), `Dashboard\` (13), `figures\`, `Proposal\` |
| `Fong Chin Wai (Vivi)` | 1 | 27 | `data_processed\` |
| `FONG HIO LAM` | 1 | 50 | `Dashboard\` (48, incl. `build_dashboard.py`, the HTML bundle) |

- The three variants `chin wai fong` / `Fong Chin Wai` / `Fong Chin Wai (Vivi)` are the same person under different local git identities → **≈12 commits** combined; `Kong Kin Meng` 6; `FONG HIO LAM` 1. Two of the six named members (SONG ZHUOXI, XIAN QILAN, KUAN CHI KIT) have **no commits at all** under their own names.
- **This evidences commits only, not chart authorship or analysis work.** Contributorship of figures cannot be inferred from history: all six figures were committed inside `figures\` by whoever ran the notebook last, and `build_dashboard.py` (48 files by FONG HIO LAM) is a code commit, not proof of chart design.

---

## 9. Gaps and risks

1. **Reproducibility blocked by my own machine, not the repo**: no `requirements.txt`/`environment.yml`; four notebooks declare three different Python versions (3.12.3, 3.14.6) and two kernels; the local interpreter has none of the libraries. The final report's "every number reproducible" criterion is currently untestable.
2. **Hard-coded absolute paths** — `notebooks\cisc7204_proposal_figures_colour.ipynb` (`REPO = r"C:\Users\07viv\Desktop\CISC7204-Team01"`, plus `D` and `OUT` derived from it) is the notebook that produced the six report figures; on any other machine it fails immediately. Also `Dashboard\build_dashboard.py` docstring (`C:\Users\lenovo\anaconda3\python.exe`) and `README.md` (`C:\Users\07viv\anaconda3\python.exe`). The other three notebooks are path-portable.
3. **Missing generation scripts**: `README.md` itself states that `demand_district_hour_panel_2023_2026.csv` and similar exploratory outputs "were produced by exploratory steps and not saved as scripts, need to be rebuilt by hand". `scripts\` contains only 3 builders (`build_panels.py`, `build_period_analysis.py`, `build_district_map.py`); the 45-file MGTO parse and the GTFS headway→departures conversion exist only inside the notebook.
4. **Report/draft inconsistencies** (all must be fixed before writing): §3.3 "45 months" vs §5 "36 monthly / 12 quarterly rows"; dashboard "hour slider" vs no slider; "Python 3.11 / pandas 3.1 / Matplotlib 3.11" vs actual metadata; five minutes promised, one delivered; "local CSV in 5 s" vs JSON-driven app.
5. **Figure numbering collision**: the draft's Figure 1–6 = `figures\fig1…fig6`; `Visualization_updated` labels its own charts Figure 1/4/8/12; `…lucas_pending test` labels the same charts Figure 3/5/7/H1. Any "see Figure N" sentence in the final report is ambiguous until a single numbering is fixed.
6. **Chart honesty / design issues, per chart**:
   - `fig02_rq1_coupling.png` (Panel A, `twinx`) and `fig12_dashboard_preview.png` (Panels 1 and 3, `twinx`): **dual axes** — two different units on one frame invite spurious co-movement readings; Panel B (z-scores) is the defensible version. If a dual-axis chart enters the report, it must carry explicit axis-unit labels and a caveat.
   - `fig07_2026_level_vs_base.png`: **truncated, index-based y-axis** (base = 100, axis starts near the series minimum) — bars/points exaggerate small deviations; needs a stated "index, 2023–2025 = 100" axis label.
   - `figures\fig2_zone_mismatch.png` and `fig02_zone_mismatch.png`: three **different denominators** (head-count share, departure share, stop share) plotted as one "%" axis — the legend says what each series is, but the axis unit conflates them.
   - `figures\fig3_hourly_profile.png`: weekday vs weekend supply distinguished by colour (green vs sky) plus dash; acceptable, but the "share of daily total" unit is not in the axis label beyond "%".
   - `figures\fig1_general_trend.png`: three emphasis devices stacked (colour, dash, two shaded bands) — band semantics are only in the title, and the 2023–2025 orange band is easy to misread as a data range.
   - `figures\fig6_workplan.png`: a **project plan Gantt** embedded in a results report; it is not evidence for any research question.
   - `figures\fig4_correlation.png`: panel (b) bars of `bus_trips_per_visitor` with an r-trend annotation, but the "roughly 40 %" text is hard-coded prose in the plot, not computed from the axis — verify before reuse.
   - Missing/uncertain across all charts: units on `bus_daily_avg_trips_wan` ("10 000 trips per day"), the Coloane 1.67 % vs 1.7 % rounding, and the absence of a data-source line on any figure (the draft's own success criterion requires "source" on every figure).
7. **Duplicate-looking files that could diverge**: `Proposal\CISC7204_ClassE_Team01_Proposal.docx` vs `Proposal\Project report\…FinalReport.docx` (identical byte size — probably the same document under two names, so "which one is the proposal and which the final report" is unresolved); `demand_district_hour_panel_2023_2026.csv` vs `mgto_district_hour_master_2023_01_2026_09.csv`; 19 mirrored files in `Dashboard\data\`.
8. **Data-level risks**: district head-count is a sample (~99.9 % of arrivals, per `qa_report.csv`), so district and total-arrival statements must not be mixed; bus ridership includes residents (draft §1 limitation, correct); 2026 is a 9-month, single-snapshot comparison; occupancy 2023 `yoy` and `buses_in_service` 2026-04…09 are blank; KR market only from 2023.
9. **Draft is 14 pages / 4,580 words** against a 50-page allowance — the analysis exists (16 notebook figures, 24 districts, partial correlations) but is not yet in the report; the report also lacks a TOC and real heading styles.
10. **Legacy material in the repo** (other pairs' proposals `Assgn02-Pair06/08/10`, `PreliminaryProject_Pair_*` in git history only, `Data cleaning\` empty folder) — a reviewer opening the repo sees other teams' files; nothing here belongs to Team 01's deliverables.

---

## 10. Questions that need your answer before writing starts

1. Which document is the **proposal** and which is the **final report**? `Proposal\CISC7204_ClassE_Team01_Proposal.docx` and `Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx` have identical byte sizes — should the final report be written from the FinalReport.docx as the base?
2. Which notebook is authoritative for figures — `…Visualization_updated.ipynb` (Python 3.12.3) or `…Visualization_lucas_pending test.ipynb` (3.14.6, "pending test")? They produce the same 16 charts with different figure numbers.
3. Should the final report use the **newer 16 charts** in `notebooks\figures\` (200 dpi, grayscale-checked) or the six older `figures\fig1…fig6` already embedded in the draft?
4. What is the **single figure numbering** to adopt (draft order vs notebook order)? I will renumber captions and in-text references to one scheme only.
5. Success criteria say "36 monthly / 12 quarterly rows", but the delivered panels have **45 months / 15 quarters**. Should the report analyse 2023-01…2025-12 only (H1–H3 are computed on n = 36) and treat 2026 strictly as out-of-sample context?
6. Is 2026 (Jan–Sep, 9 months) allowed in the report at all, and if so must every 2026 chart be labelled "9 months, single snapshot"?
7. Do you want the district-level analysis (24 districts, ~99.9 % sample of arrivals) presented as a **separate section** from the city-level correlation analysis, given they are different measurement systems?
8. Can I state "bus ridership includes Macao residents" and "district head-count is a sample" as limitations in the report's own words (they are in the draft/QA file), or do you prefer different wording?
9. What are the exact **Python / pandas / matplotlib versions** you want declared? The draft says Python 3.11 / pandas 3.1 / Matplotlib 3.11; metadata says 3.12.3 / 3.14.6; README says pandas 2.2.2.
10. Do the promised **5 meeting minutes** and the **presentation slides** exist outside this folder? If not, should the report drop those deliverables or soften them?
11. Should the dashboard section describe the **static HTML** (runnable anywhere) or the **Dash app** (not runnable here), and do you want the "hour slider" claim removed since no slider exists?
12. Which of the three git identities (`chin wai fong`, `Fong Chin Wai`, `Fong Chin Wai (Vivi)`) is the canonical name to use in a contributorship statement, if one is included at all?
13. May I use the grayscale `_gray.png` twins as colour-blind evidence in an appendix, or keep the report colour-only?
14. The `data.gov.mo` / DSEC / DSAT / MGTO downloads are dated 2026-11-04 in `README.md`; is that the citation access date to use in APA 7 references?
15. Any figures or claims you already know are wrong and want removed before I start drafting?

---

*End of inventory. No file outside `Proposal\Project report\_temp\` was created, modified or deleted; `_temp\` is retained.*
*（内容由AI生成，仅供参考）*
