import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # 1.数据准备
# pro = ts.pro_api("20231208200557-1a9c3fbc-4615-474e-8445-26c2a0019fc0")
# pro._DataApi__http_url = "http://tsapi.majors.ltd:7000"
# # df = pro.daily(
# #     ts_code="000001.SZ",
# #     start_date="20000101",
# #     end_date="20240207",
# #     fields="ts_code, trade_date,open,high,low,close,vol",
# # )
# df = ts.pro_bar(
#     ts_code="000001.SZ",
#     freq="5min",
#     start_date="20180101",
#     end_date="20181011",
#     api=pro,
# )
# df = df.reindex(index=df.index[::-1])
# df.to_csv("./5minData/000001.SZ.csv", index=None)

# 分时数据——新浪
import akshare as ak

# stock_zh_a_minute_df = ak.stock_zh_a_minute(
#     symbol="sh600751", period="60", adjust="qfq"
# )
# print(stock_zh_a_minute_df)

# 分时数据——东财
import akshare as ak

stock_zh_a_minute_df = ak.stock_zh_a_minute(symbol="sh600751", period="1", adjust="qfq")
stock_zh_a_minute_df["trade_date"] = stock_zh_a_minute_df["day"]
stock_zh_a_minute_df.drop(columns=["day"], inplace=True)
stock_zh_a_minute_df["vol"] = stock_zh_a_minute_df["volume"]
stock_zh_a_minute_df.drop(columns=["volume"], inplace=True)
print(stock_zh_a_minute_df)
stock_zh_a_minute_df.to_csv("./5minData/sh600751.csv", index=None)
