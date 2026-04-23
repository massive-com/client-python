================================================================================
Massive Python Client — 代码架构与逻辑文档
================================================================================

项目概述
--------
Massive（原 Polygon.io）官方 Python 客户端库，提供 REST 和 WebSocket 两种方式
访问股票、期权、外汇、加密货币、期货、指数等金融市场数据。发布为 PyPI 包 `massive`，
要求 Python 3.9+。


================================================================================
一、顶层目录结构
================================================================================

massive-com/
├── massive/                # 库源码
│   ├── __init__.py         # 公共 API 导出: RESTClient, WebSocketClient, exceptions
│   ├── modelclass.py       # @modelclass 装饰器（自定义 dataclass 封装）
│   ├── exceptions.py       # AuthError, BadResponse
│   ├── logging.py          # 统一日志工具 get_logger()
│   ├── rest/               # REST 客户端
│   │   ├── __init__.py     # RESTClient（多重继承组合所有 domain mixin）
│   │   ├── base.py         # BaseClient: HTTP 请求、分页、重试、参数转换
│   │   ├── aggs.py         # AggsClient — 聚合K线
│   │   ├── trades.py       # TradesClient — 逐笔成交
│   │   ├── quotes.py       # QuotesClient — 报价/NBBO
│   │   ├── snapshot.py     # SnapshotClient — 快照
│   │   ├── reference.py    # 参考数据: Markets/Tickers/Splits/Dividends/...
│   │   ├── indicators.py   # IndicatorsClient — 技术指标 SMA/EMA/RSI/MACD
│   │   ├── financials.py   # FinancialsClient — 财务报表
│   │   ├── benzinga.py     # BenzingaClient — 研报/评级
│   │   ├── economy.py      # EconomyClient — 宏观经济
│   │   ├── etf_global.py   # EtfGlobalClient — ETF 分析
│   │   ├── futures.py      # FuturesClient — 期货
│   │   ├── tmx.py          # TmxClient — 多伦多交易所
│   │   ├── summaries.py    # SummariesClient — 摘要
│   │   ├── vX.py           # VXClient — 旧版 vX 端点
│   │   └── models/         # REST 数据模型
│   │       ├── __init__.py # 统一导出所有模型
│   │       ├── common.py   # 公共枚举: Sort, Market, Timeframe 等
│   │       ├── request.py  # RequestOptionBuilder（Launchpad 边缘头构建器）
│   │       ├── aggs.py     # Agg, GroupedDailyAgg, DailyOpenCloseAgg, PreviousCloseAgg
│   │       ├── trades.py   # Trade, LastTrade, CryptoTrade
│   │       └── ...         # 各领域模型文件（与 rest/ 下 mixin 一一对应）
│   └── websocket/          # WebSocket 客户端
│       ├── __init__.py     # WebSocketClient: 异步连接、认证、订阅、重连
│       └── models/
│           ├── __init__.py # MARKET_EVENT_MAP 注册表 + parse() 解析器
│           ├── common.py   # Feed, Market, EventType 枚举
│           └── models.py   # 消息模型: EquityTrade, CryptoQuote, Level2Book 等
├── test_rest/              # REST 单元测试（pook HTTP mock）
│   ├── base.py             # BaseTest: 自动加载 mocks/ 下 JSON 文件注册 mock
│   ├── mocks/              # Mock 响应 JSON 文件（目录结构映射 URL 路径）
│   └── test_*.py           # 各领域测试
├── test_websocket/         # WebSocket 单元测试
│   ├── base_ws.py          # BaseTest: IsolatedAsyncioTestCase + mock server
│   ├── mock_server.py      # 内置 mock WebSocket 服务器
│   └── test_conn.py        # 连接/认证/订阅测试
├── examples/               # 使用示例
│   ├── rest/               # REST 示例脚本
│   └── websocket/          # WebSocket 示例脚本
├── .massive/               # OpenAPI 规范与代码生成
│   ├── rest.json           # REST OpenAPI 规范文件
│   ├── rest.py             # 从 api.massive.com/openapi 拉取规范的脚本
│   └── websocket.json      # WebSocket 规范文件
├── docs/                   # Sphinx 文档
├── pyproject.toml          # Poetry 项目配置
├── Makefile                # 开发命令入口
└── poetry.lock             # 依赖锁文件


================================================================================
二、核心架构：REST 客户端
================================================================================

2.1 多重继承 Mixin 组合模式
----------------------------

RESTClient 通过多重继承将 19 个领域 Mixin 组合为一个统一客户端：

    class RESTClient(
        AggsClient,          # 聚合K线 /v2/aggs
        FuturesClient,       # 期货 /v1/futures
        FinancialsClient,    # 财报 /vX/reference/financials
        BenzingaClient,      # 研报 /v1/meta/symbols
        EconomyClient,       # 宏观 /v1/economy
        EtfGlobalClient,     # ETF /v1/etf
        TmxClient,           # TMX /v1/tmx
        TradesClient,        # 成交 /v3/trades
        QuotesClient,        # 报价 /v3/quotes
        SnapshotClient,      # 快照 /v3/snapshot
        MarketsClient,       # 市场 /v3/reference/markets
        TickersClient,       # 标的 /v3/reference/tickers
        SplitsClient,        # 拆股 /v3/reference/splits
        DividendsClient,     # 分红 /v3/reference/dividends
        ConditionsClient,    # 条件码 /v3/reference/conditions
        ExchangesClient,     # 交易所 /v3/reference/exchanges
        ContractsClient,     # 合约 /v3/reference/options/contracts
        IndicatorsClient,    # 技术指标 /v1/indicators
        SummariesClient,     # 摘要 /v3/summaries
    )

    构造函数将所有参数传递给 BaseClient.__init__()，
    并额外实例化 self.vx = VXClient(...) 用于旧版端点。

优点:
  - 每个领域独立文件，职责单一
  - 新增 API 领域只需添加 Mixin + 模型，在 RESTClient 继承链中注册
  - 各 Mixin 可独立测试


2.2 BaseClient — HTTP 基础设施
-------------------------------

所在文件: massive/rest/base.py

BaseClient 是所有 REST Mixin 的共同基类，封装全部 HTTP 通信逻辑。

初始化流程:
  1. 验证 API key（缺失则抛出 AuthError）
  2. 构建默认请求头: Authorization: Bearer <key>, Accept-Encoding: gzip, User-Agent
  3. 创建 urllib3.PoolManager:
     - SSL 证书验证（certifi）
     - 重试策略: 默认 3 次，指数退避（因子 0.1），针对 [413,429,499,500,502,503,504]
     - 可配置连接池数量、超时时间
  4. 初始化可选的自定义 JSON 编解码器

核心方法:

  _get(path, params, result_key, deserializer, raw, options)
    │  执行 GET 请求到 BASE + path
    │  params 作为查询参数
    │  raw=True 时返回原始 HTTPResponse
    │  否则解析 JSON，提取 result_key 对应的字段
    └→ 用 deserializer 函数将每条数据转换为模型对象

  _get_params(fn, caller_locals, datetime_res="nanos")
    │  参数转换引擎: 将 Python 函数参数自动映射为 API 查询参数
    │  处理规则:
    │    - Enum → 取 .value
    │    - bool → 小写字符串 "true"/"false"
    │    - datetime → 按精度转换为 Unix 时间戳
    │    - 下划线后缀 → 点号（如 timestamp_lt → timestamp.lt）
    │    - any_of 后缀 → 逗号拼接列表
    └→ 返回可直接用于请求的 dict

  _paginate(path, params, raw, deserializer, result_key, options)
    │  分页入口
    │  raw=True → 返回单页原始响应
    └→ raw=False → 返回 _paginate_iter() 生成器

  _paginate_iter(path, params, deserializer, result_key, options)
    │  分页迭代生成器
    │  while 循环:
    │    1. 发送请求获取一页数据
    │    2. 对 result_key 下每条记录调用 deserializer → yield 模型对象
    │    3. 检查响应中的 next_url
    │    4. 有 next_url 且 pagination=True → 解析 URL 继续请求
    └→   无 next_url → 结束


2.3 领域 Mixin 方法模式
------------------------

所有 Mixin 方法遵循统一模式:

    def list_xxx(self, ticker, param1, ..., params=None, raw=False, options=None):
        url = f"/v3/some/endpoint/{ticker}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_xxx, locals()),
            raw=raw,
            deserializer=SomeModel.from_dict,
            result_key="results",
            options=options,
        )

    def get_xxx(self, ticker, ..., params=None, raw=False, options=None):
        url = f"/v2/some/endpoint/{ticker}"
        return self._get(
            path=url,
            params=self._get_params(self.get_xxx, locals()),
            result_key="results",
            deserializer=SomeModel.from_dict,
            raw=raw,
            options=options,
        )

方法命名约定:
  - list_xxx() → 分页接口，返回 Iterator[Model]
  - get_xxx()  → 单次请求，返回 Model 或 List[Model]

参数命名约定:
  - params: Optional[dict] — 额外查询参数
  - raw: bool — True 时跳过反序列化，返回原始 HTTP 响应
  - options: RequestOptionBuilder — 自定义请求头（Launchpad 边缘场景）


================================================================================
三、核心架构：WebSocket 客户端
================================================================================

所在文件: massive/websocket/__init__.py

3.1 连接与认证流程
-------------------

    客户端实例化
        ↓
    WebSocketClient(api_key, feed, market, subscriptions=["T.*"])
        ↓ 存储 scheduled_subs = {"T.*"}
        ↓
    client.run(callback)  — 同步入口，内部调用 asyncio.run(connect())
        ↓
    connect() — 异步主循环
        ↓
    建立 WebSocket 连接 → wss://socket.massive.com/{market}
        ↓
    接收 welcome 消息
        ↓
    发送认证: {"action": "auth", "params": "<api_key>"}
        ↓
    接收认证响应（失败则抛出 AuthError）
        ↓
    进入主消息循环

3.2 订阅管理
-------------

WebSocketClient 维护两个集合:
  - subs: 当前已向服务器发送的订阅
  - scheduled_subs: 用户期望的订阅集

每次循环迭代检查 schedule_resub 标志:
  若 True → 计算差集:
    新增 = scheduled_subs - subs → 发送 {"action": "subscribe", "params": "T.*,..."}
    移除 = subs - scheduled_subs → 发送 {"action": "unsubscribe", "params": "..."}
  更新 subs = scheduled_subs.copy()

通配符处理:
  订阅 "T.*" 时自动移除已有的 "T.AAPL", "T.MSFT" 等具体订阅

用户可在运行时动态调用:
  client.subscribe("Q.AAPL")     # 添加订阅
  client.unsubscribe("T.*")      # 取消订阅
  client.unsubscribe_all()        # 清空所有订阅

3.3 消息处理
-------------

    服务器推送消息（JSON 数组）
        ↓
    raw=False 路径:
        ↓
    parse(msg_list, logger, market)
        ↓ 遍历每条消息
    查找 MARKET_EVENT_MAP[(market, event_type)]
        ↓ 得到对应模型类
    Model.from_dict(msg) → 模型实例
        ↓
    返回 List[Model] 给用户 callback

    raw=True 路径:
        ↓
    直接将原始 str/bytes 传给用户 callback

3.4 重连机制
-------------

  - 默认最大重连 5 次（可配置 max_reconnects）
  - ConnectionClosedError 触发重连: 递增计数器 → 重设 schedule_resub → 重建连接
  - 超过最大次数 → 抛出最后一个异常
  - ConnectionClosedOK → 正常退出不重连

3.5 WebSocket 消息模型注册表
-----------------------------

所在文件: massive/websocket/models/__init__.py

MARKET_EVENT_MAP 是一个嵌套字典，键为 (Market, EventType)，值为模型类:

    MARKET_EVENT_MAP = {
        Market.Stocks: {
            "T":  EquityTrade,    # 逐笔成交
            "Q":  EquityQuote,    # NBBO 报价
            "A":  EquityAgg,      # 秒级聚合
            "AM": EquityAgg,      # 分钟级聚合
            "LULD": LimitUpLimitDown,
            "NOI": Imbalance,
            ...
        },
        Market.Crypto: {
            "XT": CryptoTrade,
            "XQ": CryptoQuote,
            "XA": CurrencyAgg,
            "XL2": Level2Book,
            ...
        },
        ...
    }

新增事件类型只需: 定义模型类 + 在 MARKET_EVENT_MAP 中注册。


================================================================================
四、模型系统
================================================================================

4.1 @modelclass 装饰器
-----------------------

所在文件: massive/modelclass.py

    @modelclass
    class Agg:
        open: Optional[float] = None
        high: Optional[float] = None
        ...

@modelclass 在标准 @dataclass 基础上:
  - 重写 __init__: 同时支持位置参数和关键字参数
  - 位置参数按类属性声明顺序映射
  - 允许混合使用: Agg(1.0, 2.0, close=3.0)

4.2 from_dict() 反序列化
--------------------------

每个模型类定义 @staticmethod from_dict(d) 方法:

    @staticmethod
    def from_dict(d):
        return Agg(
            d.get("o", None),   # API 简写 "o" → open
            d.get("h", None),   # "h" → high
            d.get("l", None),   # "l" → low
            d.get("c", None),   # "c" → close
            d.get("v", None),   # "v" → volume
            d.get("t", None),   # "t" → timestamp
            ...
        )

此设计将 API 响应的缩写键名与 Python 的可读属性名解耦。

4.3 公共枚举
-------------

所在文件: massive/rest/models/common.py

  Sort / Order          — 排序方向 (ASC, DESC)
  Market / AssetClass   — 市场/资产类型
  Locale                — 地区 (US, GLOBAL)
  Timeframe             — 时间框架 (ANNUAL, QUARTERLY)
  SeriesType            — 序列类型 (OPEN, CLOSE, HIGH, LOW)
  Direction             — 涨跌排行 (GAINERS, LOSERS)
  DividendType          — 股息类型
  DataType / SIP        — 数据源类型
  等等

4.4 RequestOptionBuilder
-------------------------

所在文件: massive/rest/models/request.py

用于 Launchpad 多租户场景，构建边缘请求头:

    options = RequestOptionBuilder(
        edge_id="user123",
        edge_ip_address="192.168.1.1",
        edge_user="agent-string"
    )
    client.list_trades("AAPL", options=options)

生成的头部:
  X-Massive-Edge-ID: user123
  X-Massive-Edge-IP-Address: 192.168.1.1
  X-Massive-Edge-User-Agent: agent-string


================================================================================
五、异常与日志
================================================================================

5.1 异常体系
-------------

所在文件: massive/exceptions.py

  AuthError     — API key 为空或认证失败
  BadResponse   — API 返回非 200 状态码

5.2 日志
---------

所在文件: massive/logging.py

  get_logger(name) → logging.Logger
    - 输出到 stdout
    - 格式: "%(asctime)s %(name)s %(levelname)s: %(message)s"

  verbose=True  → 设置 DEBUG 级别
  trace=True    → 额外打印请求 URL 和响应头（API key 已脱敏）


================================================================================
六、OpenAPI 规范与代码生成
================================================================================

所在文件: .massive/

  rest.json       — REST API OpenAPI 规范（从 api.massive.com/openapi 拉取）
  rest.py         — 拉取脚本: make rest-spec
  websocket.json  — WebSocket API 规范: make ws-spec

REST 客户端代码（Mixin + 模型）需与 rest.json 规范保持同步。
新增/变更 API 端点时:
  1. make rest-spec 更新规范
  2. 按规范新增或修改 Mixin 方法和模型类


================================================================================
七、测试体系
================================================================================

7.1 REST 测试
--------------

所在目录: test_rest/

基类 BaseTest (test_rest/base.py):
  - 继承 unittest.TestCase
  - 使用 pook 库拦截 HTTP 请求
  - 自动扫描 test_rest/mocks/ 目录，将 JSON 文件注册为 mock 响应
  - mock 文件路径映射 URL 路径（特殊字符替换: ? → &, : → ;）
  - setUpClass() 创建共享 RESTClient 实例

运行:
  make test_rest
  poetry run python -m unittest test_rest.test_aggs

7.2 WebSocket 测试
-------------------

所在目录: test_websocket/

基类 BaseTest (test_websocket/base_ws.py):
  - 继承 unittest.IsolatedAsyncioTestCase（异步测试支持）
  - 内置 mock WebSocket 服务器 (mock_server.py)
  - expectResponse() 预设期望消息
  - expectProcessor() 断言收到的消息与期望匹配

运行:
  make test_websocket
  poetry run python -m unittest test_websocket.test_conn


================================================================================
八、完整数据流示例
================================================================================

8.1 REST 分页请求流程
----------------------

用户代码:
    for trade in client.list_trades("AAPL", limit=100):
        process(trade)

内部流程:

    TradesClient.list_trades("AAPL", limit=100)
        │
        ├→ url = "/v3/trades/AAPL"
        ├→ params = _get_params() → {"limit": 100}
        └→ _paginate(url, params, deserializer=Trade.from_dict, result_key="results")
              │
              └→ _paginate_iter()  [生成器]
                    │
                    ├→ _get(url, params, raw=True) → HTTPResponse
                    │     │
                    │     ├→ urllib3.PoolManager.request("GET", BASE+url, fields=params)
                    │     ├→ 自动重试（指数退避，最多 3 次）
                    │     └→ 返回 HTTPResponse
                    │
                    ├→ 解析 JSON → {"results": [...], "next_url": "..."}
                    │
                    ├→ for item in results:
                    │     Trade.from_dict(item) → yield Trade 对象
                    │
                    ├→ 检查 next_url
                    │     有 → 解析新 URL 和参数 → 继续循环
                    │     无 → 生成器结束
                    │
                    └→ 用户逐个接收 Trade 对象（惰性加载，按需翻页）

8.2 WebSocket 实时数据流程
---------------------------

用户代码:
    def handle(msgs):
        for m in msgs:
            print(m)
    client = WebSocketClient(subscriptions=["T.*"])
    client.run(handle)

内部流程:

    asyncio.run(connect(handle))
        │
        ├→ 建立 wss://socket.massive.com/stocks 连接
        │
        ├→ 接收 welcome → 发送 auth → 接收 auth 确认
        │
        ├→ 检查 schedule_resub=True
        │     └→ 发送 {"action": "subscribe", "params": "T.*"}
        │
        └→ 消息循环（永久运行）:
              │
              ├→ ws.recv(timeout=1s)
              │     超时 → 继续循环
              │     收到数据 → 解析 JSON
              │
              ├→ parse(msg_list, logger, Market.Stocks)
              │     │
              │     ├→ msg["ev"] = "T" (trade 事件)
              │     ├→ MARKET_EVENT_MAP[Stocks]["T"] → EquityTrade
              │     └→ EquityTrade.from_dict(msg) → 模型实例
              │
              ├→ await handle([EquityTrade, ...])
              │
              └→ 异常处理:
                    ConnectionClosedError → 重连（最多 5 次）
                    ConnectionClosedOK   → 正常退出


================================================================================
九、扩展指南
================================================================================

新增 REST API 领域:
  1. 在 massive/rest/models/ 下创建模型文件，定义 @modelclass + from_dict()
  2. 在 massive/rest/ 下创建 Mixin 文件，继承 BaseClient，实现方法
  3. 在 massive/rest/__init__.py 的 RESTClient 继承链中加入新 Mixin
  4. 在 massive/rest/models/__init__.py 中导出新模型
  5. 在 test_rest/ 下添加测试和 mock 数据

新增 WebSocket 事件类型:
  1. 在 massive/websocket/models/models.py 定义消息模型
  2. 在 massive/websocket/models/__init__.py 的 MARKET_EVENT_MAP 中注册
  3. 在 test_websocket/ 下添加测试

自定义 JSON 编解码器:
  client = RESTClient(custom_json=orjson)
  — 自定义编解码器需提供 loads() 和 dumps() 方法

Launchpad 边缘请求:
  opts = RequestOptionBuilder(edge_id="uid", edge_ip_address="1.2.3.4")
  client.list_trades("AAPL", options=opts)


================================================================================
十、关键设计决策总结
================================================================================

  1. Mixin 多重继承 — 领域隔离，组合灵活，避免深层继承链
  2. @modelclass 装饰器 — 在 dataclass 基础上支持位置参数，简化 from_dict() 调用
  3. 参数自动转换 (_get_params) — 利用 inspect 反射将函数签名直接映射为 API 参数
  4. 生成器分页 — 惰性加载，用户无需关心分页细节，内存友好
  5. 异步 WebSocket + 同步包装 — connect() 原生 async，run() 提供便捷同步入口
  6. 事件注册表 (MARKET_EVENT_MAP) — 解耦消息路由与模型定义，扩展性好
  7. pook HTTP mock — 测试不依赖真实 API，mock 文件按 URL 路径组织
