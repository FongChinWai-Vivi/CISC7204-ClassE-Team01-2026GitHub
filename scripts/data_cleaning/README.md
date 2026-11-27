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

| order | script | input | output |
| --- | --- | --- | --- |
| 1 | `01_ingest.py` | all raw downloads (MGTO workbooks, DSEC JSON and CSVs, DSAT bus statistics), plus the delivered panels | `data_processed/clean_inventory.csv` |
| 2 | `02_clean_series.py` | `demand_monthly_arrivals.csv`, `Dataset/Hotel_occ_total.csv`, `Dataset/DSEC_hotel_guests_rooms_2023_01_2026_09.csv`, `Monthly_Bus_Database/bus_monthly_2020_2026.csv` | `data_processed/clean_arrivals.csv`, `clean_occupancy.csv`, `clean_guests_rooms.csv`, `clean_bus.csv` |
| 3 | `03_panel_build.py` | the four cleaned series and `data_processed/demand_district_hour_panel_2023_2026.csv` | `data_processed/clean_panel_rebuilt.csv` |

## What each step checks

- **01** inventories the sources and fails if one is missing or if a row count moves: 45 MGTO workbooks,
  225 months of arrivals, 25,920 district x hour rows, 45 monthly panel rows.
- **02** keys every series on the month, cuts it to the analysis window 2023-01..2026-09 and asserts 45
  complete months with no gap, no missing value and a plausible range (arrivals above 300,000; occupancy
  between 0 and 100 per cent).
- **03** folds the district x hour table into a monthly district head-count, asserts the grid is complete
  (24 districts x 24 hours x 45 months), merges the modules on the month key and rebuilds the monthly
  panel. It then compares all nine numeric series with the delivered
  `monthly_panel_2023_01_2026_09.csv` and fails if any series differs by more than 0.5 per cent. With the
  current inputs every series matches to 0.00e+00, so the delivered panel is reproducible from the raw
  files by this chain.

## What is not scripted

Two steps stay in `notebooks/cisc7204_pipeline_M3_vivi.ipynb` and are not reproduced here:

- the extraction of the district x hour table from the 45 bilingual MGTO workbooks (notebook section 2) -
  the workbooks change header depth between years and the Chinese and English sheets are not aligned, so
  the parse is kept where it can be inspected cell by cell. It is not left unchecked: step 3 re-derives the
  monthly total from that table and matches it against the delivered panel.
- the stop-to-zone and stop-to-district assignment on the supply side, which was resolved interactively
  against the stop list.

Section 3.2.2 and Section 10.7 of the report say the same thing; this file is the version that ships with
the code.

## Requirements

Python 3.11 with pandas and numpy (see the pinned `requirements.txt` at the repository root). No network
access is needed: every script reads files already in the repository.
