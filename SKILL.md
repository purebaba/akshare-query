---
name: akshare-query
description: 查询金融市场数据，包括A股行情、基金、宏观经济指标、期货、外汇、指数和财经新闻。当用户询问股票价格、基金净值、GDP/CPI等经济数据、汇率、期货价格或财经新闻时使用此技能。
allowed-tools: Bash(python:*)
---

# 金融数据查询技能 (akshare-query)

基于 akshare 的金融数据查询技能，提供 7 类工具覆盖 A股、基金、宏观经济、指数、外汇、期货和新闻数据。所有工具输出 Markdown 表格格式。

## 前置条件

需要安装依赖：
```bash
pip install -r {baseDir}/requirements.txt
```

## 工具列表

### 1. A股数据 (stock.py)

查询 A 股实时行情、历史 K 线和个股基本信息。

**实时行情** - 查询全部或单只 A 股实时行情：
```bash
python {baseDir}/scripts/stock.py quotes [--symbol 000001] [--limit 50]
```

**历史K线** - 查询个股历史 K 线，支持日/周/月线及复权：
```bash
python {baseDir}/scripts/stock.py hist --symbol 000001 [--period daily] [--start 20240101] [--end 20241231] [--adjust qfq]
```

**个股信息** - 查询个股基本信息（市值、行业、上市日期等）：
```bash
python {baseDir}/scripts/stock.py info --symbol 000001
```

参数说明：
- `--symbol`: 股票代码，如 000001、600519
- `--period`: K线周期 daily/weekly/monthly，默认 daily
- `--start`/`--end`: 日期范围，格式 YYYYMMDD
- `--adjust`: 复权方式 qfq(前复权)/hfq(后复权)/空(不复权)，默认 qfq
- `--limit`: 返回行数限制，默认 50

---

### 2. 基金数据 (fund.py)

查询 ETF 行情、基金排名和基金净值。

**ETF实时行情**：
```bash
python {baseDir}/scripts/fund.py etf [--limit 50]
```

**基金排名**：
```bash
python {baseDir}/scripts/fund.py rank [--type 全部] [--limit 50]
```

**基金净值**：
```bash
python {baseDir}/scripts/fund.py nav --code 110011 [--limit 50]
```

参数说明：
- `--type`: 基金类型，可选 全部/股票型/混合型/债券型/指数型/QDII，默认 全部
- `--code`: 基金代码，如 110011

---

### 3. 宏观经济数据 (macro.py)

查询中国宏观经济指标。

```bash
python {baseDir}/scripts/macro.py gdp [--limit 20]      # GDP数据
python {baseDir}/scripts/macro.py cpi [--limit 20]      # CPI消费价格指数
python {baseDir}/scripts/macro.py pmi [--limit 20]      # PMI制造业指数
python {baseDir}/scripts/macro.py lpr [--limit 20]      # LPR贷款市场报价利率
python {baseDir}/scripts/macro.py m2 [--limit 20]       # M2货币供应量
python {baseDir}/scripts/macro.py trade [--limit 20]    # 贸易差额数据
```

---

### 4. 指数数据 (index_query.py)

查询 A 股指数、全球指数和指数成分股。

**A股主要指数**：
```bash
python {baseDir}/scripts/index_query.py a-share [--limit 50]
```

**全球指数**：
```bash
python {baseDir}/scripts/index_query.py global [--limit 50]
```

**指数成分股**：
```bash
python {baseDir}/scripts/index_query.py constituents --symbol 000300 [--limit 50]
```

参数说明：
- `--symbol`: 指数代码，如 000300(沪深300)、000905(中证500)

---

### 5. 外汇数据 (forex.py)

查询实时外汇行情和中国银行外汇牌价。

**实时外汇行情**：
```bash
python {baseDir}/scripts/forex.py spot [--limit 50]
```

**中行外汇牌价**：
```bash
python {baseDir}/scripts/forex.py boc [--symbol 美元] [--limit 20]
```

参数说明：
- `--symbol`: 币种名称，如 美元、欧元、英镑、日元

---

### 6. 期货数据 (futures.py)

查询期货现货价格和库存数据。

**现货价格**：
```bash
python {baseDir}/scripts/futures.py spot [--date 20240101] [--limit 50]
```

**库存数据**：
```bash
python {baseDir}/scripts/futures.py inventory --symbol 铜 [--limit 50]
```

参数说明：
- `--date`: 日期 YYYYMMDD，默认今天
- `--symbol`: 品种名称，如 铜、铝、螺纹钢、黄金

---

### 7. 新闻数据 (news.py)

查询个股相关新闻资讯。

```bash
python {baseDir}/scripts/news.py --symbol 000001 [--limit 10]
```

参数说明：
- `--symbol`: 股票代码
- `--limit`: 返回条数，默认 10

## 注意事项

- 实时行情数据仅在交易时间内更新（A股交易时间：9:30-15:00）
- 所有工具需要网络连接，数据来源为东方财富等平台
- 宏观经济数据为历史时间序列，默认返回最近 20 条
- 输出为 Markdown 表格格式，错误信息输出到 stderr
