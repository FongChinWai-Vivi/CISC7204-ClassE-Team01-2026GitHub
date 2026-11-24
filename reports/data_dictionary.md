
# Data Dictionary — M1 Visitor Arrivals · M2 Hotel Occupancy · M3 Bus Ridership

**Project:** CISC7204 Data Science and Data Visualisation — Class E, Team 01
**Project title:** Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership
**Document version:** 1.0 (2026-11-22)
**Scope:** every analysed dataset produced by modules M1, M2 and M3 and by the joint integration track, as currently stored in this repository 
**Access date of all raw downloads:** 2026-11-04 (see §2); DSEC indicator snapshots carry a last-update stamp of 2026-09-18
**Status of this file:** new. Before this version, field-level definitions existed only as fragments: `Monthly_Bus_Database/README.md` (bus monthly fields), the docstrings of `scripts/build_panels.py` and `scripts/build_district_map.py`, and narrative notes in `reports/data_coverage_audit_2026-11-04.md`. No standalone data dictionary was committed, although the Proposal, README §9 and the Work Plan all promise “data acquisition & cleaning, data dictionary” for each module. This document consolidates those fragments against the actual files; **no field was invented** — every row below was checked against the stored file (column list, dtype, non-null count, observed range) and against the script or README text that produces it.

---

## 1. Module status check (is M1/M2/M3 actually done?)

| Module | Lead | Cleaning outputs present? | Field definitions found in repo | Verdict |
|---|---|---|---|---|
| M1 Visitor arrivals (DSEC) | KONG KIN MENG (Lucas) | Yes — `data_processed/demand_monthly_arrivals.csv` (225×7), `demand_goldenweek_daily.csv` (140×9), plus 9 tidy extracts in `Dataset/` | Only partial: no README for M1; definitions recoverable from the DSEC indicator IDs and the column names | Data complete, documentation was missing → now §3 |
| M2 Hotel occupancy (DSEC) | KUAN CHI KIT (Ray) | Yes — `Dataset/Hotel_occ_total.csv` (153×8), `hotel_occ_total_summary.csv` (45×4), `DSEC_hotel_guests_rooms_2023_01_2026_09.csv` (45×3), `Hotel_Arr_byHotelStar.csv` (612×9), `hotel_Arrival_byHotelStar_summary.csv` (180×5) | Only partial: no README for M2; definitions recoverable from column names and the audit note | Data complete, documentation was missing → now §4 |
| M3 Bus ridership (DSAT / open data) | FONG CHIN WAI (Vivi) | Yes — `data_processed/supply_stops.csv` (586×12), `supply_routes.csv` (91×8), `supply_stop_departures.csv` (586×10), `supply_departures_route_hour.csv` (7488×8), `Monthly_Bus_Database/bus_monthly_2020_2026.csv` (81×16) and 2 companions | Best documented already: `Monthly_Bus_Database/README.md` gives the bus-monthly field list; `build_district_map.py` docstring gives the map-layer fields | Data complete, partially documented → now §5 |
| Joint integration | Vivi (pipeline) + Lucas (validation) | Yes — `monthly_panel_2023_01_2026_09.csv` (45×13), `quarterly_panel` (15×12), `analysis_dataset_master.csv` (25920×19), 9 `match_*` tables, 3 geospatial layers | Partially: `build_panels.py` docstring lists panel columns; merge/derivation formulas were not written down anywhere | Data complete, formulas undocumented → now §6 |

Conclusion: **all three modules were already executed and their cleaned outputs exist in the repository.** What was missing is exactly the promised artefact — a formal dictionary with units, derivations, provenance and exclusion rules. That is what this file supplies.

---

## 2. Provenance

All raw files were downloaded on **2026-11-04**; raw downloads are never overwritten (README §9). Per-file provenance is also recorded in `Monthly_Bus_Database/source_index.csv` (29 sources with coverage and URL) and `data_processed/dataset_inventory.csv` (18 datasets with role in analysis).

| ID | Source | Accessed object | Local raw path | Access date |
|---|---|---|---|---|
| S1 | DSEC — visitor arrivals key indicator (indicator 14023, monthly, total arrivals) | JSON API snapshot, 224 monthly values 2008-01 → 2026-08 | `data/dsec_timeseries/DSEC_KeyIndicator_27.json` | 2026-11-04 (last update 2026-09-18) |
| S2 | DSEC — same-day / overnight arrivals key indicator (127) | JSON API snapshot, 224 monthly values 2008-01 → 2026-08 | `data/dsec_timeseries/DSEC_KeyIndicator_127.json` | 2026-11-04 (last update 2026-09-18) |
| S3 | DSEC — hotel occupancy & guest tables (monthly survey releases, 2014-01 → 2026-09; star-class breakdown) | HTML-table exports converted to CSV | `Dataset/Hotel_occ_total.csv`, `Dataset/Hotel_Arr_byHotelStar.csv`, `Dataset/Visitors_Arrival_byArrivalPoint.csv`, `Dataset/Visitors_Arrival_byOnday_Overnight_{CN,HK,KR,TW}.csv` | 2026-11-04 |
| S4 | DSEC — hotel guests and room supply (2023-01 → 2026-09) | table export | `Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv` | 2026-11-04 |
| S5 | DSEC — September 2026 arrivals released after the indicator snapshot | one-row manual capture | `Dataset/DSEC_arrivals_2026_09_supplement.csv` | 2026-11-04 |
| S6 | DSAT — public bus ridership, monthly and quarterly statistics (daily average trips, buses in service, stops) | quarterly PDF / monthly web page (page `a_id=1686905234`) transcribed to CSV | `Monthly_Bus_Database/*.csv` | 2026-11-04 |
| S7 | Government Data Open Platform (data.gov.mo) — annual bus passenger trips, number of buses / stops, hotel-shuttle ridership | XLSX from portal downloads (`Number_of_public_bus_rides.xlsx`, `Number_of_buses.xlsx`, `Total_number_of public_bus_stops.xlsx`, `Hotel_casino_shuttle_bus_ridership_and_departure_frequency.xlsx`) | `data/gov_mo_datasets/` | 2026-11-04 |
| S8 | `macau-bus-data` community mirror of DSAT open data — bus stops (`stops.json`, 586 records) and route timetables (`route-schedule/`, 91 route files, 920 headway windows) | JSON / header-less CSV | `data/github_macau-bus-data/macau-bus-data-master/` | 2026-11-04 |
| S9 | Bus on-board sensing dataset (MOPubBus travel-time / crowd-level records in the public mirror) | 6 CSV extracts for routes 3 and AP1 | `data/mopubbus/` | 2026-11-04 |
| S10 | MGTO — Macao Tourism Data Plus, visitor headcount by district and hour, plus Golden Week daily series | 45 API extracts | `data/mgtodataplus/` | 2026-11-04 |
| S11 | DSEC — official district boundaries / statistical zones | GeoJSON | `data_processed/macau_districts_official_26.geojson` | 2026-11-04 |

---

## 3. M1 — Visitor arrivals

### 3.1 `data_processed/demand_monthly_arrivals.csv` — 225 rows × 7 columns, 2008-01 → 2026-09

The single arrivals time series used by every downstream table and every arrivals figure.

| Field | Type | Unit | Definition / derivation | Source |
|---|---|---|---|---|
| `date` | string (ISO date) | — | First day of the reference month. 225 consecutive months with no gap (verified). | built |
| `year` | int | year | Calendar year, 2008–2026. | S1 |
| `month` | int | month | Calendar month, 1–12. | S1 |
| `arrivals` | float | person-trips / month | Total monthly visitor arrivals (all source markets, all modes of entry). 2008-01 → 2026-08 from indicator 27; 2026-09 = 3,216,535 from the supplement file. Min 9,759 (2022-07, the last month before the border reopening), max 4,478,073 (2026-08). | S1, S5 |
| `same_day_arrivals` | float | person-trips / month | Same-day (non-overnight) visitor arrivals, indicator 127. **224 of 225 months non-null**; 2026-09 is missing because indicator 127 has not yet published it and the supplement contains total arrivals only. Not imputed. | S2 |
| `arrivals_yoy_pct` | float | % | `(arrivals[t] / arrivals[t−12] − 1) × 100`. **212 non-null**: all 12 months of 2008 are empty (no 2007 base in the snapshot) and 2026-09 is empty (2025-09 base exists but the supplement month is flagged incomplete). Not imputed. | derived |
| `same_day_share_pct` | float | % | `same_day_arrivals / arrivals × 100`. Range 40.7–73.67. | derived |

Continuity evidence for the 2014/2015 boundary (needed by the Proposal's window statement): 2014-12 = 2,540,070 and 2015-01 = 2,465,612 sit next to each other on one unbroken DSEC series (2014-11 = 2,802,373, 2015-11 = 2,589,451, 2015-12 = 2,634,098), with no level shift, no duplicated month and no missing month in the 225-month grid. **2008–2014 and 2015-onwards are therefore the same series with no break; 2015 is only a display starting point, not a different source.**

### 3.2 `data_processed/demand_goldenweek_daily.csv` — 140 rows × 9 columns, 2017 → 2026

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `year` | int | year | 2017–2026. | S10 |
| `gw` | string | — | Golden Week name: `Spring Festival Golden Week`, `1st October Golden Week`. | S10 |
| `date` | string | — | Calendar day of the Golden Week. | S10 |
| `series` | string | — | Always `Total Visitor Arrivals`. | S10 |
| `arrivals` | int | person-trips / day | Daily total arrivals inside the Golden Week. | S10 |
| `gw_label` | string | — | Golden Week name + year, for faceting. | derived |
| `day_index` | int | day | Day within the Golden Week (1–9). | derived |
| `month_baseline_daily` | float | person-trips / day | `monthly arrivals for that month ÷ days in month`, i.e. the “ordinary day” baseline. | derived from §3.1 |
| `ratio_vs_month_avg` | float | ratio | `arrivals / month_baseline_daily`. Range 0.05–2.07. | derived |

### 3.3 M1 auxiliary extracts in `Dataset/` (tidy, not re-processed downstream)

| File | Rows × cols | Coverage | Key fields and definition | Source |
|---|---|---|---|---|
| `visitors_2023_2026_summary.csv` | 45×6 | 2023-01 → 2026-09 | `Year, Quarter, Month, SameDay, OverNight, Total` — monthly arrivals split by length of stay; `Total` reconciles with §3.1. | S3 |
| `visitors_2023_2026_by_market_summary.csv` | 180×6 | same | `Market` ∈ {CN, HK, KR, TW}; `SameDay`, `OverNight`. Used for the demand-side market mix. | S3 |
| `Visitors_Arrival_byArrivalPoint.csv` | 153×10 | 2014-01 → 2026-09 | `Modes of Transport` (e.g. The Border Gate), `Transport` (By Land / Sea / Air), `Total`, `Total Year of Year Changes` (%); `Remark` columns empty. | S3 |
| `Visitors_Arrival_byOnday_Overnight_CN/HK/KR/TW.csv` | 153×12 each | 2014-01 → 2026-09 | Per-market `SameDay` / `OverNight` with their YoY columns; `Source Markets` names the market. Superseded downstream by the 2023+ summaries; kept for long-run context. | S3 |
| `DSEC_arrivals_2026_09_supplement.csv` | 1×3 | 2026-09 | `year, month, arrivals` = 3,216,535. Exists only because the indicator snapshot ends at 2026-08. | S5 |

---

## 4. M2 — Hotel occupancy and room supply

### 4.1 `Dataset/Hotel_occ_total.csv` — 153 rows × 8 columns, 2014-01 → 2026-09

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `Year` | int | year | 2014–2026. | S3 |
| `Quarter` | float | — | Empty in this extract (monthly table). | S3 |
| `Month` | int | month | 1–12. 153 rows = 2014-01 → 2026-09 with 2026-10..12 not yet published. | S3 |
| `Hotel Establishments` | string | — | Only `Total` in this file; star-class breakdown lives in §4.4. | S3 |
| `Occupancy rate` | float | % | Monthly guest-room occupancy rate of all hotel establishments. Range 11.8 (2020 low) – 95.2. | S3 |
| `Remark` | float | — | Empty; reserved by the publisher. | S3 |
| `Difference` | float | percentage points | Publisher's year-on-year change of the occupancy rate, −81 to +53.6 pp (the −81 pp cell is 2020-07 against 2019-07). | S3 |
| `Remark.1` | float | — | Empty; publisher duplicate header artefact. | S3 |

### 4.2 `Dataset/hotel_occ_total_summary.csv` — 45 rows × 4 columns, 2023-01 → 2026-09

Tidy working copy of §4.1 restricted to the modelling window; `Year`, `Quarter`, `Month`, `Occupancy_rate` (%, 71.4–94.6). Used to attach occupancy to the monthly panel by `(year, month)`.

### 4.3 `Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv` — 45 rows × 3 columns

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `month` | string | — | `YYYY-MM`, 2023-01 → 2026-09. | S4 |
| `guests` | int | person-arrivals / month | Guests checked in to hotel establishments (847,800–1,322,000). | S4 |
| `rooms` | int | rooms | Rooms available in the month (38,550–46,950); the denominator behind the occupancy rate. | S4 |

### 4.4 Star-class guest mix

| File | Rows × cols | Fields | Definition |
|---|---|---|---|
| `Dataset/Hotel_Arr_byHotelStar.csv` | 612×9 | `Year` (2014–2026), `Quarter` (empty), `Month`, `Source Markets` (=`Total`), `Hotel Establishments` (5-/4-/3-/2-star), `Number of guests`, `Remark` (`r` = revised, 3 rows), `Year-on-year Change` (%), `Remark.1` (empty) | Long-run monthly guest counts per star class; 4 classes × 153 months = 612. Used for the demand-side hotel profile, not for the panel. |
| `Dataset/hotel_Arrival_byHotelStar_summary.csv` | 180×5 | `Year`, `Quarter`, `Month`, `Hotel_Establishments`, `Number_of_guests` | Tidy 2023-01 → 2026-09 subset (4 classes × 45 months). |

---

## 5. M3 — Bus ridership and scheduled supply

### 5.1 `data_processed/supply_stops.csv` — 586 rows × 12 columns (bus stops)

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `code` | string | — | DSAT stop code including direction suffix, e.g. `M1_2` (parent `M1`, direction 2). | S8 |
| `nameCht` | string | — | Chinese stop name, e.g. 關閘總站. | S8 |
| `namePor` | string | — | Portuguese stop name as published. | S8 |
| `parentCode` | string | — | Stop group without the direction suffix (`M1`); 586 physical stops, 1 stop per parent in this extract. | S8 |
| `lat`, `lng` | float | decimal degrees | WGS84 coordinates (lat 22.11–22.22, lng 113.50–113.60, i.e. all inside Macao). | S8 |
| `zone` | string | — | Macro-zone assignment from coordinates: `Macau Peninsula` / `Taipa & Cotai` / `Coloane`. | derived |
| `stop_code` | string | — | Working key, identical to `code` in this version (kept for join stability). | derived |
| `n_routes` | int | routes | Number of distinct routes calling at the stop (1–16). | derived from S8 |
| `n_route_dir` | int | route-directions | Number of route-direction combinations (1–17), i.e. the departures that can be counted at the stop. | derived |
| `n_records` | int | records | Raw timetable rows aggregated for the stop (1–17); differs from `n_route_dir` where a route calls twice. | derived |
| `nn_dist_m` | float | metres | Distance to the nearest other stop (1.67–396.9 m) — quality flag for co-located/duplicated platforms, not a filter. | derived |

### 5.2 `data_processed/supply_routes.csv` — 91 rows × 8 columns

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `route` | string | — | Route number as published (`1`, `1A`, `101X`, …); 91 route files. | S8 |
| `nameCht` | string | — | Terminus description (`關閘 ⇌ 媽閣`); `⇌` marks a 2-way route, `→` a circular one. | S8 |
| `type` | string | — | `2-way` or `circular`. | derived |
| `n_directions` | int | directions | 1 for circular, 2 for 2-way. | derived |
| `n_stop_records` | int | records | Stop calls per day in the timetable (9–78). | derived |
| `zones_served` | string | — | Zones touched, joined with ` + ` (e.g. `Macau Peninsula + Taipa & Cotai`). | derived |
| `cross_bridge` | bool | — | True when the route serves both the Peninsula and Taipa/Cotai. | derived |
| `reaches_coloane` | bool | — | True when the route serves Coloane. | derived |

### 5.3 `data_processed/supply_stop_departures.csv` — 586 rows × 10 columns (daily departures per stop)

| Field | Type | Unit | Definition | Source |
|---|---|---|---|---|
| `stop_code` | string | — | Join key to §5.1. | derived |
| `zone` | string | — | As §5.1. | derived |
| `weekdays`, `weekends`, `holidays` | float | departures / day | Sum over all calling route-directions of the departures implied by the published headway windows for that day type: `60 ÷ midpoint(headway minutes)`, summed across windows; windows crossing midnight are split at 24:00. **Non-null counts: 586 / 579 / 577** — 7 weekend and 9 holiday cells are blank where a route publishes no weekend/holiday window, and are left blank rather than copied from weekdays. | S8, derived |
| `code`, `nameCht`, `lat`, `lng` | — | — | Denormalised copies of §5.1 for plotting convenience. | S8 |
| `n_routes` | int | routes | As §5.1. | derived |

### 5.4 `data_processed/supply_departures_route_hour.csv` — 7488 rows × 8 columns (hourly supply curve)

Grid of 91 routes × 114 route-directions × 24 hours, present only for the day types a timetable actually publishes: **94 route-directions carry all three day types (72 rows), 10 carry two (48 rows) and 10 carry one (24 rows)**, giving 7,488 rows in total (weekdays 2,736 / weekends 2,496 / holidays 2,256).

| Field | Type | Unit | Definition |
|---|---|---|---|
| `route`, `direction` | string, int | — | Route number and direction index (0/1). |
| `daytype` | string | — | `weekdays` / `weekends` / `holidays`. |
| `hour` | int | hour of day | 0–23. |
| `departures` | float | departures / hour | Departures falling in that hour, from the same headway-to-frequency conversion as §5.3 (0–12). |
| `cross_bridge`, `reaches_coloane`, `zones_served` | bool/bool/string | — | Route attributes copied from §5.2 for stratifying the hourly curve. |

### 5.5 Official ridership series

| File | Rows × cols | Coverage | Fields and definition |
|---|---|---|---|
| `Monthly_Bus_Database/bus_monthly_2020_2026.csv` | 81×16 | 2020-01 → 2026-09 | `month`, `year`, `month_no`, `days_in_month`; `daily_avg_trips_wan` (DSAT daily average in 10k trips), `daily_avg_trips` (= ×10,000), `monthly_trips_est` (= `daily_avg_trips × days_in_month`, an estimate because DSAT publishes a daily average only); `buses_in_service`, `bus_stops`; `trips_per_bus_per_day` (= `daily_avg_trips / buses_in_service`, 114.8–705.5); `visitor_arrivals`, `same_day_arrivals` (joined from §3.1 and §3.2 by month); `trips_per_arrival` (= `monthly_trips_est / visitor_arrivals`, verified to <0.01 on 80/81 rows); `dsat_minfu_daily_wan`, `dsat_tcm_daily_wan` (per-operator daily average, only 3 months filled); `source` (which DSAT release each row came from). Documented also in `Monthly_Bus_Database/README.md`. |
| `Monthly_Bus_Database/bus_annual_reference_2011_2025.csv` | 15×7 | 2011–2025 | `official_total_trips_yi` (亿 trips/year), `official_daily_avg_wan`, `monthly_series_months` (months of our monthly series available for that year, 0–12), `computed_daily_avg_wan_from_monthly`, `abs_diff_wan` (0.001–0.006 → monthly series reconciles with the official annual total), `computed_total_trips_yi`. |
| `Monthly_Bus_Database/bus_monthly_by_operator_2026.csv` | 3×6 | 2026-07 → 2026-09 | `month`, `operator_minfu_daily_wan`, `operator_tcm_daily_wan`, `total_daily_wan`, `minfu_share_pct` (46.1–46.6 %), `source` (DSAT monthly page, updated 2026-11-04). Operator split is published only for these three months. |
| `data_processed/supply_official_series.csv` | 182×3 | monthly 2019-01 → 2026-03 (2 indicators, 87 rows each) + annual 2018 → 2025 (8 rows) | Long format: `indicator` ∈ {`public buses in service`, `public bus stops` (monthly), `annual public bus passenger trips` (annual)}, `period` (`YYYY-MM` or `YYYY`), `amount` (buses / stops / trips). The monthly capacity indicators stop at 2026-03, which is why capacity ratios end there (E-M3-5). |
| `data_processed/supply_shuttle_quarterly.csv` | 25×5 | 2020Q1 → 2026Q3 | Hotel/casino shuttle: `year`, `quarter`, `period` (`2020Q1`), `departures`, `ridership` (0 where the shuttle was suspended). |

### 5.6 `data/mopubbus/` — on-board crowd-level records (supplementary, routes 3 and AP1 only)

Six extracts (`3_*`, `AP1_*` × `grandprix_train/test`, `normal_train/test`; 1,292–6,712 records each) plus `weather_types.csv` (16 rows, weather label → numeric code).

| Field | Type | Unit | Definition |
|---|---|---|---|
| `startStation`, `endStation` | int | stop index | Stop sequence numbers inside the route, not DSAT stop codes; mapped to stop names inside the route file only. |
| `time` | string | hh:mm:ss | Observation time of the segment record. |
| `weekday` | int | 1–7 | Day of week. |
| `passengerFlow` | int | crowd level | 0–5 on-board crowding level; **`−1` means no reading and is excluded from all crowd means**. |
| `trafficCondition` | int | level | 1–3 road-traffic condition. |
| `busPlate` | string | — | Vehicle plate, used to follow a bus through segments. |
| `passbyNum` | int | buses | Number of buses that passed the stop without boarding. |
| `weather` | int | code | Weather code via `weather_types.csv` (Clear=1, Clouds=2, Drizzle=3, Rain=4, Thunderstorm=5, others=0). |
| `arrivalDuration` | int | seconds | Dwell / arrival duration at the stop. |

---

## 6. Joint integration track

### 6.1 Monthly panel — `data_processed/monthly_panel_2023_01_2026_09.csv` (45×13)

| Field | Unit | Definition |
|---|---|---|
| `month`, `year`, `month_no`, `quarter` | — | Key; `quarter` = `YYYYQn`. |
| `visitor_arrivals` | person-trips | From §3.1. |
| `hotel_occ_pct` | % | From §4.2. |
| `hotel_guests`, `hotel_rooms` | persons, rooms | From §4.3. |
| `bus_daily_avg_trips_wan` | 10k trips/day | From §5.5. |
| `bus_monthly_trips` | trips | `= bus_daily_avg_trips_wan × 10,000 × days_in_month`. |
| `buses_in_service` | buses | From §5.5; **39/45 non-null** (not published after 2026-03). |
| `mgto_district_headcount` | headcount | Sum of §6.3 over the 24 data districts for that month. |
| `bus_trips_per_arrival` | trips / arrival | `bus_monthly_trips / visitor_arrivals` (4.51–10.39). |

### 6.2 Quarterly panel — `data_processed/quarterly_panel_2023Q1_2026Q3.csv` (15×12)

Aggregated from §6.1 with documented aggregation rules: sums for flow variables (`visitor_arrivals_sum`, `hotel_guests_sum`, `bus_monthly_trips_sum`, `mgto_district_headcount_sum`), means for rates (`hotel_occ_avg_pct`, `bus_daily_avg_trips_wan_mean`, `hotel_rooms_avg`), max for capacity (`buses_in_service_max`). Also `months_in_data` (always 3, which is the reconciliation check in §10), `bus_trips_per_arrival` and `district_hits_per_arrival` (= `mgto_district_headcount_sum / visitor_arrivals_sum`, 0.94–1.19).

### 6.3 District-hour demand — `mgto_district_hour_master_2023_01_2026_09.csv` (25920×8) and `demand_district_hour_panel_2023_2026.csv` (25920×8)

45 months × 24 districts × 24 hours = 25,920 cells (balanced grid verified in §10).

| Field | Unit | Definition |
|---|---|---|
| `year`, `month`, `hour`, `period` | — | Key; `period` = `HH:00` label of `hour`. |
| `district_cn`, `district_en` | — | MGTO bilingual district name (`中區` / `Baixa de Macau`). The two spellings are the publisher's; no re-translation was applied. |
| `zone` | — | Macro-zone of the district (`Macau Peninsula` / `Taipa & Cotai` / `Coloane`). |
| `headcount` | visitor headcount | Visitors counted in that district during that hour of that month (136–104,200). Sum of 24 districts per month ≈ arrivals, but **not a partition of arrivals** — see exclusion E-INT3. |

`demand_district_hour_2026.csv` (4032×8) is the same schema restricted to 2026-01 → 2026-07 and is retained only as the mid-year extract.

### 6.4 Master analysis table — `data_processed/analysis_dataset_master.csv` (25920×19)

Same 576-cell grid as §6.3, enriched with monthly context and zone supply ratios (19 columns). Additional fields beyond §6.3:

| Field | Unit | Definition |
|---|---|---|
| `month_label` | — | `YYYY-MM` display label of `month`. |
| `headcount_share_of_month` | share (0–1) | `headcount / monthly total headcount over all 24 districts`. |
| `month_arrivals_per_district_hour` | arrivals / cell | **Equal-allocation baseline**: `visitor_arrivals ÷ (24 districts × 24 hours)` = `arrivals / 576`, i.e. a constant per month (e.g. 5,110.99 for 2023-12). It is deliberately *not* headcount-weighted; the observed `headcount` is the weighted measure. |
| `hotel_occ_pct`, `bus_monthly_trips`, `bus_trips_per_arrival`, `mgto_district_headcount`, `visitor_arrivals` | as above | Broadcast of the monthly values from §6.1 to every cell of that month. |
| `daily_bus_departures`, `departures_share_pct`, `supply_demand_ratio` | departures/day, %, ratio | Broadcast of the zone-level values from §6.6 to every district of that zone. |

### 6.5 Geographic tables

| File | Rows × cols | Fields and definition |
|---|---|---|
| `zone_area_official.csv` | 26×3 | `district_cn`, `area_km2_official` (0.2118–7.628), `has_data` (True for the 24 districts with MGTO headcount; **False for 澳門大學新校區, 新城A區及港珠澳大橋澳門口岸管理區**, which are drawn as grey context on the map but excluded from all rate calculations). |
| `district_map_metrics.csv` | 24×19 | Per district: `hits_total`, `hits_2026`, `months_present` (12/12 for all), `share_total_pct`, `share_base_pct`, `share_2026_pct`, `delta_pp` (−1.35 to +0.97 pp), `peak_hour`, `peak_hour_share_pct`, `night_share_pct` (share of the district's headcount falling in hours 0–5, i.e. 00:00–05:59), `area_polygon_km2` (as drawn) vs `area_km2` (official, used for density), `hits_per_km2_month`, `stops`, `weekday_departures`, `weekend_departures`, `hits_per_departure`. |
| `stop_district_assignment.csv` | 586×4 | `stop_code`, `district_cn` (**567 of 586 assigned**), `weekdays`, `weekends`. The 19 unassigned stops fall outside every official polygon and are excluded from district-level sums only. |
| `macau_districts_official_26.geojson` | 26 features | Official district boundaries (source S11). |
| `macau_map_layer_26.geojson` | 26 features | Rendering layer = official boundaries + `has_data` flag + hatched styling for the 2 context zones (consumed by `scripts/build_district_map.py`). |
| `macau_stats_zones.geojson` | — | Earlier 8-zone statistical layer kept for reference only; superseded by the 26-district layer. |
| `macau_visitor_transport.sqlite` | — | Local relational copy of the three modules used for ad-hoc SQL checks. |

### 6.6 Match / gap tables

| File | Rows × cols | Fields and definition |
|---|---|---|
| `match_zone_supply_demand.csv` | 3×9 | Per zone: `demand_share_pct` (share of 2026 H1 district headcount; Peninsula 42.23, Taipa & Cotai 56.10, Coloane 1.67), `departures_share_pct` (share of daily departures from §5.3; 66.42 / 28.68 / 4.91), `stops_share_pct`, `visitor_headcount_2026H1`, `daily_bus_departures`, `demand_per_departure`, `supply_demand_ratio` (= `departures_share_pct / demand_share_pct`; 1.573 / 0.511 / 2.940), `gap_index` (= `departures_share_pct − demand_share_pct`, in pp; +24.19 / −27.42 / +3.24). |
| `match_hourly_profile.csv` | 24×6 | Per hour: `demand_share_pct` (share of daily headcount), `supply_share_weekday_pct`, `supply_share_weekend_pct`, and `gap_weekday_pp` / `gap_weekend_pp` = supply share − demand share in pp. |
| `match_gateways.csv` | 7×5 | Per border gateway: `stops`, `route_numbers`, `daily_departures`, `terminal_stops` (names). |
| `match_event_crowding.csv` | 4×7 | Route × phase (Grand Prix vs normal week): `trips`, `obs` (raw segment records), `mean_crowd` (mean of valid `passengerFlow`, −1 excluded), `crowded_share` (% of valid records at crowd level ≥ 4), `mean_traffic`. |
| `match_event_segment_crowding.csv` | 88×7 | Same metrics per origin–destination segment; `optional_event_segment_crowding_top20.csv` holds the 20 largest. |
| `match_annual_alignment.csv` | 8×6 | `year` 2018–2026, `bus_passenger_trips`, `visitor_arrivals`, `trips_per_visitor`, `bus_trips_yoy_pct`, `arrivals_yoy_pct`. (Also present as `annual_alignment_2018_2026.csv`, which adds `dsec_arrivals_full_year`, `months_in_data`, `arrivals_annualised_est`.) |

### 6.7 Descriptive tables (no modelling role, used for the figures)

`monthly_detail_2023_01_2026_09.csv` (45×22: YoY/MoM/3-month moving average, season index, occupancy YoY in pp, `district_hits_per_arrival` = `mgto_district_headcount / visitor_arrivals`), `quarterly_detail_2023Q1_2026Q3.csv` (15×21, adds `arrivals_qoq_pct`, `arrivals_annualised`, `hotel_guests_per_room`, `partial`), `monthly_seasonality_index.csv` (12×7; `season_index_arrivals` = month mean ÷ overall mean × 100, means 2023/2024/2025 and 2023–2025, `peak_flag`), `annual_summary_2023_2026.csv` (4×12), `annual_zone_share.csv` (4×6), `annual_hour_profile.csv` (4×25, hour shares in % summing to 100 per year), `annual_month_profile.csv` (19×13), `zone_month_share.csv` (45×5), `mgto_quarter_district_2023Q1_2026Q3.csv` (360×3), `mgto_quarter_hour_2023Q1_2026Q3.csv` (360×3), `optional_2026_hour_shift.csv` (24×4), `optional_2026_zone_shift.csv` (3×4), `optional_gateways_summary.csv` (7×7), `optional_goldenweek_summary.csv` (19×10), `optional_shuttle_quarterly.csv` (25×6), `optional_event_crowding_summary.csv` (4×8).

### 6.8 Registry tables

`dataset_inventory.csv` (18×5: `group`, `dataset`, `rel_path`, `size_kb`, `role_in_analysis`), `phase1_usability_verdict.csv` (11×3: `dataset`, `verdict`, `reason` — all 11 PASS), `qa_report.csv` (12×4, see §10), `output_manifest.csv` (63×3: `file`, `kind`, `size_kb`).

---

## 7. Exclusion and transformation rules

### M1
1. **E-M1-1 — Long series vs analysis window.** The full arrivals series 2008-01 → 2026-09 is kept intact. Correlation, regression and panel work use **2023-01 → 2026-09** (45 months), the period for which M2 and M3 are published on the same monthly basis; the long series is used only for the long-run arrivals figure and for the 2015-onwards context line.
2. **E-M1-2 — COVID period.** 2020-02 → 2022-12 is retained in the series but excluded from all correlation/regression and from any “average month” baseline, because border restrictions make arrivals (9,759 in 2022-07) and occupancy (11.8 %) non-comparable with the rest of the series. The window is stated in the Proposal and on the figures.
3. **E-M1-3 — Snapshot duplicates.** Indicator JSON snapshots are keyed on `(year, month)`; if the same period appears twice, the value with the latest `LastUpdateDate` wins. The current snapshots contain 224 unique months each, so no row was dropped in practice.
4. **E-M1-4 — Undefined growth rates are left blank.** 2008 YoY has no 2007 base and 2026-09 YoY is withheld with the partial month; both are `NaN`, never zero-filled.
5. **E-M1-5 — September 2026 handling.** 2026-09 total arrivals come from a single-row supplement (S5). It is flagged wherever a same-day split is required: `same_day_arrivals` and `same_day_share_pct` are blank for that month.
6. **E-M1-6 — Golden Week baseline.** `ratio_vs_month_avg` divides by the *calendar-month* daily average of the same month, not by the same month of previous years, so the ratio is interpretable within a month only.

### M2
1. **E-M2-1 — One series per concept.** Only the `Hotel Establishments = Total` rows feed `hotel_occ_pct`; star-class rows are used only for the guest-mix profile, never summed into the total.
2. **E-M2-2 — Publication end.** The occupancy and guest/room series stop at 2026-09 (2026-10..12 unpublished at the access date). Panels therefore end at 2026-09 and 2026 quarters are flagged `partial` where applicable.
3. **E-M2-3 — Revised cells kept, not dropped.** Rows marked `Remark = r` (3 cells in the star-class table) are kept and reported as published; the mark means the publisher revised the figure, not that the observation is invalid.
4. **E-M2-4 — Growth rates within class.** Occupancy YoY is computed against the same star class and the same month; cross-class differences (e.g. 5-star vs 2-star) are never mixed.
5. **E-M2-5 — COVID floor.** The 11.8 % minimum (2020) reflects hotels operating as quarantine/medical facilities; those months are excluded from occupancy averages (E-M1-2 window applies).

### M3
1. **E-M3-1 — Departures are frequencies, not observations.** DSAT publishes headway windows, not trip counts. Departures are estimated as `60 ÷ midpoint(headway minutes)` per window and summed; `supply_stop_departures` and `supply_departures_route_hour` are therefore *scheduled-supply estimates*, and this is stated in the figure notes. `monthly_trips_est` in §5.5 is likewise `daily average × days in month`.
2. **E-M3-2 — Midnight-spanning windows.** A window whose end time is earlier than its start time (e.g. 20:00 → 01:15) is split across midnight and assigned to the following day's early hours, so no departure is double counted or lost.
3. **E-M3-3 — Missing day-type windows stay missing.** 7 weekend and 9 holiday stop-level cells have no published window; they are left blank and excluded pairwise, never filled from the weekday value.
4. **E-M3-4 — 19 stops outside the district layer.** 567 of 586 stops fall inside an official district polygon. The other 19 keep their zone assignment and are used in zone totals and hourly curves, but they are excluded from `district_map_metrics.csv` and from district-level sums.
5. **E-M3-5 — Capacity series ends 2026-03.** `buses_in_service` / `bus_stops` are not published after 2026-03, so `trips_per_bus_per_day` is blank for 2026-04..09 (6 months). No extrapolation was applied.
6. **E-M3-6 — Operator split is 3 months only.** `bus_monthly_by_operator_2026.csv` covers 2026-07..09 only; the operator share is not extrapolated backwards.
7. **E-M3-7 — Crowd-level records.** `passengerFlow = −1` is a “no reading” code and is removed before any mean; crowd level ≥ 4 defines “crowded” (matching `crowded_share` in the code). Records exist only for routes 3 and AP1, so `match_event_crowding.csv` is a two-route case study and is never presented as network-wide.
8. **E-M3-8 — Annual totals.** 2026 passenger trips are year-to-date; `arrivals_annualised_est` is filled for exactly one year (`months_in_data = 9`) and flagged as an estimate.
9. **E-M3-9 — Portal files.** data.gov.mo distributions arrive with an `.xlsx` extension but are zip archives; they were matched to the declared format before parsing and are never read as spreadsheets directly. Year-to-date cumulative portal tables are de-cumulated to monthly.

### Integration
1. **E-INT-1 — Balanced grid only.** The district-hour layer is a complete 24 districts × 24 hours × 45 months grid; any month with a different number of cells would fail the QA check and be rejected rather than padded (current grid: 576 cells per month, §10).
2. **E-INT-2 — Equal-allocation baseline is not a model output.** `month_arrivals_per_district_hour` is the uniform `arrivals / 576` benchmark used to compare against observed `headcount`; it must not be read as allocated demand.
3. **E-INT-3 — District headcount is not a partition.** A visitor can be counted in more than one district, so monthly district headcount sums to 0.88–1.32 × arrivals (`district_hits_per_arrival`; 0.94–1.19 on the quarterly panel). District shares are therefore computed *within* the district total, never as a share of arrivals.
4. **E-INT-4 — Two context zones carry no data.** 澳門大學新校區, 新城A區及港珠澳大橋澳門口岸管理區 have `has_data = False`; they appear on the map as hatched context and are excluded from every denominator (median, density, share).
5. **E-INT-5 — Area basis.** Densities use `area_km2` (official area from `zone_area_official.csv`), not `area_polygon_km2` (the drawn polygon, e.g. 路環區 13.46 vs 7.63 km²), because the drawn polygon absorbs adjacent water/reclaimed area.
6. **E-INT-6 — No imputation anywhere.** No value in M1–M3 or the integration layer is synthetic. Where a source is missing the cell is blank and the affected analysis is scoped accordingly.

---

## 8. Known gaps and caveats

| Item | Effect | Handling |
|---|---|---|
| DSEC indicator snapshot ends 2026-08 | 2026-09 arrivals exist only as a total | supplement file; same-day fields blank (E-M1-5) |
| Occupancy not published for 2026-10..12 | panel ends 2026-09 | stated window (E-M2-2) |
| `buses_in_service` missing 2026-04..09 | no capacity ratio for those months | left blank (E-M3-5) |
| Operator split only 2026-07..09 | no operator time series | used as a 3-month snapshot only (E-M3-6) |
| 19 stops outside official polygons | district totals slightly under-count stops | excluded from district sums, kept in zone sums (E-M3-4) |
| Crowd data only routes 3 & AP1 | event effect is illustrative | labelled as case study (E-M3-7) |
| District headcount ≠ arrivals | share denominators differ | E-INT-3 |
| M2 star-class table 2014–2026 vs totals only 2023+ | guest mix is not comparable before 2023 in the panel | long-run mix used descriptively only |

---

## 9. Conventions

- **Period keys:** `YYYY-MM` for months, `YYYYQn` for quarters; hourly keys are integer `hour` 0–23 with `period` as the `HH:00` label.
- **Zones:** exactly three macro-zones — `Macau Peninsula`, `Taipa & Cotai`, `Coloane`; districts roll up to zones; the two context zones in §6.5 belong to no zone total.
- **District names:** MGTO publishes bilingual names; `district_cn` is the key and `district_en` is the publisher's English/Portuguese spelling, kept verbatim (e.g. 中區 → `Baixa de Macau`).
- **Units:** arrivals / guests are **person-trips per month** (not unique persons); trips are **boardings**; departures are **scheduled vehicle departures per day or per hour**; shares are percentages of the stated denominator; occupancy is % of rooms.
- **Missing values:** empty = not published / not applicable. No sentinel codes (−1, 0, 999) are used in the processed layer; the single `−1` convention lives only in the raw crowd data (E-M3-7).
- **Rounding:** published (not recomputed) roundings are kept; derived ratios are stored unrounded and rounded only at display time.

---

## 10. QA checks carried over from `data_processed/qa_report.csv`

| Check | Result | Status |
|---|---|---|
| Monthly panel row count (expected 45) | 45 | PASS |
| Duplicate months in panel | 0 | PASS |
| Missing months in panel | 0 | PASS |
| Duplicate district-hour keys | 0 | PASS |
| District-hour grid balance | 1 grid size / 576 cells per month | PASS |
| Negative headcount values | 0 | PASS |
| Zero-headcount cells | 0.0 % | INFO |
| Hotel series completeness | 45 / 45 | PASS |
| Bus series completeness | 45 / 45 | PASS |
| Arrivals outliers (\|z\| > 3, 2023–2026) | 0 | INFO |
| Monthly → quarterly row reconciliation | 45 == 45 | PASS |
| District headcount as share of arrivals (2025) | 99.9 % | INFO |

Earlier field-level cross-checks used for this dictionary and reproducible from the stored files: arrivals series has 225 consecutive months with no gap; KI-27/KI-127 snapshots each hold 224 monthly values whose first and last values equal the 2008-01 and 2026-08 rows of §3.1; `trips_per_arrival` reproduces `monthly_trips_est / visitor_arrivals` within 0.01 on 80 of 81 months; `supply_demand_ratio` reproduces `departures_share_pct / demand_share_pct` for all three zones; `month_arrivals_per_district_hour × 576 = visitor_arrivals` for every month; `season_index_arrivals` averages exactly 100 across the 12 months.

---

## 11. Change log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-22 | First consolidated dictionary. Consolidates fragments from `Monthly_Bus_Database/README.md`, `scripts/build_panels.py`, `scripts/build_district_map.py`, `reports/data_coverage_audit_2026-11-04.md`; adds field-level tables for M1, M2, M3 and the integration track, explicit exclusion rules (E-M1-*, E-M2-*, E-M3-*, E-INT-*) and the known-gap register. |

