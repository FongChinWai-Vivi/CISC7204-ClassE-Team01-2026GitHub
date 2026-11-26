---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5480d5b254a487a11b77a101419fe1ce_6ac43661e95211f1961f525400f8a581
    ReservedCode1: 52npDHkEDPDCXKN/1YRiYaPED+oc/ACAeevXtwfXucUj8KDjM5cZO7PnEd1Khv0vzWkg1xSIe6VTZSwb5nV84lyoESEjfts0jazDb2muMJSfEsTxMRkIPQK7QIxHA3DrK4QLTYf+CuuOPJRDZp29wTSPAvl5bk9exLf9tR+NQ4jxV+A1a47ktw4ZL7o=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5480d5b254a487a11b77a101419fe1ce_6ac43661e95211f1961f525400f8a581
    ReservedCode2: 52npDHkEDPDCXKN/1YRiYaPED+oc/ACAeevXtwfXucUj8KDjM5cZO7PnEd1Khv0vzWkg1xSIe6VTZSwb5nV84lyoESEjfts0jazDb2muMJSfEsTxMRkIPQK7QIxHA3DrK4QLTYf+CuuOPJRDZp29wTSPAvl5bk9exLf9tR+NQ4jxV+A1a47ktw4ZL7o=
---





# Progress Log

Step 0 done - inventory saved

## Step 0 clarification round (user answers, 2026-11-26)

Decisions locked (source: user chat replies):

| # | Topic | Decision |
|---|---|---|
| 1 | Base document | FinalReport.docx and Proposal.docx are byte-identical copies (705,834 B); FinalReport.docx is the working base |
| 2 | Chart source notebook | notebooks/Visualization_updated.ipynb is authoritative; lucas_pending_test is superseded |
| 3 | Figure assets | Use notebooks/figures/ (not the old Proposal figures/ set) |
| 4 | Figure numbering | Follow report narrative order; notebook figure numbers to be remapped |
| 5 | Analysis window | H1-H3 on 2023-01..2025-12 (n=36 months, 12 quarters); 2026 used only for seasonal pattern |
| 6 | 2026 data | May appear if labelled: 9 months, single snapshot, out-of-sample |
| 7 | District layer | 24-district analysis presented as a separate section (different system from DSEC arrivals) |
| 8 | Limitation wording | Allowed to state bus ridership includes residents and district headcount is a sample |
| 9 | Environment versions | Do not present per-member environment differences; one reproducibility statement only |
| 10 | Meeting briefs / slides | Not delivered; remove or soften those deliverables in the report |
| 11 | Dashboard description | Describe as self-contained offline HTML with 4 dropdown filters + Play years + 16 linked Plotly charts; NO hour slider claim |
| 12 | Git author name | Canonical: "Fong Chin Wai (Vivi)" |
| 13 | Grayscale figures | Do not use _gray.png variants |
| 14 | Data citation date | Confirmed 2026-11-26: cite retrieval date "Retrieved November 4, 2026" (APA 7); state coverage to 2026-09 in the data table |
| 15 | Known errors | 4 defects confirmed (see below); no further errors found |

Confirmed defects to fix in the final report:
1. "hour slider" claimed in draft (paras 62, 264, 317) but no slider exists in Dashboard/app.py or the built HTML (0 <input>, 0 type=range).
2. Month-count contradiction: data_processed/phase1_usability_verdict.csv says 43 months (2026-11-04), qa_report.csv says 45 (2026-11-08); physical data 25,920 rows = 45 months x 24 districts x 24 h -> 45 is correct, 43 is stale.
3. Plotly version mismatch: README declares plotly 5.22.0, but the built HTML inlines plotly.js v3.5.0.
4. 2025 headcount reconciliation gap: total_headcount 40,045,669 vs arrivals sum 40,069,360 (delta 23,691) - must be disclosed.

Additional read-only facts verified for the dashboard section:
- Dashboard/CISC7204_ClassE_Team01_Dashboard.html: 6,426,206 B, self-contained (0 external script src, 0 link), opens offline by double-click.
- app.py controls: 4 dcc.Dropdown (selYear/selZone/selDistrict/selMetric), 2 buttons (btnPlay/btnReset), 1 dcc.Interval (playTick, 1700 ms), 5 callbacks; no Slider/RangeSlider/Tabs/RadioItems/Checklist.
- data_processed/qa_report.csv: 13 checks -> 9 PASS, 4 INFO, 0 WARN, 0 FAIL.
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*

---

# Writing run log (Stage A-F, 2026-11-26)

Appended; nothing above this line was overwritten. Run started 03:02. The report was edited directly in this run; no approval was requested between stages.

## Reading completed before writing (INSTRUCTIONS section 0.2)

| File | What it contributed to the report |
|---|---|
| `cisc7204-Class_E-Team_01_WorkPlan01.docx` / `.pdf`, `WorkPlan02.docx` / `.pdf` | Four-week schedule, task allocation and the planned-versus-actual table in 2.3 and Table 3; plan chart Figure 1 |
| `reports\data_dictionary.md` (v1.0, 2026-11-22) | Module ownership (M1 KONG KIN MENG, M2 KUAN CHI KIT, M3 FONG CHIN WAI), row/column counts of every cleaned output, exclusion rules E-M1-1..E-M3-9, and the documented gaps (2026-04..09 `buses_in_service` blank, operator split only 2026-07..09, 19 stops outside official polygons, crowd data only routes 3 and AP1). These became Appendix B excerpts and 5.2 limitations. |
| `reports\data_coverage_audit_2026-11-04.md` | Confirms coverage to 2026-09 and 15 quarters; explains that each MGTO file is year-to-date, so only the last file of each year (202312 / 202412 / 202512 / 202609) may be used - otherwise 160,704 duplicate rows and quarterly totals 4-5x too high. This is the basis of the YTD de-duplication paragraph in 3.2.2. It also reports correlations on n = 15 (0.9455 arrivals-bus, 0.9722 arrivals-occupancy); those are the 45-month coverage figures and are **not** used in 4.3, which quotes the 36-month window (n = 12 quarterly: 0.917 and 0.970). Both windows are labelled wherever they appear. |
| `notebooks\Cross_check_and_pending_revisions.md` | Names `Visualization_updated` as the cross-checked notebook; supplies the final H1-H3 statistics and the per-year stability coefficients reused in 4.3; used to confirm that H3 is computed with df = 33 (n = 36). |
| `README.md` | Run order, key numbers, the statement that some panels came from exploratory steps not saved as scripts, and the outdated environment block (pandas 2.2.2, plotly 5.22.0, dash 4.4.1). Reflected in 9.3, 9.7 and 10.4. |
| `Dashboard\README.md`, `Dashboard\README_Dashboard.md` | Interaction inventory of the built HTML (Year / Zone / District / map-metric dropdowns, Play years auto-cycle at 1.7 s, reset, legend highlight, 16 Plotly containers), the 36-month convention, the HHI convention, and the plotly.min.js bundling statement. Used for 3.2.6 and 9.4; confirms there is no hour slider. |

Cross-check against the locked decisions: no conflict found except the QA row count (see "Defects" below), which is disclosed rather than silently changed.

## Stage A - planning artefacts (saved before any docx edit)

- `_temp\figure_register.md` - 18 figures in report order with report number, caption, file, notebook and cell, data source and window.
- `_temp\outline.md` - the ten-section structure of INSTRUCTIONS section 5, the 68 Heading 1/2/3 paragraphs actually in the file, per-section page estimates and the estimation method.
- `_temp\old_to_new_content_map.md` - draft section -> new section, T1-T10 -> new location, draft Figure 1-6 -> new figure number, and the list of deleted claims.
- `_temp\visual_to_member_mapping.md` - M1/M2/M3 plus interpretation and relationship analysis, lead/support per the docx roles table, 17 of the 18 figures distributed (Figure 18 treated as a shared dashboard illustration).
- Page projection at Stage A: 44 planned, about 42-43 estimated. Below the 45-page stop line, so writing continued without asking.

## Cover page (recorded before the change)

Original text of the first eight paragraphs of the backup copy
`_temp\backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx`:

1. University of Macau
2. Faculty of Information Science and Computing
3. CISC7204: Data Science and Data Visualization
4. Class E (2026-2027 Semester 1)
5. Team Project Proposal
6. Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao
7. Group name: Class E - Team 01
8. Submission date: 5 November 2026

Change made (one phrase, paragraph 5 only):

| Item | Before | After |
|---|---|---|
| Document type line | `Team Project Proposal` | `Team Project Final Report` |

Font, size (14 pt), alignment, spacing, bold flag, the logo, the member table with student IDs, the university/faculty/course lines, the project title and the submission date are unchanged. The submission date still reads "5 November 2026" (the proposal date); it was **not** guessed - it is listed as a suggestion in `final_checklist.md`.

## Stage B - sections 1-3 and 6

- Rebuilt the heading system: Heading 1/2/3 defined in `styles.xml` (Times New Roman, 16 / 13 / 12 pt, outline levels 0/1/2), replacing the single custom style used for every title in the draft.
- Inserted a real TOC field (`TOC \o "1-3" \h \z \u`) on page 2 and set `updateFields` in `settings.xml` so Word refreshes it on open; page numbering suppressed on page 1 via `titlePg`.
- Body text set to Times New Roman 11 pt, line spacing 1.15, margins 2.5 cm (1417 twips each side).
- Section 1: topic, RQ1/RQ2, H1-H3, purpose and scope, data context table with sources, coverage and "Retrieved November 4, 2026".
- Section 2: goals; success criteria corrected (45 months / 15 quarters delivered, 36 / 12 analysis window, meeting-minutes criterion deleted); four-week plan as Figure 1 and Table 3 with a planned-versus-actual column.
- Section 3: T1-T10 table; methodology 3.2.1-3.2.6 written only from what the notebooks and scripts do, each step citing file or cell; roles table kept verbatim.
- Section 6: per-member duties table from the docx roles, matching Section 7 assignments.
- Saved. Cumulative page estimate at Stage B: about 9-10 pages (front matter + sections 1, 2, 3, 6).

## Stage C - sections 4 and 5

- 4.1 delivered/not delivered table, including the honest entries: no hour slider, no separate presentation deck confirmed, meeting-minutes deliverable removed.
- 4.2 long-run context (Figure 2, Table 8); 4.3 RQ1 with H1-H3 (Figures 3, 4, 6, 16, 17; Tables 9-11); 4.4 RQ2 seasonality (Figures 9, 10, Table 12); 4.5 zone and hour mismatch (Figures 11, 12, Table 13); 4.6 24-district layer (Figures 13, 14, Table 14); 4.7 2026 out-of-sample (Figure 15).
- Every coefficient carries n and period; every 2026 chart carries "9 months (Jan-Sep), single snapshot, out-of-sample".
- Section 5: association-not-causation, five limitations, and the disclosed-defects table.
- Saved. Cumulative page estimate at Stage C: about 28 pages.

## Stage D - section 7

- Six member blocks in the order of the visual-to-member mapping, one figure group each; each block gives figure number, caption, data source, key finding, then Truthful / Functional / Beautiful / Insightful scored against named elements (axis labels, scale, baseline, colour, annotation, legend, title).
- Weak points stated where they exist: dual axis in Figure 4 Panel A versus the z-score Panel B, the index-based truncated axis in Figure 15, three denominators on one percentage axis in Figure 11, and the plan chart Figure 1 used only as a schedule illustration.
- Saved. Cumulative page estimate at Stage D: about 33-34 pages.

## Stage E - sections 8, 9, 10

- 8.1 collective lessons drawn only from evidence (cross-check findings, the four defects, YTD de-duplication, dual-axis and baseline lessons, partial correlation, reproducibility).
- 8.2.1-8.2.6 personal reflections, 150-250 words each. 8.2.2 KONG KIN MENG is the supplied text inserted as-is with light formatting; the other five were drafted from the roles table and project facts and must be reviewed by each member.
- 9.1-9.8 manual: folder structure, single environment statement, run order, opening the HTML dashboard, rebuilding and running the Dash port, expected outputs, gaps (no requirements file, empty "Data cleaning" folder, exploratory steps not saved as scripts), and the explicit status sentence "Checked statically against the files by the AI agent. The team ran Visualization_updated.ipynb end-to-end in the stated environment."
- 10.1-10.6: figure register, data dictionary excerpts, code excerpts, QA table and open items, GenAI Use Statement (existing text kept, one sentence added about AI drafting and the draft reflections), References (14 kept, Cairo 2019 added = 15).
- Saved. Cumulative page estimate at Stage E: about 42-43 pages.

## Stage F - verification

- Numbers re-checked one by one against `data_processed\monthly_panel_2023_01_2026_09.csv`, `quarterly_panel_2023Q1_2026Q3.csv`, `match_zone_supply_demand.csv`, `match_hourly_profile.csv`, `district_map_metrics.csv`, `annual_summary_2023_2026.csv`, `monthly_seasonality_index.csv`, `qa_report.csv`, `phase1_usability_verdict.csv` and the stored outputs of `Visualization_updated.ipynb` cells 5, 8, 12, 14, 15, 16, 17, 18, 20, 21. The 2026-09 arrivals figure (32,181,272) is confirmed by the supplement row documented in the data dictionary; the DSEC JSON files stop at 2026-08, and the report states that the ninth month comes from the single-row 2026-09 supplement.
- Figure numbering: Figures 1-18 appear once each in narrative order; Table 1-17 likewise; every figure and table is referenced in the text; every figure carries a source line.
- `docx` integrity: the package opens, 19 drawing elements (1 cover logo + 18 figures), 18 tables, 372 paragraphs, TOC field and `updateFields` present.
- `git status` shows only the edited docx and the files in `_temp` from this run. The `notebooks` modification timestamp 2026-11-26 02:01 predates the run start (03:02) and was not caused by this run; nothing under `notebooks`, `data_processed`, `figures`, `Dashboard` or `scripts` was touched, and no git write command was issued.
- Page count: two static estimators disagree (about 42-43 pages by section content, about 55-58 pages if every table row is charged a full line). The true count can only be read after the TOC field is updated in Word; this is the first item in `final_checklist.md`.

## Defects: what was fixed, what was disclosed

| # | Defect | Action |
|---|---|---|
| 1 | "hour slider" claimed in the draft | Removed. Dashboard described as four dropdown filters + Play + Reset + 16 linked charts; the hour dimension is carried by Figures 12 and 14. |
| 2 | 43 versus 45 months | 45 months / 25,920 rows stated; the stale "(43 months)" label in `phase1_usability_verdict.csv` noted in 10.4. |
| 3 | Plotly version | Bundled plotly.js v3.5.0 reported for the HTML, plotly 6.7.0 for the team environment, README's 5.22.0 marked outdated in 10.4. |
| 4 | 2025 reconciliation gap | 40,045,669 head-count versus 40,069,360 arrivals, difference 23,691 (0.06%), disclosed in 4.6 and 5.3. |
| 5 | Success criteria 36 / 12 versus delivered 45 / 15 | Criterion rewritten; both windows labelled in every table. |
| 6 | QA row count | See below - the locked description and the file disagree; disclosed with a highlighted TODO. |
| 7 | "5 meeting minutes" deliverable and criterion | Deleted, not replaced; minutes are mentioned nowhere in the report. |
| 8 | "opens from local CSV" | Replaced: static HTML is self-contained; `app.py` reads baked JSON. |
| 9 | Version claims "Python 3.11, pandas 3.1, Matplotlib 3.11" | Replaced by the single reproducibility statement of decision 14. |
| 10 | Coloane 1.67 % versus 1.7 % | 1.67 % used everywhere. |
| 11 | Time window of `match_zone_supply_demand.csv` | The column is named `visitor_headcount_2026H1` but the window is 2026-01..2026-07 (seven months); figures and tables say 2026-01..07 and the column-name mismatch is disclosed in 10.4. |
| 12 | DSEC JSON ends 2026-08, monthly arrivals run to 2026-09 | Source of the ninth month identified (single-row supplement `DSEC_arrivals_2026_09_supplement.csv`, 3,216,535) and stated in 1.3 and 3.2.1. |

### QA row count - confirmed discrepancy

`data_processed\qa_report.csv` was read directly: **12 data rows**, columns `check, value, status, note`, status counts **9 PASS / 3 INFO / 0 WARN / 0 FAIL**. The locked instruction and `reports\data_dictionary.md` both describe 13 checks with 4 INFO (the data dictionary even writes "12 PASS / 4 INFO" in one place and "9 PASS / 4 INFO / 0 WARN / 0 FAIL" in another). The report therefore states 9 PASS / 3 INFO / 0 WARN / 0 FAIL and discloses the conflict in 9.6 and 10.4 with a highlighted TODO. The team must confirm whether a 13th check was intended and never appended to the file.

## Old-to-new mapping (summary; full table in `old_to_new_content_map.md`)

| Draft | New |
|---|---|
| 1 Project Title and Research Question | 1.1 |
| 2 Project Purpose | 1.2 |
| 3 Data Context (3.1-3.7) | 1.3 + 3.2.1-3.2.3 |
| 4 Project Tasks and Deliverables (T1-T10) | 3.1 + 4.1 |
| 5 Success Criteria | 2.2 |
| 6 Team Collaboration | 3.3 + 6 |
| 7 Timeline | 2.3 |
| GenAI Use Statement | 10.5 |
| References | 10.6 |
| (results scattered in 1/3/4) | 4.2-4.7 |
| (one limitation sentence) | 5.1-5.3 |
| - | 7.1-7.6, 8.1-8.2, 9.1-9.8, 10.1-10.4 (new) |

Draft Figure 1-6 -> new Figures 2, 11, 12, 5 (+3, 6), 14 and 1 respectively; 12 figures are new.

## Numbers changed relative to the draft

| Quantity | Draft | Now | Why |
|---|---|---|---|
| Months of data | 45 in one place, 43 in another, "36 monthly rows" as a criterion | 45 months of coverage (2023-01..2026-09), 36-month analysis window | 43 was stale; criterion corrected |
| Quarters | 12 as a criterion | 15 delivered, 12 analysed | same |
| Grid rows | 25,920 (unchanged) | 25,920 = 45 x 24 x 24 | consistent |
| Plotly version | 5.22.0 | bundled plotly.js v3.5.0; environment plotly 6.7.0 | README mismatch disclosed |
| pandas / Python / matplotlib versions | pandas 3.1, Python 3.11, Matplotlib 3.11 | pandas 3.0.3, Python 3.14.6, matplotlib 3.11.0 | single team statement |
| 2025 head-count vs arrivals | not reconciled | 40,045,669 vs 40,069,360, delta 23,691 | disclosed |
| Coloane demand share | 1.7 % | 1.67 % | one rounding style |
| Taipa & Cotai departure share | 28.7 % | 28.68 % | one rounding style |
| Zone-hour window | not stated | 2026-01..2026-07 (column named 2026H1) | verified against the CSV |
| QA checks | 13 checks / 4 INFO | 12 checks / 9 PASS / 3 INFO | file read directly |
| Dashboard controls | "hour slider, shared time axis" | 4 dropdowns + Play + Reset, no slider | no slider in code or HTML |
| Meeting minutes | 5 presented | removed | not to be mentioned |
| References | 14 | 15 (Cairo 2019 added) | INSTRUCTIONS section 7 |
| Figures | 6 | 18 | narrative renumbering |

Coefficients that did **not** change: H1 r = 0.759 (n = 36) and 0.917 (n = 12); H2 r = 0.913 (n = 36) and 0.970 (n = 12); H3 partial r = 0.179, p = 0.296 (n = 36, df = 33); overnight-occupancy 0.861, same-day-occupancy 0.891; overnight-guests 0.921, same-day-guests 0.694; occupancy-bus raw 0.741; per-year H1 0.818 / 0.254 / 0.625.

## Open items left as highlighted TODO

1. Dash version for the reproducibility statement (teammate).
2. QA count 12/3 versus 13/4 (user or teammate).
3. Cairo (2019) publisher and place (user, if it should be completed).
4. Whether a separate presentation deck is part of the submission (user).
5. Whether the cover submission date should change (user).
6. Members confirming they reviewed their own reflection (each member).
7. TOC page numbers must be refreshed in Word (user).

No number was invented; anything unverifiable was written as a TODO and listed here and in `final_checklist.md`.


---

## Format patch - 2026-11-26 (after Stage F, body formatting only)

Two edits were applied to the report docx. **No text was added, deleted or reworded.**

### Patch 1 - body default size 10.5 pt -> 11 pt

`word/styles.xml`, `w:docDefaults/w:rPrDefault/w:rPr`:

| Element | Before | After |
|---|---|---|
| `w:sz` | 21 (10.5 pt) | 22 (11 pt) |
| `w:szCs` | 21 (10.5 pt) | 22 (11 pt) |

Only the two values inside `docDefaults` were changed. Heading 1/2/3, Caption, SourceLine, TblText and every other style keeps its explicit size (the other 34 `w:sz` values in `styles.xml` are byte-identical), and no run-level `w:rPr/w:sz` in `word/document.xml` was touched.

### Patch 2 - the tenth TODO was not highlighted

In the section 4.1 deliverables table the presentation-deck TODO was a single run with no `w:highlight`. `<w:highlight w:val="yellow"/>` was inserted into that run's `w:rPr`, after `w:szCs`, which is the schema-correct position. Text of that run is unchanged, including the brackets.

| Item | Before | After |
|---|---|---|
| `<w:highlight w:val="yellow"/>` occurrences in `word/document.xml` | 9 | 10 |
| Highlight colours present | yellow only | yellow only |
| TODO markers in the body text | 10 | 10 |

### Validation after the patch (package reopened with zipfile + ElementTree)

| Check | Result |
|---|---|
| `docDefaults` size | `22` / `22` (11 pt) |
| Highlight runs | 10, all `yellow` |
| TOC field `TOC \o "1-3" \h \z \u` | present |
| `w:updateFields` in `settings.xml` | present |
| Tables | 18 (unchanged) |
| `wp:extent` drawings | 19 = 1 cover logo + 18 report figures (unchanged) |
| Heading 1/2/3 paragraphs | 68 (unchanged) |
| Body text | concatenated `w:t` identical to the pre-patch copy: 110,959 characters, 16,059 words, 10 TODO markers |
| Parts changed inside the package | `word/document.xml` and `word/styles.xml` only |
| XML well-formedness | `document.xml`, `styles.xml`, `settings.xml` all parse cleanly |
| File size | 4,124,397 bytes (was 4,124,376) |

Pre-patch snapshot kept at `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_format_patch_2026-11-26.docx` (4,124,376 bytes). The untouched original proposal backup is unchanged.

### Page-count effect

Raising the body default from 10.5 pt to 11 pt adds roughly **1-2 pages** over the whole document. Keep **43 pages as the working figure and 50 as the ceiling** in `final_checklist.md`; the real count still has to be read in Word after the TOC field is refreshed.

### Method note

`python-docx` is not installed and neither is `pywin32`, so the patch was made with the standard library (`zipfile` + text/XML handling) and every check above is a static package inspection. Word was not launched, so no layout, pagination or field result was produced here. No git write command was issued.
*（内容由AI生成，仅供参考）*

---

## Stage G - Section 7 cross-references and document-wide spacing tightening (2026-11-26, formatting only)

Reviewer feedback: section 7 names every figure but never says where the figure is printed, and the body carried a 10 pt paragraph gap with 20/15/12 pt heading space throughout.

### 1. Cross-references in section 7

Pre-change snapshot: `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_crossref_spacing_2026-11-26.docx` (4,124,397 bytes, identical to the file before this stage).

Each visual block in section 7 opened with `Figure N. <caption>. *Source: ...*` while the picture itself is printed in another section. The number was changed to `Figure N (shown in Section X.Y).` and nothing else in the block was touched (caption, Source, Key finding and the four analysis paragraphs are byte-identical).

Section numbers were taken from the Heading 1/2 numbering that actually precedes each `<w:drawing>` in this document, not from any plan or from `figure_register.md`:

| Figure | Printed in | Figure | Printed in | Figure | Printed in |
|---|---|---|---|---|---|
| 1 | 2.3 | 7 | 4.3 | 13 | 4.6 |
| 2 | 4.2 | 8 | 4.3 | 14 | 4.6 |
| 3 | 4.3 | 9 | 4.4 | 15 | 4.7 |
| 4 | 4.3 | 10 | 4.4 | 16 | 5.1 |
| 5 | 4.3 | 11 | 4.5 | 17 | 5.1 |
| 6 | 4.3 | 12 | 4.5 | - | - |

**17 blocks, not 18.** Section 7 contains 17 figure blocks (Figure 1 to Figure 17). Figure 18 is the dashboard screenshot and is printed once, in 9.4 (`Opening the dashboard`); section 7 has no block for it, so no 18th parenthetical exists. Section 7's lead-in sentence still says "The 18 figures are numbered in the order in which they are first used", which remains true for the document even though only 17 blocks are walked through there; that sentence was left untouched.

### 2. Spacing (format only, no text change)

| Target | Before | After |
|---|---|---|
| `docDefaults` `w:spacing` | `after=200` (10 pt), `line=276` | `after=120` (6 pt), `line=276` kept |
| `Heading1` | `before=400 after=180` | `before=240 after=120`, `line=276` kept |
| `Heading2` | `before=300 after=120` | `before=200 after=80`, `line=276` kept |
| `Heading3` | `before=240 after=100` | `before=160 after=80`, `line=276` kept |
| `Figure` style (the 18 drawing paragraphs) | `before=120 after=0` | `before=60 after=60`, `line=240` kept |
| `SourceLine` style | `before=0 after=120` | `before=0 after=60` |
| `Caption` style | `before=120 after=60` | unchanged, already at 60 |
| `TblText` style | `before=0 after=0` | unchanged, table cells left alone |

Explicit paragraph-level overrides that fought the new defaults were normalised, keeping each `w:line` value:

- 52 `Body11` paragraphs with `after=60 line=264` to `before=0 after=120 line=264`
- 18 `Caption` paragraphs with `before=60 after=10` to `before=60 after=60`
- 18 `SourceLine` paragraphs with `before=0 after=170` to `before=0 after=60`
- 9 `SourceLine` paragraphs with `before=40 after=140` to `before=40 after=60`

### 3. Empty paragraphs

There are exactly 13 empty paragraphs outside table cells, but only 6 of them are really blank (cover spacers at paragraph indices 0, 1, 2, 9, 11, 27). The other 7 consist solely of `<w:r><w:br w:type="page"/></w:r>` and are the section breaks in front of 6, 7, 8, 9 and 10; deleting them would merge those sections onto the same page, so they were kept. The 6 cover spacers were removed. Paragraph count 1,084 to 1,078.

### 4. Static verification

| Check | Result |
|---|---|
| `(shown in Section X.Y)` parentheticals | 17, each section number matching the section where that figure is actually printed (0 mismatch) |
| Body text vs pre-change copy | after stripping the 17 parentheticals the concatenated `w:t` is identical: 110,959 characters both sides |
| Character count | 110,959 to 111,350 (+391, i.e. only the cross-references) |
| Paragraph count | 1,084 to 1,078 |
| Empty non-table paragraphs | 7 left, all of them page-break carriers |
| `docDefaults` spacing | `after=120 line=276` |
| Heading spacing | H1 240/120, H2 200/80, H3 160/80, all `line=276` |
| Tables / drawings / Heading 1-2-3 | 18 / 19 / 68 (unchanged) |
| TOC field and `w:updateFields` | present |
| Highlight runs | 10 |
| Package | 47 parts, `testzip` clean, `document.xml`/`styles.xml`/`settings.xml` well-formed |
| Parts changed | `word/document.xml` and `word/styles.xml` only |
| File size | 4,124,372 bytes (was 4,124,397) |

### 5. Page-count effect

The tighter spacing removes roughly **1.5-2 pages**; the cross-references add about 400 characters (about a fifth of a page) and add no figures. Working figure 43 pages can drop to about 41-42, but `final_checklist.md` keeps 43 as the working number and 50 as the ceiling until Word reports the real count.

### Method note

`python-docx` and `pywin32` are still unavailable, so this stage used the standard library (`zipfile` with the original `ZipInfo` order, timestamps and compression preserved) and every number above is a static package inspection. Word was not launched: pagination and the TOC field result were not produced here. No git write command was issued.

## Stage H - Cover block rollback (2026-11-26)

The previous stage deleted 6 blank paragraphs inside the front cover to tighten the layout. That broke `INSTRUCTIONS.md` section 2 ("keep the cover layout as it is"), so the whole cover block was restored from the pre-patch snapshot.

| Item | Value |
|---|---|
| Source of the restored block | `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_crossref_spacing_2026-11-26.docx` |
| Range restored | paragraphs 0 to the first paragraph carrying `w:br w:type="page"` (inclusive) |
| Cover paragraphs | 30 (matches backup) |
| Blank cover paragraphs | 8 (matches backup; the 6 deleted spacers plus the two page-break carriers) |
| Last cover paragraph | page break present, so the TOC still starts on page 2 |
| Cover text | character-for-character identical to the backup, including `Team Project Final Report`; no `Team Project Proposal` remains |
| Body paragraphs | 1,054 after the cover (matches backup) |
| Body text delta vs backup | +391 characters, entirely the 17 `(shown in Section X.Y)` cross-reference notes (34 diff lines = 17 pairs) |
| Totals | 1,084 paragraphs, 111,350 characters, 18 tables, 19 drawings, 68 Heading runs, 10 highlight runs, 17 cross-references |
| Styles | docDefaults `after` 120; H1 240/120; H2 200/80; H3 160/80; all `line` 276 kept; TOC field and `updateFields` intact |
| Package | 47 parts, `testzip` clean |

Only `word/document.xml` changed in this stage; `styles.xml`, `settings.xml` and every other part are byte-identical to the previous stage. `python-docx` and `pywin32` are still unavailable, so this is a static package check: Word was not launched and no pagination was produced. No git write command was issued.
