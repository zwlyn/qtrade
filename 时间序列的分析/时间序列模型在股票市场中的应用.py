import tushare as ts

ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
ts_pro = ts.pro_api()
df = ts_pro.daily(
    ts_code="000002.SZ",
    start_date="20180101",
    end_date="20190201",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])
df.to_csv("./000002.SZ.csv", index=None)


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


import pandas as pd

# 读取数据
df = pd.read_csv("000002.SZ.csv")
# 将日期设置为索引
df.index = pd.to_datetime(df["trade_date"], format="%Y%m%d")
# 可视化自相关和偏自相关系数
# draw_ac_pac(df["close"], nlags=30)
"""
可见其自相关系数拖尾，偏自相关系数截尾，但其后后置项中也有超过显著区域的，所以可以通过ARMA模型对其进行建模。
另外，从自相关和偏自相关图中可看出原序列是不平稳的，所以需要先对其选择合适的差分次数使其平稳，因此选择了ARIMA模型
"""

from statsmodels.tsa.api import ARIMA
import numpy as np
import matplotlib.pyplot as plt

# 划分训练数据和测试数据
train_data = df["close"][:-10]
test_data = df["close"][-10:]
# 定义全局变量
min_aic = np.inf
best_order = None
best_arima = None
# 遍历范围
counter = 5
# 循环遍历
for i in range(counter):
    for k in range(counter):
        for j in range(counter):
            # try:
            tmp_arima = ARIMA(train_data, order=(i, j, k)).fit()
            tmp_aic = tmp_arima.aic
            if tmp_aic < min_aic:
                min_aic = tmp_aic
                best_order = (i, k, j)
                best_arima = tmp_arima
            # except:
            #     continue
# 输出最优结果
print("order", best_order)
print("para", best_arima.params)

# 预测后10天价格数据
result = best_arima.forecast(10)
predicted = result
index = test_data.index
predicted_df = pd.DataFrame(predicted, index=index)
# 可视化预测值与真实值
fig = plt.figure()
plt.plot(df["close"][-100:], c="blue")
plt.plot(predicted_df, c="red")
plt.legend(["true", "prediction"])
plt.show()
