import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 计算ATR指标
ATR = talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)
print(ATR.dropna())

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
# 绘制ATR曲线
ax2.plot(0, np.mean(ATR))
ax2.plot(ATR, label="ATR")
plt.legend()
plt.show()
