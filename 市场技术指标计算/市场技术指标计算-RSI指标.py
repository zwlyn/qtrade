import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 计算RSI指标
rsi = talib.RSI(df["close"], timeperiod=14)  # timeperiod=14时至少需要14个数据才能够计算RSI指标
print(rsi.dropna())
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
# 绘制RSI曲线
ax2.plot(0, np.mean(rsi))  # 使得上下坐标对应(rsi也从0开始)
ax2.plot(rsi, label="RSI")
# 显示图像
plt.legend()
plt.show()
