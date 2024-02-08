import tushare as ts

ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
ts_pro = ts.pro_api()
"""
open 开盘价
high 最高价 
low 最低价
close  收盘价
pre_close 前一天的收盘价
change 价格变动
pct_chg 涨跌幅
vol 成交量
amount 
"""
# daily:以天为单位进行数据获取，weekly(周),monthly(月)
# df = ts_pro.daily(ts_code="600848.SH", start_date="20240101", end_data="20240118")

# 获取历史数据,ktype:D表示日，W表示周，M表示月，5、15、30、60分别表示几分钟，默认是D
# df = ts.get_hist_data(code="600848", start="2024-01-01", end="2024-01-18", ktype="5")
# print(df)

# Tushare获取涨停股票数据
# df = ts_pro.limit_list()
# print(df)

# Tushare获取期货合约信息
# df = ts_pro.fut_basic(exchange="DCE", fut_type="1")
# print(df)

# 根据合约代码、交易所代码获取期货历史数据
# df = ts_pro.fut_daily(ts_code="RB2005.SHF")
# print(df)

# 获取新闻快讯：能够用其进行舆情监测、市场情绪等方面的研究(无积分限制)
# df = ts_pro.news(src="sina", start_date="2024-01-17", end_date="2024-01-18")
# print(df)

# 通用行情接口(无积分限制)
# df = ts.pro_bar(
#     ts_code="000001.SZ",  # 证券代码
#     start_date="201910010",
#     end_date="20191020",
#     asset="E",  # E表示股，I表示沪深指数，C表示数字货币，FT表示期货，FD表示基金，O表示期权，CB表示可转债，默认是E
#     freq="D",  # min分钟，D日，W周，M月，默认是D
# )
# print(df)

# 用通用行情接口获取期货，五分钟级别的数据
df = ts.pro_bar(
    ts_code="RB1910.SHF",
    start_date="20191010",
    end_date="20191015",
    asset="FT",
    freq="5min",
)

print(df)
