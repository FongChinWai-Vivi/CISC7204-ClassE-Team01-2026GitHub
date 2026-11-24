---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_b911f542e6de11f184bd52540072b1e8
    ReservedCode1: 75mShYUWl2x0Eu19Gh3OninEZKo52f0kgPq3YDPbn/D1lSz5freuhkkiFujQYRpRWRO5bCpJXjxRkAsIgGp78Y9SoBTLzrzAfHr3VXd5kgaaaClSOENfM5PEtZI8dU/4TDcuj7Q/MHgzmVuOxv718SjWLVhoHF5b0h2VgZauDljiJ6nHoeipnv+zc14=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_b911f542e6de11f184bd52540072b1e8
    ReservedCode2: 75mShYUWl2x0Eu19Gh3OninEZKo52f0kgPq3YDPbn/D1lSz5freuhkkiFujQYRpRWRO5bCpJXjxRkAsIgGp78Y9SoBTLzrzAfHr3VXd5kgaaaClSOENfM5PEtZI8dU/4TDcuj7Q/MHgzmVuOxv718SjWLVhoHF5b0h2VgZauDljiJ6nHoeipnv+zc14=
---

# 静态 HTML 结构基准（CISC7204_ClassE_Team01_Dashboard.html）

- 源文件：`C:\Users\07viv\Desktop\CISC7204-Team01\Dashboard\CISC7204_ClassE_Team01_Dashboard.html`（6.12 MB）
- 页面标题：Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao
- CSS：`assets/dashboard.css`（5510 字符），变量 `--navy:#1B4965`, `--blue:#2E86AB`, `--sky:#62B6CB`, `--red:#EE6C4D`, `--gold:#F4A259`, `--green:#3E8914`, `--purple:#7B2CBF`, `--ink:#0E2136` …
- 版面：`header`（标题 + pills）→ `.filterbar`（sticky，Year/Zone/District 下拉 + Play/Reset + hiChip + scopeText）→ `.kpis`（6 张数字卡）→ `.grid`（12 列，16 张图卡）→ `footer`

## 一、筛选控件

| id | 标签 | 选项 | 默认 |
|---|---|---|---|
| `selYear` | Year | All years (2023-2026)、2023、2024 …（共 5 项） | all |
| `selZone` | Zone | All zones、Macau Peninsula、Taipa & Cotai …（共 4 项） | all |
| `selDistrict` | District | All 24 districts、COTAI Reclamation Area (路氹填海區)、Zona de Aterros do Porto Exterior (新口岸區) …（共 25 项） | all |
| `selMetric` | Map metric | Headcount share (%)、Headcount per km² per month、2026 share shift (pp) …（共 4 项） | share |
| `btnPlay` | ▶ Play years (auto-cycle 2023→2026, 1.7 s/step) | ▶ Play years (auto-cycle 2023→2026, 1.7 s/step) | — |
| `btnReset` | Reset filters | Reset filters | — |

## 二、KPI 卡片

| # | 文本 |
|---|---|
| 1 | 103.2M Visitor arrivals |
| 2 | 42.5M Visitor-guests |
| 3 | 9.96 → 5.83 Bus trips per visitor |
| 4 | 2,229 District concentration (HHI) |
| 5 | 85.7% Occupancy rate |
| 6 | 0.51 Taipa & Cotai demand/supply |

> 过滤生效时仅 KPI-4（HHI）与 KPI-4 副标题由 JS 重算，其余 5 张为静态值。

## 三、图表卡片（按页面顺序）

| # | 图 id | 卡片跨度 | 卡片标题 / 副标题 | trace 构成 | 高度 |
|---|---|---|---|---|---|
| 1 | `f_long` | span12 | 1 · Long-run monthly visitor arrivals, 2015-2026 / Pandemic years are drawn in red and cannot be read as normal demand; the shaded band is the 36-month estimation window used in every correlation reported below. | 3 条：scatter(2015-2019 (pre-pandemic))；scatter(2020-2022 (pandemic, red dashed))；scatter(2023-2026 (recovery)) | 330 |
| 2 | `f_month` | span7 | 2 · Arrivals and bus passenger trips, monthly / Arrivals recover year by year, but the ridership line on the right axis does not keep pace - the coupling weakens as the market grows. | 3 条：bar(Visitor arrivals (M, left))；scatter(Bus passenger trips (M, right))；scatter(Trips per visitor (right)) | 330 |
| 3 | `f_quarter` | span5 | 3 · Bus trips per visitor, quarterly / The headline ratio falls every quarter: each visitor is served by fewer scheduled trips than the quarter before. | 2 条：bar(Bus trips per visitor)；scatter | 330 |
| 4 | `f_hocc` | span7 | 4 · Visitor arrivals and the hotel occupancy rate / Rooms fill as the city fills: the occupancy rate on the right axis tracks visitor arrivals on the left, month by month, so the hotel stock is doing the work of absorbing the crowd. | 2 条：bar(Visitor arrivals (million, left))；scatter(Hotel occupancy rate (%, right)) | 356 |
| 5 | `f_hrel` | span5 | 5 · Occupancy against bus trips per visitor / Each point is one month and the colour is the year. Occupancy pushes to the right across 2023-2026 while ridership per visitor slides down: the rooms fill up, but the bus network does not carry proportionally more. | 4 条：scatter(2023)；scatter(2024)；scatter(2025)；scatter(2026) | 356 |
| 6 | `f_hstar` | span6 | 6 · Who fills the rooms: hotel guests by hotel class / Monthly guest counts split by hotel star rating, straight from the DSEC hotel survey. The 5-star tier dominates the stack, so capacity that ignores it is capacity aimed at a minority of the hotel base. | 4 条：bar(2-Star hotels)；bar(3-Star hotels)；bar(4-Star hotels)；bar(5-Star hotels) | 356 |
| 7 | `f_hhist` | span6 | 7 · The long occupancy record, 2014-2026 / The full DSEC monthly occupancy series: the pandemic collapse, the 2023-2026 climb, and how far the market now sits above the 2019 mean before the buses are planned for it. | 1 条：scatter(Hotel occupancy rate) | 356 |
| 8 | `f_zone` | span6 | 8 · Supply-demand mismatch across the three zones / Demand share is compared with the share of scheduled departures and of bus stops. A zone where the demand bar is taller than the supply bars is under-supplied. | 3 条：bar(Visitor demand)；bar(Scheduled departures)；bar(Bus stops) | 330 |
| 9 | `f_dep` | span6 | 9 · Visitor headcount carried per scheduled departure / The cleanest single measure of load: how many visitor-hours of demand sit behind each scheduled departure in the zone. Hover for the supply/demand ratio. | 1 条：bar | 330 |
| 10 | `f_hour` | span12 | 10 · Demand and scheduled supply by hour of day / The red line is the visitor demand share for the current filter; the blue line is the scheduled departure share. Bars are the gap in percentage points - red bars are hours where demand runs ahead of supply. | 5 条：scatter(Visitor demand share (all periods))；scatter(Visitor demand share (filtered))；scatter(Scheduled departures (weekday))；scatter(Scheduled departures (weekend))；bar(Gap vs weekday supply (pp)) | 360 |
| 11 | `f_map` | span7 | 11 · The 24 DSEC statistical districts / The Year / Zone / District filters above drive this map (colours are recomputed for the selected year); pick a Zone or a district with the top filters to spotlight it. Click a district here to filter views 8, 9, 10 and 12. | 1 条：choropleth | 470 |
| 12 | `f_heat` | span5 | 12 · District by hour-of-day profile / Each row is rescaled to that district's own daily total, so a small district and Cotai can be read side by side. Click a row to filter. | 1 条：heatmap | 470 |
| 13 | `f_season` | span6 | 13 · Seasonality of arrivals, 2023-2025 / Index on the 2023-2025 monthly mean; red bars are the flagged peak months. Capacity planning that ignores this shape under-supplies the peaks. | 1 条：bar(Seasonal index (2023-2025 mean = 100)) | 330 |
| 14 | `f_golden` | span6 | 14 · Golden Week daily intensity / Daily arrivals inside the 1st October Golden Week expressed as a multiple of that month's average day. The shape of the peak is what the bus schedule has to absorb. | 5 条：scatter(2019)；scatter(2023)；scatter(2024)；scatter(2025)；scatter(2026 Spring Festival (partial year)) | 330 |
| 15 | `f_shift_zone` | span12 | 15 · What shifted in 2026 / 2026 year-to-date against the 2023-2025 baseline: the demand keeps tilting towards Cotai, and the hour-of-day shape barely moves. | 1 条：bar(Zone share shift (pp)) | 300 |
| 16 | `f_shift_hour` | span12 | 15 · What shifted in 2026 / 2026 year-to-date against the 2023-2025 baseline: the demand keeps tilting towards Cotai, and the hour-of-day shape barely moves. | 1 条：bar(Hour share shift (pp)) | 340 |

## 四、前端交互逻辑（JS → Dash 回调映射）

| JS 函数 | 作用 | Dash 实现 |
|---|---|---|
| `fillSelects` | 生成 Year/Zone/District 选项 | dcc.Dropdown 静态 options |
| `filteredRows` | 按 year/zone/district 过滤 panel 行 | filtered_rows() |
| `hourProfile` | 24 小时需求占比 v/total*100 | hour_profile() |
| `heatFromRows` | 分区 × 小时的行归一化百分比 | heat_from_rows() |
| `refreshHotel` | 按年份重切 3 张酒店图 | rebuild_hotel() |
| `applyMap` | 按 metric 重建 choropleth z / 色阶 / 色条刻度 | rebuild_map() |
| `highlightZone` | zone 高亮 + 过滤 chip | 更新 f_zone/f_dep 的 marker.opacity + hiChip |
| `updateHHI` | HHI、等值区数、top3 占比 | update_hhi() |
| `togglePlay` | 1.7 s 自动轮播年份 | dcc.Interval + Play 按钮 |
| `pickDistrict/pickZone` | 点击地图/热力图/柱状图联动筛选 | clickData 回调写入对应 Dropdown |

## 五、Plotly 统一配置

```json
{"responsive": true, "displaylogo": false, "modeBarButtonsToRemove": ["select2d", "lasso2d", "autoScale2d", "toggleSpikelines"], "toImageButtonOptions": {"format": "png", "filename": "cisc7204-team01-chart", "scale": 2}}
```
*（内容由AI生成，仅供参考）*
