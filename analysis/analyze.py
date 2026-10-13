# -*- coding: utf-8 -*-
"""
比亚迪（002594）股票价格走势分析与可视化 —— 描述性分析脚本
教材：《金融大数据分析与应用》第4章 实战演练（P92）

输入：data/比亚迪后复权历史行情数据.xlsx（2023 年日线，后复权）
输出：
  data/byd_data.json   —— 供 H5 页面（ECharts）使用的全部分析结果
  docs/descriptive_stats.md —— 描述性统计文字报告
"""
import json
import os

import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE_DIR, "data", "比亚迪后复权历史行情数据.xlsx")
OUT_JSON = os.path.join(BASE_DIR, "data", "byd_data.json")
OUT_MD = os.path.join(BASE_DIR, "docs", "descriptive_stats.md")

# ---------------------------------------------------------------
# 步骤 1：数据读取与预处理
# ---------------------------------------------------------------
df = pd.read_excel(SRC)
df["日期"] = pd.to_datetime(df["日期"])
df = df.sort_values("日期").reset_index(drop=True)

# 后复权数据：价格列为后复权价；成交量单位“手”，成交额单位“元”
df.rename(columns={
    "日期": "date", "开盘": "open", "收盘": "close", "最高": "high",
    "最低": "low", "成交量": "volume", "成交额": "amount", "振幅": "amplitude",
    "涨跌幅": "pct_chg", "涨跌额": "chg", "换手率": "turnover",
}, inplace=True)

# ---------------------------------------------------------------
# 步骤 2：移动平均线（简单移动平均线 SMA，见教材 4.3.2）
# ---------------------------------------------------------------
for n in (5, 10, 20, 60):
    df[f"ma{n}"] = df["close"].rolling(window=n).mean()

# ---------------------------------------------------------------
# 步骤 3：描述性统计量（集中趋势 / 离散程度 / 分布形态，见教材 4.1）
# ---------------------------------------------------------------
def desc(series):
    s = series.dropna()
    return {
        "count": int(s.count()),
        "mean": round(float(s.mean()), 2),
        "std": round(float(s.std()), 2),
        "min": round(float(s.min()), 2),
        "q25": round(float(s.quantile(0.25)), 2),
        "median": round(float(s.median()), 2),
        "q75": round(float(s.quantile(0.75)), 2),
        "max": round(float(s.max()), 2),
        "skew": round(float(s.skew()), 3),
        "kurt": round(float(s.kurt()), 3),
    }

stats = {col: desc(df[col]) for col in
         ["open", "close", "high", "low", "volume", "amount",
          "amplitude", "pct_chg", "turnover"]}

# ---------------------------------------------------------------
# 步骤 4：涨跌幅（日收益率）分布分析
# ---------------------------------------------------------------
ret = df["pct_chg"]
bins = [-np.inf, -5, -3, -1, 0, 1, 3, 5, np.inf]
labels = ["<-5%", "-5~-3%", "-3~-1%", "-1~0%", "0~1%", "1~3%", "3~5%", ">5%"]
cat = pd.cut(ret, bins=bins, labels=labels)
ret_dist = [{"label": str(k), "value": int(v)} for k, v in cat.value_counts(sort=False).items()]

# ---------------------------------------------------------------
# 步骤 5：区间走势指标（波动率、最大回撤、涨跌家数）
# ---------------------------------------------------------------
ann_vol = round(float(ret.std() * np.sqrt(252)), 2)          # 年化波动率(%)
up_days = int((ret > 0).sum())
down_days = int((ret < 0).sum())
flat_days = int((ret == 0).sum())
max_up = round(float(ret.max()), 2)
max_down = round(float(ret.min()), 2)

# 最大回撤
cummax = df["close"].cummax()
drawdown = (df["close"] - cummax) / cummax
max_dd = round(float(drawdown.min() * 100), 2)
max_dd_date = df.loc[drawdown.idxmin(), "date"].strftime("%Y-%m-%d")

# 年内涨跌幅
year_open = float(df.iloc[0]["open"])
year_close = float(df.iloc[-1]["close"])
year_ret = round((year_close - year_open) / year_open * 100, 2)

# ---------------------------------------------------------------
# 步骤 6：月度分析（月度收益、月内最高/最低、月均成交量）
# ---------------------------------------------------------------
df["month"] = df["date"].dt.to_period("M")
monthly = []
for m, g in df.groupby("month"):
    m_ret = round((g.iloc[-1]["close"] / g.iloc[0]["open"] - 1) * 100, 2)
    monthly.append({
        "month": str(m),
        "ret": m_ret,
        "high": round(float(g["high"].max()), 2),
        "low": round(float(g["low"].min()), 2),
        "avg_vol": round(float(g["volume"].mean()), 0),
        "close": round(float(g.iloc[-1]["close"]), 2),
    })

# ---------------------------------------------------------------
# 步骤 7：成交量 / 成交额分析
# ---------------------------------------------------------------
vol_peak_idx = df["volume"].idxmax()
vol_peak = {
    "date": df.loc[vol_peak_idx, "date"].strftime("%Y-%m-%d"),
    "volume": int(df.loc[vol_peak_idx, "volume"]),
    "amount": round(float(df.loc[vol_peak_idx, "amount"]) / 1e8, 2),  # 亿元
}
avg_amount = round(float(df["amount"].mean()) / 1e8, 2)  # 亿元
avg_turnover = round(float(df["turnover"].mean()), 2)

# 价格与成交量相关性（教材 4.2.2 双定量变量相关性）
corr = round(float(df[["close", "volume", "amount", "turnover", "pct_chg"]].corr().loc["close", "volume"]), 3)

# ---------------------------------------------------------------
# 步骤 8：组装 H5 数据（K线 + 均线 + 成交量，全量 242 个交易日）
# ---------------------------------------------------------------
def r2(x):
    return None if pd.isna(x) else round(float(x), 2)

kline = []
for _, row in df.iterrows():
    kline.append([
        row["date"].strftime("%Y-%m-%d"),
        r2(row["open"]), r2(row["close"]), r2(row["low"]), r2(row["high"]),
        int(row["volume"]),
    ])

ma_lines = {}
for n in (5, 10, 20, 60):
    ma_lines[f"ma{n}"] = [
        [row["date"].strftime("%Y-%m-%d"), r2(row[f"ma{n}"])]
        for _, row in df.iterrows()
    ]

result = {
    "meta": {
        "name": "比亚迪",
        "code": "002594",
        "market": "深圳证券交易所",
        "adjust": "后复权",
        "start": df.iloc[0]["date"].strftime("%Y-%m-%d"),
        "end": df.iloc[-1]["date"].strftime("%Y-%m-%d"),
        "trading_days": int(len(df)),
    },
    "overview": {
        "year_open": round(year_open, 2),
        "year_close": round(year_close, 2),
        "year_high": round(float(df["high"].max()), 2),
        "year_low": round(float(df["low"].min()), 2),
        "year_ret": year_ret,
        "ann_vol": ann_vol,
        "max_dd": max_dd,
        "max_dd_date": max_dd_date,
        "up_days": up_days,
        "down_days": down_days,
        "flat_days": flat_days,
        "max_up": max_up,
        "max_down": max_down,
        "avg_amount": avg_amount,
        "avg_turnover": avg_turnover,
        "vol_peak": vol_peak,
        "corr_close_volume": corr,
    },
    "stats": stats,
    "ret_dist": ret_dist,
    "monthly": monthly,
    "kline": kline,
    "ma": ma_lines,
}

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, separators=(",", ":"))

# ---------------------------------------------------------------
# 步骤 9：输出 Markdown 描述性统计报告
# ---------------------------------------------------------------
def md_table(cols):
    lines = ["| 指标 | 均值 | 标准差 | 最小值 | 25% | 中位数 | 75% | 最大值 | 偏度 | 峰度 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    names = {"open": "开盘价", "close": "收盘价", "high": "最高价", "low": "最低价",
             "volume": "成交量(手)", "amount": "成交额(元)", "amplitude": "振幅(%)",
             "pct_chg": "涨跌幅(%)", "turnover": "换手率(%)"}
    for c in cols:
        s = stats[c]
        lines.append("| %s | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.3f | %.3f |"
                     % (names[c], s["mean"], s["std"], s["min"], s["q25"],
                        s["median"], s["q75"], s["max"], s["skew"], s["kurt"]))
    return "\n".join(lines)

md = f"""# 比亚迪（002594）2023 年行情描述性统计报告

> 数据口径：{result['meta']['start']} 至 {result['meta']['end']}，共 {result['meta']['trading_days']} 个交易日，**后复权**日线数据。

## 一、价格描述性统计

{md_table(['open', 'close', 'high', 'low'])}

## 二、交易与波动描述性统计

{md_table(['volume', 'amplitude', 'pct_chg', 'turnover'])}

## 三、关键走势指标

| 指标 | 数值 | 指标 | 数值 |
|---|---|---|---|
| 年初开盘价（后复权） | {year_open:.2f} | 年末收盘价（后复权） | {year_close:.2f} |
| 年内最高价 | {result['overview']['year_high']:.2f} | 年内最低价 | {result['overview']['year_low']:.2f} |
| 年度涨跌幅 | {year_ret}% | 年化波动率 | {ann_vol}% |
| 最大回撤 | {max_dd}%（{max_dd_date}） | 上涨/下跌/平盘天数 | {up_days} / {down_days} / {flat_days} |
| 单日最大涨幅 | {max_up}% | 单日最大跌幅 | {max_down}% |
| 日均成交额 | {avg_amount} 亿元 | 日均换手率 | {avg_turnover}% |
| 成交量峰值日 | {vol_peak['date']}（{vol_peak['volume']} 手，{vol_peak['amount']} 亿元） | 收盘价-成交量相关系数 | {corr} |

## 四、日涨跌幅分布

| 区间 | {' | '.join(d['label'] for d in ret_dist)} |
|---|---|
| 天数 | {' | '.join(str(d['value']) for d in ret_dist)} |

## 五、月度收益率（%）

| 月份 | {' | '.join(m['month'][-2:] + '月' for m in monthly)} |
|---|---|
| 月涨跌幅 | {' | '.join(str(m['ret']) for m in monthly)} |
"""
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(md)

print("分析完成：")
print(" JSON ->", OUT_JSON)
print(" 报告 ->", OUT_MD)
print(f" 年度涨跌幅 {year_ret}%，年化波动率 {ann_vol}%，最大回撤 {max_dd}%")
