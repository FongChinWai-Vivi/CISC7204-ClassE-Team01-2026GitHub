---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5480d5b254a487a11b77a101419fe1ce_60b9741be95211f1961f525400f8a581
    ReservedCode1: W4Xg3/ByzfT5P2Reqzy8umXgFJdXUuVIL7Ft83nuZyf6vGMdzS703h3od88zJDendHzB4YtcpUL2sWvtgjtS6j/qOfE6gpzDRbIZu4WYMMddwFEePdQ3fGQ6K9+nbr4Mg3hxtgh4b8wgFoC3WYrMunYMXgBJolTVyM1DZg5T7Fzlau/tvK2upyKqx5o=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5480d5b254a487a11b77a101419fe1ce_60b9741be95211f1961f525400f8a581
    ReservedCode2: W4Xg3/ByzfT5P2Reqzy8umXgFJdXUuVIL7Ft83nuZyf6vGMdzS703h3od88zJDendHzB4YtcpUL2sWvtgjtS6j/qOfE6gpzDRbIZu4WYMMddwFEePdQ3fGQ6K9+nbr4Mg3hxtgh4b8wgFoC3WYrMunYMXgBJolTVyM1DZg5T7Fzlau/tvK2upyKqx5o=
---

# Final checklist - CISC7204 Class E Team 01 final report

Generated 2026-11-26. Report revised in place: `Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx` (4,124,376 bytes). Backup of the untouched original: `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx` (705,834 bytes). Nothing outside the docx and `_temp` was written; no dataset, notebook, code, figure or other docx was modified; no git write command was issued.

---

## 1. Estimated page count

| Estimator | Result |
|---|---|
| Section-by-section content estimate (words 16,413 + 18 figures + 18 tables) | **about 43 pages** (front matter 2.0; §1 1.7; §2 1.8; §3 3.2; §4 15.6; §5 3.1; §6 0.8; §7 5.3; §8 3.4; §9 3.3; §10 2.8) |
| Pessimistic row-by-row table estimate (every table row charged a full 11 pt line) | **about 53-58 pages** |

**Format patch (2026-11-26):** the body default in `styles.xml` was raised from 10.5 pt (`w:sz` 21) to 11 pt (`w:sz` 22), so the page count is expected to grow by roughly **1-2 pages**; keep **43 pages as the working figure and 50 as the ceiling**.

**Spacing and cross-reference patch (2026-11-26):** paragraph spacing was tightened (body `after` 10 to 6 pt; Heading 1/2/3 `before` 20/15/12 to 12/10/8 pt and `after` 9/6/5 to 6/4/4 pt; `SourceLine` and `Caption` held at 6 pt; the 18 figure paragraphs at 3 pt above and below) and the 6 blank cover spacers were deleted, which removes roughly **1.5-2 pages** net. Section 7 now uses cross-references (`Figure N (shown in Section X.Y).`) instead of reprinting figures: all 18 figures are already printed in 2.3, 4.2-4.7, 5.1 and 9.4, so reprinting them in section 7 would duplicate about 18 figure blocks (roughly 8-10 pages), repeat the same images under the same numbers, and make the list of figures ambiguous; the 17 section 7 blocks therefore only point at where each picture is printed. Net effect: the working figure can fall from 43 to about 41-42 pages; **43 stays as the working number and 50 as the ceiling** until the real count is read in Word. The 7 empty paragraphs in front of sections 6-10 were kept because they carry the page breaks.

**Cover rollback (2026-11-26):** 封面空段已恢复，间距收紧不含封面. All 8 blank front-cover spacers were restored byte-for-byte from `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_crossref_spacing_2026-11-26.docx`, so the cover layout is again identical to the original and the 1.5-2 page saving applies to the body only.


The two estimators diverge because Word may wrap long table cells and paragraphs differently from any static model. Treat **43 pages as the working figure and 50 as the ceiling**; the real count can only be read after the TOC field is refreshed in Word. Section 4 is the heavy section (14 figures, 6 tables) - if the real count exceeds 50, trim 4.3 and 4.6 first (the weakest figures are already discussed as weak in 5.2 and section 7, so text can be shortened without losing evidence).

**Suggested action:** open the docx, press Ctrl+A then F9 (update all fields), read the page count on the status bar, and compare with 50.

## 2. All TODO items, grouped by who must fill them

### 2.1 You (the report owner)

| # | Location | Text | What to do |
|---|---|---|---|
| 1 | §4.1 deliverables table | `[TODO: confirm - whether a separate presentation deck is part of the submission; the only deck in the repository is the introductory-video deck]` | Decide whether a separate slide deck exists / is required; either delete the TODO or name the deliverable |
| 2 | §9.6 expected outputs | `TODO: confirm - the locked instruction states 13 checks and 4 INFO; the file contains 12 rows with 3 INFO` | Confirm the QA count (see §9 below) and delete the TODO |
| 3 | Appendix D open items | `TODO: confirm - whether the cover date should be updated for the final submission` | The cover still says "Submission date: 5 November 2026"; change it or leave it deliberately |
| 4 | Appendix D open items | `TODO: verify - publisher and place of publication for Cairo (2019) How Charts Lie` | Add "W. W. Norton & Company, New York" only if you verify it; otherwise keep the TODO |
| 5 | Appendix D open items | `TODO: confirm - QA count discrepancy: source file has 12 checks with 3 INFO, the locked description says 13 with 4 INFO` | Duplicate of item 2; resolve together |
| 6 | §10.6 References, Cairo entry | `[TODO: verify - publisher and place of publication]` | Same as item 4 |

### 2.2 Teammate (Dash app owner - FONG CHIN WAI per the roles table)

| # | Location | Text | What to do |
|---|---|---|---|
| 7 | §9.2 environment statement | `dash TODO: confirm - the teammate maintaining the Dash app must fill the dash version` | Insert the dash version actually used; delete the TODO |
| 8 | Appendix D open items | `TODO: confirm - dash version for the reproducibility statement` | Same value as item 7 |

### 2.3 Each member (own reflection)

| # | Member | Section | What to do |
|---|---|---|---|
| 9 | SONG ZHUOXI | 8.2.1 | Read and edit your reflection |
| 10 | KONG KIN MENG | 8.2.2 | Your text was inserted verbatim; check the light formatting only |
| 11 | KUAN CHI KIT | 8.2.3 | Read and edit your reflection |
| 12 | XIAN QILAN | 8.2.4 | Read and edit your reflection |
| 13 | FONG CHIN WAI | 8.2.5 | Read and edit your reflection |
| 14 | FONG HIO LAM | 8.2.6 | Read and edit your reflection |
| 15 | All six | §10.5 GenAI Use Statement | `TODO: members confirm review` - replace with a confirmation sentence once everyone has read their reflection |

**Please tell the team:** five of the six reflections (all except KONG KIN MENG's) were drafted by the AI assistant from the roles recorded in the docx and from project facts. They contain no invented incidents, but each member must rewrite their own text in their own voice before submitting.

## 3. Cover page: before and after

Original text of the first eight paragraphs (from the backup copy):

1. University of Macau
2. Faculty of Information Science and Computing
3. CISC7204: Data Science and Data Visualization
4. Class E (2026-2027 Semester 1)
5. **Team Project Proposal**
6. Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao
7. Group name: Class E - Team 01
8. Submission date: 5 November 2026

Change made - one phrase only:

| Item | Before | After |
|---|---|---|
| Paragraph 5 | `Team Project Proposal` | `Team Project Final Report` |

Unchanged: 14 pt size, bold, centring, spacing, the logo, the member/student-ID table, paragraphs 1-4, the project title, the group name, the submission date. **Suggestion (not applied):** the date still reads 5 November 2026, which was the proposal deadline.

## 4. Figure list with sources

| No. | Caption (short) | File | Notebook cell | Data source / window |
|---|---|---|---|---|
| 1 | Four-week delivery plan (Gantt) | `figures/fig6_workplan.png` (old folder - only copy) | `cisc7204_pipeline_M3_vivi.ipynb`, section 12 | Team plan, no dataset |
| 2 | Long-run monthly arrivals, 2015-2026 | `notebooks/figures/fig01_arrivals_longrun.png` | `Visualization_updated.ipynb` cell 4 | `demand_monthly_arrivals.csv`; 2015-01..2026-09 |
| 3 | Correlation matrix of the core series | `fig_h1_correlation_matrix.png` | cell 8 | `monthly_panel_2023_01_2026_09.csv`; 2023-01..2025-12, n = 36 |
| 4 | Arrivals vs occupancy: dual axis (A) and z-scores (B) | `fig02_rq1_coupling.png` | cell 5 | `monthly_panel_2023_01_2026_09.csv`; n = 36 |
| 5 | Bus trips per visitor by quarter | `fig04_intensity_decline.png` | cell 8 | `quarterly_panel_2023Q1_2026Q3.csv`; 2023Q1..2025Q4 analysed |
| 6 | Scatter matrix of the three series | `fig_h2_scatter_matrix.png` | cell 8 | `monthly_panel_2023_01_2026_09.csv`; n = 36 |
| 7 | Distribution diagnostics (density, ECDF, QQ) | `fig08_distribution_diagnostics.png` | cell 15 | `monthly_panel_2023_01_2026_09.csv`; n = 36 |
| 8 | Source-market composition | `fig09_market_waffle.png` | cell 19 | `Dataset/visitors_2023_2026_by_market_summary.csv`; 2023-01..2026-09 |
| 9 | Seasonal shape and seasonality index | `fig05_seasonality_2026.png` | cell 12 | `monthly_seasonality_index.csv`, `monthly_detail_2023_01_2026_09.csv`; base 2023-2025, 2026 = 9 months |
| 10 | Quarterly profile | `fig06_quarter_profile.png` | cells 10-11 | `quarterly_panel_2023Q1_2026Q3.csv`; 15 quarters |
| 11 | Zone demand vs scheduled supply shares | `fig02_zone_mismatch.png` | cell 16 | `match_zone_supply_demand.csv`; 2026-01..2026-07 |
| 12 | Hourly demand vs supply, weekday and weekend | `fig03_hourly_mismatch.png` | cell 17 | `match_hourly_profile.csv`; 2026-01..2026-07 |
| 13 | 24 statistical districts (choropleth) | `figures/fig14_district_choropleth.png` (old folder - only copy) | `cisc7204_pipeline_M3_vivi.ipynb`, section 15 | `district_map_metrics.csv`, `macau_stats_zones.geojson`; 2023-12 and 2026 |
| 14 | Ten busiest districts by hour | `fig05b_district_hour_heatmap.png` | cell 18 | `demand_district_hour_panel_2023_2026.csv`; 2023-01..2026-09 |
| 15 | Each 2026 month against the 2023-2025 base | `fig07_2026_level_vs_base.png` | cell 14 | `monthly_detail_2023_01_2026_09.csv`; 9 months, single snapshot, out-of-sample |
| 16 | Cross-correlation of arrivals and ridership, lags -3..+3 | `fig10_lag_crosscorrelation.png` | cell 20 | `monthly_panel_2023_01_2026_09.csv`; n = 36 |
| 17 | Regression diagnostics | `fig11_regression_diagnostics.png` | cell 21 | `monthly_panel_2023_01_2026_09.csv`; n = 36 |
| 18 | Dashboard illustration (cropped, not an analytic figure) | `Dashboard/preview/00_full_page.png` and `01_filtered_year2024_taipa.png`, cropped | not from a notebook | `CISC7204_ClassE_Team01_Dashboard.html` |

Tables 1-17 are numbered in narrative order and each is referenced in the text. `notebooks/figures/fig12_dashboard_preview.png` was deliberately **not** used (it carries two twin axes inside a screenshot).

## 5. Visual-to-member mapping used

| Module / stream | Lead | Support | Section 7 blocks |
|---|---|---|---|
| M1 Visitor arrivals | KONG KIN MENG | SONG ZHUOXI | KONG KIN MENG: 7.2 (Figures 2, 9, 15); SONG ZHUOXI: 7.1 (Figures 1, 8) |
| M2 Hotel occupancy | KUAN CHI KIT | XIAN QILAN | KUAN CHI KIT: 7.3 (Figures 3, 4, 17); XIAN QILAN: 7.4 (Figures 6, 7, 10) |
| M3 Bus ridership, master pipeline, dashboard | FONG CHIN WAI | FONG HIO LAM | FONG CHIN WAI: 7.5 (Figures 5, 11, 13, 16); FONG HIO LAM: 7.6 (Figures 12, 14) |
| Interpretation | XIAN QILAN | - | inside 7.4, referenced from 5.1 |
| Relationship analysis | KUAN CHI KIT | - | inside 7.3, referenced from 4.3 |

Basis: the roles table already in the docx (module lead/support, analyst, reporter). Git history was not used as evidence and is not cited. Every member owns at least two figures; Figure 18 is treated as a shared dashboard illustration. The mapping is phrased as responsibility under a team role, never as proof that a named person produced a specific file.

## 6. Old-to-new content map

| Draft section | New location |
|---|---|
| 1 Project Title and Research Question | 1.1 Topic and Research Questions |
| 2 Project Purpose | 1.2 Purpose and Scope |
| 3 Data Context (3.1-3.7) | 1.3 Data Context + 3.2.1 Acquisition + 3.2.2 Cleaning + 3.2.3 Integration and QA |
| 4 Project Tasks and Deliverables (T1-T10) | 3.1 Task Breakdown + 4.1 Delivered / Not delivered |
| 5 Success Criteria | 2.2 Success Criteria (corrected) |
| 6 Team Collaboration | 3.3 Team Structure and Roles + 6 Division of Work |
| 7 Timeline | 2.3 Four-Week Plan and Planned-versus-Actual |
| GenAI Use Statement | 10.5 |
| References (14) | 10.6 (15 entries) |
| results scattered in 1 / 3 / 4 | 4.2-4.7 |
| one limitation sentence in 1 | 5.1-5.3 |
| - (new) | 7.1-7.6, 8.1-8.2, 9.1-9.8, 10.1-10.4 |

T1-T10: T1 -> 3.2.2, T2 -> 3.2.3, T3 -> 4.2/4.3, T4 -> 4.2 (Figure 2), T5 -> 4.3 (Figure 4), T6 -> 4.3 (Figures 3, 6, 16, 17), T7 -> 4.4, T8 -> 4.3, T9 -> 3.2.6 + 4.1 + 7.5/7.6 + 9.4/9.5, T10 -> 2.3 + 4.1.

Draft Figure 1-6 -> new Figures 2, 11, 12, 5 (plus 3 and 6), 14 and 1. Full detail in `old_to_new_content_map.md`.

## 7. Sections added or changed

**Added:** real TOC field on page 2 with update-on-open; Heading 1/2/3 styles in `styles.xml`; §2.3 planned-versus-actual; §3.2 methodology with six sub-steps; §4.2-4.7 results; §5.1-5.3 discussion, limitations and disclosed defects; §6 division-of-work table; §7 six storytelling blocks; §8 collective and personal learning; §9 eight-step manual; §10.1-10.4 appendices (figure register, data dictionary excerpts, code excerpts, QA table and open items).

**Changed:** cover paragraph 5; success criteria; the dashboard description (no hour slider, no shared time axis claim, no CSV claim); the version statement; §1 scope and data table; §3 roles table kept but re-typeset; §2.2 criterion on row counts; GenAI statement (one sentence appended); References (Cairo added, all reformatted to APA 7).

**Deleted:** the "5 meeting minutes" deliverable and its success criterion; the "hour slider" claim; "opens from local CSV in 5 s"; "Python 3.11 / pandas 3.1 / Matplotlib 3.11"; the "36 monthly / 12 quarterly rows" criterion as written.

## 8. Numbers changed relative to the draft

| Quantity | Draft | Now |
|---|---|---|
| Data coverage | 45 months one place, 43 another, "36 monthly rows" criterion | 45 months 2023-01..2026-09; analysis window 36 months 2023-01..2025-12 |
| Quarters | 12 (criterion) | 15 delivered, 12 analysed |
| Plotly | 5.22.0 | bundled plotly.js v3.5.0 (HTML); plotly 6.7.0 (environment); README marked outdated |
| Python / pandas / matplotlib | 3.11 / 3.1 / 3.11 | 3.14.6 / 3.0.3 / 3.11.0 |
| 2025 head-count vs arrivals | not reconciled | 40,045,669 vs 40,069,360; delta 23,691 (0.06%) |
| Coloane demand share | 1.7 % | 1.67 % |
| Taipa & Cotai departure share | 28.7 % | 28.68 % |
| Zone/hour match window | unstated | 2026-01..2026-07 (column named `visitor_headcount_2026H1`) |
| QA checks | 13 checks / 4 INFO | 12 checks: 9 PASS / 3 INFO / 0 WARN / 0 FAIL |
| Dashboard controls | hour slider + shared time axis | 4 dropdowns (year, zone, district, map metric) + Play + Reset; 16 linked charts |
| Meeting minutes | 5 | removed |
| Figures | 6 | 18 |
| References | 14 | 15 |

**Unchanged and re-verified:** H1 r = 0.759 (n = 36) / 0.917 (n = 12); H2 r = 0.913 (n = 36) / 0.970 (n = 12); H3 partial r = 0.179, p = 0.296 (n = 36, df = 33); occupancy-overnight 0.861, occupancy-same-day 0.891; guests-overnight 0.921, guests-same-day 0.694; occupancy-ridership raw 0.741; per-year H1 0.818 / 0.254 / 0.625; 25,920 rows; 586 stops; 91 routes; Peninsula 42.23 % / 66.42 % / ratio 1.573; Taipa & Cotai 56.10 % / 28.68 % / ratio 0.511; Coloane ratio 2.940; 00:00-05:59 = 20.2 % demand vs 3.6 % weekday supply; top district 43.96 %; top three 62.43 %-62.6 % as printed by the source; HHI 2,229.

## 9. QA count discrepancy (must be resolved)

`data_processed\qa_report.csv` contains **12 data rows** with status counts **9 PASS / 3 INFO / 0 WARN / 0 FAIL**. The locked instruction says 13 checks with 4 INFO, and `reports\data_dictionary.md` is internally inconsistent (it writes "12 x 4, 12 PASS / 4 INFO" in one section and "9 PASS / 4 INFO / 0 WARN / 0 FAIL" in another). The report states the file's own numbers and discloses the conflict. Someone must confirm whether a thirteenth check was intended and never appended.

## 10. What you must verify by hand

1. **Update the TOC in Word** (Ctrl+A, F9, or right-click the field -> Update Field -> entire table). The AI cannot compute page numbers; the field is inserted and `updateFields` is set, but Word must do the layout.
2. **Real page count.** Static estimates range 43-58 pages; confirm the actual count is within 50 and adjust if it is not.
3. **Run the manual (section 9) on your own machine** - `python scripts/build_panels.py`, the pipeline notebook, `Visualization_updated.ipynb`, `python Dashboard/build_dashboard.py`, `python Dashboard/app.py`. The AI checked the steps statically only; it did not execute anything.
4. **Member review of the five AI-drafted reflections** (all except KONG KIN MENG's).
5. **Dash version** for the reproducibility statement.
6. **Cairo (2019) publisher and place of publication**, if the reference is to be completed.
7. **QA count** 12/3 versus 13/4.
8. **Cover date**: "5 November 2026" is still the proposal date.
9. **Whether a separate presentation deck is part of the submission.**
10. **Git state before you commit:** `git status` should show only the edited docx and `_temp`. The `notebooks` timestamp 2026-11-26 02:01 predates this run (03:02) and was not produced by it.
11. **Word count and section balance:** §4 carries 14 figures and 6 tables; if a reviewer finds it heavy, shorten 4.3 and 4.6 text rather than removing figures that the section 7 blocks analyse.
12. **Check that no grayscale figure slipped in** - only colour files are referenced.

## 11. Files produced in `_temp`

| File | Content |
|---|---|
| `figure_register.md` | 18 figures, report number / caption / file / notebook cell / data source and window |
| `outline.md` | Ten-section plan, 68 actual Heading 1/2/3 paragraphs, per-section page estimates and method |
| `old_to_new_content_map.md` | Draft -> new mapping including T1-T10, draft Figures 1-6, deleted claims and verbatim-kept text |
| `visual_to_member_mapping.md` | M1/M2/M3 plus interpretation and relationship analysis, with the three limits on what the mapping claims |
| `progress_log.md` | Original file plus appended Stage A-F log: reading, artefacts, cover before/after, per-stage page estimates, defect table, QA discrepancy, mapping summary, numbers changed, TODOs |
| `final_checklist.md` | This file |
| `backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx` | Untouched original |

No file was deleted. `_temp` is intact.
*（内容由AI生成，仅供参考）*
