# 设计系统 —— 比亚迪股票走势分析移动端 H5

> 由 **ui-ux-pro-max** 技能（`nextlevelbuilder/ui-ux-pro-max-skill`）生成，
> 命令：`search.py "stock finance mobile dashboard data visualization candlestick" --design-system --density 7`
> 结合 A 股使用场景做了语义色适配。

## 1. 产品分析（Step 1）

| 维度 | 判定 |
|---|---|
| 产品类型 | 金融数据看板 / 工具型（移动端 H5） |
| 行业 | Fintech / 证券行情 |
| 目标用户 | 金融大数据课程师生；移动端查看行情分析结果 |
| 场景 | 单手竖屏浏览、触控缩放 K 线 |
| 技术栈 | Vue 3（全局构建）+ TDesign Mobile Vue + ECharts 5 |

## 2. 模式与风格

- **Pattern**：Trust & Authority（信任与权威）—— 数据口径透明、结论可追溯。
- **Style**：**Minimalism & Swiss Style（瑞士极简）**
  - 关键词：干净、克制、留白、高对比、栅格、几何无衬线
  - 适配：仪表盘、数据工具、专业金融产品
  - 浅色模式（Light），支持后续扩展深色模式。

## 3. 色彩 Token

| 角色 | 色值 | 用途 |
|---|---|---|
| Primary | `#0F172A` | 标题、主文本 |
| Secondary | `#1E3A8A` | 信任蓝、品牌强调 |
| Accent | `#A16207` | 少量金色强调（标签、分隔） |
| Background | `#F8FAFC` | 页面底色 |
| Card | `#FFFFFF` | 卡片背景 |
| Muted Foreground | `#475569` | 次要文字 |
| Border | `#E2E8F0` | 描边、分割线 |
| **Up（A 股涨）** | `#D54941` | 阳线、上涨、正收益 |
| **Down（A 股跌）** | `#2BA471` | 阴线、下跌、负收益 |
| MA5 | `#FAAD14` | 5 日均线 |
| MA10 | `#722ED1` | 10 日均线 |
| MA20 | `#1E3A8A` | 20 日均线 |
| MA60 | `#5B6B7B` | 60 日均线 |

> 注：技能默认图表建议为欧美市场 Bullish 绿 / Bearish 红，因本产品面向 **A 股**，
> 按 AGENTS.md 强制约束反转为**红涨绿跌**。

## 4. 字体

- 字体族：**IBM Plex Sans**（金融、可信、专业）
- 回退栈：`-apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif`
- 字号：标题 20px / 区块标题 16px / 正文 14px / 辅助 12px；行高 1.5。

## 5. 图表选型（chart 域检索结果）

| 数据 | 图表 | 库 | 说明 |
|---|---|---|---|
| OHLC（242 根） | K 线 Candlestick | ECharts candlestick | 叠加 MA5/10/20/60；≤500 根可见 |
| 成交量 | 柱形图 | ECharts bar | 与主图 dataZoom 联动；40% 透明度 |
| 日涨跌幅分布 | 柱形直方图 | ECharts bar | 8 个区间，正负异色 |
| 月度收益 | 柱形图 | ECharts bar | 12 个月，正负异色 |
| 描述统计 | 表格 / 指标卡 | TDesign | t-table / t-cell / t-tag |

交互级别：tooltip + 触控缩放（dataZoom inside / slider）。

## 6. 关键效果与 UX 规则

- 转场 150–300ms；阴影锐利克制；层级靠留白与描边而非重投影。
- 触控目标 ≥ 44×44px；无横向滚动；卡片圆角 12px，卡片间距 12px。
- 图表加载时预留容器高度，避免 CLS；loading 使用 TDesign `t-loading`。
- 遵守 `prefers-reduced-motion`；键盘/读屏可获取数值（表格为颜色之外的兜底）。

## 7. 避免的反模式

- 卡通 / 娱乐化风格；AI 紫粉渐变；玻璃拟态堆叠；
- 用 emoji 充当图标；绿涨红跌（A 股场景）；仅靠颜色区分涨跌；
- 小于 12px 的正文文字、灰底灰字、无 tooltip 的图表。

## 8. 交付前检查清单（Pre-Delivery Checklist）

- [ ] 无 emoji 图标，全部使用 SVG / TDesign 内置图标
- [ ] 所有可点击元素有触控反馈（TDesign 自带点击态）
- [ ] 正文对比度 ≥ 4.5:1
- [ ] 375px 宽度下无横向滚动、无内容溢出
- [ ] K 线、成交量、分布图、月度图均有 tooltip 与图例
- [ ] 红涨绿跌配色全页一致
- [ ] 页面可离线打开（vendor 本地库）
