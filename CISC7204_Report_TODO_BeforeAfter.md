---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_822a2005ea0a11f1961f525400f8a581
    ReservedCode1: tsHhWc5Wv++1K27Ail1526v3TYor8I0RB8qQujJrxNM8zJfKgWBtkqoqfYSpFzHe5Bx3dj9lqXnRFPACaoLNTk/o1C20WUdgHH79BRJH6R+B4QT9yRnXhk/k2PCo4vc2rdg2J24QT7FTszr4rxn6gIvTpbrgfW6qZTj0XMRjPa7wevxcWVVVtF/QyP8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_822a2005ea0a11f1961f525400f8a581
    ReservedCode2: tsHhWc5Wv++1K27Ail1526v3TYor8I0RB8qQujJrxNM8zJfKgWBtkqoqfYSpFzHe5Bx3dj9lqXnRFPACaoLNTk/o1C20WUdgHH79BRJH6R+B4QT9yRnXhk/k2PCo4vc2rdg2J24QT7FTszr4rxn6gIvTpbrgfW6qZTj0XMRjPa7wevxcWVVVtF/QyP8=
---

# 报告 TODO 原文 → 定稿成稿 对照表

- 检索范围：`C:\Users\07viv\Desktop\CISC7204-Team01` 全仓库 + `Proposal\Project report\_temp\backup`
- 早期版本（docx 备份 3 份）：

| 别名 | 文件 | 大小 | 段落/表格 | TODO 命中 |
|---|---|---|---|---|
| 原始草稿 | `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx` | 705,834 B | 166 段 / 12 表 | 0（无任何 TODO/TBD/占位标记） |
| 格式补丁前 | `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_format_patch_2026-11-26.docx` | 4,124,376 B | 372 段 / 18 表 | 8 处段落 + 2 处表格 |
| 交叉引用前 | `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_before_crossref_spacing_2026-11-26.docx` | 4,124,397 B | 372 段 / 18 表 | 同上 10 处，逐字一致 |

- 定稿：`Proposal\Project report\cisc7204-Class_E-Team_01-FinalReport.docx`（4,648,225 B，2026-11-27 09:02）
- 检索式：`TODO|TBD|to be (added|confirmed|completed|decided)|placeholder|占位|待补|待定|待核|XX+|\[ ?\]`
- 结论：10 处显式 TODO 全部清除；因 TODO 被删而整条重写的附录 D 条目 5 条、参考文献 1 条、交付物表 1 行、期望输出表 1 行、GenAI 声明 1 段、§9.2 复现声明 1 段。

## 逐条对照

| # | 早期版本中的 TODO 原文 | 出处（文件 · 位置） | 定稿写成什么（位置 · 原文） |
|---|---|---|---|
| 1 | “…plotly 6.7.0, openpyxl 3.1.5 and dash **TODO: confirm - the teammate maintaining the Dash app must fill the dash version**.”（同段此前为 Python 3.14.6 / pandas 3.0.3 / numpy 2.4.6 / matplotlib 3.11.0 / scipy 1.18.0 / statsmodels 0.14.6 / plotly 6.7.0 / openpyxl 3.1.5） | 格式补丁前 · ¶295（§9.2 Environment） | §9.2 整段改写，版本全部换成实装值并补 dash 4.4.1：“**requirements.txt at the repository root pins the environment: Python 3.12.3 with pandas 2.2.2, numpy 1.26.4, scipy 1.13.1, statsmodels 0.14.2, matplotlib 3.8.4, seaborn 0.13.2, plotly 5.22.0, dash 4.4.1 and openpyxl 3.1.2, plus the notebook stack … (nbformat 5.9.2, nbconvert 7.10.0, ipykernel 6.28.0)**. The pipeline notebooks, the dashboard build and the timings in Section 5.3 were all run in this environment…The version block in the repository README (pandas 2.2.2, plotly 5.22.0, dash 4.4.1) agrees with the pinned file…” |
| 2 | “• Dash version. The reproducibility statement in Section 9.2 is complete except for the dash version, which the teammate maintaining the Dash port must supply. **TODO: confirm - dash version for the reproducibility statement**” | 格式补丁前 · ¶345（10.4 Appendix D） | 该条目**整条删除**；同一事实改由 Appendix D 第二条承接：“• **README version block (resolved).** The repository README lists pandas 2.2.2, plotly 5.22.0 and **dash 4.4.1**, which are the versions pinned in requirements.txt and quoted in Section 9.2.”（定稿 ¶417） |
| 3 | “• Cairo (2019). The reference is added as required by the report brief. The publisher details are not verified from a catalogue and must be completed or left out. **TODO: verify - publisher and place of publication for Cairo (2019) How Charts Lie**” | 格式补丁前 · ¶346（10.4 条目） | 条目**整条删除**；出版社直接写入参考文献：“Cairo, A. (2019). How charts lie: Getting smarter about visual information. **W. W. Norton & Company.**”（定稿 ¶426；出版地仍未写） |
| 4 | “• Presentation deck. The brief asks for a presentation; the repository contains the introductory video deck but no separate report-presentation deck. Whether a separate deck is part of the submission is unresolved. **TODO: confirm - whether a separate presentation deck is part of the submission**” | 格式补丁前 · ¶347（10.4 条目） | 条目**整条删除**；结论写进交付物表 Table 7“Presentation”行：“**Not part of this report package; the introductory-video slides were submitted separately with the video.**”（第 4 列 Where 记为 “—”） |
| 5 | “• Quality report count. The locked description … 13 checks with nine passing and four informational. The file data_processed/qa_report.csv contains 12 rows: nine PASS, three INFO, none WARN, none FAIL. The report uses the file. **TODO: confirm - QA count discrepancy: source file has 12 checks with 3 INFO, the locked description says 13 with 4 INFO**” | 格式补丁前 · ¶348（10.4 条目） | 条目保留为 Appendix D 开放项第一条，TODO 换为定论句：“…**The count in Section 9.6 is the one in the file.**”（定稿 ¶416） |
| 6 | “• Cover page date. The cover still reads 5 November 2026, which is the proposal submission date rather than the final report date. It was left unchanged as instructed. **TODO: confirm - whether the cover date should be updated for the final submission**” | 格式补丁前 · ¶351（10.4 条目） | 条目改为已解决：“• **Cover page date (resolved).** The cover page now carries the final submission date, **5 December 2026**, which is the course deadline; the proposal submission date of 5 November 2026 has been replaced. The four-week delivery plan in Section 3 keeps its original planning dates, and the data retrieval dates of 4 November 2026 are unchanged.”（定稿 ¶419）；封面同步改为 “Submission date: 5 December 2026” |
| 7 | “…including the draft personal reflections in Section 8.2, which the members reviewed. **TODO: members confirm review of their own reflection** All data are taken from the official sources cited below…” | 格式补丁前 · ¶354（10.5 GenAI Use Statement） | 整段重写，TODO 换为确认句：“…and to check the internal consistency between the text and the tables; every script was re-run by the team on its own data files, each figure was checked against the source tables, and the labels, units and numbers were corrected by the members themselves… **Every member reviewed and verified the text of their own reflection and of the sections they own, and the team as a whole takes responsibility for the final content of this report.**”（定稿 ¶422） |
| 8 | “Cairo, A. (2019). How charts lie: Getting smarter about visual information. **TODO: verify - publisher and place of publication**” | 格式补丁前 · ¶358（10.6 References） | “Cairo, A. (2019). How charts lie: Getting smarter about visual information. **W. W. Norton & Company.**”（定稿 ¶426） |
| 9 | Table 7（交付物表）Presentation 行“Final state”单元格：**“[[TODO: confirm - whether a separate presentation deck is part of the submission; the only deck in the repository is the introductory-video deck]]”** | 格式补丁前 · Table 7 第 7 数据行 c2 | Table 7 同一行改为：“**Not part of this report package; the introductory-video slides were submitted separately with the video.**”（定稿 Table 7 “Presentation” 行） |
| 10 | Table 15（期望输出表）`data_processed/qa_report.csv` 行“Where it is checked”单元格：**“status column TODO: confirm - the locked instruction states 13 checks and 4 INFO; the file contains 12 rows with 3 INFO”** | 格式补丁前 · Table 15 第 8 数据行 c2 | 定稿 Table 16 同一行改为：“**status column; the file carries 12 rows, and the locked description of 13 checks with 4 INFO is noted in Section 10.4**”（定稿 Table 16，另 Table 14 记 “Report states 12 checks in the file; the difference is listed for manual confirmation”） |

## 附：无 TODO 字样但属同类待办的条目（一并被改写成结论）

| # | 早期版本原文 | 定稿写法 |
|---|---|---|
| 11 | “• Outdated README block. The repository README still lists pandas 2.2.2, plotly 5.22.0 and dash 4.4.1, and gives a personal interpreter path. These are recorded here as out of date and were not used for the report's environment statement.”（¶349） | 合并进 “README version block (resolved)…which are the versions pinned in requirements.txt and quoted in Section 9.2. The personal interpreter paths … are not used anywhere in this report.”（¶417 与 §9.2 末句） |
| 12 | “• Missing dependency file. No requirements.txt or environment file exists; adding one would close the largest reproducibility gap. The README also states that some exploratory outputs were not saved as scripts, and the Data cleaning folder is empty.”（¶350） | “• Dependency file: resolved. requirements.txt now at repo root, pinned to versions installed; Section 9.3 install command as step 0. Two reproducibility gaps: README says exploratory outputs not saved as scripts; Data cleaning folder empty.”（定稿 Appendix D 第三条）；Table 7 新增 “Dependency file — Delivered: requirements.txt pinned to the installed versions (Section 9.2)” |
| 13 | “• Table of contents page numbers. The TOC is a real Word field. Page numbers must be generated in Word by updating the field once…”（¶352） | “• Table of contents page numbers (updated). The TOC is a real Word field; it was updated in Word after the final edits, so the page numbers printed here match this version of the document.”（定稿 ¶420） |
*（内容由AI生成，仅供参考）*
