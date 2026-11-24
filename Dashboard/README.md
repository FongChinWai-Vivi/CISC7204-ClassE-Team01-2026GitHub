---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 8aaebaa239fa14c1cf5eb03fd99189ca_b7197a35e6de11f184bd52540072b1e8
    ReservedCode1: nCbvzQ3+ZIOdoGG9BUrw08z0RyYgpB+k+lo94JkZo2c2z0YRwU/e34oDnoMG93MDvnWEHiHWNBBoDmwQb5bkVXpTsjIQRSleDSfXEZdPqctIX8oRRWjxqkSLXxa5i2tRHnQtSVWKEINK/X3/7rSbZzHe1myIh/8IWoHpaf2oSZmjN36yx7dJAwachJU=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 8aaebaa239fa14c1cf5eb03fd99189ca_b7197a35e6de11f184bd52540072b1e8
    ReservedCode2: nCbvzQ3+ZIOdoGG9BUrw08z0RyYgpB+k+lo94JkZo2c2z0YRwU/e34oDnoMG93MDvnWEHiHWNBBoDmwQb5bkVXpTsjIQRSleDSfXEZdPqctIX8oRRWjxqkSLXxa5i2tRHnQtSVWKEINK/X3/7rSbZzHe1myIh/8IWoHpaf2oSZmjN36yx7dJAwachJU=
---

# Dashboard (Plotly Dash, aligned 1:1 with the static HTML)

CISC7204 Class E Team 01 — Macau visitor-arrival / hotel-occupancy / bus-ridership dashboard.

本文件夹同时保留「静态 HTML」与「Dash 可执行版」两条交付线，两者版面、内容、图表顺序完全一致：

| 文件 | 状态 | 说明 |
|---|---|---|
| `CISC7204_ClassE_Team01_Dashboard.html` | **未改动** | 6.12 MB 预渲染静态版，作为 Dash 版的唯一版面基准 |
| `build_dashboard.py` | **未改动** | 生成静态 HTML 的构建脚本 |
| `README_Dashboard.md` | **未改动** | 静态 HTML 版的说明 |
| `app.py` | 本轮重写 | Dash 应用，863 行，版面对齐静态 HTML |
| `README.md` | 本轮重写 | 本文件 |

---

## 1. 与静态 HTML 的对应关系

Dash 版不是"另做一套"，而是把静态 HTML 拆成三份可编程资产，再原样在 Dash 里重建：

| 资产 | 路径 | 来源与作用 |
|---|---|---|
| 页面骨架 | `data/dash/body_template.html` (10.8 KB) | 从静态 HTML 的 `<body>` 抽出：header → sticky filterbar → 6 张 KPI 卡 → 16 张图卡 → footer，含全部文案与 class |
| 16 张图的 Plotly JSON | `data/dash/figures.json` (1.1 MB) | 从静态 HTML 中内联的 Plotly figure 直接抽出，Dash 首屏原样注入，保证与静态版同一套 trace / 轴 / 配色 |
| 回调所需数据 | `data/dash/payload.json` (639 KB) | 24 个区的中英名/分区/份额/密度、区×月×小时面板行、酒店序列、KPI 常量 |
| 样式 | `assets/dashboard.css` | 静态 HTML 的原始 CSS（`--navy:#1B4965`、`--blue:#2E86AB`、`--sky:#62B6CB`、`--red:#EE6C4D`、`--gold:#F4A259`、`--green:#3E8914`、`--purple:#7B2CBF`、`--ink:#0E2136`） |
| 结构基准 | `preview/html_structure.json` / `preview/html_structure.md` | 解析出的页面结构清单：标题、版面顺序、控件选项、KPI 文案、16 图卡片表、JS→Dash 映射 |

`app.py` 启动时读取上述三份 JSON/HTML，用 `TAG_MAP` 把 body 的每个 HTML 标签映射成对应的 `dash.html` 组件（`class`/`style`/`id` 全部保留），因此 DOM 层级、class 名、文案与静态版一致；**8 张静态图**（`f_long`、`f_month`、`f_quarter`、`f_hhist`、`f_season`、`f_shift_zone`、`f_shift_hour`、`f_golden`）在首屏即用 `figures.json` 的原始 JSON 渲染，**8 张联动图**（`f_hour`、`f_heat`、`f_map`、`f_zone`、`f_dep`、`f_hocc`、`f_hrel`、`f_hstar`）在服务端按筛选重算。

> `data/dash/` 下的三份资产与 `preview/html_structure.*` 是一次性从静态 HTML 抽取的产物（抽取脚本不随仓库交付）；静态 HTML 若重新构建，需按 `preview/html_structure.md` 描述的结构重新抽取这三份资产。

### 1.1 控件（对应 HTML 的 4 个 `<select>` + 2 个按钮）

| Dash id | 原 HTML 元素 | 选项 | 默认 | 作用 |
|---|---|---|---|---|
| `selYear` | Year | All years (2023-2026)、2023–2026（5 项） | all | 重算酒店 2 图 + 地图 + HHI + scope 文案 |
| `selZone` | Zone | All zones、Macau Peninsula、Taipa & Cotai、Coloane（4 项） | all | 过滤区→图的散点不透明度 + 高亮 chip |
| `selDistrict` | District | All districts + 24 个区（25 项，值为 0–23 索引） | all | 过滤小时图/热图/HHI |
| `selMetric` | Map metric | Headcount share (%)、Headcount per km² per month、2026 share shift (pp)、Headcount per departure（4 项） | share | 重建 choropleth 的 z、色阶与色条刻度 |
| `btnPlay` | ▶ Play years | — | — | 配合 `dcc.Interval(1700 ms)` 轮播 2023→2026 |
| `btnReset` | Reset filters | — | — | 4 个下拉 + 播放状态全部复位 |

HTML 里没有新增控件，也没有删减控件；没有月份范围滑块、没有 24 区多选——这两项属于上一版自设布局，本轮已全部移除。

### 1.2 KPI（6 张，与 HTML 一致）

| # | 文本 | Dash 中是否重算 |
|---|---|---|
| 1 | 103.2M Visitor arrivals | 静态 |
| 2 | 42.5M Visitor-guests | 静态 |
| 3 | 9.96 → 5.83 Bus trips per visitor | 静态 |
| 4 | 2,229 District concentration (HHI) | **动态**（`kpiHhiV` / `kpiHhiS`） |
| 5 | 85.7% Occupancy rate | 静态 |
| 6 | 0.51 Taipa & Cotai demand/supply | 静态 |

### 1.3 16 张图 1:1 对照

| # | fig id | 卡片跨度 | HTML 标题（截断） | trace 构成 | 高度 | Dash 实现 |
|---|---|---|---|---|---|---|
| 1 | `f_long` | span12 | 1·Long-run monthly visitor arrivals, 2015-2026 | 3 scatter（pre-pandemic / pandemic dashed red / recovery） | 330 | 静态 JSON |
| 2 | `f_month` | span7 | 2·Arrivals and bus passenger trips, monthly | bar + scatter + scatter（双轴） | 330 | 静态 JSON |
| 3 | `f_quarter` | span5 | 3·Bus trips per visitor, quarterly | bar + scatter（趋势线） | 330 | 静态 JSON |
| 4 | `f_hocc` | span7 | 4·Visitor arrivals and the hotel occupancy rate | bar + scatter（双轴） | 356 | 动态（年份切换重切序列） |
| 5 | `f_hrel` | span5 | 5·Occupancy against bus trips per visitor | 4 scatter（2023–2026 按年份着色） | 356 | 动态 |
| 6 | `f_hstar` | span6 | 6·Who fills the rooms: hotel guests by hotel class | 4 bar（2/3/4/5 星堆叠） | 356 | 动态（年份切换重切） |
| 7 | `f_hhist` | span6 | 7·The long occupancy record, 2014-2026 | 1 scatter | 356 | 静态 JSON |
| 8 | `f_zone` | span6 | 8·Supply-demand mismatch across the three zones | 3 bar（需求/班次/站点份额） | 330 | 动态 + 点击联动 |
| 9 | `f_dep` | span6 | 9·Visitor headcount carried per scheduled departure | 1 bar | 330 | 动态 + 点击联动 |
| 10 | `f_hour` | span12 | 10·Demand and scheduled supply by hour of day | 5 trace（2 需求线 + 2 班次线 + 缺口 bar） | 360 | 动态 |
| 11 | `f_map` | span7 | 11·The 24 DSEC statistical districts | choropleth（24 区 GeoJSON） | 470 | 动态（metric 重建 z/色阶） |
| 12 | `f_heat` | span5 | 12·District by hour-of-day profile | heatmap（行归一化 100%） | 470 | 动态 + 点击行联动 |
| 13 | `f_season` | span6 | 13·Seasonality of arrivals, 2023-2025 | 1 bar（峰值月红色） | 330 | 静态 JSON |
| 14 | `f_golden` | span6 | 14·Golden Week daily intensity | 5 scatter（2019/2023–2026） | 330 | 静态 JSON |
| 15 | `f_shift_zone` | span12 | 15·What shifted in 2026（分区份额） | 1 bar | 300 | 静态 JSON |
| 16 | `f_shift_hour` | span12 | 15·What shifted in 2026（小时份额） | 1 bar | 340 | 静态 JSON |

---

## 2. 依赖与运行

环境：Windows 11、`C:\Users\07viv\anaconda3\python.exe`（Python 3.12.3）、dash 4.4.1、plotly 5.22.0、pandas 2.2.2、numpy 1.26.4。

```powershell
cd "C:\Users\07viv\Desktop\CISC7204-Team01\Dashboard"
& "C:\Users\07viv\anaconda3\python.exe" app.py
```

打开 <http://127.0.0.1:8050>。入口参数 `app.run(debug=False, host="127.0.0.1", port=8050)`：

- `debug=False`，不会 spawn 第二个进程；
- 若 8050 已被占用，先 `Stop-Process -Id <pid>`（查进程：`Get-NetTCPConnection -LocalPort 8050`）；
- 全部路径基于 `__file__` 解析，`python app.py` 在任何工作目录下均可运行；
- 运行时**不访问网络**：plotly.js 由 Dash 从 `/_dash-component-suites/plotly/package_data/plotly.min.js` 本地提供，CSS 走 `assets/dashboard.css`。

`app.py` 还对 `app.index_string` 做了覆盖，去掉 Dash 默认外层的 `<footer>` 包装，否则整页高度会多出 43 px、与静态版对不齐。

---

## 3. 回调清单（5 个）

| # | 回调 | 输出 | 输入 |
|---|---|---|---|
| 1 | `update_linked` | `f_hour`、`f_heat`、`f_map`、`f_zone`、`f_dep`、`f_hocc`、`f_hrel`、`f_hstar`、`kpiHhiV`、`kpiHhiS`、`scopeText`、`hiChip`(children+style)、`heatCount`（共 14 个输出） | `selYear.value`、`selZone.value`、`selDistrict.value`、`selMetric.value` |
| 2 | `pick_district` | `selDistrict.value` | `f_map.clickData`、`f_heat.clickData` |
| 3 | `pick_zone` | `selZone.value`、`selDistrict.value` | `f_zone.clickData`、`f_dep.clickData` |
| 4 | `drive_play` | `selYear.value`、`playTick.disabled`、`btnPlay.children`、`btnPlay.className` | `btnPlay.n_clicks`、`playTick.n_intervals` |
| 5 | `reset_all` | 4 个下拉 value + `playTick.disabled` + `btnPlay.children` + `btnPlay.className` | `btnReset.n_clicks` |

复用的纯函数：`filtered_rows`、`hour_profile`、`heat_from_rows`、`scope_mask`、`year_share`、`hhi_texts`、`rebuild_hour`、`rebuild_heat`、`rebuild_map`、`rebuild_zone_charts`、`rebuild_hotel`、`compute_view`。

> 注意：`PLAY_SEQ` 里必须是 **int** 年份（与 `selYear` 的 options 值同类型）。若输出字符串 `"2025"`，Dash 的 dropdown 找不到匹配项，按钮照常播放但年份标签会显示为空白——这一点在联调中实际踩到并已修正。

---

## 4. 验证结果

用 headless Chrome（CDP，1600 px 宽，`captureBeyondViewport`）分别截取两版整页：

- 静态 HTML 基准：`preview/html_reference.png`（1600 × 5104）
- Dash 实际运行：`preview/dash_preview.png`（1600 × 5104）
- 播放态截图（附加证据）：`preview/dash_play_state.png`

| 检查项 | 结果 |
|---|---|
| 页面标题 | 两版完全一致（Visualizing the Relationship Between Visitor Arrivals, Hotel Occupancy, and Bus Ridership in Macao） |
| 整页尺寸 | 均为 1600 × 5104，逐像素对齐 |
| 整页像素差（灰度阈值 24） | **0.263%** |
| 16 张图 bbox / 轴标题 / trace 数量 | 全部一致 |
| 静态图（8 张） | 直接使用 HTML 内联的 Plotly JSON，**0.00% 差异** |
| 联动图 | `f_long` 0.50%、`f_month` 0.78%、`f_hocc` 0.59%、`f_hrel` 0.25%、`f_hstar` 0.52%、`f_zone` 0.57%、`f_hour` 0.79%、`f_golden` 0.65%（差异集中在图例文字与抗锯齿边缘） |
| Year 切换 | 选 2024 → `scopeText` 变 `2024 · all 24 districts 33.74M ...`，酒店 3 图与地图重算 |
| Zone 点击联动 | 点 `f_zone` 第一根柱 → `selZone` 变 Macau Peninsula、`scopeText` 变 `2023-2026 · Macau Peninsula districts 58.14M ...` |
| District 过滤 | 选 Cotai → HHI 10,000（单一区，等价区数 1.00） |
| Play 轮播 | 点击后按钮变 `❚❚ Pause`，Year 标签 2023→2024→2025 逐格前进，再次点击暂停 |
| Reset | 4 个下拉全部回到 All，页面回到初始态（高度回到 5104） |
| 外部依赖 | HTML 中无 `cdn.plot.ly` / unpkg / jsdelivr 引用；plotly.js 本地加载 |

### 残留差异（已知）

1. 8 张联动图的图例文字与曲线边缘存在 0.25%–0.79% 的抗锯齿级差异（同一份 JSON 结构、同一套字体族，渲染子像素不同），肉眼不可辨；
2. 播放态下整页高度为 5109 px（比默认态多 5 px），原因是按钮文案在 `▶ Play years` / `❚❚ Pause` 之间切换时 filterbar 内文本宽度变化引起的换行差异，不影响图表布局；
3. 静态版中由 JS 现算的 `f_golden` / `f_season` / `f_hour` / `f_shift_hour` 在 Dash 里改由服务端重建，数值取自 `payload.json`，与 HTML 首屏展示值一致，但不再是"浏览器端算出来"的同一条代码路径。

---

## 5. 已知限制

- **开发服务器**：`app.run()` 为 Flask/Werkzeug dev server，无 WSGI/HTTPS 配置，仅本机使用。
- **无缓存**：每次筛选重算 8 张图并整份序列化返回；`payload.json` 的面板已按行压缩（`y/d/h/v` 四列），但仍无 `dcc.Store` 级缓存。
- **启动成本**：导入时读取约 1.8 MB JSON（payload + figures）并解析 body 模板，冷启动约 3–5 s。
- **状态在浏览器侧**：刷新即回到默认 All/All/All/share，不做会话持久化。
- **地图粒度**：24 个 DSEC 统计区多边形，无街道级细节；色阶按 metric 固定分档。
- **无自动化测试**：验证为一次性 headless Chrome 脚本 + 像素比对，脚本不随仓库交付。
- **编码**：全部文件 UTF-8；Windows 旧代码页控制台打印中文区名可能乱码，浏览器渲染正常。

---

*本 README 描述的是本轮重写后的 Dash 版（`app.py`，863 行，5 个回调、4 个下拉 + 2 个按钮、16 张图、6 张 KPI 卡），与静态 HTML 逐图对齐。*
*（内容由AI生成，仅供参考）*
