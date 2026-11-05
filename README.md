---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_6dbe133cd90911f19280525400393706
    ReservedCode1: k0d72YyF4cXP2TOYtZayUoscMZ8RtFzM8VIYmqMRSaL/lgdUhORxub1OPTJofWa2BJOKKsvJgjQiYexpPstssni8FdSTvTFKcQd2kIN3ZSIICmjFOuQkBFxDjufjcOcNT1i5AzJyD+htI/vgiJbNt2uHyVxbXsNY40cTM77f/2WtrZRrh1jBFpsjmSY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_6dbe133cd90911f19280525400393706
    ReservedCode2: k0d72YyF4cXP2TOYtZayUoscMZ8RtFzM8VIYmqMRSaL/lgdUhORxub1OPTJofWa2BJOKKsvJgjQiYexpPstssni8FdSTvTFKcQd2kIN3ZSIICmjFOuQkBFxDjufjcOcNT1i5AzJyD+htI/vgiJbNt2uHyVxbXsNY40cTM77f/2WtrZRrh1jBFpsjmSY=
---

# CISC7204 Class E Team 01 - Visitor Arrivals, Hotel Occupancy and Bus Ridership in Macao

This repository holds everything behind the team proposal
`Proposal/CISC7204_ClassE_Team01_Proposal.docx` (and its `.pdf` export): the raw
downloads, the integrated panels, the figure notebook, the figure files, and the one
script that rebuilds the panels from the raw files.

The rule the repository follows is simple: **every number printed in the proposal is
produced by a file in this repository, and every figure is produced by a cell in one
notebook.** The two tables further down give that chain file by file.

---

## 1. Reproduce the whole chain

Run from the repository root, in this order.

```bash
# Step 1 - rebuild the three integrated panels from the raw / intermediate files
python scripts/build_panels.py

# Step 2 - rebuild the six figures from data_processed/
jupyter nbconvert --to notebook --execute notebooks/cisc7204_proposal_figures_colour.ipynb \
        --output cisc7204_proposal_figures_colour.ipynb

# Step 3 - open Proposal/CISC7204_ClassE_Team01_Proposal.docx and export to PDF
#          (Word: File > Export > Create PDF/XPS, or LibreOffice --convert-to pdf)
```

Step 1 is byte-for-byte reproducible: re-running it overwrites the three panels with
files identical to the ones committed here (checked with `md5sum` on 2026-11-05).

Requirements: Python 3.11 or newer, `pandas`, `numpy`, `matplotlib`, `seaborn`,
`scipy`, `openpyxl`, plus Jupyter for step 2. No network access is needed; every input
is already in the repository.

---

## 2. Where things live

| Path | What it is |
| --- | --- |
| `scripts/build_panels.py` | The only script: builds the three integrated panels from raw / intermediate files |
| `notebooks/cisc7204_proposal_figures_colour.ipynb` | The only figure notebook: draws Figures 1-6 into `figures/` |
| `figures/fig1_general_trend.png` ... `fig6_workplan.png` | The six figure files embedded in the proposal, in proposal order |
| `figures/archive/` | Superseded figures kept for traceability - **not** used by the proposal |
| `data/mgtodataplus/` | MGTO *Macao Tourism Data Plus* district x hour downloads (year-to-date workbooks) |
| `data/dsec_timeseries/` | DSEC key-indicator JSON snapshots used for the arrivals series |
| `data/data.gov.mo_bus_route_shp/` | data.gov.mo bus route / stop shapefile export |
| `data/mopubbus/` | Public-bus running-time exports (exploratory, not used in the proposal) |
| `Dataset/` | Small DSEC / MGTO CSV and Excel exports kept next to the report (occupancy, hotel guests and rooms, arrivals by day type, 2026-09 arrivals supplement) |
| `Monthly_Bus_Database/` | DSAT monthly bus statistics and the per-row source index |
| `data_processed/` | All integrated panels and matching layers read by the notebook |
| `Proposal/` | Final deliverable: proposal `.docx` and `.pdf` |
| `cisc7204-Class_E-Team_01_WorkPlan01.docx/.pdf`, `cisc7204-Class_E-Team_01_Photos/` | Course work plan and team photos submitted with the proposal |

`figures/archive/legacy_fig1_research_question_supply_demand_match.png` and
`legacy_fig2_supplementary_district_event_shuttle.png` are older drawings whose names
began with `fig1_` and `fig2_`. They were moved into `archive/` and prefixed `legacy_`
so that the `fig1_...` / `fig2_...` prefixes in `figures/` map one-to-one onto Figure 1
and Figure 2 of the proposal.

---

## 3. Script to panel: what `build_panels.py` reads and writes

Inputs (read-only):

| Input | Used for |
| --- | --- |
| `data/mgtodataplus/MacaoDistrictTourismData_{202312,202412,202512,202609}_en.xlsx` | District x hour visitor headcount. Each monthly file is year-to-date, so only the last file of each year is read, otherwise months would be counted two to four times |
| `data_processed/demand_monthly_arrivals.csv` | DSEC monthly visitor arrivals |
| `Dataset/DSEC_arrivals_2026_09_supplement.csv` | The single September 2026 arrivals row published after the JSON snapshot |
| `Dataset/Hotel_occ_total.csv` | DSEC monthly occupancy rate (all hotels) |
| `Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv` | DSEC monthly hotel guests and room supply |
| `Monthly_Bus_Database/bus_monthly_2020_2026.csv` | DSAT daily-average bus trips and buses in service |

Outputs (overwritten on every run):

| Output | Shape | Columns |
| --- | --- | --- |
| `data_processed/mgto_district_hour_master_2023_01_2026_09.csv` | 25,920 rows | `year, month, hour, district, headcount` - 8 districts x 24 hours x 45 months (2023-01 to 2026-09) |
| `data_processed/monthly_panel_2023_01_2026_09.csv` | 45 rows | `month, year, month_no, quarter, visitor_arrivals, hotel_occ_pct, hotel_guests, hotel_rooms, bus_daily_avg_trips_wan, bus_monthly_trips, buses_in_service, mgto_district_headcount, district_hits_per_arrival` |
| `data_processed/quarterly_panel_2023Q1_2026Q3.csv` | 15 rows | `quarter, months_in_data, visitor_arrivals_sum, hotel_occ_avg_pct, hotel_guests_sum, hotel_rooms_avg, bus_daily_avg_trips_wan_mean, bus_monthly_trips_sum, buses_in_service_max, mgto_district_headcount_sum, bus_trips_per_arrival, district_hits_per_arrival` |

The 36-month estimation window (2023-01 to 2025-12) is a **filter applied to these
files**, not a separate file: the panels carry the whole published span so that the
window and the pandemic exclusion can be audited from the data itself.

Three further panels in `data_processed/` are read by the notebook but are **not**
produced by `build_panels.py` (see the gap note in section 6):

| Panel | Shape | Role |
| --- | --- | --- |
| `demand_district_hour_panel_2023_2026.csv` | 24,768 rows | District x hour panel with the zone mapping (`zone` = Macau Peninsula / Taipa & Cotai / Coloane); covers 2023-01 to 2026-07 |
| `match_zone_supply_demand.csv` | 3 rows | Zone-level demand, departure and stop shares, plus the demand-per-departure and supply-to-demand ratios |
| `match_hourly_profile.csv` | 24 rows | Hour-of-day demand share and weekday / weekend departure shares, with the gap in percentage points |

---

## 4. Panel to figure: what each notebook cell draws

| Cell | Figure file | Reads | What it shows |
| --- | --- | --- | --- |
| cell 4 | `figures/fig1_general_trend.png` | `demand_monthly_arrivals.csv` | Monthly arrivals 2015-2026, pandemic years in red dashed and left blank, 36-month estimation window shaded |
| cell 6 | `figures/fig2_zone_mismatch.png` | `match_zone_supply_demand.csv` | Three shares per zone (demand, departures, stops), January-July 2026 |
| cell 8 | `figures/fig3_hourly_profile.png` | `match_hourly_profile.csv` | Hour-of-day demand share against weekday and weekend departure shares, undersupplied hours shaded |
| cell 10 | `figures/fig4_correlation.png` | `monthly_panel_2023_01_2026_09.csv`, `quarterly_panel_2023Q1_2026Q3.csv` | (a) monthly scatter with `r` printed, n = 36; (b) bus trips per arrival by quarter, n = 12 |
| cell 12 | `figures/fig5_district_hour_heatmap.png` | `demand_district_hour_panel_2023_2026.csv` | The ten busiest districts by hour, each row rescaled to its own daily total, 2023-2025 |
| cell 14 | `figures/fig6_workplan.png` | hard-coded work plan | The four-week delivery plan, bar length = duration, red outline = critical chain |

Figure numbers in the proposal caption correspond one-to-one to these files; the
caption of Figure 5 describes the ten-district subset the cell actually draws, and the
caption of Figure 6 refers to the week-by-week plan of Section 7 (there is no Table 10
in the proposal).

---

## 5. Figure to number: what the proposal quotes, and where it comes from

| Number in the proposal | Where it comes from |
| --- | --- |
| Arrivals 3.28 million per month in 2019, 11,041 in April 2020, 3.34 million in 2025 | `demand_monthly_arrivals.csv` (read by Figure 1 cell) |
| 36 months, 12 quarters, 103.2 million arrivals, 42.6 million hotel guests | `monthly_panel_2023_01_2026_09.csv`, filtered to 2023-01..2025-12 |
| Quarterly arrivals 4.95 to 10.40 million, occupancy 74.9% to 89.9%, bus trips 549,000 to 659,000 per day | `quarterly_panel_2023Q1_2026Q3.csv` (Table 1 of the proposal is this table) |
| Bus trips per visitor 9.96 to 5.83, a 41% decline | `quarterly_panel_2023Q1_2026Q3.csv`, column `bus_trips_per_arrival` |
| Taipa & Cotai 56.1% of headcount, 28.4% of departures, ratio 0.51; Peninsula 42.2% of headcount, 66.6% of departures, ratio 1.58; Coloane ratio 2.99 and 1.7% of headcount | `match_zone_supply_demand.csv` (Figure 2 cell) |
| 204 departures-per-visitor in Taipa & Cotai against 66 on the Peninsula | `match_zone_supply_demand.csv`, column `demand_per_departure` |
| Visitor peak 5.4% at 16:00; 20.2% between 00:00 and 05:59 against 2.1% of weekday departures | `match_hourly_profile.csv` (Figure 3 cell) |
| Cotai 43.7% of city-wide headcount; 17:00-19:00 cells about 2.1% of the city total each | `demand_district_hour_panel_2023_2026.csv` (Figure 5 cell) |
| r = 0.759 pooled over the 36 months (printed on panel a); bus trips per visitor against time r = -0.798 over the 12 quarters (printed on panel b); quarterly arrivals against quarterly passenger trips r = 0.917 (quoted in the text, not drawn on either panel); 0.818 / 0.254 / 0.625 by year and 0.470 for 2024-2025 | `monthly_panel_2023_01_2026_09.csv` and `quarterly_panel_2023Q1_2026Q3.csv`; every `r` in that row is produced by the Figure 4 cell of the notebook, the by-year values are the same correlation computed on year subsets |
| 25,920 district-hour rows over 45 months; 45 monthly rows; 15 quarterly rows | `build_panels.py` outputs (section 3) |

---

## 6. Known gaps

- `demand_district_hour_panel_2023_2026.csv`, `match_zone_supply_demand.csv` and
  `match_hourly_profile.csv` were produced by exploratory steps that were not saved as
  scripts. They are committed here so the notebook runs end to end, but rebuilding them
  from `data/` still requires redoing those steps by hand. `build_panels.py` covers the
  three panels the proposal quotes as dataset rows 3.1-3.7; the matching layers are the
  remaining gap.
- The bus ridership series is assembled from DSAT monthly and quarterly PDF releases;
  the per-row provenance is in `Monthly_Bus_Database/source_index.csv`.
- The DSEC portal download for hotel guests and rooms is not stored in the repository;
  the export in `Dataset/` is the file the report was computed from.

---

## 7. Data sources and access dates

All downloads were taken on 4 November 2026. Provenance per file is recorded in
`Monthly_Bus_Database/source_index.csv` and in the `Note.` line of the proposal's
reference list.

- Macao Government Tourism Office - *Macao Tourism Data Plus*, regional tourism data by
  district and hour, and visitor arrivals by source market: <https://dataplus.macaotourism.gov.mo/>
- Statistics and Census Service (DSEC) - visitor arrivals, hotel occupancy, hotel guests
  and room supply: <https://www.dsec.gov.mo/en-US/>
- Transport Bureau (DSAT) - public bus ridership and scheduled departures, monthly and
  quarterly releases: <https://www.dsat.gov.mo/>
- Government Data Open Platform - public bus passenger trips, cumulative:
  <https://data.gov.mo/Detail?id=ca8e7bbb-4eef-4118-8893-90b3fc8d3cb1>

Raw downloads are never overwritten; cleaning decisions are recorded in the data
dictionaries handed in with the report.
*（内容由AI生成，仅供参考）*
