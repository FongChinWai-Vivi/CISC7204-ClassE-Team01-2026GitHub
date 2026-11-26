---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5480d5b254a487a11b77a101419fe1ce_63cdbec9e95211f1961f525400f8a581
    ReservedCode1: 75RueX0J9xXv39NmLlVLBGCPUMBCHNtRSjj1Vbrto/z/Fab2jt9d/hwrxrzlrdH0uukzN4sBP1VaxgxJ06b6KXL+iI6h2cdxoYF0Pi7Yd277GgychZam/dFqqem+59iH1bICcv2iqputXICELDJNGOc2AhzenvS5LBRyShtGm5ou9gHRW0w2yW9Mebg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5480d5b254a487a11b77a101419fe1ce_63cdbec9e95211f1961f525400f8a581
    ReservedCode2: 75RueX0J9xXv39NmLlVLBGCPUMBCHNtRSjj1Vbrto/z/Fab2jt9d/hwrxrzlrdH0uukzN4sBP1VaxgxJ06b6KXL+iI6h2cdxoYF0Pi7Yd277GgychZam/dFqqem+59iH1bICcv2iqputXICELDJNGOc2AhzenvS5LBRyShtGm5ou9gHRW0w2yW9Mebg=
---

# Figure register - CISC7204 Class E Team 01 Final Report

Built 2026-11-26 (Stage A; re-verified in Stage F against the finished docx and the repository files).
Numbering follows report narrative order. Source files were checked to exist on disk. Colour versions only; no `_gray` variants are used.

Column key: **No.** = figure number printed in the report | **File** = PNG actually embedded in the docx | **Notebook / cell** = where the chart is drawn | **Data source and window** = CSV/GeoJSON read by that cell and the period covered.

| No. | Caption as printed in the report | File | Notebook / cell | Data source and window |
|---|---|---|---|---|
| 1 | Figure 1. Four-week delivery plan, with task tracks and owners. | `figures/fig6_workplan.png` | `notebooks/cisc7204_pipeline_M3_vivi.ipynb`, section 12 | Internal work plan (Table 3); no dataset. Old `figures/` folder: the only copy of this chart, flagged here as required by decision 3. |
| 2 | Figure 2. Monthly visitor arrivals, 2015 to 2026. Shaded bands mark the pandemic years and the 2023-2025 analysis window. | `notebooks/figures/fig01_arrivals_longrun.png` | `notebooks/CISC7204_ClassE_Team01_Visualization_updated.ipynb`, cell 4 | `data_processed/demand_monthly_arrivals.csv` (225 rows, 2008-01 to 2026-09; plotted from 2015); DSEC key indicators 27, 127, 28 plus the 2026-09 supplement. |
| 3 | Figure 3. Correlation matrix of the core series, 2023-01 to 2025-12 (n = 36). | `notebooks/figures/fig_h1_correlation_matrix.png` | cell 8 | `data_processed/monthly_panel_2023_01_2026_09.csv`, filtered to 36 months (2023-01..2025-12). |
| 4 | Figure 4. Arrivals and hotel occupancy, 2023-01 to 2025-12. Panel A plots both series on dual y-axes; Panel B plots the same data as standardised scores (z-scores). | `notebooks/figures/fig02_rq1_coupling.png` | cell 5 | `data_processed/monthly_panel_2023_01_2026_09.csv`, 36 months. |
| 5 | Figure 5. Bus trips per visitor by quarter, 2023Q1 to 2026Q3, with the 2023-2025 regression shown as a reference. | `notebooks/figures/fig04_intensity_decline.png` | cell 8 | `data_processed/quarterly_panel_2023Q1_2026Q3.csv` (15 quarters). |
| 6 | Figure 6. Scatter matrix for arrivals, same-day and overnight arrivals, hotel guests and occupancy, 2023-01 to 2025-12 (n = 36). | `notebooks/figures/fig_h2_scatter_matrix.png` | cell 8 | `data_processed/monthly_panel_2023_01_2026_09.csv` (36 months). |
| 7 | Figure 7. Distribution diagnostics for monthly arrivals: density (Panel A), empirical CDF with the 2026 months placed in-sample (Panel B) and quantile-quantile plot (Panel C). | `notebooks/figures/fig08_distribution_diagnostics.png` | cell 15 | `data_processed/monthly_panel_2023_01_2026_09.csv` (36 months) plus the 9 months of 2026 for Panel B. |
| 8 | Figure 8. Source-market composition of visitor arrivals, 2023 to 2026 (four reported markets; 2026 covers nine months only). | `notebooks/figures/fig09_market_waffle.png` | cell 19 | `Dataset/visitors_2023_2026_by_market_summary.csv` (2023-01 to 2026-09; Korea from 2023 only). |
| 9 | Figure 9. Seasonal shape: monthly pattern of 2023-2025 against the nine months of 2026 (Panel A) and the seasonal index (Panel B). | `notebooks/figures/fig05_seasonality_2026.png` | cell 12 | `data_processed/monthly_seasonality_index.csv` (base 2023-2025) and `monthly_detail_2023_01_2026_09.csv`. 2026 = 9 months, single snapshot, out-of-sample. |
| 10 | Figure 10. Quarterly profile of arrivals, occupancy and bus trips per visitor, 2023Q1 to 2026Q3. | `notebooks/figures/fig06_quarter_profile.png` | cells 10 and 11 | `data_processed/quarterly_panel_2023Q1_2026Q3.csv` (15 quarters; 2026Q1-Q3 are 9-month/partial quarters). |
| 11 | Figure 11. Where visitors are and where the buses are: zone shares of head-count, scheduled departures and stops (Panel A) and the supply-demand ratio (Panel B). | `notebooks/figures/fig02_zone_mismatch.png` | cell 16 | `data_processed/match_zone_supply_demand.csv`, window 2026-01 to 2026-07 (noting the `visitor_headcount_2026H1` column name does not match the seven-month window; disclosed in Section 5.3). |
| 12 | Figure 12. Hourly demand and supply profiles: share of daily head-count against share of weekday and weekend scheduled departures. | `notebooks/figures/fig03_hourly_mismatch.png` | cell 17 | `data_processed/match_hourly_profile.csv`, window 2026-01 to 2026-07; supply from the timetable snapshot, not tracked over 45 months. |
| 13 | Figure 13. Head-count share by the 24 statistical districts, 2023-01 to 2026-09. The choropleth uses the official statistical-zone polygons. | `figures/fig14_district_choropleth.png` | `notebooks/cisc7204_pipeline_M3_vivi.ipynb`, section 15 | `data_processed/district_map_metrics.csv` and `data_processed/macau_stats_zones.geojson` (24 features). Old `figures/` folder: the only copy, flagged here as required by decision 3. |
| 14 | Figure 14. When the ten busiest districts are busy: share of the daily head-count by hour. | `notebooks/figures/fig05b_district_hour_heatmap.png` | cell 18 | `data_processed/demand_district_hour_panel_2023_2026.csv` (25,920 rows = 45 months x 24 districts x 24 h). |
| 15 | Figure 15. Each month of 2026 relative to the same month in 2023-2025 (2023-2025 mean = 100). Nine months only, single snapshot, out-of-sample. | `notebooks/figures/fig07_2026_level_vs_base.png` | cell 14 | `data_processed/monthly_detail_2023_01_2026_09.csv`. Index chart with a truncated, index-based axis; labelled as such in Section 5.2 and Section 7. |
| 16 | Figure 16. Cross-correlation of monthly arrivals and bus trips at lags from -3 to +3 months, 2023-01 to 2025-12. | `notebooks/figures/fig10_lag_crosscorrelation.png` | cell 20 | `data_processed/monthly_panel_2023_01_2026_09.csv` (36 months). |
| 17 | Figure 17. Residuals against fitted values and normal quantile-quantile plot for the arrivals-ridership regression. | `notebooks/figures/fig11_regression_diagnostics.png` | cell 21 | `data_processed/monthly_panel_2023_01_2026_09.csv` (36 months). |
| 18 | Figure 18. The delivered dashboard open in a browser: filter bar with the year, zone and district dropdowns above the KPI row and the first three linked charts. | `Dashboard/preview/00_full_page.png` and `Dashboard/preview/01_filtered_year2024_taipa.png` (cropped to the top of the page) | Not drawn in a notebook; static capture of the built HTML | `Dashboard/CISC7204_ClassE_Team01_Dashboard.html` (6.1 MB, plotly.js inlined), built by `Dashboard/build_dashboard.py` from the 15 CSV files in `Dashboard/data/`. Used as a dashboard illustration only, not as an analytic figure. |

## Notes

- 18 figures, embedded once each. Figures 1-17 carry results or plan content; Figure 18 is a user-interface illustration.
- `notebooks/figures/fig12_dashboard_preview.png` was deliberately **not** used: it is a three-panel screenshot with two twin axes and would be read as an analytic chart (rule in INSTRUCTIONS section 6).
- Two figures (1 and 13) come from the old `figures/` folder because no colour copy exists in `notebooks/figures/`; both are marked as such above (decision 3).
- Old draft figures map to new numbers as follows: draft fig1 -> 2; fig2 -> 11; fig3 -> 12; fig4 -> 5 (plus new 3 and 6); fig5 -> 14; fig6 -> 1. Twelve further figures (3, 4, 6, 7, 8, 9, 10, 13, 15, 16, 17, 18) are new in this report.
- Every figure caption in the report is followed by a source line naming the CSV/source and the notebook cell; the same information is reproduced in Appendix A, Table 16.
*（内容由AI生成，仅供参考）*
