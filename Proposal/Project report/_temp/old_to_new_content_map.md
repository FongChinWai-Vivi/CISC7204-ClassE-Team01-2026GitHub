---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 5480d5b254a487a11b77a101419fe1ce_675cd55ee95211f1961f525400f8a581
    ReservedCode1: mySvOTL9fuVIl4uKNCrJe60+RzBmEcXhlGiUF6kKoiBPNkVyqsht3SGgBwrpDAAhkOZL+7JCsgywvfV/yCmJ2VU6yAQLg9ueqRU9iPaC2Lm85NwTlbmiFz0jDWGcO46NQFuy13nZ2MKB7eCpqkGzmCDtBGbTCYX364Ln3bpge7ds6EHwIe+VYB+To3Y=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 5480d5b254a487a11b77a101419fe1ce_675cd55ee95211f1961f525400f8a581
    ReservedCode2: mySvOTL9fuVIl4uKNCrJe60+RzBmEcXhlGiUF6kKoiBPNkVyqsht3SGgBwrpDAAhkOZL+7JCsgywvfV/yCmJ2VU6yAQLg9ueqRU9iPaC2Lm85NwTlbmiFz0jDWGcO46NQFuy13nZ2MKB7eCpqkGzmCDtBGbTCYX364Ln3bpge7ds6EHwIe+VYB+To3Y=
---

# Old-to-new content map - draft `cisc7204-Class_E-Team_01-FinalReport.docx` -> revised report

Built 2026-11-26 (Stage A). Nothing from the draft was deleted except the four claims listed in section 4 below; every other draft paragraph was moved into the new structure.

## 1. Section-level map

| Draft section (single-level heading, 14 pages, 4,580 words) | New location | Treatment |
|---|---|---|
| Cover page ("Team Project Proposal") | Cover, page 1 | One phrase changed to "Team Project Final Report"; layout, names, IDs, logo, title, date untouched |
| (none - no TOC existed) | Page 2 | Real TOC field, levels 1-3, update-on-open |
| 1. Project Title and Research Question | 1.1 Topic and Research Questions | Moved; RQ1/RQ2 and H1-H3 separated into a table-free list, each hypothesis given its tested statistic and window |
| 2. Project Purpose | 1.2 Purpose and Scope | Moved and merged; scope statement (what the report does not claim) added |
| 3. Data Context (3.1 arrivals by market; 3.2 same-day/overnight; 3.3 occupancy; 3.4 bus; 3.5 room supply; 3.6 MGTO district x hour; 3.7 DSAT GTFS) | 1.3 Data Context (dataset table with source, coverage, retrieval date) + 3.2.1 Data acquisition + 3.2.2 Cleaning + 3.2.3 Integration and QA | Split: the "what the data are" part went to 1.3, the "how they were built" part to 3.2.1-3.2.3, with the file/cell cited for each step |
| 4. Project Tasks and Deliverables (T1-T10) | 3.1 Task Breakdown (Table 4) + 4.1 Deliverables: Delivered and Not Delivered (Table 7) | Task list moved to 3.1; each task's delivery status moved to 4.1 with an honest delivered/not-delivered column |
| 5. Success Criteria | 2.2 Success Criteria (Table 2) | Rewritten: the row-count criterion now states 45 months / 15 quarters delivered against a 36-month / 12-quarter analysis window; the meeting-minutes criterion removed |
| 6. Team Collaboration | 3.3 Team Structure and Roles (Table 6) + 6 Project Division of Work (Table 14) | Roles kept in 3.3; per-member duties and section ownership in 6 |
| 7. Timeline | 2.3 Four-Week Plan and Planned-versus-Actual (Figure 1, Table 3) | Moved; a planned-versus-actual column added; meeting dates kept only as plan entries with no minutes referenced |
| (results were scattered inside sections 1, 3, 4) | 4.2-4.7 | Consolidated: long-run context, RQ1 for H1-H3, RQ2, zone/hour mismatch, 24-district layer, 2026 out-of-sample |
| (limitations were one sentence in section 1) | 5.1-5.3 | Expanded: association-not-causation, five limitations, and a table of every disclosed defect |
| (no individual-contribution section) | 7.1-7.6 | New: six member blocks, one per visual group |
| (no learning section) | 8.1-8.2 | New: collective lessons from evidence plus six personal reflections |
| (no manual) | 9.1-9.8 | New: folder structure, environment, run order, dashboard, rebuild, expected outputs, gaps, check status |
| (no appendices) | 10.1-10.4 | New: figure register, data dictionary excerpts, code excerpts, QA table and open items |
| GenAI Use Statement | 10.5 GenAI Use Statement | Text kept; one sentence added about AI drafting and revision of the report and of the draft reflections |
| References (14 entries) | 10.6 References | 14 entries kept and reformatted to APA 7; Cairo (2019) added -> 15 entries |

## 2. Task map (draft T1-T10)

| Draft task | New location | Note |
|---|---|---|
| T1 Cleaning | 3.2.2 Cleaning | Cites the YTD de-duplication of the 45 MGTO workbooks, CN-to-EN district mapping, three macro-zones, headway midpoint conversion |
| T2 Master monthly dataset | 3.2.3 Integration and quality assurance | QA file named; 9 PASS / 3 INFO / 0 WARN / 0 FAIL reported (see defect 6) |
| T3 EDA | 4.2, 4.3 and 7.1-7.6 | Distributional diagnostics in 4.3 (Figure 7); interpretation in section 7 |
| T4 Figure 1 long-run context | 4.2 | Re-drawn from `notebooks/figures/fig01_arrivals_longrun.png`; now Figure 2 |
| T5 RQ1 twin-axis chart | 4.3 | Now Figure 4, with Panel A (dual axis) shown next to Panel B (z-scores); the dual axis is criticised in 5.2 and 7.3 |
| T6 H1-H3 correlation and partial correlation | 4.3 | Figures 3, 6, 16, 17; tables 9-11; every coefficient carries n and period |
| T7 RQ2 seasonality | 4.4 | Figures 9, 10; Table 12; 2026 labelled as nine months, single snapshot, out-of-sample |
| T8 Overnight and same-day distributions | 4.3 | Table 10 (overnight vs same-day correlations) and Figure 6 |
| T9 Plotly dashboard | 3.2.6 (design) + 4.1 (delivered) + 7.5, 7.6 (storytelling) + 9.4, 9.5 (manual) + Figure 18 | "Hour slider" and "shared time axis" claims removed; described as self-contained offline HTML with four dropdown filters, Play, Reset and 16 linked charts |
| T10 Report, slides and review | 2.3 (planned-versus-actual) + 4.1 (Table 7) | Report and review delivered; a separate presentation deck is marked as an open item, not claimed |

## 3. Figure map (draft Figure 1-6)

| Draft figure embedded | Draft content | New number | Action |
|---|---|---|---|
| `figures/fig1_general_trend.png` | arrivals 2015-2026 with pandemic band | 2 | Replaced by the newer 200-dpi `notebooks/figures/fig01_arrivals_longrun.png` |
| `figures/fig2_zone_mismatch.png` | three zone shares | 11 | Replaced by `notebooks/figures/fig02_zone_mismatch.png` (two panels, ratio added) |
| `figures/fig3_hourly_profile.png` | hourly demand vs supply | 12 | Replaced by `notebooks/figures/fig03_hourly_mismatch.png` |
| `figures/fig4_correlation.png` | scatter + quarterly bars | 5 (and new 3, 6) | Replaced by `fig04_intensity_decline.png`; the scatter half is now covered by Figures 3 and 6 |
| `figures/fig5_district_hour_heatmap.png` | ten busiest districts by hour | 14 | Replaced by `notebooks/figures/fig05b_district_hour_heatmap.png` |
| `figures/fig6_workplan.png` | four-week Gantt | 1 | Kept (only copy) but moved from the results to 2.3, where a plan chart belongs |

Twelve figures are new: 3 (correlation matrix), 4 (dual axis vs z-scores), 6 (scatter matrix), 7 (distribution diagnostics), 8 (market composition), 9 (seasonality), 10 (quarterly profile), 13 (district choropleth), 15 (2026 level vs base), 16 (lag cross-correlation), 17 (regression diagnostics), 18 (dashboard screenshot).

## 4. Deleted claims (not moved anywhere)

| Claim in the draft | Why removed | Where the correction is recorded |
|---|---|---|
| Dashboard has an "hour slider" (and a "shared time axis" that implied one) | No slider exists in `Dashboard/app.py` or the built HTML; the hour dimension is exposed through the heat-map and the hourly profile instead | 4.1 Table 7, 5.3 and 7.5 |
| "5 meeting minutes" as a deliverable and as a success criterion | Meeting minutes are not to be mentioned; the deliverable was never completed | Removed from 2.2 and 4.1; no replacement invented (INSTRUCTIONS section 4, item 5) |
| "Dashboard opens from local CSV in 5 s" | The static HTML is self-contained; the Dash port reads pre-baked JSON, not CSV | 5.3 and 9.4 |
| "Python 3.11, pandas 3.1, Matplotlib 3.11" | Not supported by any file in the repository | Replaced by the single reproducibility statement in 9.2 (decision 14); README versions noted as outdated in 10.4 |
| Success criteria "36 monthly / 12 quarterly rows" | Delivered panels hold 45 and 15 rows | Rewritten in 2.2 as data coverage 45/15 versus analysis window 36/12 |

## 5. Content that stayed verbatim

- The project title, all six member names and the role wording in the roles table.
- KONG KIN MENG's personal reflection (section 8.2.2), inserted as supplied with light formatting only.
- The existing GenAI Use Statement sentences (one sentence appended).
- The 14 existing reference entries (reformatted, not rewritten).
*（内容由AI生成，仅供参考）*
