---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_6ae1ee8dd84011f19232525400248c00
    ReservedCode1: exiRMLT8bWnP9qeMsJzXPV6kmEGgCXAruhRT8Zr1ccY9kHFdpV6wHRGXhKDOt0X+WV3CfmWR3rcNsd0Q3xH68SuPiuaVq7kQq3J70uuGhf/OiwtlaFdfkDIZhG9aNan54d/dJFpey0eG6ZUuYGJMotmwfYzn7wBv2oWxwLb2oHfLmJi8oO4oPCpushg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_6ae1ee8dd84011f19232525400248c00
    ReservedCode2: exiRMLT8bWnP9qeMsJzXPV6kmEGgCXAruhRT8Zr1ccY9kHFdpV6wHRGXhKDOt0X+WV3CfmWR3rcNsd0Q3xH68SuPiuaVq7kQq3J70uuGhf/OiwtlaFdfkDIZhG9aNan54d/dJFpey0eG6ZUuYGJMotmwfYzn7wBv2oWxwLb2oHfLmJi8oO4oPCpushg=
---

# Monthly Bus Database - Macau public bus

Built 2026-11-04. Owner: Fong Chin Wai (mc653748) / Fong Hoi Lam (mc654953).

## What this folder is

A tidy, reproducible monthly database for Macau public bus demand and supply. It extends
`data_processed/supply_official_series.csv` (monthly fleet and stop counts, annual ridership only)
with a true monthly ridership series, so demand and supply can be analysed at the same frequency.
Every monthly ridership number is traceable to an official DSAT artefact listed in `source_index.csv`.

## Files

| File | Content |
|---|---|
| `bus_monthly_2020_2026.csv` | Core tidy table: 81 monthly observations, 2020-01 to 2026-09 |
| `bus_annual_reference_2011_2025.csv` | Official DSAT annual totals and daily averages 2011-2025, plus reconciliation against the monthly series |
| `bus_monthly_by_operator_2026.csv` | 2026 monthly daily average by operator (New Welfare / TCM) with market share |
| `bus_monthly.sqlite` | Same data as four tables: `bus_monthly`, `annual_reference`, `monthly_by_operator_2026`, `source_index` |
| `source_index.csv` | Provenance per artefact: DSAT quarterly PDF URL, coverage window, as-of date |
| `raw_pdfs/` | 26 archived DSAT quarterly statistics PDFs (2020Q1 to 2026Q2), unmodified |

## Field dictionary (`bus_monthly_2020_2026.csv`)

| Field | Meaning | Unit / note |
|---|---|---|
| `month` | YYYY-MM | primary key |
| `days_in_month` | calendar days | used to expand daily averages |
| `daily_avg_trips_wan` | DSAT published daily average ridership | 10k trips per day, official figure as published |
| `daily_avg_trips` | same in absolute terms | trips per day = `daily_avg_trips_wan` x 10000 |
| `monthly_trips_est` | monthly estimate | `daily_avg_trips` x `days_in_month` |
| `buses_in_service`, `bus_stops` | fleet and stop counts | joined from `supply_official_series.csv`, coverage 2019-01 to 2026-03 |
| `trips_per_bus_per_day` | daily load per bus | `daily_avg_trips` / `buses_in_service` |
| `visitor_arrivals`, `same_day_arrivals` | monthly visitor arrivals | from `demand_monthly_arrivals.csv`, coverage to 2026-08 |
| `trips_per_arrival` | bus intensity per visitor | `monthly_trips_est` / `visitor_arrivals` |
| `dsat_minfu_daily_wan`, `dsat_tcm_daily_wan` | per-operator daily average | 2026 only |
| `source` | provenance string | identifies the exact DSAT artefact |

## Method

1. Probed the DSAT quarterly statistics PDF series `https://www.dsat.gov.mo/pdf/statistics/<year>/<quarter>/tc/1.pdf`
   for 2011Q1 to 2026Q4. Archived files exist only for **2020Q1 to 2026Q2** (26 PDFs, all kept in `raw_pdfs/`).
2. Parsed the section "X nian mei yue ba shi ri jun zai ke liang" (monthly daily average ridership) from every PDF,
   handling both single-line and multi-block 12-month grids. Where a month appears in several PDFs, the latest
   quarterly file wins. 2026-07, 2026-08 and 2026-09 come from the live DSAT monthly table.
3. Joined the ridership series with the local monthly fleet/stop series and monthly visitor arrivals.
4. Reconciled the monthly series against DSAT official annual daily averages (table below).

## Reconciliation: monthly series vs official annual

Weighted monthly mean (weight = `days_in_month`) compared with DSAT official annual daily average:

| Year | Official daily avg (10k) | Months in series | Computed from monthly | Abs diff |
|---|---|---|---|---|
| 2020 | 45.47 | 12 | 45.47 | 0.001 |
| 2021 | 52.94 | 12 | 52.94 | 0.003 |
| 2022 | 46.16 | 12 | 46.16 | 0.003 |
| 2023 | 58.69 | 12 | 58.69 | 0.003 |
| 2024 | 62.47 | 12 | 62.48 | 0.006 |
| 2025 | 63.60 | 12 | 63.59 | 0.005 |

All diffs are within 0.01 (10k trips per day), i.e. rounding level. 2026 is a partial year (9 months) and
is therefore excluded from `annual_reference`.

## Known limits - do not over-claim

- **Monthly ridership exists only from 2020-01.** DSAT does not publish monthly ridership before 2020 and the
  pre-2020 quarterly PDFs are no longer served at that archive URL. 2011-2019 therefore stays annual only.
- `monthly_trips_est` is a **derived estimate** (published daily average x calendar days), not an official
  monthly total. Annualising it can drift from the official annual total by roughly 1 percent (for example
  2025: 2.32 yi estimated vs 2.31 yi official) because each month's daily average is rounded to 2 decimals.
- Fleet and stop supply stop at 2026-03, the last official local month; supply columns are blank after that.
- Visitor arrivals run to 2026-08, so `trips_per_arrival` is blank for 2026-09.
- The per-operator split is available for 2026 only.
- 2026-07 to 2026-09 come from the live web table (page updated 2026/11/4); DSAT may revise recent months.

## Regenerating

Source scripts sit outside this folder, in the session temp directory:
`probe_dsat.py` (probe and download PDFs), `parse_dsat2.py` (PDF parsing), `build_monthly_db.py`
(join, export, README). Re-running the three scripts in that order rebuilds this folder.
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
