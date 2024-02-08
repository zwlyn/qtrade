import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 计算CCI指标
CCI = talib.CCI(df["high"], df["low"], df["close"], timeperiod=14)
print(CCI.dropna())
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
# 绘制CCI曲线
ax2.plot(0, np.mean(CCI))
ax2.plot(CCI, label="CCI")
plt.legend()
plt.show()
