import numpy as np
import statsmodels.tsa.api as smt


def draw_ac_pac(series, nlags=30):
    import statsmodels.tsa.api as smt
    import matplotlib.pyplot as plt

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


# 样本数
n_sample = 1000
# AR自回归系数
a = np.array([0.3, 0.6])
# MA移动平均数
b = np.array([0.4, 0.8])
# 转换为指定形式
ar = np.concatenate(([1], -a))
ma = np.concatenate(([1], b))
# 创建ARMA过程
arma = smt.arma_generate_sample(ar=ar, ma=ma, nsample=n_sample)
# 可视化
draw_ac_pac(arma)

# 拟合数据
from statsmodels.tsa.api import ARIMA

# 拟合数据
order = (2, 0, 2)  # ARMA(p, d, q) order
result = ARIMA(arma, order=order).fit()
print(result.params)
