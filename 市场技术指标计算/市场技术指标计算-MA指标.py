# import tushare as ts

# ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# # 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
# ts_pro = ts.pro_api()
# df = ts_pro.daily(
#     ts_code="000001.SZ",
#     start_date="20190801",
#     end_date="20191201",
#     fields="ts_code, trade_date,open,high,low,close,vol",
# )
# df = df.reindex(index=df.index[::-1])
# df.to_csv("./000001.SZ.csv", index=None)


import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")

# 绘制MA指标可视化
ma5_df = talib.MA(df["close"], timeperiod=5)
ma10_df = talib.MA(df["close"], timeperiod=10)
ma20_df = talib.MA(df["close"], timeperiod=20)
fig = plt.figure()
ax = fig.add_subplot()
# 绘制MA指标
ax.plot(ma5_df, label="MA5")
ax.plot(ma10_df, label="MA10")
ax.plot(ma20_df, label="MA20")
mpf.candlestick2_ohlc(
    ax,
    df["open"],
    df["high"],
    df["low"],
    df["close"],
    width=0.6,
    colorup="red",
    colordown="green",
)
plt.legend()
plt.show()
