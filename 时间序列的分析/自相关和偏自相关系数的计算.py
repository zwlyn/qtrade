"""
# 自相关和偏相关系数
自相关系数是由自自协方差除以变量的方差得到的，则随机变量Xt与其滞后l期的随机变量Xt-l之间的自相关系数的表达式如下：
ACt = Cov(Xt, Xt-1) / Var(Xt)
为了衡量过去单独某个时刻对现在的影响，所以引入了偏自相关系数（Partial Autocorrelation）,变量Xt与其滞后l期的随机变量
Xt-l之间的偏自相关系数的表达式如下：PACl = Corr(Xt, Xt-l|Xt-1, Xt-2,...,Xt-l+1)
由上式可以看出，变量Xt与其滞后l期的随机变量Xt-1之间的偏自相关系数是它们之间的条件自相关系数，就是在给定随机变量Xt-1,Xt-2,
...,Xt-l+1的条件下，或是剔除了中间l-1个变量的干扰后，Xt与Xt-l的相关程度。相关系数越大，则相关性越强。
"""
import statsmodels.tsa.api as smt
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("000001.SZ.csv")
# 将日期设置为索引
df.index = pd.to_datetime(df["trade_date"], format="%Y%m%d")
# 计算自相关系数和偏自相关系数
ac = smt.acf(df["close"], nlags=30)
pac = smt.pacf(df["close"], nlags=30)
print(ac)
print(pac)

# 可视化
fig = plt.figure()
# 设置子图
ts_ax = fig.add_subplot(311)
acf_ax = fig.add_subplot(312)
pacf_ax = fig.add_subplot(313)
# 绘制图像
ts_ax.set_title("time series")
acf_ax.set_title("autocorrelation coefficient")
pacf_ax.set_title("partial autocorrelation coefficient")
ts_ax.plot(df["close"])
smt.graphics.plot_acf(df["close"], lags=30, ax=acf_ax)
smt.graphics.plot_pacf(df["close"], lags=30, ax=pacf_ax)
# 自适应布局
plt.tight_layout()
plt.show()

# 由图可见自相关系数一直维持在较高的值，而且下降趋势很缓慢，所有可以推测其不具有平稳性
