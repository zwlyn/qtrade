import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

import tushare as ts

ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
ts_pro = ts.pro_api()
df = ts_pro.daily(
    ts_code="000007.SZ",
    start_date="20230801",
    end_date="20231201",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])

# df = pd.read_csv("000001.SZ.csv")
# 识别捉腰带线的K线组合
nums = talib.CDLBELTHOLD(df["open"], df["high"], df["low"], df["close"])
# 可视化
fig = plt.figure()
ax = fig.add_subplot(111)
# 绘制K线图
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
# 标注识别K线组合的位置
index = nums[nums == 100].index.values
for i in index:
    ax.annotate(
        text="",
        xy=(i, df["high"][i]),
        xytext=(i, df["high"][i] + 0.5),
        arrowprops={"arrowstyle": "->"},
    )
plt.show()
