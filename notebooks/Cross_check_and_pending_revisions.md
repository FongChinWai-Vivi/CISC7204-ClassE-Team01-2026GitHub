# Cross-check: Proposal (.docx) vs Notebook (.ipynb)
Project: Visualizing Visitor Arrivals, Hotel Occupancy and Bus Ridership in Macao (CISC7204 Class E Team 01)
Notebook revised: `..._lucas_pending-test_revised.ipynb` (only H1/H2 code changed)

## 1. What was changed in the notebook
| Cell | Change |
|---|---|
| 13 (markdown) | Section 7 intro now states H1 = arrivals~bus, H2 = arrivals~occupancy, H3 = occupancy~bus controlling arrivals (proposal numbering). |
| 14 (code) | H1 now = arrivals vs bus trips (monthly r, quarterly r, verdict). The arrivals vs occupancy verdict is relabelled H2. Report text has separate H1 and H2 sentences. |
| 19 (code) | Scatter matrix is now H1 (arrivals~bus) plus three H2 panels (arrivals, overnight, same-day vs occupancy). Panel titles carry the hypothesis tag. |
| 20 (code) | Coefficient table is relabelled and extended to 6 rows: H1; H2 arrivals/overnight/same-day vs occupancy; overnight/same-day vs hotel guests. Added H2 asymmetry printout. Sensitivity table columns tagged [H1]/[H2]. **Partial-correlation (H3) code, bootstrap function and everything else untouched.** |

Not run: the data paths are `C:\...` on your machine, so outputs of cells 14/19/20 were cleared. Please re-run top to bottom.

## 2. Differences still to settle (proposal vs notebook)
| # | Item | Proposal | Notebook | Action |
|---|---|---|---|---|
| 1 | Hypothesis numbering | H1 arrivals~bus; H2 arrivals~occupancy | was H1 arrivals~occupancy, H2 arrivals~bus | FIXED in revised notebook |
| 2 | Overnight ~ hotel guests | 0.921 | 0.896 | Check window/monthly vs quarterly; fix whichever is wrong |
| 3 | Same-day ~ hotel guests | 0.694 | 0.691 | Same |
| 4 | Occupancy ~ overnight / same-day | 0.861 / 0.891 | 0.828 / 0.887 (old matrix) | Re-run revised cell 20 and update the doc |
| 5 | Taipa-Cotai departures share | 28.4% | 28.68% | Align |
| 6 | Peninsula departures share | 66.6% | 66.42% | Align |
| 7 | Coloane supply/demand ratio | 2.99 | 2.94 | Align |
| 8 | Night (00-05) weekday supply share | 2.1% | 3.58% | Largest gap; check definition (weekday only? hours?) |
| 9 | Supply source | DSAT timetable, 586 stop records | "GTFS-derived stop departures" | Use one name |
| 10 | Use of 2026 | "never used for a correlation or seasonal index" | Section 10 builds a 2026 seasonal index and Spearman test | Reword proposal as out-of-sample robustness check, or drop |
| 11 | Heatmap districts | top 10 | top 12 | Align |
| 12 | Summary table label (cell 42) | - | still says "Pairwise support for H2/H3" | Optional: rename to H1/H2 |

## 3. Pending: in proposal, missing or weak in notebook
- Overnight vs same-day **KDE** (T8). Notebook KDE shows bus trips per visitor instead.
- **Plotly Dash** dashboard: only a static preview; `dash` not installed in kernel.
- **Seasonal index with trend removed** (T7). Notebook uses own-year-mean index.
- Optional hotel room supply (dataset 3.5) as control variable: in descriptives only.
- 2024-2025 pooled coefficient (r = 0.470 in doc): not in sensitivity table.

## 4. Pending: not in the proposal, recommended
- **H3 result** (partial r = 0.179, p = 0.296: link largely explained by arrivals) should be written into the report.
- Trend risk: add first-difference or detrended correlations.
- Use block bootstrap (monthly data is autocorrelated); partial-correlation p should use df = n-3.
- OLS: arrivals p = 0.079, occupancy p = 0.303, collinear; do not interpret coefficients separately.
- Replace hard-coded `C:\` paths with relative paths for reproducibility.
- Final check: confirm every number in the report equals the re-run notebook output.
