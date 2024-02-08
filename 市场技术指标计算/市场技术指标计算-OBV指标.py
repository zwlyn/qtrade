import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 计算OBV指标
OBV = talib.OBV(df["close"], df["vol"])
print(OBV.dropna())
OBV_MA9 = talib.MA(OBV, timeperiod=9)
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
# 绘制OBV曲线
ax2.plot(0, np.mean(OBV))
ax2.plot(OBV, label="OBV")
ax2.plot(OBV_MA9, label="OBV_MA9")
plt.legend()
plt.show()
