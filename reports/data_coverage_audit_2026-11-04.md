---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_081c5f19d85f11f19232525400248c00
    ReservedCode1: Dyy6ixsDvCi7s6V02KFF3kckmFl2aY9mYle4UA3GWqKAURBJ+dpPAVaMkP78nTlne5IFvdH8nGOx/yyFF/TLUwXJKHBYtZNqBeExOm0BODRofKR3hugN+Px9+l4eB2m43plKgphyjw3hqTBuArEgQ4fvdMG5041ufRbeaEH60+sJKk3ldXLCx5ZR8UA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_081c5f19d85f11f19232525400248c00
    ReservedCode2: Dyy6ixsDvCi7s6V02KFF3kckmFl2aY9mYle4UA3GWqKAURBJ+dpPAVaMkP78nTlne5IFvdH8nGOx/yyFF/TLUwXJKHBYtZNqBeExOm0BODRofKR3hugN+Px9+l4eB2m43plKgphyjw3hqTBuArEgQ4fvdMG5041ufRbeaEH60+sJKk3ldXLCx5ZR8UA=
---

# 数据覆盖与更新时间审计（核查日期 2026-11-04）

结论：四类核心数据源均可覆盖到 **2026-09**，季度分析窗口可扩展为 **2023Q1 – 2026Q3（15 个季度 / 45 个月）**。

## 一、各数据源覆盖状态

| 数据源 | 本地文件 | 本地覆盖 | 上游最新 | 状态 |
|---|---|---|---|---|
| MGTO Data+ 澳门区域旅游数据（分区×时段） | `data/mgtodataplus/*.xlsx`（45 个） | 2023-01 – 2026-09 | 2026-09（2026-10 未发布） | 本次补齐 4 个月，已同步 |
| DSEC 入境旅客（月度） | `data_processed/demand_monthly_arrivals.csv` | 2008-01 – 2026-09 | 2026-09（2026-10-22 发布） | 本次补 2026-09 |
| DSEC 酒店业（入住率 / 住客数 / 客房数） | `data_processed/monthly_panel_2023_01_2026_09.csv` | 2023-01 – 2026-09 | 2026-09（2026-10-29/30 发布） | 本次新增，45 个月 |
| DSAT 公共巴士（月度） | `Monthly_Bus_Database/bus_monthly_2020_2026.csv` | 2020-01 – 2026-09（81 个月） | 2026-09 | 原本已到 9 月，无需更新 |
| data.gov.mo 镜像（旅游及博彩类） | `data/gov_mo_datasets/*.xlsx` | 记录更新时间 2026-08-31 | 落后 Data+ 约 1 个月 | 不建议作为主源 |

## 二、mgtodataplus 缺口的真实构成（原判断「41 个 xlsx，缺 2023-01 / 2023-02 / 2025-11」需修正）

| 月份 | 原判断 | 核查结果 |
|---|---|---|
| 2023-01 | 缺失 | **确实缺失**。Data+ 统计表页面下拉只给 `202301_en.pdf`，该 pdf 直链已失效（返回 HTML 错误页）；xlsx 直链可用 → 已下载补齐（84,487 B） |
| 2023-02 | 缺失 | **确实缺失**，同上 → 已下载补齐（136,252 B） |
| 2025-11 | 缺失 | **并未缺失**。官方文件名本身即 `MacaoDistrictTourismData_2025011_en.xlsx`（年份 2025 后多一个 `0`），文件内部 year=2025、month=11。本地 41 个文件中已含此文件 |
| 2026-08 | — | 上游已发布，本地原缺 → 已下载（544,511 B） |
| 2026-09 | — | 上游已发布，本地原缺 → 已下载（594,007 B） |

修正后的缺口 = 2023-01、2023-02、2026-08、2026-09 共 **4 个月**；补齐后 45 个文件，**2023-01 – 2026-09 连续无缺月**。

## 三、关键结构发现：每月文件是「年度累计（YTD）」

同一文件夹内文件为年内累计：`_202506` 内含 2025-01 至 2025-06 共 6 个月、每月 576 行（24 分区 × 24 时段）；`_202512` 含全年 12 个月；`_202609` 含 2026-01 至 09。

- 必须**每年只取该年最后一个文件**（202312 / 202412 / 202512 / 202609）建面板，否则同月重复累加。
- 若按「逐文件读取全部月份行」处理，会得到 160,704 行的重复样本，季度总量虚高 4–5 倍（例如 2025Q1 会被算成 1.11 亿人次）。
- 正确去重后：25,920 行 = 45 月 × 576，每月行数完全一致。

## 四、本次产出数据集

| 文件 | 内容 | 规模 |
|---|---|---|
| `data_processed/mgto_district_hour_master_2023_01_2026_09.csv` | 分区×时段长表（去重） | 25,920 行 |
| `data_processed/mgto_quarter_hour_2023Q1_2026Q3.csv` | 季度×时段合计 | 360 行 |
| `data_processed/mgto_quarter_district_2023Q1_2026Q3.csv` | 季度×分区合计 | 360 行 |
| `data_processed/monthly_panel_2023_01_2026_09.csv` | 月度综合面板（游客 / 酒店三项 / 巴士 / 分区人次） | 45 行，无缺值 |
| `data_processed/quarterly_panel_2023Q1_2026Q3.csv` | 季度综合面板 | 15 行 |

## 五、按季度的初步相关性（2023Q1–2026Q3，n=15）

| 关系 | 相关系数 |
|---|---|
| 入境旅客 vs 巴士日均班次（万人次） | 0.9455 |
| 入境旅客 vs 酒店客房平均入住率 | 0.9722 |

季度指标中 `bus_trips_per_arrival` 呈持续下行：2023Q1 9.96 → 2024 年均约 6.4–7.1 → 2025 年 5.5–6.1 → 2026Q3 5.55，与旅客结构由团客转向自由行、以及轻轨／步行分流一致，可作为 M3 供需模型的解释变量线索。

## 六、后续注意事项

1. 2026-10 数据尚未发布（MGTO Data+ 与 DSEC 均无），若做「最新月」结论需停在 2026-09。
2. 巴士 `buses_in_service` 自 2026-04 起为空值，季度面板中西侧该列取季度内最大值（2026Q2、2026Q3 为空）。
3. 酒店入住率为月度值的算术平均，非按客房夜加权；若要加权需补房晚数据。
4. `data/gov_mo_datasets/*.xlsx` 实为 data.gov.mo 的下载包（zip 内含 csv + readme.json），扩展名虽为 xlsx 但 openpyxl 无法读取，需按 zip 处理。
*（内容由AI生成，仅供参考）*
