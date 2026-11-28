---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_cc275532ea8a11f1a20652540072b1e8
    ReservedCode1: BmJDcW2BoKhVJyztgLGN2+kVI3Nbu4J64THuzofvzJtjF7NgeS1RoSc9mHa2cyOKyfVE3GzFHD7FYqCMQS/4I37BWWda6FwTMeuKlMfPzU+Y5AFb4fFR3X1znCdpDSzcP7/c5RPyTg6hSI0SifNtkyA8YDbsCDSScTuToJk5oxK1hEXBHcX2Sko17Us=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_cc275532ea8a11f1a20652540072b1e8
    ReservedCode2: BmJDcW2BoKhVJyztgLGN2+kVI3Nbu4J64THuzofvzJtjF7NgeS1RoSc9mHa2cyOKyfVE3GzFHD7FYqCMQS/4I37BWWda6FwTMeuKlMfPzU+Y5AFb4fFR3X1znCdpDSzcP7/c5RPyTg6hSI0SifNtkyA8YDbsCDSScTuToJk5oxK1hEXBHcX2Sko17Us=
---

# scripts/data_cleaning

Numbered cleaning scripts behind Section 3.2.2 of the final report. They take the raw downloads in
`data/`, `Dataset/` and `Monthly_Bus_Database/`, clean the three module series, rebuild the analysis
panel and check the result against the delivered files.

Run everything, in order, from the repository root:

```
python scripts/data_cleaning/run_all.py
```

Each script exits non-zero on a failed assertion, and `run_all.py` stops at the first failure, so a broken
input never reaches a figure.

## The chain, in order

```
                raw download / committed extract                     script                      output
data/mgtodataplus/MacaoDistrictTourismData_{202312,202412,202512,202609}_en.xlsx   (gated by 01)
Dataset/*.csv, demand_monthly_arrivals.csv, DSEC hotel extracts, bus_monthly_2020_2026.csv
    -> 01_ingest.py          -> data_processed/clean_inventory.csv      (inventory + row-count gates)
    -> 02_clean_series.py    -> data_processed/clean_arrivals.csv, clean_occupancy.csv,
                                clean_guests_rooms.csv, clean_bus.csv   (45 complete months)
DSEC_KeyIndicator_{27,127,28}.json + Dataset/DSEC_arrivals_2026_09_supplement.csv
    -> build_arrivals.py     -> data_processed/demand_monthly_arrivals.csv        (225 rows)
Dataset/hotel_occ_total_summary.csv, hotel_Arrival_byHotelStar_summary.csv, Hotel_occ_total.csv
    -> build_hotel_tables.py -> Dashboard/data/hotel_*.csv                        (45 / 180 / 153 rows)
the four year-end MGTO workbooks + the cleaned series + the DSEC / DSAT extracts
    -> build_panels.py       -> data_processed/demand_district_hour_panel_2023_2026.csv (25,920 rows),
                                monthly_panel_2023_01_2026_09.csv (45), quarterly_panel_2023Q1_2026Q3.csv (15)
the four cleaned series + the district x hour panel
    -> 03_panel_build.py     -> data_processed/clean_panel_rebuilt.csv   (compared with the delivered panel)
data_processed/*.csv, *.geojson
    -> sync_dashboard_data.py -> Dashboard/data/*.csv, *.geojson         (MD5 compared, copied when different)
```

The six cleaned files that `01_ingest.py`, `02_clean_series.py` and `03_panel_build.py` write into
`data_processed/` (`clean_inventory.csv`, `clean_arrivals.csv`, `clean_occupancy.csv`,
`clean_guests_rooms.csv`, `clean_bus.csv`, `clean_panel_rebuilt.csv`) are committed to the repository
rather than ignored, for three reasons: the rest of `data_processed/` is committed as well, so a half
ignored directory would be confusing; the six files are small (0.6-4 KB); and `03_panel_build.py` compares
its rebuild against the delivered panel, which only means something if both files are in the tree. They are
derived artifacts, so the chain overwrites them in place from the committed inputs and nothing is lost by
re-running it.

## What each step reads and writes

| order | script | input | output |
| --- | --- | --- | --- |
| 1 | `01_ingest.py` | all raw downloads (MGTO workbooks, DSEC JSON and CSVs, DSAT bus statistics), plus the delivered panels | `data_processed/clean_inventory.csv` |
| 2 | `02_clean_series.py` | `data_processed/demand_monthly_arrivals.csv`, `Dataset/Hotel_occ_total.csv`, `Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv`, `Monthly_Bus_Database/bus_monthly_2020_2026.csv` | `data_processed/clean_arrivals.csv`, `clean_occupancy.csv`, `clean_guests_rooms.csv`, `clean_bus.csv` |
| 3 | `../build_arrivals.py` | `data/dsec_timeseries/DSEC_KeyIndicator_{27,127,28}.json`, `Dataset/DSEC_arrivals_2026_09_supplement.csv` | `data_processed/demand_monthly_arrivals.csv` (225 rows, 2008-01..2026-09) |
| 4 | `../build_hotel_tables.py` | `Dataset/hotel_occ_total_summary.csv`, `Dataset/hotel_Arrival_byHotelStar_summary.csv`, `Dataset/Hotel_occ_total.csv` | `Dashboard/data/hotel_occ_monthly_2023_2026.csv`, `hotel_guests_by_star_2023_2026.csv`, `hotel_occ_history_2014_2025.csv` |
| 5 | `../build_panels.py` | the four year-end MGTO year-to-date workbooks, `data_processed/demand_monthly_arrivals.csv`, the DSEC hotel and DSAT bus extracts | `data_processed/demand_district_hour_panel_2023_2026.csv`, `monthly_panel_2023_01_2026_09.csv`, `quarterly_panel_2023Q1_2026Q3.csv` |
| 6 | `03_panel_build.py` | the four cleaned series, `data_processed/demand_district_hour_panel_2023_2026.csv` | `data_processed/clean_panel_rebuilt.csv` |
| 7 | `../sync_dashboard_data.py` | the 18 panels the dashboard reads | `Dashboard/data/` (copy only when the MD5 differs, then re-hashed) |

`run_all.py` runs steps 1, 2, 3, 4, 6 and 7 in that order and prints the source of each: steps 3-4 are
placed before the panels because the arrivals series and the hotel tables are inputs of the panel and
dashboard stages, not outputs of them. `build_panels.py` (step 5) is deliberately not in `run_all.py`
because it overwrites the three integrated panels; run it directly when those files have to be rebuilt,
which is why it takes its own snapshot first.

Steps 3 and 4 both accept `--check`: they rebuild in memory, compare with the files on disk and write
nothing. On the delivered tree both report a match, so the two series that used to exist only as notebook
cells are now reproducible from the repository alone.

## Which steps need the raw downloads again

- **Needs the raw downloads:** step 1 (it gates them), step 2 (it reads the raw DSEC and DSAT extracts) and
  step 5 (the four year-end MGTO workbooks are the only source of the district x hour table; the other 41 downloads are gated by step 1 but not parsed).
- **Runs from the repository alone:** step 3 (three DSEC JSON snapshots plus the 2026-09 supplement, all
  committed), step 4 (three DSEC extracts committed in `Dataset/`), step 6 (intermediate panels) and
  step 7 (copies of step 5-6 output).

## What each step checks

- **01** inventories the sources and fails if one is missing or if a row count moves: 45 MGTO workbooks,
  225 months of arrivals, 25,920 district x hour rows, 45 monthly panel rows.
- **02** keys every series on the month, cuts it to the analysis window 2023-01..2026-09 and asserts 45
  complete months with no gap, no missing value and a plausible range (arrivals above 300,000; occupancy
  between 0 and 100 per cent).
- **03** asserts the three DSEC snapshots cover the same months, that no arrivals month comes back empty,
  that the rebuild is 225 rows over 2008-01..2026-09, and prints the MD5 before and after writing (the
  previous file is copied to `data_processed/_backup/<stamp>/` first).
- **04** checks each extract before republishing it: exact header (including the repeated `Remark` column
  in `Hotel_occ_total.csv`), row count (45 / 180 / 153), month coverage and the four hotel classes. A
  truncated or re-sorted DSEC export fails here instead of silently changing a chart.
- **05** folds the district x hour table into a monthly district head-count and asserts the grid is
  complete (24 districts x 24 hours x 45 months), merges the modules on the month key and rebuilds the
  monthly panel. It snaps the three panels to `data_processed/_backup/<stamp>/` before overwriting them and
  writes the before / after MD5 to `manifest.csv` next to the snapshot.
- **06** compares all nine numeric series with the delivered `monthly_panel_2023_01_2026_09.csv` and fails
  if any series differs by more than 0.5 per cent, or if a series comes back NaN. With the current inputs
  every series matches to 0.00e+00, so the delivered panel is reproducible from the raw files by this
  chain.
- **07** compares the MD5 of all 18 dashboard inputs against `data_processed/` and copies only the ones that
  differ, then re-hashes the copies to prove that what the dashboard reads is what the chain produced.

## What is still not scripted, and what is

The MGTO workbook extraction **is** scripted. `scripts/build_panels.py` (`build_mgto_master`) reads the four
annual `MacaoDistrictTourismData_{202312,202412,202512,202609}_en.xlsx` workbooks - sheet `1`, header depth
handled per year - and writes the 25,920-row district x hour table. An earlier version of this README said
the parse only existed in the notebook; that is no longer true, and the 45-workbook row count is gated by
step 1 before the parse runs.

What genuinely has no script, and is therefore outside the reach of the checks above:

- `analysis_dataset_master*.csv` - the wide analysis file used for the exploratory work in the notebook.
  Every column it carries is also in `monthly_panel_2023_01_2026_09.csv` or `monthly_detail_2023_01_2026_09.csv`,
  so nothing the report quotes depends on it.
- the stop-to-zone and stop-to-district assignment on the supply side, which was resolved interactively
  against the stop list; `data_processed/stop_district_assignment.csv` is the committed result (586 stops,
  567 matched by point-in-polygon).

The two series that used to be listed here - `demand_monthly_arrivals.csv` and the three hotel tables - are
now built by `build_arrivals.py` and `build_hotel_tables.py` (steps 3 and 4).

Section 3.2.2 and Section 10.7 of the report say the same thing; this file is the version that ships with
the code.

## Requirements

Python 3.11 or newer with pandas, numpy and openpyxl (see `requirements.txt` at the repository root; the
delivered run used Python 3.11.8 with pandas 3.1.1). No network access is needed: every script reads files
already in the repository.
*（内容由AI生成，仅供参考）*
