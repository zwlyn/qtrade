import pandas as pd
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams["font.sans-serif"] = ["KaiTi"]
# 解决负号无法显示的问题
plt.rcParams["axes.unicode_minus"] = False
df = pd.read_csv("sample.csv")
print(df)

fig = plt.figure()
df["Close"].plot()
fig = plt.figure()
# df["Open"].plot(kind="bar")

# 柱状图绘制
plt.bar(df["Datetime"], df["Close"])
# 设置坐标轴的标签
plt.xlabel("日期")
plt.ylabel("价格")
fig = plt.figure()

# 散点图绘制
plt.scatter(df["Close"], df["Open"])

# 饼图绘制
plt.pie([20, 10, 70], labels=["A", "B", "C"])
# 设置字体样式
title_style = {"family": "KaiTi", "size": 16, "weight": "normal", "color": "red"}
plt.title("饼图一个")


# 绘制多个子图
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.plot(df["Close"], c="r", linestyle="-", marker="o")
ax2.plot(df["Open"], c="g", linestyle="--", marker="*")
plt.show()
