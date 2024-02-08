import talib
import pandas as pd
import mpl_finance as mpf
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("000001.SZ.csv")
# 计算KDJ指标,因为RSV需要9个周期的数据,K值和D值需要3个周期的数据,所以有效值是从索引位置12开始的
K, D = talib.STOCH(
    df["high"], df["low"], df["low"], fastk_period=9, slowk_period=3, slowd_period=3
)
J = 3 * K - 2 * D
print(K.dropna())
print(D.dropna())
print(J.dropna())

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
# 绘制KDJ曲线
ax2.plot(0, np.mean(K))  # 使得上下坐标对其
ax2.plot(K, label="K")
ax2.plot(D, label="D")
ax2.plot(J, label="J")
# 显示图像
plt.legend()
plt.show()
