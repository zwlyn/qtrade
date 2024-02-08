import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 识别晨星的K线组合
nums = talib.CDLMORNINGSTAR(df["open"], df["high"], df["low"], df["close"])
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
index = nums[nums == 100].index.values
for i in index:
    ax.annotate(
        xy=(i, df["high"][i]),
        xytext=(i, df["high"][i] + 0.5),
        arrowprops={"arrowstyle": "->"},
        text="",
    )
plt.show()
