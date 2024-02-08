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
    ts_code="000010.SZ",
    start_date="20230101",
    end_date="20230801",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])

# 识别昏星的K线组合
nums = talib.CDLEVENINGSTAR(df["open"], df["high"], df["low"], df["close"])
print(nums)

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
index = nums[nums == -100].index.values
print(index)
for i in index:
    ax.annotate(
        xy=(i, df["high"][i]),
        xytext=(i, df["high"][i] + 0.15),
        arrowprops={"arrowstyle": "->"},
        text="",
    )
plt.show()
