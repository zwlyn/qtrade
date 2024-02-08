import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf

# 解决中文显示问题
plt.rcParams["font.sans-serif"] = ["KaiTi"]
# 解决负号无法显示的问题
plt.rcParams["axes.unicode_minus"] = False
df = pd.read_csv("sample.csv")
print(df)
# K线数据的可视化
fig = plt.figure()
ax = fig.add_subplot(111)
mpf.candlestick2_ohlc(
    ax,
    df["Open"],
    df["High"],
    df["Low"],
    df["Close"],
    colordown="green",
    colorup="red",
    width=0.6,
)
plt.show()
