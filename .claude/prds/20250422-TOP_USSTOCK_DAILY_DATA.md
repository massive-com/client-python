# 需求描述

搜集头部公司的日级别交易数据（massive/rest/models/aggs.py:Agg）
1、获取纳斯达克、道琼斯、标普500 市值>=50亿美金的公司列表，存储到data/us_daily_data目录下
2、针对每个股票，按月获取从2020年开始的日级别数据，每个股票有一个单独的文件夹，每月有一份数据（存储到data/us_daily_data）
    - 如果已经存储给定月份的股票数据，当不是当前月份，则更新，否则不用重新请求

# 限制
一次请求后，sleep 20s


# 相关文件：
- rest模块：./massive/rest
- 数据存储：./data/us_daily
- 代码目录：./project

# 要求
design和plan文档写到.claude/plans目录
