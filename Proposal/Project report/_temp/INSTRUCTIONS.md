# INSTRUCTIONS - FINAL REPORT (WRITING RUN)

Team 01, Class E, CISC7204, University of Macau.
Topic: "Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao".
Deadline: 2026-12-05 11:00 pm. Each member submits the PDF personally (not your job).

## 0. Read first

1. Read Proposal\Project reporttemp\progress_log.md (locked decisions) and _temp\project_inventory.md (evidence). They override your assumptions.
2. Before writing, also read the files the inventory did not summarize: WorkPlan01/02 (docx+pdf) in the repo root, reports\data_dictionary.md, reports\data_coverage_audit_2026-11-04.md, notebooks\Cross_check_and_pending_revisions.md, README.md, Dashboard\README*.md. Add what you learn to the progress log. (Meeting minutes are NOT to be mentioned in the report; you may skip them.)



## 1. Paths and permissions

- Root: C:\Users\user\Documents\cisc7204\Project\Github\CISC7204-ClassE-Team01-2026GitHub
- Edit ONLY: Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx (working copy, no backup needed).
- You may create/update files only inside Proposal\Project reporttemp Do NOT delete _temp until I approve the end of Stage F.
- Never modify datasets, notebooks, code, figures, other docx files. Never run notebooks in place.
- Git: read-only (git log, git status, git diff). No commit/push/reset/checkout/stash.
- No emails, secrets or passwords in the report.
- Use python-docx or an equivalent safe method. Preserve the existing tables, images and team information. If the file is locked, tell me to close Word. Do not pip install into the system. If a package is missing, ask me.



## 2. COVER PAGE (page 1): LIMITED EDIT ALLOWED

Page 1 may now be edited, but only minimally:

- Change the document-type wording from "Proposal" to "Final Report" (for example "Team Project Proposal" becomes "Team Project Final Report"), keeping the same font, size, alignment and spacing.
- Do NOT change team member names, student IDs, the logo, the university/faculty/course lines, the project title, the layout or the table structure.
- If the cover contains a date or other wording that looks outdated, do not guess: leave it and list it in the final checklist as a suggestion.
- Record the before/after text of every cover change in progress_log.md and in the final checklist.
Insert the TOC and all new content AFTER page 1. Page numbers start from page 2 (page 1 has no number).



## 3. Locked decisions (from progress_log.md plus later answers; do not re-ask)

1. Base = FinalReport.docx.
2. Authoritative notebook = notebooks\CISC7204_ClassE_Team01_Visualization_updated.ipynb (ignore "lucas_pending test").
3. Figures: use notebooks\figures\ (colour versions only, never _gray). If a needed figure exists only in the old figures\ folder, use the old one and mark it in the figure register.
4. Figure numbers follow report narrative order; keep a mapping table (report number, file name, notebook cell, data source) in the Appendix.
5. Analysis windows: H1-H3 and RQ1 use the 36 complete months 2023-01..2025-12 (12 quarters). The 9 months 2026-01..2026-09 are used only for the seasonal pattern (RQ2) and out-of-sample comparison. Other analyses (zone/hour supply-demand match, district layer, etc.) use the real data windows coded in the notebooks; state the exact period on every figure/table (confirm each against the notebook/CSV before quoting).
6. Every 2026 chart is labelled "9 months (Jan-Sep), single snapshot, out-of-sample" where relevant.
7. The 24-district analysis is a separate subsection (different measurement system from DSEC arrivals).
8. You may state that bus ridership includes residents and district head-count is a sample (about 99.9% of arrivals per qa_report.csv).
9. Meeting minutes/meeting briefs: do NOT mention them anywhere in the report (no "5 minutes", no "1 minutes"). The introductory video and its slides: one short line in the deliverables table ("submitted separately"), no detail.
10. Dashboard = self-contained offline HTML, 4 dropdown filters (year, zone, district, map metric) + auto-cycle (Play) + Reset, 16 linked Plotly charts. NO hour slider claim. The Dash app (app.py) may be mentioned as a secondary port.
11. Names: use exactly the names written in the current docx (e.g. FONG CHIN WAI). Git aliases (chin wai fong / Fong Chin Wai / Fong Chin Wai (Vivi)) are the same person; do not print aliases in the report. Roles come from the docx roles table (e.g. dashboard and master pipeline = FONG CHIN WAI). "Lucas" = KONG KIN MENG.
12. No grayscale variants.
13. Data citation: "Retrieved November 4, 2026" (APA 7); state data coverage to 2026-09 in the data table.
14. Reproducibility statement (one only): Python 3.14.6 (confirmed by the team), pandas 3.0.3, numpy 2.4.6, matplotlib 3.11.0, seaborn 0.13.2, scipy 1.18.0, statsmodels 0.14.6, plotly 6.7.0, openpyxl 3.1.5, dash [TODO: teammate to fill dash version]. Do not present per-member environment differences. Note the README's older versions (pandas 2.2.2, plotly 5.22.0, dash 4.4.1) as outdated only in the appendix. The team confirms that Visualization_updated.ipynb was run end-to-end successfully in this environment. The manual may state this in one sentence, without dates or run logs. The AI agent itself did not re-execute it.



## 4. Defects to fix or disclose

1. Remove the "hour slider" claim (draft T9/dashboard text).
2. Month count: 45 months is correct (25,920 = 45 x 24 districts x 24 h). data_processed\phase1_usability_verdict.csv says 43 (stale). State 45; note the stale label in an appendix.
3. Plotly: README says plotly 5.22.0; the HTML inlines plotly.js v3.5.0; the team environment has plotly 6.7.0. Report the bundled version and note the README mismatch.
4. 2025 reconciliation gap: total_headcount 40,045,669 vs arrivals sum 40,069,360 (difference 23,691). Disclose.
5. Also correct or disclose: success criteria "36 monthly/12 quarterly rows" vs delivered 45/15 (analysis window 36 months, data coverage 45); "5 meeting minutes" (delete this deliverable and criterion, do not replace it); "opens from local CSV" (the app reads JSON; the static HTML is self-contained); version claims in the draft (replace with the statement in decision 14); Coloane share 1.67% (use one rounding style everywhere); the time window of match_zone_supply_demand.csv ("2026H1" column name vs "2026-01..07" in the inventory; check before quoting); DSEC JSON ends 2026-08 but monthly arrivals run to 2026-09 (find the source and state it).



## 5. Report structure

Page 1 cover (limited edit, section 2) + page 2 real TOC field. Keep GenAI Use Statement and References (inside Section 10). Replace the single-level headings with Heading 1/2/3 styles. Move (do not delete) existing draft text into the new structure and keep an "old to new" content map in progress_log.md.


| #   | Section                                                   | Proposed content                                                                                                            | Pages |
| --- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ----- |
| -   | Cover + TOC                                               |                                                                                                                             | 2     |
| 1   | Project Background                                        | topic, RQ1/RQ2, H1-H3, purpose, data context (dataset table with sources, coverage, retrieval date)                         | 4     |
| 2   | Project Goals and Schedule                                | goals, success criteria (corrected), 4-week plan (Gantt), planned vs actual                                                 | 2     |
| 3   | Project Tasks and Team Structure                          | tasks T1-T10 + METHODOLOGY (acquisition, cleaning, integration/QA, statistics, chart design, dashboard design), roles table | 7     |
| 4   | Project Deliverables and Incomplete                       | delivered vs incomplete (honest), RESULTS (H1-H3, RQ2, zone/hour mismatch, district layer, 2026 out-of-sample) with tables  | 6     |
| 5   | Project Discussion and Limitations                        | interpretation (associational, not causal), limitations, disclosed defects                                                  | 3     |
| 6   | Project Division of Work                                  | per-member table from the docx roles                                                                                        | 2     |
| 7   | Project Individual Contributions - Storytelling with Data | one block per visual, grouped by member                                                                                     | 9     |
| 8   | Project Learning - Collective and Personal                | collective + six personal reflections                                                                                       | 3     |
| 9   | Project Manual - README                                   | step-by-step verification                                                                                                   | 3     |
| 10  | Project Appendices                                        | figure register, QA table, data dictionary excerpts, code excerpts, GenAI statement, References                             | 3     |


Total target about 44 pages. HARD LIMIT 50. Stop and ask me if the projection exceeds 45.

## 6. Section rules

- Methodology: describe only what the notebooks and scripts do (e.g. YTD de-duplication of the 45 MGTO files, CN-to-EN district mapping, 3 macro-zones, headway midpoint conversion to departures per hour, QA report 9 PASS / 4 INFO / 0 WARN / 0 FAIL). Cite the file/cell for each step.
- Results: numbers from notebooks/CSVs only (e.g. H1 r = 0.759, H2 r = 0.913, H3 partial r = 0.179 p = 0.296 for n = 36; quarterly H1 0.917 for n = 12). Label n and period each time. Re-check each number against its source before writing.
- Sections 6/7 authorship: use the docx roles table (module lead/support, analysis, reporter) as the basis. In Stage A, build a visual-to-member mapping: M1 visitor arrivals (KONG KIN MENG lead, SONG ZHUOXI support), M2 hotel occupancy (KUAN CHI KIT lead, XIAN QILAN support), M3 bus ridership/master pipeline/dashboard (FONG CHIN WAI lead, FONG HIO LAM support), interpretation (XIAN QILAN), relationship analysis (KUAN CHI KIT). Every member must receive at least one visual or a clearly described storytelling contribution. Phrase it as responsibility per team role, not as git evidence. Never claim a specific action you cannot support. Record the mapping in _temp and in the final checklist.
- Section 7 (each visual): figure number, caption, data source, key finding, then Truthful / Functional / Beautiful / Insightful, each pointing to concrete elements (axis labels, scale, baseline, colours, annotations, legend, title). Be honest about weak points (dual axis in fig02_rq1_coupling Panel A, index-based truncated axis in fig07_2026_level_vs_base, three denominators on one % axis in the zone chart). Prefer the honest alternative (e.g. z-score Panel B). Weak points also go to Section 5. Use fig12_dashboard_preview only as a dashboard illustration, not as an analytic figure.
- Section 8, collective: only from evidence (cross-check findings, defects found, pipeline and data-quality lessons, dual-axis and baseline lessons, partial correlation, reproducibility). KONG KIN MENG's reflection is already written (see the block below). Insert it as-is, with only light formatting. Write the other five members' reflections yourself under the same rules.
  [KONG KIN MENG REFLECTION - insert verbatim]
  (paste the text from the section below)Personal: write one first-person reflection (about 150-250 words) for each of the six members, based ONLY on that member's documented roles in the docx and on project facts (e.g. what the module involved, what the analysis taught). Do not invent specific events, conversations, hours worked, emotions tied to specific incidents, or achievements not documented. Keep each reflection distinct in content, not copy-paste. Tell me in the final checklist that these are AI-drafted from role information and each member should review and edit their own reflection before submitting.
- GenAI Use Statement: keep the existing text and add one sentence that an AI assistant was used to draft and revise parts of the final report, including the draft personal reflections, which members reviewed [TODO: members confirm review].
- Section 9 Manual: steps from README, scripts\ and notebooks: folder structure, environment (decision 14), run order (scripts\build_panels.py, then notebooks pipeline, then Visualization_updated), how to open the HTML dashboard, how to rebuild (build_dashboard.py) and run app.py, expected outputs (row counts 25,920, 45 and 15 rows, QA 9/4/0/0). Replace personal interpreter paths with generic `python`. State clearly: "Checked statically against the files by the AI agent. The team ran Visualization_updated.ipynb end-to-end in the stated environment."  Disclose: exploratory steps not saved as scripts (README), no requirements file, "Data cleaning" folder empty.
- Dashboard: use Dashboard\preview screenshots; crop to fit the page; do not insert 1600x5000 px full-page images unscaled.

[Kong Kin Meng. As the lead of the visitor-arrivals module, I worked with the monthly arrivals series from DSEC, including the same-day and overnight split. This showed me that a dataset is only usable after its structure is understood. Source markets start in different years (for example, Korea only from 2023), some raw files carry duplicated "Remark" headers and blank columns, and monthly values must be tied to a proper year before they can be merged.

Validating the master dataset taught me to test assumptions instead of trusting them. Checks such as the monthly-to-quarterly roll-up, the 45-month coverage and the 2025 gap between district head-count and total arrivals reminded me that two measurement systems should not be treated as one population, and that a small difference should be disclosed rather than hidden.

As a project tracker, I learned to turn a broad goal into small, checkable tasks that fit the four-week plan. As an analyst and developer, I learned that a chart can look convincing and still mislead. A dual-axis plot can suggest a link that a z-score view does not, so I now ask what the axis, the baseline and the unit are telling the reader before I trust a visual.

In future work I would add a dependency file and save every cleaning step as a script, so that others can reproduce the results without guessing.]

## 7. Format

- English only. A4. Output .docx only. Final PDF name (by me): cisc7204-Class_E-Team_01-FinalReport.pdf.
- Times New Roman, body 11 pt, line spacing about 1.15, margins about 2.5 cm (apply to new content; keep the cover layout as in section 2), Heading 1/2/3 defined in styles.xml. Tables and figures numbered with captions and referenced in the text. Images fit within the margins and stay legible (about 150-200 dpi).
- APA 7, in-text and reference list consistent; keep the 14 existing references; add Cairo, A. (2019). How Charts Lie. Add publisher details only if verified, otherwise [TODO: verify]. Every figure needs a source line (data source and notebook).
- Insert a TOC field and enable update-on-open. You cannot compute TOC page numbers: tell me to update the field in Word.
- Concise plain academic English. No filler. No repeated points. Prefer tables and figures.



## 8. No fabrication

- Use only the folder, progress_log.md, project_inventory.md and my answers.
- Never invent data, results, dates, contributions, references or URLs.
- Missing information: highlighted [TODO: confirm - ...] and list it for me.
- If you cannot verify a number, do not write it.



## 9. Workflow (single run, stop only on blockers)

The report must be revised directly in this run. Do not wait for approval between stages. Work in this order and record each completed step in progress_log.md:

1. Stage A: build the figure register, outline, old-to-new content map and the visual-to-member mapping (from the docx roles table). Save them to _temp. Use them as your plan without waiting for approval.
2. Record the original cover-page text in progress_log.md before changing it (section 2).
3. Stage B: sections 1-3 and 6. Stage C: sections 4-5. Stage D: section 7. Stage E: sections 8-10. Edit the docx after each stage and save it, so work is not lost.
4. After each stage: estimate the total page count and update progress_log.md.
5. Stage F (verify): cross-check every number against its source; check figure/table numbering and references; confirm the docx opens; run git status and confirm only the docx and _temp changed.

STOP and ask me ONLY if:

- the projected total exceeds 45 pages;
- a cover change beyond section 2 seems necessary;
- a number cannot be verified against a source file (write [TODO] and continue if it is minor);
- a decision in section 3 conflicts with the evidence in a way you cannot resolve;
- the docx cannot be edited safely (locked, corrupted, missing package).
For all other gaps, insert a highlighted [TODO: confirm - ...] placeholder and continue.

Final output (as your last message and saved to _temp\final_checklist.md): estimated page count; ALL [TODO] items grouped by who must fill them (me / teammate / each member); cover-page before/after text; figure list with sources (report number, file, notebook cell); the visual-to-member mapping you used; the old-to-new content map; sections added or changed; all numbers that were changed from the draft; and what I must verify manually (TOC update in Word, real page count, run the manual on my machine, member review of reflections, dash version). Do not delete _temp.