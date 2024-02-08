import statsmodels.tsa.api as smt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def draw_ac_pac(series, nlags=30):
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
    ts_ax.plot(series)
    smt.graphics.plot_acf(series, lags=nlags, ax=acf_ax)
    smt.graphics.plot_pacf(series, lags=nlags, ax=pacf_ax)
    # 自适应布局
    plt.tight_layout()
    plt.show()


df = pd.read_csv("000001.SZ.csv")
# 将日期设置为索引
df.index = pd.to_datetime(df["trade_date"], format="%Y%m%d")
# 差分处理后绘制自相关和偏自相关系数的图表
draw_ac_pac(np.diff(df["close"]))
