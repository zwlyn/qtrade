import numpy as np


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


n_sample = 1000
# 白噪声过程
w = np.random.normal(size=n_sample)
# 移动平均系数
b1 = 0.4
b2 = 0.8
x = np.zeros(n_sample)
# 模拟MA(2)过程
for t in range(n_sample):
    x[t] = b1 * w[t - 1] + b2 * w[t - 2] + w[t]
# 可视化MA(2)
draw_ac_pac(x)

from statsmodels.tsa.api import ARIMA

# Assuming 'x' is your time series data
order = (0, 0, 2)  # ARMA(p, d, q) order
result = ARIMA(x, order=order).fit()

# Output results
print(result.summary())
print(result.params)
