import numpy as np

close_price = np.array([10.81, 10.85, 10.92, 10.75, 10.59, 10.86, 11.02, 11.13, 11.34])


# 计算收益率
def cal_return_rate(price_series, type="sim"):
    """
    计算简单收益率和对数收益率,P94
    """
    if type == "sim":
        return np.diff(price_series)
    elif type == "log":
        return np.diff(np.log(price_series))
    raise TypeError("Input type not in ['sim','log']")


# 计算滑动窗口
def cal_sliding_window(series, size):
    """
    滑动窗口在建立回测模型时经常会用到，指定一定长度的窗口，在大量数据中取出窗口大小的数据，
    每个窗口的数据分析结束后，窗口再继续位移一个单位。可以极大减少内存的消耗，且可对数据当前
    特征进行分析（指标计算、机器学习模型的预测）
    """
    windows_arr = np.zeros(shape=(len(series) - size + 1, size))
    for i in range(len(series) - size + 1):
        window = series[i : i + size]
        windows_arr[i] = window
    return windows_arr


# 计算均线
def cal_MA(series, period=10):
    """
    在股票市场中10日均线（MA10）和20日均线（MA20）常被作为两种技术指标用来
    判断当前市场的趋势情况，因此有很多CTA策略都会以来均线作为买卖的信号
    period: int 周期，默认为MA10即10
    """
    # 定义存储数组MA
    ma_arr = np.zeros(shape=len(series) - period + 1)
    windows = cal_sliding_window(series, period)
    for i in range(len(windows)):
        ma_arr[i] = np.mean(windows[i])
    return ma_arr


price = np.random.normal(loc=10, scale=1, size=50)
print(cal_MA(price))
