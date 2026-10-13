# AGENTS.md —— Agent 工作约束与项目说明

> 本文件用于约束 AI 编码 Agent（含 Codex / Claude Code / 豆包等）在本仓库中的行为。
> 所有自动化开发必须先阅读本文件，并严格遵守其中的背景口径与技术选型约束。

## 1. 项目背景

- **课程**：金融大数据分析与应用（第 4 章 金融数据描述性分析与可视化）
- **任务**：教材 P92 实战演练 —— **比亚迪股票价格走势分析与可视化**
- **标的**：比亚迪（A 股代码 **002594**，深圳证券交易所）
- **数据**：`data/比亚迪后复权历史行情数据.xlsx`
  - 时间范围：2023-01-03 至 2023-12-29，共 **242 个交易日**
  - 价格口径：**后复权**日线（开盘 / 收盘 / 最高 / 最低）
  - 其他字段：成交量（手）、成交额（元）、振幅、涨跌幅(%)、涨跌额、换手率(%)
- **分析目标**（对应教材 4.1–4.3）：
  1. 价格与交易变量的描述性统计（集中趋势、离散程度、分布形态）；
  2. 日涨跌幅（日收益率）分布、年化波动率、最大回撤；
  3. K 线图 + 成交量 + 简单移动平均线 MA5/MA10/MA20/MA60；
  4. 月度收益统计；
  5. 以**移动端 H5 静态页面**呈现分析过程与结果。

## 2. 技术选型约束（强制）

### 2.1 数据分析

- Python 3.10+，仅使用 **pandas / numpy**（分析脚本 `analysis/analyze.py`）。
- 分析结果统一输出为 `data/byd_data.json`，供页面消费；不得让前端直接解析 xlsx。
- 所有统计量必须可由脚本复算，禁止在页面或文档中手写未经计算的数字。

### 2.2 数据可视化（重点约束）

- 图表库统一使用 **Apache ECharts 5（Canvas 渲染）**，不得混用 Chart.js / D3 / Highcharts 等。
- 必备图表及系列：
  - **K 线图（candlestick）**：主图，叠加 MA5/MA10/MA20/MA60 折线；
  - **成交量柱形图**：与 K 线主图联动（dataZoom 同步），涨跌日按 A 股配色；
  - **日涨跌幅分布直方图/柱形图**；
  - **月度收益率柱形图**（正负异色）；
  - 描述统计以表格 / 指标卡呈现。
- 图表必须包含：tooltip 提示、图例、dataZoom 区间缩放；移动端单指可操作。
- **A 股配色约定（强制）**：红涨绿跌 —— 上涨 `#D54941`（红）、下跌 `#2BA471`（绿），
  严禁使用欧美市场的绿涨红跌。
- 可访问性：不得仅靠颜色传达含义，阳线/阴线同时以文字（涨跌幅数值）表达。

### 2.3 UI 控件与设计

- UI 控件统一使用 **TDesign（腾讯设计体系）移动端组件：tdesign-mobile-vue**。
  - 组件规范来自 **TDesign MCP**（<https://tdesign.tencent.com/vue-next/mcp>），
    由 MCP 输出的组件用法与设计 Token 落地为本仓库的静态实现；
  - 静态页无构建步骤，使用其 UMD 产物 `vendor/tdesign.min.js` + `tdesign.min.css`。
- 视觉设计必须遵循 **ui-ux-pro-max** 技能生成的设计系统（见 `docs/design-system.md`）：
  - 风格：Minimalism & Swiss Style（瑞士极简），移动端浅色金融数据风；
  - 字体：IBM Plex Sans（系统无此字体时回退 -apple-system / PingFang SC）；
  - 主色：海军蓝 `#0F172A` / 信任蓝 `#1E3A8A`；背景 `#F8FAFC`；卡片纯白；
  - 图标使用 SVG，禁止用 emoji 充当图标。
- 移动端基线：宽度按 **375px** 设计，触控目标 ≥ 44×44px，
  页面无横向滚动，viewport 禁止禁止缩放（`user-scalable=no` 仅限展示页，需保留无障碍可读性）。

### 2.4 运行形态

- 交付物为**纯静态 H5**（`index.html`），Vue 3 通过全局构建（`vendor/vue.global.prod.js`）加载，
  不使用 npm 构建、不引入后端服务。
- 所有第三方库存放于 `vendor/`，页面**运行时不依赖外网 CDN**，可离线打开。
- 数据文件 `data/byd_data.json` 以相对路径 fetch；用本地静态服务器（或 Playwright 路由）打开。

## 3. 目录结构

```
byd-stock-analysis/
├── AGENTS.md                     # 本文件：Agent 约束
├── README.md                     # 项目说明与运行方式
├── index.html                    # 移动端 H5 单页（TDesign + ECharts）
├── vendor/                       # 本地第三方库（vue / tdesign / echarts）
├── data/
│   ├── 比亚迪后复权历史行情数据.xlsx  # 原始数据
│   └── byd_data.json             # 分析结果（脚本生成，页面消费）
├── analysis/
│   └── analyze.py                # pandas 描述性分析脚本
├── docs/
│   ├── design-system.md          # ui-ux-pro-max 设计系统
│   └── descriptive_stats.md      # 描述性统计报告（脚本生成）
├── screenshots/                  # H5 移动端截图
└── conversation/
    └── agent-conversation.md     # 与 Agent 的完整交互记录（脱敏）
```

## 4. 常用命令

```bash
# 1) 运行描述性分析（生成 JSON 与统计报告）
python3 analysis/analyze.py

# 2) 本地打开 H5（任选其一）
python3 -m http.server 8000        # 浏览器访问 http://localhost:8000

# 3) 移动端截图（Playwright，375×812）
python3 screenshots/capture.py
```

## 5. Agent 行为边界

- 只允许在本仓库目录内读写；不得改动原始 xlsx 数据。
- 价格单位、后复权口径、红涨绿跌配色为硬约束，需要偏离时必须先征得用户同意。
- 所有结论需标注数据来源与口径（2023 年、后复权、242 个交易日）。
- 本项目仅为课程教学的数据分析练习，**不构成任何投资建议**。
