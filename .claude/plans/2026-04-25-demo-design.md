# 设计文档：AKShare 东财美股数据 Demo

**日期：** 2026-04-25
**状态：** Approved

## 1. 背景与目标

实现一个 akshare 东财美股数据获取 demo 脚本，演示通过 `stock_us_spot_em` 获取所有美股代码，再通过 `stock_us_hist` 获取每只股票 2026 年的天级别数据。

底层数据获取基础设施（Provider 层的 `AkshareFetcher` 和 Processor 层的 `AkshareSource`）已就绪，demo 脚本负责编排和存储。

## 2. 文件结构

- **脚本**: `./script/demo_akshare_us.py` — 单文件，端到端
- **数据存储**:
  - `./data/demo_list/us_stocks.json` — 美股代码列表
  - `./data/demo_stock/{TICKER}/{TICKER}_2026.json` — 每只股票 2026 年日线数据
  - `./data/demo_stock/fetch_summary.json` — 抓取摘要（成功/失败计数）
- **设计/计划文档**: `./.claude/plans/`

## 3. 数据流

```
main()
  ├─ Step 1: ak.stock_us_spot_em()
  │    └─ 提取代码、名称 → 写入 ./data/demo_list/us_stocks.json
  │
  └─ Step 2: for each ticker in us_stocks.json
       ├─ AkshareSource().fetch_daily(ticker, "20260101", "20261231")
       ├─ 失败时重试 3 次（指数退避：2s, 4s, 8s），耗尽则跳过
       └─ 成功 → 写入 ./data/demo_stock/{TICKER}/{TICKER}_2026.json
```

## 4. 关键决策

| 决策 | 选择 |
|------|------|
| 脚本结构 | 单文件 script，3 个函数 + main() |
| 代码复用 | 复用 `AkshareSource.fetch_daily()` |
| 文件格式 | JSON |
| 错误处理 | 重试 3 次后跳过，记录摘要 |
| 进度跟踪 | 日志 + fetch_summary.json |
| 测试 | 手动 smoke test + --dry-run 参数 |

## 5. 输出格式

### us_stocks.json
```json
[
  {"ticker": "AAPL", "name": "苹果", "em_code": "105.AAPL"}
]
```

### {TICKER}_2026.json
```json
[
  {"date": "2026-01-02", "open": 195.5, "high": 198.2, "low": 194.1, "close": 197.8, "volume": 50000000, "amount": 9800000000, "pct_chg": 1.2, "amplitude": 2.1, "change": 2.3, "turnover_rate": 0.8}
]
```

## 6. 错误处理

- `akshare` 未安装 → 早期退出，exit code 1
- `stock_us_spot_em` 失败 → 致命，退出
- 单只股票失败 → 重试 3 次，跳过，记录到 fetch_summary.json
- 速率限制 → 继承 AkshareSource 内部的反爬逻辑
- KeyboardInterrupt → 捕获，打印已完成摘要后退出

## 7. 测试计划

- `--dry-run` 参数：仅执行 Step 1（获取列表），不抓取数据
- 手动 smoke test：运行脚本，检查输出文件结构和内容
- 无需独立单元测试（核心逻辑已在 processor 层覆盖）
