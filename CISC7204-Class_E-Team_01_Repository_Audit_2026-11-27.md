---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_353205c1ea1b11f1a20652540072b1e8
    ReservedCode1: yGwd4G75mEzvxTzfRRT4u8JJ2pRyUJtwbQ2YWqz43JjTaphlkfAPJG89u6+PEQCljosgcueRW64Q6vXqvG2qq6ru9YnIAnB05H+U1VQNk/40ENmZlq61ncjvSrQ1aCw4yS19ht4Ex8iRi9CZOZ1vFOT10yYAFvf0Dou/k5mw8PCnFxsc4GRJk/4zmTI=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_353205c1ea1b11f1a20652540072b1e8
    ReservedCode2: yGwd4G75mEzvxTzfRRT4u8JJ2pRyUJtwbQ2YWqz43JjTaphlkfAPJG89u6+PEQCljosgcueRW64Q6vXqvG2qq6ru9YnIAnB05H+U1VQNk/40ENmZlq61ncjvSrQ1aCw4yS19ht4Ex8iRi9CZOZ1vFOT10yYAFvf0Dou/k5mw8PCnFxsc4GRJk/4zmTI=
---

# CISC7204 Class E – Team 01 仓库体检与最终报告审计

| 项目 | 内容 |
|---|---|
| 审计对象 | `C:\Users\07viv\Desktop\CISC7204-Team01`（492 个文件，236.4 MB，其中 `.git` 占 187.7 MB） |
| 受审报告 | `reports\cisc7204-Class_E-Team_01-FinalReport.docx`（4.65 MB）及其同名 PDF（2.48 MB，42 页） |
| 审计时间 | 2026-11-27 |
| 审计方式 | 全盘文件清单 + 内容 SHA-256 哈希比对 + python-docx 结构化解析（440 段 / 19 表 / 24 内嵌图）+ PyMuPDF 逐页页码核对 + 用 `data_processed/`、`Dataset/` 原始数据复算报告数值 + 抽查图件的视觉可读性 |
| 未执行项 | 未运行任何 git 写操作；未在浏览器中实测 Dashboard 交互计时；`extension/` 视为课程外资料，仅登记不评价；报告源数据只复算到 `data_processed/` 与 `Dataset/` 一级，未回溯 MGTO 原始工作簿逐格核对 |
| 结论 | **整体达到可提交水平（初评 84/100），但有 4 项必须在提交前修掉的硬伤，另有 8 项建议修。** 报告本体质量明显高于仓库卫生状况，主要风险集中在"参考文献缺项、分工表图号错位、根目录残留外组文件、临时备份未清" |

---

## 0. 摘要：三句话结论

1. **脏文件问题真实存在但可控**：7 类临时/备份残留共约 18.5 MB，其中三处（根目录别组作业 4 份、`Proposal\Project report\_temp\`、`notebooks\.ipynb_checkpoints\`）会被助教直接看到，属于"印象分"风险而非内容风险。
2. **报告一致性核查整体通过率很高**：图表编号 1–23 / 1–18 无缺号无重号、目录 51 条页码与 PDF 实际页码 **0 处不一致**、全部关键统计量（r=0.759 / 0.913 / 0.179、季节指数 109.8–155.8、分区份额 43.28/55.18/1.54）经原始数据复算全部复现；**未通过的只有 4 项**：参考文献缺 2 条、分工表内部图号错位、3 张表未被正文引用、图号未按首次引用递增。
3. **教师视角**：这是一份"论证诚实、证据链完整、工程量大"的报告，明显加分项是缺陷自披露（Table 14）与复现手册（第 9 章）；扣分集中在**格式与引用细节**和**章节结构错配**（全部结果分析被放在"交付物与未完成工作"章名下）。

---

# 第一部分 仓库体检：脏文件与重复文件

## 1.1 脏文件清单（按处理紧急度分档）

### P0 — 提交前必须清除（对外可见、易被误判为抄袭或未清理）

| 路径 | 内容 | 大小 | 判定理由 | 建议 |
|---|---|---|---|---|
| `CISC7204-Assgn02-Pair06-RevisedProjectProposal.docx.docx` | 别组作业（Pair06） | 19.1 KB | 双扩展名 `.docx.docx`，且非本组文件 | 移出仓库 |
| `CISC7204-Assgn02-Pair08-RevisedProjectProposal_b989b26d8efd2037d13f0a26a427b5ea.docx` | 别组作业（Pair08，文件名含下载哈希后缀） | 1001.2 KB | 同上，哈希后缀说明是浏览器下载原件 | 移出仓库 |
| `CISC7204-Assgn02-Pair08-ProposalVerification.ipynb` | 别组作业 | 865.0 KB | 同上 | 移出仓库 |
| `CISC7204-Assgn02-Pair10-RevisedProjectProposal.docx` | 别组作业（Pair10） | 440.5 KB | 同上 | 移出仓库 |
| `temp_nbrun.log` / `temp_nbrun.err` | 临时运行日志 | <1 KB + 0.9 KB | 典型临时产物残留（虽已在 `.gitignore` 命中） | 删除 |
| `Proposal\Project report\_temp\backup\` 3 个 docx | 修订前备份 | **8.54 MB** | 含 2 份 4.03 MB 旧报告 + 1 份 689 KB 提案副本 | 移出仓库（保留在本地或个人网盘） |
| `Proposal\Project report\_temp\` 9 个 `.md` | 评审回应记录、逐条修复清单 | ≈153 KB | 内部工作笔记（`A_to_D_revision_log`、`Section_by_section`、`Reference_sweep` 等） | 移出仓库 |
| `notebooks\.ipynb_checkpoints\` 3 个文件 | Jupyter 自动检查点 | **5.94 MB** | 自动生成，且是旧版 notebook，易与正式版混淆 | 删除（`.gitignore` 已覆盖） |
| `Dashboard\__pycache__\` 2 个 `.pyc` | Python 字节码缓存 | 0.11 MB | 自动生成 | 删除 |
| `temp\fig15_render.png` | 临时渲染图 | 0.08 MB | 无引用的一次性产物 | 删除 |

### P1 — 建议清除（历史版本堆积）

| 路径 | 内容 | 大小 | 说明 |
|---|---|---|---|
| `minutes\archive_old\` 4 个文件 | 会议纪要旧版（含 `(1)`、`(3)` 重名副本与 "forum_CH_post" 版） | 0.51 MB | 其中 3 个与 `minutes\` 现行版**内容完全相同**（见 2.2 表 C） |
| `minutes\_backup_before_download_20261126_222958\` | 空目录（自动命名的时间戳备份夹） | 0 MB | 空壳目录，删除即可 |
| `figures\archive\` 2 个 PNG | 早期导出版 | 0.88 MB | 报告未引用；建议保留 1 份并加注释，或移出 |
| `Group_dataset_Visitor.py`（根目录） | 4.7 KB 零散脚本 | 4.7 KB | 不在 `scripts/` 内、报告 9.1 未登记，来源不明；建议并入 `scripts/` 或删除 |
| `.vscode\` 1 个配置文件 | IDE 配置 | <1 KB | 个人环境残留 |

### P2 — 保留但需在 README 说明（不建议删）

| 路径 | 内容 | 大小 | 说明 |
|---|---|---|---|
| `figures\grayscale\` 30 个 PNG | 30 张图的灰度打印校验版 | 2.02 MB | 报告 9.1 已明确说明"单色打印校验用、未被正文引用"，属合理保留；**但需注意报告正文不得出现 "grayscale/灰度" 措辞（已核查：正文无该词）** |
| `extension\` 40 个文件 | 微信小程序 `bus_arrival_online` | 1.73 MB | 已在 `.gitignore` 中，课程外延产物；不影响评分，但会拉大仓库体积 |
| `video\` 3 个文件 | 团队介绍视频 mp4 ×2 + pp tx | **91.99 MB** | 见下方命名问题 |

### 视频目录的命名问题（需处理）

```
video\CISC7204-ClassE-Team01_Team Project Introductory Video.mp4    44.23 MB
video\CISC7204-ClassE_Team01_Introductory Video.mp4                 41.55 MB
video\CISC7204-ClassE-Team01_Team Project Introductory Video ppt.pptx 6.21 MB
```

- 两个 mp4 内容不同（大小不同，非哈希重复），**版本关系不明**：文件名一为 `Team01_Team Project…`、一为 `Team01_Introductory Video…`，也让"哪一版是最终提交版"无法判断。
- 均不符合团队既定命名规范 `CISC7204-Class_E-Team_01_`（`ClassE`、`Team01` 缺下划线）。
- 建议：只保留最终版，重命名为 `CISC7204-Class_E-Team_01_IntroductoryVideo.mp4`，另一版移出仓库（可省约 41–44 MB）。

## 1.2 重复文件（按内容 SHA-256 判定）

**扫描结果：17 组内容完全相同的文件（≥1 KB、排除 `.git`），冗余占用 6.58 MB。**

> 说明：小于 1 KB 的同类文件（如 shapefile 的 `.prj` / `.cpg` 边车文件）本就内容相同，属正常现象，已从"重复"统计中排除，不作为问题。

### A. 设计性副本——Dashboard 离线包内嵌数据（可接受，建议在 README 加一句说明）

| 文件 | 相同副本位置 | 单份大小 |
|---|---|---|
| `demand_district_hour_panel_2023_2026.csv` | `Dashboard\data\` ↔ `data_processed\` | 1969.0 KB |
| `macau_stats_zones.geojson` | `Dashboard\data\` ↔ `data_processed\` | 834.6 KB |
| `demand_goldenweek_daily.csv` | `Dashboard\data\` ↔ `data_processed\` | 19.6 KB |
| `demand_monthly_arrivals.csv` | `Dashboard\data\` ↔ `data_processed\` | 13.8 KB |
| `monthly_detail_2023_01_2026_09.csv` | `Dashboard\data\` ↔ `data_processed\` | 7.4 KB |
| `district_map_metrics.csv` | `Dashboard\data\` ↔ `data_processed\` | 6.3 KB |
| `monthly_panel_2023_01_2026_09.csv` | `Dashboard\data\` ↔ `data_processed\` | 4.4 KB |
| `zone_month_share.csv` | `Dashboard\data\` ↔ `data_processed\` | 1.7 KB |
| `annual_month_profile.csv` | `Dashboard\data\` ↔ `data_processed\` | 1.5 KB |
| `quarterly_panel_2023Q1_2026Q3.csv` | `Dashboard\data\` ↔ `data_processed\` | 1.4 KB |
| `hotel_guests_by_star_2023_2026.csv` | `Dashboard\data\` ↔ `Dataset\hotel_Arrival_byHotelStar_summary.csv` | 5.5 KB |
| `hotel_occ_history_2014_2025.csv` | `Dashboard\data\` ↔ `Dataset\Hotel_occ_total.csv` | 4.4 KB |

**结论：不是问题。** 离线 Dashboard 要求"双击即开、不依赖 `data_processed/`"，副本是必要设计。`Dashboard\data\` 实际 20 个 CSV，其中 12 个与上游完全相同，其余为预烘焙转换结果，逻辑自洽（`build_dashboard.py` 读 15 CSV + 1 geojson，与报告 9.5 一致）。

### B. 真冗余——同名不同目录 + 同内容不同名（建议合并）

| 组 | 路径 | 大小 | 问题 |
|---|---|---|---|
| 1 | `Dashboard\data\demand_district_hour_panel_2023_2026.csv` **↔** `data_processed\demand_district_hour_panel_2023_2026.csv` **↔** `data_processed\mgto_district_hour_master_2023_01_2026_09.csv` | 1969.0 KB ×3 | **同一内容三份、两个不同文件名**。`mgto_..._master` 与 `demand_..._panel` 完全一致，但报告 9.1/9.6 只提"district-hour panel（25,920 行）"，读者无法判断哪个是权威源 |
| 2 | `extension\bus_arrival_online\dist\server\index.js` **↔** `...\worker\index.js` | 804.2 KB | 构建产物与源文件同内容（课程外延，可忽略） |

**建议**：`data_processed` 内只保留 `demand_district_hour_panel_2023_2026.csv`，删除 `mgto_..._master`（或反之），并在 `data_dictionary.md` 注明"两者为同一面板的两个历史命名"。约省 1.9 MB，更重要的是消除"同一数据两个名字"的溯源歧义。

### C. 备份/历史副本——可直接删除

| 组 | 路径 | 大小 |
|---|---|---|
| 1 | `minutes\..._1st_Meeting_Minutes.pdf` ↔ `minutes\archive_old\..._1st_Meeting_Minutes(3).pdf` | 107.1 KB |
| 2 | `minutes\..._2nd_Meeting_Minutes.pdf` ↔ `minutes\archive_old\..._2nd_Meeting_Minutes(1).pdf` | 117.8 KB |
| 3 | `minutes\..._3rd_Meeting_Minutes.pdf` ↔ `minutes\archive_old\CISC7204_3rd_Meeting_Minutes_forum_CH_post.pdf` | 184.9 KB |
| 4 | `Proposal\CISC7204_ClassE_Team01_Proposal.docx` ↔ `Proposal\Project report\_temp\backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx` | 689.3 KB |

第 4 组是**本次审计发现的最具误导性的一处**：

> `_temp\backup\cisc7204-Class_E-Team_01-FinalReport_original_2026-11-26.docx`（689 KB，166 段，封面为 University of Macau 的 **Proposal** 文档）实际是**提案**，却按 `FinalReport_original` 命名，且与 `Proposal\CISC7204_ClassE_Team01_Proposal.docx` 哈希一致。
> 后果：任何"用 FinalReport_original 对比修订前后"的操作都会拿到错误基线；若助教翻到该目录，会被误读为"最终报告存在未披露的原始版本"。

**建议**：删除该文件与同目录另两份旧版；如确需保留修订链，改名为 `Proposal_v1_2026-11-26.docx` 并移出 `reports` 相关目录。

### 1.3 清理收益汇总

| 类别 | 可回收空间 |
|---|---|
| P0 临时/备份/别组文件 | ≈ 16.2 MB（`_temp` 8.69 + `.ipynb_checkpoints` 5.94 + 根目录杂项 2.30 + `temp`/`__pycache__`/`minutes` 0.70，扣除重叠后） |
| 重复文件（C 类可删副本） | ≈ 1.1 MB |
| 视频去重（保留一版） | ≈ 41.6 MB |
| **合计** | **≈ 57 MB（仓库体积 236 MB → 约 179 MB）** |

---

# 第二部分 最终报告一致性核查

## 2.1 图表编号与登记表

| 检查项 | 方法 | 结论 |
|---|---|---|
| 图编号连续 | 提取全部 `Figure N.` 题注 | **PASS**：F1–F23 连续，无缺号、无重号 |
| 表编号连续 | 提取全部 `Table N.` 题注 | **PASS**：T1–T18 连续 |
| 图注三件套完整 | 每个图后是否跟 `Source:` 行 | **PASS**：23/23 具备 "Figure 题注 + Source Line" |
| 图登记表（Table 17）真实性 | 抽取 24×4 登记表，逐条核对 `figures\` 文件是否存在、所指 notebook cell 是否为对应绘图代码 | **PASS**：23 个文件全部存在；所指 cell（vis 10/16/18/21/25/26/27/29/31/33/35/37/38/39、pipe 48/56/62/64/66/68/73）均存在且源码内容对应；1 处文件名拼写差异（登记 `optional_gateway_share.csv`，实际文件 `optional_gateways_summary.csv`） |
| 图号是否按首次引用递增 | 扫描正文首次出现位置 | **未通过（轻微）**：首次引用顺序为 1→4→17→12→2→3→…，非单调。正文 §6 设计原则段先引用了 Figure 4/12/17，与附录 A 自述"按讨论顺序编号"存在张力 |
| 未被使用的图 | 比对 `figures\` 30 个 PNG 与 Table 17 | **PASS**：报告用 23 张（22 来自 `figures\` + Figure 23 来自 `Dashboard\preview\`），`figures\` 内 8 个未被引用 = 7 个 pipeline 重复图 + `viz_fig12_dashboard_preview.png`，与正文自述**完全一致**（此前的"30−23=7"直觉算法会误判，实际 23 张里有 1 张不在 `figures\`） |

## 2.2 正文交叉引用

| 检查项 | 结论 |
|---|---|
| 图是否全部被正文引用 | **PASS**：F1–F23 在正文各自至少出现 1 次（其中 Figure 3/6/10/20 的正文引用是上一轮修订补入的，已确认存在） |
| 表是否全部被正文引用 | **未通过**：**T12、T16、T18 在正文中引用次数为 0**，仅以其题注/附录形式出现（T16 = 干净运行产物清单、T18 = 附录 B 字段表、T12 = 分区份额表）。读者顺着正文读会跳过这三张表 |
| 范围引用写法 | **PASS**：未发现 "Tables x–y" 之类的范围误写 |
| 章节引用（"Section N.N"） | **PASS**：抽查 §5.3/§9.2/§9.6/§10.4 互指均指向存在的节 |

## 2.3 目录与页码

| 检查项 | 结论 |
|---|---|
| 目录条目数 | 51 条（`toc 1` 10 + `toc 2` 41） |
| 目页页码 vs PDF 实际页码 | **PASS：0 处 mismatch**（归一化空格后逐条比对 PDF 42 页内的实际标题页） |
| 标题总数 | 68 个（Heading 1 + Heading 2）；17 个三级标题未进目录，但正文层级连续，属可接受的目录深度设置 |
| 目录页码区间 | 4–41 页，与 PDF 总页数 42 页自洽（封面 3 页 + 正文 + 尾页） |
| 分页漂移 | **PASS**：docx 与 PDF 均为 2026-11-27 11:09，PDF 由同一 docx 导出，无 Word/PyMuPDF 分页差异 |

## 2.4 表格数字 vs 数据源（逐项复算）

| 报告位置 | 报告数值 | 复算来源 | 结论 |
|---|---|---|---|
| Table 9 / §4.3 H1 | Pearson r = 0.759，p = 8.2e-8，n = 36 | `monthly_panel_2023_01_2026_09.csv`（arrivals vs bus_monthly_trips） | **一致**（0.7587） |
| Table 9 H2 | r = 0.913（p = 7.8e-15） | 同上（arrivals vs hotel_occupancy） | **一致**（0.9135） |
| Table 9 H3 月度偏相关 | r = 0.179，p = 0.296 | 残差化 bus↔occ | **一致** |
| Table 9 H3 季度偏相关 | r = 0.340，p = 0.28 | 季度面板 n=12 | **一致** |
| §4.4 / Figure 10 季节指数 | 109.8（6 月）–155.8（2 月） | `seasonality_index.csv` | **一致** |
| §4.4 Spearman（2026 vs 2023-2025 基准） | +0.80（p = 0.0096） | 2026 实际 vs 基准同月均值 | **一致**（正相关，报告未误写负值） |
| §4.7 2026 水平 | 3,575,697，较基准同月均值 +27.84%、较全年均值 +24.72% | `monthly_panel` | **一致** |
| §4.3 H2 拆分（过夜/同日） | r_A = 0.921、r_B = 0.694、r_B(occ) = 0.891、r_A(occ) = 0.861、过夜↔同日 = 0.841 | `visitors_*_by_market_summary.csv`（180 行）汇总后复算 | **全部精确复现**（与 notebook 输出一致），确认使用**绝对量口径**，未把份额当水平值 |
| Table 13 三区分区份额 | Peninsula 43.28% / Taipa & Cotai 55.18% / Coloane 1.54% | `match_zone_supply_demand.csv` | **一致** |
| Table 14 24 区份额 | 路氹填海區 44.70%（2026）/ 43.96%（总） | `district_map_metrics.csv` | **一致** |
| §4.5 小时错配 | 夜间 0–5 时需求份额 20.18%、工作日供给峰值 8 时 7.16% | `match_hourly_profile.csv` | **一致** |
| §4.5 季度比率趋势 | `bus_trips_per_arrival` 9.96（2023Q1）→ 5.55（2026Q3） | 季度面板 | **一致** |
| §5.3 / Table 5 QA | 12 项检查，9 PASS / 3 INFO | `qa_report.csv`（13 行含表头） | **一致**，与 §10.4 "12 vs 13" 差异说明自洽（notebook cell 24 只定义 12 个 chk，git 仅 0547248 一版） |
| §3.2 回归 | slope 1.541 / intercept 14.33 / R² 0.576 / Shapiro p=0.022 | `monthly_panel` + scipy | **一致** |
| §9.6 Table 16 自述 | data_processed 49 文件、figures 30 PNG、dashboard 16 charts、html 6.1 MB | 实际目录 + HTML 内 `Plotly.newPlot` 计数 | **一致**（16 个 chart 容器逐一匹配，`f_long`…`f_hhist`） |
| §9.1 目录自述 | notebooks 4 文件、Dashboard 顶层 6 文件、Dashboard/data 20 CSV、figures 30+archive+grayscale | 实际目录 | **一致** |

> 说明：报告已在 §5.3 / Table 14 主动披露 Figure 4 Panel A 双轴、Figure 17 截断轴、Figure 12 三分母同百分比轴等问题，与本次抽查所见一致，属"已披露缺陷"，不计为隐瞒。

## 2.5 假设与成功标准闭环

| 检查项 | 结论 |
|---|---|
| H1–H3 是否有独立变量定义、检验方法、结论 | **PASS**：§4.3/§4.4 正文 + Table 9 汇总（H1 Supported r=0.759；H2 Partially supported r=0.913，且明确 "only the first clause is borne out"；H3 Not supported，月 0.179 / 季 0.340）+ §5.1 解释三方一致 |
| RQ1/RQ2 是否与结论对应 | **PASS**：RQ1 对应 §4.3，RQ2 对应 §4.4，均在摘要/§1.1/§4 三处一致复述 |
| 成功标准表（Table 2） | **部分不足**：9 条标准全部标记 "Met"，但其中 `Length | Not specified | Met` 属空洞项（原文即未设标准却判达标），且与 §5.3 披露的 7 项缺陷并存，"全 Met"与"存在已知缺陷"的口径未作说明 → 建议加一句"Met 指达成既定标准，不排除 §5.3 已披露的可读性缺陷" |
| 未支持假设的处理 | **PASS**：H3 未被支持时未强行解释，改为报告同源共变与不可区分性，并保留 Williams/Steiger 检验结果 |

## 2.6 引用规范（APA 7）

| 检查项 | 结论 |
|---|---|
| 参考文献数量与排序 | 15 条，按字母序排列 |
| 正文引用 ↔ 文献表双向核对 | **未通过（硬伤）**：正文在 p136、p168、p172、p187、p304 多处引用 **Williams (1959)** 与 **Steiger (1980)**（H3 相关差异检验的方法学来源），但文献表（p425–p439）**缺失这两条** |
| 数据集类文献 | **PASS**：MGTO / DSEC / DSAT / Macao SAR Gov 均在 p85 正文以缩写合并引用，且在文献表 p431–p436 列出 |
| 工具类文献 | **PASS**：Hunter (2007)、Hunter & Matplotlib team (2024)、McKinney (2022)、Virtanen (2020)、Waskom (2021)、Plotly (2015)、Cairo (2016/2019)、Downey (2014)、Knaflic (2015)、Tufte (2001) 均正文引用且在表 |
| 未被引用的文献 | **PASS**：无孤立条目 |
| 方法名词误标 | **PASS**：Pearson / Spearman / Shapiro 仅作方法名出现，未误加引用 |

## 2.7 页数与格式规范

| 检查项 | 结论 |
|---|---|
| 页数 | **PASS**：42 页（Word `ComputeStatistics` 与 PDF 页数一致），低于课程 50 页上限 |
| 目录 | **PASS**：真实 Word TOC 域，51 条，页码正确 |
| 页脚页码 | **PASS**：全节连续 |
| 残留占位符 | **PASS**：全文无 `TODO` / `TBD` / `Error!` / `Reference source not found` |
| 摘要 | **缺失**：封面后直接进入目录，无 Abstract / Executive Summary，也无 List of Figures / List of Tables |
| 文档元数据 | **需清理**：`docProps/core.xml` 的 `creator` 为 `python-docx`、`created` 为 2013-12-23（模板自带）；`document.xml` 含 **72 处空 `<w:ins>`**（python-docx 写入遗留，作者多为空或 "Fong Chin Wai"），虽无评论/无 `<w:del>`，但会成为"文档来源"疑点 |
| 图件可读性（抽查） | **基本合格**：`.set_title`/轴标签/图例/数值标注完整；瑕疵为 Figure 10 Panel A 的热力图色阶仅单色系（无负相关冷色）、Figure 14 子图 (b) 零值区与底色对比偏低 → 均属可读性建议，不构成错误 |

## 2.8 报告自述与仓库实际的一致性

| 自述位置 | 声称 | 实际 | 结论 |
|---|---|---|---|
| §9.1 | notebooks 4 个文件 | 3 ipynb + `Cross_check_and_pending_revisions.md` | 一致 |
| §9.1 | Dashboard 顶层 6 个文件（含 2 个 README） | 6 个 + `__pycache__`（gitignore 内） | 一致 |
| §9.1 | Dashboard/data 20 CSV + geojson + dash/ | 20 CSV + 1 geojson + dash/(3) | 一致 |
| §9.1 | figures 30 PNG + archive/ + 单色副目录 | 30 + 2 + 30 | 一致 |
| §9.6 | data_processed 49 文件（45 CSV / 3 geojson / 1 SQLite） | 49 | 一致 |
| §9.6 / §9.4 | dashboard 16 charts、6.1 MB | 16 个 `Plotly.newPlot`、6.14 MB | 一致 |
| §9.5 | builder 读 15 CSV + 1 geojson | `build_dashboard.py` 读 15 CSV + geojson | 一致 |
| §10.1 | 正文用 23 / 30 张图，8 个文件未被引用 | 22 from figures + 1 from preview；8 未引用 | 一致 |
| §10.2 | `reports/data_dictionary.md` 存在 | 存在（另有 `data_coverage_audit_2026-11-04.md`、`district_map_interactive.html` 等未在 §9.1 枚举） | 基本一致 |

## 2.9 可复现性专项

| 检查项 | 结论 |
|---|---|
| requirements.txt | **PASS**：772 B，全部 pin 版本，与 §9.2 环境声明一致 |
| 运行顺序 | **PASS**：§9.3 给出 0–3 共 4 步，含 `pip install` 前置，与实际脚本名匹配 |
| 路径可移植性 | **PASS**：两个主 notebook 均"向上搜索 data_processed"，报告明确声明 `cisc7204_proposal_figures_colour.ipynb` 硬编码绝对路径且不参与本报告 |
| **notebook 编码** | **未通过（轻微）**：`CISC7204_ClassE_Team01_Visualization_updated.ipynb` 有 **21 个单元存在 UTF-8 二次编码**（如 cell 16、cell 25 的 `ax.set_title(f"Panel A. … â€” …")`），仓库现有 PNG 正常，但**任何人重跑 notebook 都会在图片标题里输出 `â€"` 乱码** → 现场复现演示有风险 |

---

# 第三部分 教师视角评分

> 以下按课程报告惯例设维度（百分制），采**严格评分者**口径：格式与引用细节按 0 容忍处理，论证质量按研究生课程标准衡量。若课程只做"完成度"评价，可上浮 4–5 分（约 88–89）。

## 3.1 维度评分

| 维度 | 权重 | 得分 | 评语 |
|---|---|---|---|
| 问题与目标（RQ 清晰度、假设可检验性、成功标准） | 10 | **9.0** | 两个 RQ + 三个可检验假设（H1 相关、H2 拆分、H3 偏相关）+ 成功标准表，目标—方法—结论三处一致。扣分：Table 2 出现 "Length \| Not specified \| Met" 的空洞标准 |
| 数据与方法（数据源、清洗、方法匹配度） | 20 | **17.0** | MGTO 45 个月度工作簿 → 无重复键/576 格平衡网格/单位重建（万次/日×天数）四道门禁，方法（Pearson、偏相关、Williams-Steiger、交叉相关、季节指数、YTD 口径）与问题匹配，样本 n=36 与 n=12 均明示。扣分：district-hour 面板"由未保存为脚本的探索性步骤产生"（§9.7 自述），削弱端到端可复现 |
| 结果与论证（数值正确性、结论强度、局限） | 25 | **21.0** | 全部关键统计量经独立复算 100% 复现；H2 拆成两个子句并明确"只成立其一"；H3 未支持时改为报告不可区分性，不硬拗因果。扣分：H1 仅报 r 与 p，未给 95% CI / 效应量（n=36 下 CI 很宽）；三张表（T12/T16/T18）未在正文引用，论证链上有断点 |
| 可视化与叙事（图质量、图注、设计原则） | 15 | **12.0** | 23 图、图注 + Source Line 全覆盖、按讨论顺序编号、主动披露双轴/截断轴/同分母轴等自身缺陷（Table 14）——这在课程作业里属高水准。扣分：Figure 4 Panel A 双轴仍在正文（仅作披露未替换）；图号与首次引用顺序不一致；单一色系色阶弱化负相关；Figure 12 三分母同轴只披露未修 |
| 可复现与交付手册（README、环境、运行顺序） | 10 | **8.0** | 第 9 章 8 小节是全篇最强部分：pin 环境、4 步运行、产物清单（Table 16）、不包含的内容（§9.7）、验证状态（§9.8）。扣分：可视化 notebook 21 处乱码 + 存在 `__pycache__`/`.ipynb_checkpoints` 等污染，复现环境未真正"干净" |
| 写作与格式（结构、长度、目录、排版） | 10 | **8.5** | 42 页、10 章、目录 51 条页码 0 错、编号连续、无占位符残留。扣分：**第 4 章标题为 "Project Deliverables and Incomplete Work"，却承载 4.2–4.7 全部结果分析**（结果章缺位）；无摘要；文档元数据残留 python-docx/2013 创建时间/72 处空修订 |
| 引用规范（APA 7） | 5 | **3.5** | 15 条、字母序、数据源与工具文献齐备。**硬扣**：Williams (1959)、Steiger (1980) 正文 5 处引用、文献表缺失 |
| 团队协作与反思（分工、个人贡献、反思） | 5 | **4.0** | §6 分工表 + §7 六人各自 verified 块 + §8 集体/个人学习，符合课程要求且写得实。扣分：Table 15 分工表 "Section 7 blocks" 列图号错位（7.4 写 "Figure 7, 7, 10"、7.6 写 "Figure 14, 14"），机械错误一眼可见 |
| **合计** | **100** | **83.5 → 84** | 等级：A−（优秀，但需一次"清稿"才能到 A） |

## 3.2 扣分明细（按严重程度排序）

### P0 — 必须提交前修掉（不改会直接扣分或被质疑）

| # | 问题 | 位置 | 影响 | 修法 | 预计提分 |
|---|---|---|---|---|---|
| 1 | 参考文献缺 **Williams (1959)**、**Steiger (1980)**，正文 5 处引用无出处 | 文献表 p425–p439 | APA 硬伤，考据型评分者必查 | 按字母序补两条完整条目 | +1.0 |
| 2 | 分工表 **图号错位**："Figure 7, 7, 10"、"Figure 14, 14" 重复 | Table 15，Section 7.4 / 7.6 行 | 机械错误，一眼可见 | 按 Table 17 重映射 | +0.4 |
| 3 | **T12 / T16 / T18 正文零引用** | §4.5、§9.6、§10.2 | 论证链断点，表格成"孤儿" | 各加一句 "as shown in Table N" | +0.4 |
| 4 | 根目录存**别组作业 4 份**（Pair06/08/10）+ 2 份内部工作笔记 md | 仓库根 | 观感与合规风险 | 移出仓库 | +0.5（印象） |
| 5 | `_temp\backup\…FinalReport_original_2026-11-26.docx` **实为 Proposal**（哈希与 Proposal 一致） | `Proposal\Project report\_temp\backup\` | 误导修订基线，可能被误读为"隐藏的原始版" | 删除或改名为 `Proposal_v1` | +0.3 |

### P1 — 强烈建议修（低成本高分）

| # | 问题 | 修法 | 预计提分 |
|---|---|---|---|
| 6 | 无 **Abstract / Executive Summary**、无 List of Figures/Tables | 封面后补半页摘要（RQ + 数据 + 三假设结论 + 一图结论），目录后加图表清单 | +0.5 |
| 7 | 第 4 章标题与内容错配（结果分析藏在 "Deliverables and Incomplete Work"） | 改为 "Results: Deliverables and Analysis"，或拆出 §5 为 "Results" | +0.5 |
| 8 | Table 2 全 "Met" 与 §5.3 缺陷并存，且 `Length \| Not specified` 空洞 | 加进度口径注释，删除或改写 Length 行 | +0.3 |
| 9 | docx 元数据：`creator=python-docx`、`created=2013-12-23`、72 处空 `<w:ins>` | Word 中"另存为"新文件并接受全部修订；或改 `core.xml` | +0.2 |
| 10 | notebook 21 处 UTF-8 二次编码（`â€"`）出现在 `set_title`/注释 | 以 UTF-8 重存 notebook，改回 `—`；重跑一次确认图题正常 | +0.3 |
| 11 | 图号未按首次引用递增（Figure 4/12/17 首现于 §6） | 若坚持"按讨论顺序"，则把 §6 中这三图的引用改为回指（"discussed in §4.x"）；否则统一改为按首次引用重编 | +0.2 |
| 12 | 视频两版 mp4 命名不规范、版本不明（91.99 MB） | 只留最终版并统一为 `CISC7204-Class_E-Team_01_` 前缀 | +0.2（印象） |

### P2 — 可选优化

13. H1/H2 相关系数补 95% bootstrap CI 与效应量说明（n=36 的宽区间本可成为加分点）。
14. Figure 4 Panel A 双轴改为两个单轴子图（现已披露，直接替换更彻底）。
15. `data_processed` 中 `mgto_district_hour_master_…` 与 `demand_district_hour_panel_…` 二选一，消除同数据两名。
16. 清理 `figures\archive\`、`minutes\archive_old\`、`extension\`（或 README 一句话交代用途）。

## 3.3 加分项（评分时已计入，但仍值得在提交说明中点出）

- **缺陷自披露（Table 14，7 项 + 修正动作）**：主动列出 Figure 4 双轴、Figure 17 截断轴、Figure 12 同分母轴等问题，在课程作业中极为罕见，显示方法自觉。
- **复现手册（第 9 章 8 节 + Table 16）**：pin 环境、运行顺序、产物清单、"不包含的内容"与"验证状态"四件套完整，远超一般课程报告。
- **诚实处理未支持假设**：H3 未成立时没有改口径凑显著性，而是改为报告"过夜更强于同日"（0.921 vs 0.694，t=6.29）与"对入住率不可区分"（0.861 vs 0.891，p=0.463）。
- **图注溯源到 notebook cell 级**（Table 17）：每张图都能落到具体单元与数据文件，这在本科/授课型硕士作业里属高配。

---

# 第四部分 提交前 Checklist

**必须（P0）**

- [ ] 补 Williams (1959)、Steiger (1980) 到参考文献（字母序位置）
- [ ] 修 Table 15 分工表图号（7.4 "Figure 7, 7, 10" → 正确映射；7.6 "Figure 14, 14" → 去重）
- [ ] 正文补 Table 12 / 16 / 18 的引用句
- [ ] 移出根目录 4 份别组作业与 2 份内部 md（`CISC7204_Report_TODO_BeforeAfter.md`、`CISC7204_TempMD_Compliance_Audit.md`）
- [ ] 删除 `Proposal\Project report\_temp\`（含误命名的 `FinalReport_original`）

**建议（P1）**

- [ ] 删 `temp_nbrun.log` / `temp_nbrun.err` / `temp\` / `notebooks\.ipynb_checkpoints\` / `Dashboard\__pycache__\` / `minutes\archive_old\` / 空目录 `minutes\_backup_before_download_20261126_222958\`
- [ ] 补 Abstract 与 List of Figures/Tables
- [ ] 改第 4 章标题（结果章命名）
- [ ] 清理 docx 元数据与 72 处空修订（Word 另存）
- [ ] 修 notebook 21 处 `â€"` 乱码并重跑确认图题
- [ ] 视频目录只留最终版 + 统一命名
- [ ] Table 2 加"Met 口径"注释

**收尾核对**

- [ ] 清理后重跑一次 `scripts/build_panels.py` + 两个 notebook，确认图/表数量与 Table 16 仍一致
- [ ] 重新导出 PDF，核对页数仍 < 50、目录页码仍 0 mismatch
- [ ] `git status` 确认无临时文件进入版本库（`.gitignore` 已覆盖大部分，但 `CISC7204_Report_TODO_BeforeAfter.md` 等未被忽略）

---

## 附录 A 审计方法与证据

| 环节 | 方法 | 关键输出 |
|---|---|---|
| 文件清单 | 递归枚举，排除 `.git` | 492 文件 / 236.4 MB；根目录 15 项 |
| 脏文件识别 | 模式匹配（`temp_nbrun.*`、`~$*`、`__pycache__`、`.ipynb_checkpoints`、`_temp`、`archive_old`、`_backup*`）+ 目录体积统计 | 7 类命中，共约 18.5 MB |
| 重复识别 | SHA-256 全量哈希（≥1 KB，排除 `.git`） | 17 组、6.58 MB |
| 报告结构 | python-docx：段落 440 / 表格 19 / 内嵌图 24；样式分离 Heading1/2/Caption T/Source Li/Code Bloc | 图 F1–F23、表 T1–T18 |
| 页码核对 | PyMuPDF 提取每页标题 → 与 TOC 51 条归一化比对 | 0 mismatch |
| 数值复算 | pandas + scipy：相关/偏相关/残差化/季节指数/份额/回归/Shapiro | 全部一致（见 2.4 表） |
| 视觉抽查 | 三图视觉解析（相关矩阵、季节指数、24 区地图）+ 定向核验 Figure 6 标题字符 | 轴/图例/单位完整；Figure 6 图题 `—` 正常（乱码仅存在于 ipynb 源码层） |
| 元数据 | 解包 docx 读 `docProps/core.xml`、`app.xml`、`document.xml` 统计修订标记 | Pages=42、Words=20286、72 `<w:ins>` |

## 附录 B 本次审计未覆盖的范围

1. 未运行任何 git 写操作，未核查提交历史与作者归属（仅读取到 §10.4 提到的单一提交 `0547248` 这一文本证据）。
2. 未在浏览器中实测 Dashboard 交互与 1.55 s 首屏计时，仅静态核对了 16 个 chart 容器与文件体积。
3. `extension\`（微信小程序）按课程外延产物处理，未做代码审计。
4. MGTO 原始 45 个工作簿未逐格重算，数值一致性以前述 `data_processed/` 与 `Dataset/` 为基准。
5. 视频内容未做质量评价，仅登记命名与体积问题。
*（内容由AI生成，仅供参考）*
