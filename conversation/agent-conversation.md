# 与 AI Agent 交互全过程记录（脱敏）

> 作业：教材《金融大数据分析与应用》第 4 章 P92 实战演练 —— 比亚迪股票价格走势分析与可视化
>
> **AI Agent 软件名称**：豆包（Doubao，Web 端办公模式 / 智能体开发助手）
> **使用的大模型**：豆包大模型（Doubao LLM）
> **交互时间**：2026-10-13
>
> 脱敏说明：以下记录中个人姓名、邮箱、账号、机器路径等敏感信息均已做打码或替换（如 `陈同学`、`27***@qq.com`、`/home/**`）；无密码、令牌等凭证出现。

---

## 一、任务下达

### 👤 用户

完成教材 P92 页实战演练：比亚迪股票价格走势分析与可视化。

考核点：
1. 在 AGENTS.md 做好背景信息、技术选型的约束（比如数据可视化的技术）；
2. 使用 ui-ux-pro-skill 做设计，将过程和结果通过移动端展示（提供 H5 静态页面）；
3. 使用 TDesign MCP 做 UI 控件。

交付要求：
- 将代码和运行结果通过 git 提交到个人仓库中，提交 git 链接；
- 提供 HTML 截图；
- 提交跟 Agent 交互的全部对话，输出 markdown 文档（提交记录脱敏），同时提供 AI Agent 软件名称和使用的大模型名称。

附件：`第4章 金融数据描述性分析与可视化.pptx`、`Codex4.docx`、`比亚迪后复权历史行情数据.xlsx`。

### 🤖 Agent

我先查看三个附件，了解实战演练的具体要求和数据结构。

---

## 二、需求与数据探查

### 🤖 Agent（操作：解析 Codex4.docx）

读取 `Codex4.docx`，确认作业要点：
- 需在 `AGENTS.md` 中做好背景与技术选型约束；
- 参考资料：`ui-ux-pro-max-skill`（设计）、TDesign MCP（UI 控件）、Playwright（网页测试）；
- 外部资源链接（已脱敏，仅保留域名）：
  - Agents.md 指南：`codexguide.ai/advanced/02-agents-md.html`
  - 技能与 MCP：`codexguide.ai/advanced/03-skills-plugins-mcp.html`、`modelcontextprotocol.io`
  - TDesign MCP：`tdesign.tencent.com/vue-next/mcp`
  - 设计技能：`uupm.cc`

### 🤖 Agent（操作：解析第 4 章 PPT）

PPT 共 29 页，确认本章知识脉络：
- 4.1 统计量和描述性分析（频数、集中趋势/离散程度/分布形态统计量）；
- 4.2 双变量描述性分析（列联表、相关系数、散点图、热力图、分组箱线图）；
- 4.3 金融技术分析工具（K 线图、简单/加权/指数移动平均线、mplfinance 绘图）。

### 🤖 Agent（操作：读取行情 Excel）

`比亚迪后复权历史行情数据.xlsx` 数据结构：
- **242 行 × 11 列**，时间范围 **2023-01-03 至 2023-12-29**；
- 字段：`日期、开盘、收盘、最高、最低、成交量、成交额、振幅、涨跌幅、涨跌额、换手率`；
- 价格为**后复权**口径；示例：

| 日期 | 开盘 | 收盘 | 最高 | 最低 | 成交量 |
|---|---|---|---|---|---|
| 2023-01-03 | 257.66 | 261.73 | 263.17 | 251.25 | 121374 |
| … | … | … | … | … | … |
| 2023-12-29 | 201.37 | 200.40 | 202.20 | 199.55 | 80367 |

---

## 三、环境与工具确认

### 🤖 Agent（操作：检查本机环境）

- 技能目录检查：`ui-ux-pro-max` 未在本地预装，`guizang-ppt-skill` 已在用户技能目录；
- 工具链：`git`、`node v22`、`npm`、`gh`、`python3` 均可用；
- Playwright Python 已安装，但浏览器内核未安装；
- `gh` 未登录任何 GitHub 账号（后续由用户自行推送）。

### 🤖 Agent（操作：获取 ui-ux-pro-max 设计技能）

- 访问技能官网 `uupm.cc`，了解其设计方法论（样式库、产品色板、字体配对、图表类型、UX 规则、交付清单）；
- 从官方开源仓库克隆技能：`github.com/nextlevelbuilder/ui-ux-pro-max-skill`；
- 阅读其 `SKILL.md`，按规范执行设计系统生成流程。

### 🤖 Agent（操作：生成设计系统）

执行命令（设计密度 7，数据看板场景）：

```bash
python3 <skill>/scripts/search.py \
  "stock finance mobile dashboard data visualization candlestick" \
  --design-system --density 7 -p "BYD Stock Analysis" -f markdown
```

生成结果要点：
- **模式**：Trust & Authority（信任与权威）；
- **风格**：Minimalism & Swiss Style（瑞士极简，浅色）；
- **主色**：海军蓝 `#0F172A`、信任蓝 `#1E3A8A`、背景 `#F8FAFC`；
- **字体**：IBM Plex Sans；
- **图表建议**：OHLC 用 Candlestick，趋势用 Line，时间序列交互支持 tooltip + 缩放；
- 交付清单：SVG 图标、对比度 ≥ 4.5:1、375px 适配、无横向滚动等。

补充检索图表域（`--domain chart`）：K 线建议含成交量副图（40% 透明度）、键盘/触控缩放、不依赖颜色传达涨跌。

> 针对 A 股场景的适配：技能默认图表建议为欧美市场“绿涨红跌”，本项目按 AGENTS.md 约束**反转为红涨绿跌**：涨 `#D54941`、跌 `#2BA471`。

---

## 四、AGENTS.md 约束编写

### 🤖 Agent（操作：创建 AGENTS.md）

在仓库根目录创建 `AGENTS.md`，约束内容包括：
- 项目背景（课程、标的、数据口径、242 个交易日、分析目标）；
- 数据分析约束：pandas/numpy，结果统一输出 `data/byd_data.json`；
- **可视化约束**：统一 Apache ECharts 5（Canvas），必备 K 线 + MA5/10/20/60 + 成交量 + 分布图 + 月度图，红涨绿跌、tooltip/图例/缩放齐备；
- UI 约束：TDesign Mobile Vue 控件（规范来自 TDesign MCP），遵循 ui-ux-pro-max 设计系统；
- 运行形态：纯静态 H5、无构建步骤、vendor 本地库、可离线打开；
- 目录结构、常用命令与 Agent 行为边界；
- 教学免责声明。

### 🤖 Agent（操作：保存设计系统文档）

将设计系统结果与 A 股适配写入 `docs/design-system.md`，含色彩 Token、字体、图表选型、UX 规则、反模式、交付前检查清单。

---

## 五、Python 描述性分析

### 🤖 Agent（操作：编写 analysis/analyze.py）

脚本按 9 个步骤实现：
1. 数据读取与预处理（日期转 datetime、排序、英文列名）；
2. 计算简单移动平均线 MA5/MA10/MA20/MA60；
3. 描述统计量（均值、标准差、分位数、偏度、峰度）；
4. 日涨跌幅分布（8 个区间）；
5. 走势指标（年化波动率、最大回撤、涨跌天数）；
6. 月度分析（月度收益、高低点、均量）；
7. 成交量/成交额分析（峰值日、日均额、量价相关系数）；
8. 组装 H5 数据（全量 K 线 + 均线，输出 `data/byd_data.json`）；
9. 输出 Markdown 报告 `docs/descriptive_stats.md`。

### 🤖 Agent（运行结果）

```bash
$ python3 analysis/analyze.py
分析完成：
 JSON -> data/byd_data.json
 报告 -> docs/descriptive_stats.md
 年度涨跌幅 -22.22%，年化波动率 26.96%，最大回撤 -38.71%
```

关键描述统计（摘自报告）：

| 指标 | 均值 | 标准差 | 最小 | 中位 | 最大 |
|---|---|---|---|---|---|
| 收盘价 | 250.68 | 22.58 | 187.28 | 252.22 | 305.58 |
| 成交量(手) | 113649.47 | 49020.71 | 41380 | 100847 | 307863 |
| 涨跌幅(%) | -0.09 | 1.70 | -5.18 | -0.18 | 6.46 |
| 换手率(%) | 0.98 | 0.42 | 0.36 | 0.86 | 2.64 |

走势指标：上涨 102 天 / 下跌 140 天；最大单日涨/跌幅 +6.46% / -5.18%；
日均成交额 28.38 亿元；成交量峰值 2023-10-18（成交额 76.46 亿元）；
收盘价-成交量相关系数 0.078；最强月 1 月（+11.41%），最弱月 11 月（-16.16%）。

---

## 六、移动端 H5 开发

### 🤖 Agent（操作：下载本地依赖到 vendor/）

从 jsdelivr / 腾讯 CDN 下载：
- `vue.global.prod.js`（Vue 3）
- `tdesign.min.js` + `tdesign.min.css` + `reset.css`（tdesign-mobile-vue 1.16.2，UMD 全局名 `TDesign`）
- `echarts.min.js`（ECharts 5）
- 图标 sprite：`t-icons.js`（`tdesign.gtimg.com/icon/0.4.5/fonts/index.js`，供 `t-icon` 的 `<use href="#t-icon-xxx">` 引用）

### 🤖 Agent（操作：编写 index.html）

页面结构：
- TDesign `Navbar`：标题“比亚迪股票走势分析”；
- 深色价格卡：年末收盘价 200.40、年度涨跌标签、8 宫格关键指标；
- TDesign `NoticeBar`：数据口径与免责声明；
- TDesign `Tabs`，四个 Tab：
  1. **行情走势**：ECharts K 线（红涨绿跌）+ MA5/10/20/60 + 成交量副图 + inside/slider 双缩放 + cross tooltip；
  2. **描述统计**：价格/交易统计表（可横向滚动）+ TDesign `CellGroup/Cell` 关键指标；
  3. **收益分布**：日涨跌幅分布柱图 + 月度收益率柱图（正负异色、数值标签）；
  4. **分析过程**：五步流程时间线（TDesign Icon）+ 分析结论清单。

### 🤖 Agent（调试过程：问题 1 —— 图标不显示）

- 现象：`t-icon` 渲染为空 `<use href="#t-icon-...">`，但图标 sprite 未加载；
- 定位：阅读 UMD 中 `Icon` 组件源码，确认其默认按需从 `tdesign.gtimg.com/icon/0.4.5/fonts/index.js` 加载 sprite；
- 修复：下载该 sprite 为 `vendor/t-icons.js` 并在本地页面引用；同时替换该版本不存在的图标名（`candlestick→chart-analytics`、`devices→mobile`）。

### 🤖 Agent（调试过程：问题 2 —— Tabs 不渲染）

- 现象：TDesign `NoticeBar` 与 `Tabs` 直接相邻时，`Tabs` 整块不渲染（页面 DOM 中无 `t-tabs`），无报错；
- 排查：构造 9 组最小复现页逐一对照，确认“**组件直接相邻（NoticeBar 后紧跟 Tabs）时，后者被丢弃**”，普通元素相邻或调换顺序均正常；
- 修复：将 NoticeBar 与 Tabs 分别包裹在独立 `<div>` 中隔离插槽树；同样地，结论行内 `Icon` 与文本也分别包裹，避免文本节点被丢弃。

### 🤖 Agent（微调）

- 月度收益柱图：正值标签在柱顶、负值标签在柱底；
- 缩放滑块补充 `dataBackground` 预览线条与填充色；
- 结论文本补全后复跑截图验证。

---

## 七、Playwright 移动端截图

### 🤖 Agent（操作：安装浏览器内核）

默认浏览器路径无写权限，改为可写路径安装：

```bash
export PLAYWRIGHT_BROWSERS_PATH=/home/**/pw-browsers
python3 -m playwright install chromium
```

### 🤖 Agent（操作：编写 screenshots/capture.py）

- 脚本自动启动本地静态服务器；
- 移动视口 375×812、2 倍像素、`isMobile + hasTouch`、iPhone UA；
- 先截首屏，再依次切换四个 Tab 截取整页：
  `00-first-screen.png`、`01-kline.png`、`02-stats.png`、`03-dist.png`、`04-process.png`。

运行结果：

```bash
$ python3 screenshots/capture.py
saved 01-kline.png
saved 02-stats.png
saved 03-dist.png
saved 04-process.png
全部截图完成 -> screenshots/
```

截图经人工逐张核对：K 线、均线、成交量、配色、统计表、分布图、分析过程与结论均正常显示。

---

## 八、Git 提交

### 🤖 Agent（操作：本地仓库初始化与提交）

配置本地仓库身份并创建 4 个逻辑提交：

```bash
git init -b main
git config user.name "陈同学"
git config user.email "***@users.noreply.github.com"

git add AGENTS.md .gitignore README.md data/
git commit -m "chore: 初始化项目，添加 AGENTS.md 约束与原始行情数据"

git add analysis/ docs/
git commit -m "feat: 基于 pandas 完成比亚迪行情描述性分析与统计报告"

git add vendor/ index.html
git commit -m "feat: 开发 TDesign 移动端 H5（K线+均线+成交量，ECharts 可视化）"

git add screenshots/*.png screenshots/capture.py
git commit -m "test: 添加 Playwright 移动端截图脚本与运行结果"
```

`git log --oneline`：

```
0e2ad4c test: 添加 Playwright 移动端截图脚本与运行结果
b2929e9 feat: 开发 TDesign 移动端 H5（K线+均线+成交量，ECharts 可视化）
bfddebe feat: 基于 pandas 完成比亚迪行情描述性分析与统计报告
953b301 chore: 初始化项目，添加 AGENTS.md 约束与原始行情数据
```

### 👤 用户

选择**自己推送**，计划使用的仓库名 `fintech-byd-analysis`。

### 🤖 Agent（给出推送命令）

```bash
# 1) 在 GitHub/Gitee 新建空仓库 fintech-byd-analysis（不要勾选 README）
# 2) 进入本地项目目录
cd byd-stock-analysis
git remote add origin https://github.com/<你的用户名>/fintech-byd-analysis.git
git push -u origin main
# 提交后把仓库链接（git 链接）填入作业即可
```

最后一个提交包含本对话记录：

```bash
git add conversation/agent-conversation.md
git commit -m "docs: 添加与 Agent 的完整交互记录（脱敏）"
git push
```

---

## 九、分析结论（汇总）

1. **全年走势**：2023 年比亚迪后复权收盘价由 257.66 跌至 200.40，年度涨跌幅 **-22.22%**；最大回撤 **-38.71%**（2023-12-20）。
2. **波动特征**：年化波动率 26.96%；140 个交易日下跌、102 日上涨；单日最大涨/跌幅 +6.46% / -5.18%。
3. **量价关系**：收盘价与成交量相关系数仅 0.078，基本无线性相关；成交量峰值出现在 2023-10-18（成交额 76.46 亿元）。
4. **月度特征**：1 月最强（+11.41%），11 月最弱（-16.16%）；全年仅 5 个月收阳。
5. **分布形态**：收盘价偏度 -0.921，分布左偏，高价位交易日更多分布在上半年。

---

## 附：环境与工具清单

| 类别 | 名称 / 版本 |
|---|---|
| AI Agent 软件 | 豆包（Doubao），Web 端办公模式 |
| 大模型 | 豆包大模型（Doubao LLM） |
| 数据分析 | Python 3.12、pandas、numpy |
| 可视化 | Apache ECharts 5 |
| UI 组件 | TDesign Mobile Vue 1.16.2（规范来自 TDesign MCP） |
| 设计技能 | ui-ux-pro-max（nextlevelbuilder/ui-ux-pro-max-skill） |
| 前端框架 | Vue 3 |
| 测试/截图 | Playwright（Chromium，375×812 移动视口） |
| 版本控制 | git（main 分支，用户自行推送） |

> 本项目为课程教学练习，所有分析结果**不构成任何投资建议**。
