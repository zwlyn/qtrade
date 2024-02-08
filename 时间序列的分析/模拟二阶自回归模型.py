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
# 自回归系数
a1 = 0.3
a2 = 0.6
x = np.zeros(n_sample)
# 模拟AR(2)过程
for t in range(n_sample):
    x[t] = a1 * x[t - 1] + a2 * x[t - 2] + w[t]
# 可视化AR(2)
draw_ac_pac(x)
"""
从自相关图中就可以看出序列存在明显的序列相关性，而且偏自相关图中在阶数为2时迅速截尾，所以预先指导这是一个AR过程就可以初步判断它
是AR(2)过程。
"""

# 使用statsmodels.tsa.api.AR 对这个序列进行拟合
from statsmodels.tsa.api import AutoReg

# 拟合数据
model = AutoReg(x, lags=2, trend="n")
result = model.fit()
# 输出结果
print(result.params)
"""
输出结果如下，于前面常见过程中定义的参数0.3和0.6近似，说明通过AR模型大致拟合除了前面创建的AR(2)的过程
[0.31273958 0.60614796]
"""
