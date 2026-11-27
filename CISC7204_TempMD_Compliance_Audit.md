---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_6ce8f601ea0911f1961f525400f8a581
    ReservedCode1: UJcDUZb3cnk4/F87l8y29CRlESg/UyJX1/AuAxmIel1bw7MxbyyusqIgzPpO6JsKDiUFTT1uua3eF0velm2KD0v5wDFfW0sMkhbi671JgVbWJ5k1zJ/XtsFJ1PCqGf7hkynIdq2KnBRMYnYd2y9v++CyndFsZDNKfyxNzOrAE7+I5lTMnbaxQiMaQzM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_6ce8f601ea0911f1961f525400f8a581
    ReservedCode2: UJcDUZb3cnk4/F87l8y29CRlESg/UyJX1/AuAxmIel1bw7MxbyyusqIgzPpO6JsKDiUFTT1uua3eF0velm2KD0v5wDFfW0sMkhbi671JgVbWJ5k1zJ/XtsFJ1PCqGf7hkynIdq2KnBRMYnYd2y9v++CyndFsZDNKfyxNzOrAE7+I5lTMnbaxQiMaQzM=
---

# _temp 目录 MD 待办 / 结论性要求 × 最终报告 逐条核查表

- 核查对象（要求来源）：`C:\Users\07viv\Desktop\CISC7204-Team01\Proposal\Project report\_temp` 下全部 8 个 MD —— `INSTRUCTIONS.md`、`final_checklist.md`、`progress_log.md`、`outline.md`、`project_inventory.md`、`figure_register.md`、`old_to_new_content_map.md`、`visual_to_member_mapping.md`
- 被核查文件：`CISC7204-Class_E-Team_01-FinalReport.docx`（4,648,225 B，2026-11-27 09:02）与同名 `.pdf`（2,607,280 B，09:03）
- 核查时间：2026-11-27
- 核查方式：python-docx 全文段落 + 19 张表格 + settings/styles/页码设置解析；pypdf 全文 42 页逐页检索；关键数值与图注交叉比对

## 0. 总体结论

| 指标 | 结果 |
|---|---|
| docx 内 `TODO` 残留 | 0 处（PDF 内亦为 0） |
| 表格内 `TODO` 残留 | 0 处 |
| `grayscale` / `gray` 字样 | 0 处 |
| PDF 页数 | 42 页（上限 50） |
| 标题样式 | Heading 1 = 10、Heading 2 = 41、Heading 3 = 17 |
| 图表 | 23 图（编号 1-23 连续）、18 表（编号 1-18 连续）、来源行 34 条 |
| 参考文献 | 15 条（Reference Entry 样式） |
| 目录 | 真实 TOC 域，页码由 Word 更新后与 PDF 实际页一致（1→4、2→5、3→7、4→11、5→23、6→26、7→27、8→32、9→35、10→38）；封面无页码，第 2 页起显示 2 |
| 版面 | A4（11906×16838 twips）、Times New Roman、正文 11 pt、1.15 倍行距 |

待办项基本落地，但存在 9 项仍未落实或与 MD 要求冲突的问题，见第 3 节。

## 1. INSTRUCTIONS.md —— 锁定决策、缺陷修复与格式要求

| # | 条目（原文/要点） | 出处 | 报告中的落点 | 状态 |
|---|---|---|---|---|
| 1 | 封面只允许把 "Proposal" 改为 "Final Report"，姓名、学号、logo、标题、课程名不得改动 | INSTRUCTIONS §2 | 封面第 8 段 "Team Project Final Report"，其余封面元素未变 | 已落实 |
| 2 | 封面日期不猜、不填，只在清单中列为建议 | INSTRUCTIONS §2 / final_checklist §10 | 封面 "Submission date: 5 December 2026"，Appendix D 记为 "Cover page date: resolved" | 已变更（有据，但覆盖了"不猜"原则，需认可） |
| 3 | 第 2 页插入真实目录域，页码必须由 Word 更新，设置 update-on-open | INSTRUCTIONS §2 | 存在 TOC 域，页码与 PDF 实际页一一对应 | 部分落实（域与页码有，`word/settings.xml` 无 `w:updateFields`） |
| 4 | 页码从第 2 页开始，封面不显示页码 | INSTRUCTIONS §2 | `titlePg=True`，PDF 第 1 页无页码，第 2 页显示 "2" | 已落实 |
| 5 | 全文英文、A4、TNR 11 pt、1.15 行距、2.5 cm 页边距、Heading 1/2/3 样式 | INSTRUCTIONS §3 | A4、TNR、11 pt、行距 276(=1.15)、Heading 1/2/3 齐备 | 部分落实（页边距 1247 twips = 2.2 cm，非 2.5 cm） |
| 6 | 不得改动数据集、notebook、代码、图片；不写 git；不得泄露密钥 | INSTRUCTIONS §2 | 属过程约束，progress_log Stage F 记录仅改动 docx 与 _temp | 报告层无痕迹，过程项不可从文件复核 |
| 7 | 全文不得提"5 次会议纪要" | INSTRUCTIONS 决策 5 | 全文无 meeting minutes 表述 | 已落实 |
| 8 | 交付物表须写"介绍视频已单独提交"，不得声称随报告提交幻灯 | INSTRUCTIONS §2 | Table 7："Presentation — Not part of this report package; the introductory-video slides were submitted separately"；"Introductory video — Not part of this document" | 已落实 |
| 9 | Dashboard 定义为离线 HTML（四下拉 + Play + Reset + 16 图），**禁止声明小时滑块**；Dash app 仅作次要端口 | INSTRUCTIONS 决策 10、缺陷 1 | 现以 `Dashboard/app.py` 为主，明确写 "hour slider (dcc.Slider, 0 to 23)" 且标为 "Delivered"（Table 7 "Hour slider — Delivered"；§4 注 T9 delivered in full） | **与 MD 相反**（因滑块已真实实现并验证，报告按实物写；MD 已过期，需回写） |
| 10 | 图表只用彩色版；引自旧 `figures/` 目录的必须在附录标注 | INSTRUCTIONS 决策 3 | Appendix A：Figure 1、Figure 13 标注 "Old `figures/` folder: the only copy" | 已落实 |
| 11 | 2026 年相关图必须标注"9 个月 / 单快照 / 样本外" | INSTRUCTIONS 决策 4 | Figure 9、Figure 15、Figure 8 图注均写入 9 months / single snapshot / out-of-sample | 已落实 |
| 12 | 24 区分析须独立小节，不与小时供需混写 | INSTRUCTIONS 决策 6 | 独立小节 + Figure 13/14（24 statistical districts） | 已落实 |
| 13 | 报告不得出现 grayscale / 灰度字样，不得引用灰度图 | INSTRUCTIONS 决策 12 | 全文 0 命中（改用 "monochrome, luminance-converted copy" 描述目录） | 已落实 |
| 14 | 数据引用须带 "Retrieved November 4, 2026" | INSTRUCTIONS 决策 13 | 正文 "Retrieval date: November 4, 2026"、Table 1 注 "downloaded ... 4 November 2026"；但 6 条数据集参考文献条目未使用 "Retrieved ... from" 措辞 | 部分落实 |
| 15 | 只保留一句复现声明，写明精确版本（Python 3.14.6 / pandas 3.0.3 …），dash 版本留 TODO | INSTRUCTIONS 决策 14、缺陷 8 | §9.3 单一声明：Python 3.12.3 + pandas 2.2.2 + numpy 1.26.4 + scipy 1.13.1 + statsmodels 0.14.2 + matplotlib 3.8.4 + seaborn 0.13.2 + plotly 5.22.0 + **dash 4.4.1** + openpyxl 3.1.2，并指 requirements.txt | 已落实（dash TODO 已填；版本值取自真实 `requirements.txt`，与 MD 锁定值 3.14.6 不同，见第 3 节） |
| 16 | 缺陷 2：交付面板为 45 个月 / 15 季度，须说明 "43 months" 陈旧标签 | INSTRUCTIONS 缺陷 2 | §5 与 Appendix D 说明 45 个月；"43 month" 仅 1 处，为陈旧标签披露 | 已落实 |
| 17 | 缺陷 3：plotly 5.22.0 与 README/报告不符须披露 | INSTRUCTIONS 缺陷 3 | Appendix D "README version block (resolved)"：pandas 2.2.2 / plotly 5.22.0 / dash 4.4.1 与 requirements.txt 一致 | 已落实 |
| 18 | 缺陷 4：2025 年口径差（DSEC vs 汇总）须披露 | INSTRUCTIONS 缺陷 4 | §5 与 Appendix D 有 2025 差异说明 | 已落实 |
| 19 | 缺陷 5：成功准则 36/12 与 45/15 冲突须改写 | INSTRUCTIONS 缺陷 5 | §2.2 与表注统一为 36 个月分析窗 / 45 个月覆盖 | 已落实 |
| 20 | 缺陷 7：删除"从本地 CSV 打开仪表板" | INSTRUCTIONS 缺陷 7 | 改为自包含 HTML（6.1 MB、plotly.js 内联），无 local CSV 表述 | 已落实 |
| 21 | 缺陷 9：Coloane 份额统一为 1.67%（不得 1.7%） | INSTRUCTIONS 缺陷 9 | "1.67" 出现 5 次，"1.7 %" 0 次 | 已落实 |
| 22 | 缺陷 10：zone 窗口 2026-01..07 与 `visitor_headcount_2026H1` 列名不符须披露 | INSTRUCTIONS 缺陷 10 | Figure 11 图注写明窗口 2026-01 至 2026-07 并提示列名不符，正文 §5.3 披露 | 已落实 |
| 23 | 缺陷 11：DSEC JSON 止于 2026-08、月度面板到 2026-09，须说明补充来源 | INSTRUCTIONS 缺陷 11 | Table 1 注与 §4 数据来源段落说明 2026-09 supplement | 已落实 |
| 24 | 结构：封面 + 目录 + 10 章（1-10），附录 A-D、10.5 GenAI、10.6 References；总页数硬上限 50 | INSTRUCTIONS §4/§5 | 10 章齐备（1→38 页），PDF 42 页 | 已落实 |
| 25 | 每图每表须编号、图注在下表注在上、正文引用、图下附来源行 | INSTRUCTIONS §6 | 23 图 18 表连续编号；Source Line 样式 34 条；Caption Text 41 条 | 已落实 |
| 26 | APA 7，保留原 14 条文献，新增一条 Cairo（出版社须核实，未核实留 TODO） | INSTRUCTIONS §7 | 15 条文献；Cairo (2016) New Riders、Cairo (2019) W. W. Norton & Company 已补，无 TODO | 部分落实（出版社已补、出版地未写，APA 7 不强制；另发现 Knaflic 条目文本损坏，见第 3 节） |
| 27 | 不得虚构数据/文献；未核实项用高亮 TODO 并集中列出 | INSTRUCTIONS §8 | 无 TODO 残留，数值均可回溯；Appendix D 以普通项目符号列出开放项（非高亮） | 已落实（高亮形式未保留） |
| 28 | §9 手册须含运行顺序、期望输出、静态核查声明、并披露"无 requirements 文件 / Data cleaning 空目录 / 探索步骤未存脚本" | INSTRUCTIONS §9 | §9 已含；requirements.txt 已补并回写 10.4；"Data cleaning folder empty""exploratory outputs not saved as scripts" 仍如实披露 | 已落实 |

## 2. final_checklist.md / progress_log.md / 其他 MD

| # | 条目 | 出处 | 报告中的落点 | 状态 |
|---|---|---|---|---|
| 29 | TODO：§4.1 交付物表补"独立演示文件"一行 | final_checklist §2 #1、progress_log 开放项 4 | Table 7 "Presentation — slides submitted separately" | 已落实 |
| 30 | TODO：§9.6 质量报告计数与锁定描述冲突须定论 | final_checklist §2 #2、§9；progress_log 开放项 2 | 全文统一为 "12 checks: 9 PASS, 3 INFO, 0 WARN, 0 FAIL"（9.6、Table 16）；Appendix D 首条仍标为开放项 | 部分落实（表述按文件如实写，13 vs 12 的事实未定论） |
| 31 | TODO：Appendix D 封面日期须定 | final_checklist §2 #3 | "Cover page date: resolved. 5 December 2026" | 已落实 |
| 32 | TODO：Cairo 参考文献补出版社/出版地，未核实则留 TODO | final_checklist §2 #4/#6、progress_log #3 | Cairo 两条均已补出版社，无 TODO | 部分落实（出版地缺，APA 7 允许缺） |
| 33 | TODO：§9.2 dash 版本号 | final_checklist §2 #7/#8、progress_log #1 | §9.2/§9.3 "dash 4.4.1"，与 requirements.txt、README 一致 | 已落实 |
| 34 | TODO：六位成员反思须各自复核（各成员 #9-#15） | final_checklist §2 #9-15 | §8.2 六段齐备（8.2.1-8.2.6，含 KONG KIN MENG 逐字版） | 文本已落实；"已复核"事实无法从文件核实 |
| 35 | TODO：§10.5 GenAI 声明加 "[TODO: members confirm review]" | INSTRUCTIONS §10、final_checklist | 已替换为陈述句 "Every member reviewed and verified the text of their own reflection and of the sections they own…" | 文本已落实；属未经核实的事实主张 |
| 36 | 手工核实项：TOC 页码 | final_checklist §10 | 目录页码与 PDF 实际页一致 | 已落实 |
| 37 | 手工核实项：真实页数 ≤50 | final_checklist §10 | 42 页 | 已落实 |
| 38 | 手工核实项：按手册实跑脚本 | final_checklist §10 | 报告 §9 声明 "team ran Visualization_updated.ipynb end-to-end…"，本次未重跑 | 未核实（人工项） |
| 39 | 手工核实项：§4 篇幅偏重，可再删 | final_checklist §10、outline.md | §4 仍为 11→23 页（12 页，占比最高） | 未落实（未再压缩） |
| 40 | 手工核实项：git 状态仅 docx 与 _temp 变更 | final_checklist §10 | — | 未核实（本次明确不做 git） |
| 41 | 重建 Heading 1/2/3 样式（不得用加粗正文冒充标题） | project_inventory 记录 | H1=10 / H2=41 / H3=17 | 已落实 |
| 42 | 图号冲突须消除，全文唯一编号 | project_inventory 记录 | 图 1-23、表 1-18，无重号 | 已落实 |
| 43 | 权威 notebook 未定（Visualization_updated vs lucas_pending），须统一 | project_inventory 记录 | 全文统一引用 `CISC7204_ClassE_Team01_Visualization_updated.ipynb`，Appendix A 逐图标注 cell | 已落实 |
| 44 | 图目录须逐图给来源与窗口（18 图） | figure_register.md | Appendix A 为 24 行表（表头 + 23 图），逐图给文件、cell、数据源与窗口 | 已落实（图数已增至 23，注册表 MD 过期） |
| 45 | 第 7 节每图四问评估（truthful / functional / beautiful / insightful） | INSTRUCTIONS §7、visual_to_member_mapping.md | 四词各出现 17 次（17 个 block），按成员分组，覆盖 6 人 | 已落实 |
| 46 | 新旧章节映射须兑现 | old_to_new_content_map.md | 章节结构 1-10 与映射一致 | 已落实 |
| 47 | 页数估算 43 页、上限 50 | outline.md | 42 页 | 已落实 |

## 3. 仍缺失 / 未落实条目清单（9 项）

| # | 问题 | 证据 | 建议动作 |
|---|---|---|---|
| 1 | 目录"打开时更新"未启用 | `word/settings.xml` 无 `w:updateFields`（docx 与 XML 均确认为 False） | 加 `<w:updateFields w:val="true"/>`，否则读者本地打开时域不会自动刷新 |
| 2 | 页边距不符合 2.5 cm | `w:pgMar` 四边均 1247 twips = 2.2 cm | 改为 1417 twips（2.5 cm），改后须复核页数 ≤50 |
| 3 | QA 计数 13/4 与文件 12/3 的事实未定论 | Appendix D 首条仍为开放项；报告按文件写 12/9/3 | 由团队确认第 13 项检查是否存在；确认后删除 Appendix D 该条并同步 §9.6 |
| 4 | Knaflic 文献条目文本损坏 | 第 430 段："Knaflic, C. N. (2015). Storyt A data visualization guide for business professionals. Wiley." | 改为 "Storytelling with data: A data visualization guide for business professionals. Wiley." |
| 5 | 数据集文献缺检索日期措辞 | 6 条 Data set 条目仅给 URL，无 "Retrieved November 4, 2026, from" | 按 APA 7 在条目补检索日期 |
| 6 | Cairo (2019) 缺出版地 | 第 426 段仅 "W. W. Norton & Company" | APA 7 第 10 版不强制出版地，可选保留 |
| 7 | GenAI 声明中"每位成员已审核"为未经核实的事实主张 | 第 422 段末句 | 需六位成员确认后保留，否则回退为如实描述 |
| 8 | 复现环境与 MD 锁定值冲突未回写 | 报告写 Python 3.12.3 / pandas 2.2.2；INSTRUCTIONS 决策 14 锁定 3.14.6 / 3.0.3 | 以 requirements.txt 实际环境为准，更新 INSTRUCTIONS 决策 14 |
| 9 | MD 已过期项未回写，导致核查口径冲突 | INSTRUCTIONS 决策 10、缺陷 1 要求"禁止 hour slider 声明"、figure_register.md 记 18 图，而报告已按实物写滑块、23 图 | 更新 `INSTRUCTIONS.md`（决策 10、缺陷 1）与 `figure_register.md`（18→23），或加"以实物为准"批注 |

## 4. 备注

- "hour slider" 一项不是报告缺陷：本轮确实把滑块做成按小时真切片（`Dashboard/app.py` 新增 `hour_rows/hour_share/hour_rank`、`HOUR_ALL=-1`），报告改为 "Delivered" 与实物一致；冲突源于 MD 停留在滑块尚未实现时的口径。
- "43 months"、"1.7%"、"grayscale"、"meeting minutes"、"local CSV"、"Python 3.14.6" 等原始缺陷字样在报告中均为 0 命中，唯一例外是两处对旧值/旧标签的显式披露。
- 页数与编号自洽：23 图与 Appendix A 的 23 条登记、Source Line 34 条、17 个第 7 节 block 无冲突。
*（内容由AI生成，仅供参考）*
