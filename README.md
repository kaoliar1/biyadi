# 比亚迪股票价格走势分析与可视化

《金融大数据分析与应用》第 4 章 · 教材 P92 实战演练

## 项目简介

以 **比亚迪（002594，深圳证券交易所）2023 年（242 个交易日）后复权日线数据**为对象，
完成描述性统计分析与移动端可视化，并交付一个可离线打开的静态 H5 页面。

## 技术栈

| 环节 | 选型 | 说明 |
|---|---|---|
| 数据分析 | Python 3 + pandas / numpy | 描述统计、均线、波动率、最大回撤、月度收益 |
| 数据可视化 | **Apache ECharts 5**（Canvas） | K线+均线+成交量联动、涨跌幅分布、月度收益 |
| UI 控件 | **TDesign Mobile Vue**（tdesign-mobile-vue 1.16） | 组件规范来自 **TDesign MCP** |
| 视觉设计 | **ui-ux-pro-max** 技能生成的设计系统 | 瑞士极简 / 金融浅色风 / IBM Plex Sans |
| 前端框架 | Vue 3（全局构建，无打包步骤） | 纯静态 H5，可离线运行 |
| 网页测试/截图 | Playwright | 375×812 移动视口 |

## 快速开始

```bash
# 1. 运行分析（生成 data/byd_data.json 与 docs/descriptive_stats.md）
python3 analysis/analyze.py

# 2. 启动静态服务器，浏览器访问
python3 -m http.server 8000
#    http://localhost:8000/index.html

# 3. 移动端截图（可选；需先安装 playwright chromium）
PLAYWRIGHT_BROWSERS_PATH=<浏览器路径> python3 screenshots/capture.py
```

## 页面结构（移动端 H5）

- 顶部：TDesign `Navbar` + 年末收盘价价格卡（8 项关键指标）
- `NoticeBar`：数据口径与免责声明
- 四个 Tab（TDesign `Tabs`）：
  1. **行情走势**：K 线图叠加 MA5/10/20/60 + 成交量柱 + 区间缩放
  2. **描述统计**：价格、交易波动描述统计表 + 关键指标（TDesign `Cell`）
  3. **收益分布**：日涨跌幅分布直方图 + 月度收益率柱形图
  4. **分析过程**：五步分析流程 + 分析结论

## 目录结构

```
byd-stock-analysis/
├── AGENTS.md                 # Agent 工作约束（背景/技术选型）
├── README.md
├── index.html                # 移动端 H5
├── vendor/                   # vue / tdesign / echarts / 图标（本地，可离线）
├── data/
│   ├── 比亚迪后复权历史行情数据.xlsx
│   └── byd_data.json
├── analysis/analyze.py
├── docs/
│   ├── design-system.md      # ui-ux-pro-max 设计系统
│   └── descriptive_stats.md
├── screenshots/              # H5 移动端截图
│   ├── capture.py
│   └── *.png
└── conversation/
    └── agent-conversation.md # 与 Agent 的完整交互记录（脱敏）
```

## 主要结论

- 全年后复权收盘价由 **257.66 跌至 200.40**，年度涨跌幅 **-22.22%**；
- 年化波动率 **26.96%**，最大回撤 **-38.71%**（2023-12-20）；
- 140 个交易日下跌、102 日上涨；1 月最强（+11.41%），11 月最弱（-16.16%）；
- 收盘价与成交量相关系数仅 0.078，量价基本无线性相关。

> 本项目仅供课程教学使用，**不构成任何投资建议**。
