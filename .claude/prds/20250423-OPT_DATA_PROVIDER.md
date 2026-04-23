# 需求描述

## 一、目录修改
data_provider 目录 修改成 processor 目录

## 二、逻辑优化
将data_provider升级成两部分：

1、获取股票列表
功能描述：给定交易所（纳斯达克、道琼斯、标普500），获取对应交易所所有股票，并获取股票detail信息，不再做市值过滤，存储TickerDetails所有字段
文件地址：./data/us_list

2、引入更多获取股票数据的源头
阅读 https://github.com/ZhuLinsen/daily_stock_analysis，将data_provider的内容迁移过来，存储为provider

3、获取股票天级数据
* 功能描述：给定股票列表文件和时间区间，获取股票文件对应的天级别数据
    - 每个股票一个文件夹，放在./data/us_daily
    - 每个股票中的数据按月存储
    - 如果目录中的月份已经存在，当不是当前月份，则更新，否则不用重新请求
* 除了原来的massive获取方式，


相关限制：一次请求后，sleep 12s


将data_provider的逻辑分两部分
step1：使用massive-com包（不用支持多家获取），获取纳斯达克、道琼斯、标普500三个交易所的所有股票代码，并获取detail信息，但不再做市值过滤，字段丰富一些，直接使用massive-com中的TickerDetails，每个交易所存一份
step2: 读取ticker_details文件，获取给定时间区间的天级别数据，按月存储，保持原来的存储方式

1、参考/Users/gjh/code/AKI/massive-com/data_provider，在本项目中实现同等功能
   - 依赖 git 上 的 massive-com/client-python 包
2、将daily_stock_analysis中的数据获取方法，同步到./src/data_provider/sdk中
3、由于massive-com的api限速比较厉害，us_daily实现可以优先使用sdk的数据获取方法

## 相关文件：
- 数据存储：./data/us_daily
- 代码目录：./src/data_provider
- 参考代码：/Users/gjh/code/AKI/massive-com/data_provider

## 引入依赖
- https://github.com/ZhuLinsen/daily_stock_analysis
- https://github.com/massive-com/client-python

# 要求
design和plan文档写到.claude/plans目录
