import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 绘制MACD
diff, dea, macd = talib.MACD(df["close"], fastperiod=12, slowperiod=26, signalperiod=9)
# print(diff.dropna(), dea.dropna(), macd.dropna())
# 可视化
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
# 绘制K线图
mpf.candlestick2_ohlc(
    ax1,
    df["open"],
    df["high"],
    df["low"],
    df["close"],
    width=0.6,
    colorup="red",
    colordown="green",
)
# 绘制DIFF和DEA曲线
ax2.plot(diff, label="DIFF")
ax2.plot(dea, label="DEA")
# 分别得到MACD的Bar市正值和负值的数据
macd_red = np.where(macd > 0, macd, 0)
macd_green = np.where(macd < 0, macd, 0)
# 绘制MACD Bar
ax2.bar(range(len(macd)), macd_red, width=0.6, facecolor="red", label="MACD")
ax2.bar(range(len(macd)), macd_green, width=0.6, facecolor="green", label="MACD")
# 显示图像
plt.legend()
plt.show()
