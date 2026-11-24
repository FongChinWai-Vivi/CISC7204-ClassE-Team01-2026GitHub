# Cross-check: proposal, notebooks and data_processed

Project: *Is Macau's transport keeping up with its visitors?* (CISC7204 Class E Team 01)
State recorded: **2026-11-24**, after the consistency revision. Every "current value" below was recomputed from
the CSV files in `data_processed/` on that date, not copied from an earlier draft.

Artifacts compared:

| Artifact | Role |
| --- | --- |
| `Proposal/CISC7204_ClassE_Team01_Proposal.docx` (+ `.pdf` re-exported 2026-11-24) | the written deliverable |
| `notebooks/CISC7204_ClassE_Team01_Visualization_updated.ipynb` | Figures 1-16 and the H1-H3 tests (25 code cells, executed top to bottom, 0 errors, 0 unexecuted) |
| `notebooks/cisc7204_pipeline_M3_vivi.ipynb` | cleaning, integration, Figures 1-6 of the proposal (40 code cells, all outputs stored) |
| `notebooks/cisc7204_proposal_figures_colour.ipynb` | the original colour set of the six proposal figures |
| `data_processed/*.csv` | the single source of every number below |

## 1. Table 1 — quarterly extremes

The old text took the first and last quarters of the window and called them the extremes. They are not: the
series turns inside the window, so the endpoints are neither the minimum nor the maximum.

| Item | Was (wrong) | Current value | Source | Status |
| --- | --- | --- | --- | --- |
| Quarterly arrivals | "4.95 to 10.40 million (2025Q4)", i.e. the first and last quarters presented as the range extremes | **4.95 million in 2023Q1 (low) rising to 10.45 million in 2025Q3 (high)**; 2025Q4 is 10.40 million, i.e. inside the range | `quarterly_panel_2023Q1_2026Q3.csv`, column `visitor_arrivals_sum` | Fixed in the docx (Section 3), PDF re-exported with Word COM |
| Hotel occupancy, quarterly | 74.9% (2023Q1) to 89.9% (2025Q4) as the range | **74.9% in 2023Q1 (low) and 90.2% in 2025Q1 (high)**; 2025Q4 is 89.9% | `quarterly_panel_2023Q1_2026Q3.csv`, column `hotel_occ_avg_pct` | Fixed |
| Bus trips per visitor, quarterly | 9.96 to 5.83 with "a 41% decline", i.e. the last quarter quoted as the low | **9.9637 in 2023Q1 falling to 5.5595 in 2025Q3 (the true low); 5.8254 in 2025Q4**; the text now reads "a decline of 41 to 44 per cent", so both the endpoint and the low are stated | `quarterly_panel_2023Q1_2026Q3.csv`, column `bus_trips_per_arrival` | Fixed |
| Average daily bus trips | 549,000 (2023Q1) to 659,000 (2025Q4) | confirmed: **549,200 to 658,600 daily**, and 2025Q4 is also the maximum | `quarterly_panel_2023Q1_2026Q3.csv`, column `bus_daily_avg_trips_wan_mean` | Checked, no change needed |
| Table 1 body rows | — | 2025Q4 keeps its own published values (10.40 / 89.9% / 5.83) | same CSVs | Correct as printed; only the narrative sentence was wrong |

## 2. Correlation coefficients

All correlations are Pearson on the 36-month core window (2023-01 to 2025-12, n = 36) unless marked quarterly
(n = 12). The window is fixed in the notebook, so a re-run cannot drift.

| Item | Was | Current value | Source | Status |
| --- | --- | --- | --- | --- |
| Overnight arrivals ~ hotel guests | proposal 0.921 vs notebook 0.896 | **r = 0.921 (p = 1.9e-15)** | `monthly_panel` joined with `demand_monthly_arrivals` (overnight = arrivals - same-day) | Fixed: the 0.896 came from a quarterly aggregation |
| Same-day arrivals ~ hotel guests | 0.694 vs 0.691 | **r = 0.694 (p = 2.7e-06)** | same join | Fixed |
| Occupancy ~ overnight / same-day arrivals | 0.861 / 0.891 vs 0.828 / 0.887 | **r = 0.861 (p = 1.6e-11) and r = 0.891 (p = 3.2e-13)** | same join, occupancy = `hotel_occ_pct` | Fixed in the notebook's coefficient table |
| Arrivals ~ bus ridership | - | **r = 0.759 monthly (p = 8.2e-08), r = 0.917 quarterly (p = 2.7e-05)** | `monthly_panel` / `quarterly_panel` | Confirmed by re-run |
| Arrivals ~ occupancy | - | **r = 0.913 monthly (p = 7.8e-15), r = 0.970 quarterly (p = 1.9e-07)** | same | Confirmed by re-run |
| Occupancy ~ bus ridership, raw | - | **r = 0.741** | `monthly_panel` | Confirmed by re-run |
| Occupancy ~ bus ridership, controlling for arrivals | missing from the report | **partial r = 0.179, p = 0.296 (df = n - 3 = 33)** | residuals of both series on arrivals, 36 months | Added to proposal, README and notebook Section 9 |
| By-year stability of arrivals ~ bus | 0.818 / 0.254 / 0.625 | unchanged | `monthly_panel`, year subsets | Confirmed |

## 3. Zone and hourly shares (2026-01..2026-07 matching window)

The matching layers are frozen to that window, so the shares below are reproducible.

| Item | Was | Current value | Source | Status |
| --- | --- | --- | --- | --- |
| Taipa & Cotai share of scheduled departures | 28.4% | **28.68% (28.7% in the text)** | `match_zone_supply_demand.csv`, `departures_share_pct` | Fixed |
| Peninsula share of scheduled departures | 66.6% | **66.42% (66.4% in the text)** | same file | Fixed |
| Coloane supply-to-demand ratio | 2.99 | **2.940** | same file, `supply_demand_ratio` | Fixed |
| Taipa & Cotai ratio | - | **0.511** | same file | Confirmed |
| Demand per departure, Taipa & Cotai vs Peninsula | - | **203 vs 66** | same file, `demand_per_departure` | Confirmed |
| Weekday 00:00-05:59 supply share | proposal 2.1% vs notebook 3.58% | **3.584% (3.6%)**, against **20.2%** of demand in the same hours | `match_hourly_profile.csv`, `supply_share_weekday_pct` and `demand_share_pct` summed over hours 0-5 | Fixed: the 2.1% was the average per hour, the 3.6% is the six-hour total |
| Heatmap districts | proposal "top ten" vs notebook "top 12" | **ten busiest districts**, one row each, rescaled to the district's own total | `match` district-hour panel; notebook Figure 12 | Fixed: the notebook now uses the same ten districts |
| Supply source wording | "DSAT timetable, 586 stop records" vs "GTFS-derived stop departures" | **"DSAT GTFS timetable (stop-level records)"** everywhere | proposal Section 2, notebook provenance stamps | Fixed: one name for one file |

## 4. Hypothesis numbering and where each test runs

| Item | Was | Current state | Source | Status |
| --- | --- | --- | --- | --- |
| Numbering | notebook had H1 = arrivals ~ occupancy, H2 = arrivals ~ bus | **H1 arrivals ~ bus ridership; H2 arrivals ~ hotel occupancy; H3 occupancy ~ bus ridership controlling for arrivals**, matching the proposal | notebook Section 9; README "H1-H3 at a glance" | Fixed |
| H1 / H2 location | - | Section 7, code cell 7 (H1 monthly and quarterly; H2 monthly and quarterly) | notebook, counted from 1 | Documented |
| H3 location | - | Section 9, code cell 11: partial correlation plus bootstrap percentile interval | notebook | Documented |
| Pipeline notebook | no mention of H1-H3, which reads like "no test was done" | a markdown note after Section 1 points to both notebooks and cells; no code or output changed | `cisc7204_pipeline_M3_vivi.ipynb`, cell 5 | Fixed |
| Figure 5 registry label | "Pairwise support for H2/H3" | **"Pairwise support for H1-H3"** | notebook Section 17 summary table | Fixed |

## 5. Figures and cell references

| Item | Was | Current state | Status |
| --- | --- | --- | --- |
| README Figure-to-cell table | cells 4 / 6 / 8 / 10 / 12 / 14 | **code cells 19-24** of the pipeline notebook (Figures 1-6 of the proposal) | Fixed |
| README notebook size | "81 cells" | **81 cells, of which 40 are code** (80 before this revision; the note added after Section 1 makes it 81) | Fixed |
| README long-horizon window | "2015-2026" | **2015-01 to 2026-09** (the DSEC series starts in 2008; the long line runs to 2026-09) | Fixed |
| README quarterly extremes | 4.95 to 10.40, 74.9% to 89.9% | the corrected extremes of section 1 above | Fixed |
| Unnumbered panels in the visualisation notebook | 5 panels had no figure number | **Figures 1-16, one label per figure, increasing with the section order** (previously Figure 4 appeared in section 8, Figures 2-3 after sections 12-13) | Fixed |
| Machine paths | the visualisation notebook carried `C:\` paths for its inputs | derived with `pathlib` from the notebook's own location, with a walk-up fallback; the run log now prints the figure folder as a repository-relative path | Fixed |

## 6. Repository hygiene

| Item | Was | Current state | Status |
| --- | --- | --- | --- |
| `.gitignore` | only `~$*` | also `extension/`, `__pycache__/`, `*.py[cod]`, `.ipynb_checkpoints/`, `temp/`, `temp_nbrun.*` | Fixed |
| `extension/` | untracked dataset drop folder | still ignored, never staged | Fixed |

## 7. Open items (not fixed in this revision)

These are deliberately left out of this commit; none of them contradicts a number in the proposal.

1. **Consolidated analysis report.** The proposal carries the argument; there is no separate long-form report
   file in `reports/` yet (`data_coverage_audit_2026-11-04.md` and `data_dictionary.md` are data documents).
2. **Meeting minutes M2-M7.** Only the 1st meeting minutes PDF is in `minutes/`.
3. **Grayscale variants of the figures.** A grayscale check exists inside the notebook (Section 16) but no
   separate grayscale figure set is published.
4. **Static dashboard hosting.** `Dashboard/` runs locally (`app.py`, Dash build) and a static HTML preview is
   committed; there is no public URL.
