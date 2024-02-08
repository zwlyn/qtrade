"""
双均线策略是一种经典的趋势跟踪策略，也就是常说的金叉死叉信号组合得到的策略，常用于捕捉一段大趋势，思想很简单
根据长短周期的价格的移动平均线之间的关系来确认买卖点。其中短周期均线和长周期均线分别代表近期的走势和长期的走势，
当短周期均线从下向上突破长周期均线时，意味着当前时间段具有上涨趋势，突破点也就是常说的金叉，这是多头信号；当长
周期均线从上向下突破短周期信号时，则意味着当前时间段具有下跌趋势，突破点也就是常说的死叉，这是空头信号。
"""
import tushare as ts

# 1.数据准备
# ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# # 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
# ts_pro = ts.pro_api()
# df = ts_pro.daily(
#     ts_code="000001.SZ",
#     start_date="20180101",
#     end_date="20191230",
#     fields="ts_code, trade_date,open,high,low,close,vol",
# )
# df = df.reindex(index=df.index[::-1])
# # 用到的列
# used_cols = ["trade_date", "close"]
# df = df["used_cols"]
# df.to_csv("./000001.SZ.csv", index=None)

# 策略编写
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ffn

# 是否持仓
hold = False
# 持仓数
pos = 0
# 回测资金
capital = 100000
# 剩余资金
rest = 0
# 手续费万分之三
fee = 0.003
# 每日资金数列表
capital_list = []
# 20日均线数组
MA20_array = np.zeros(20)
# 10日均线数组
MA10_array = np.zeros(10)
# 读取历史数据
df = pd.read_csv("./000001.SZ.csv")
print(df)

# 遍历历史数据
import talib

ma10_df = talib.MA(df["close"], timeperiod=10)
ma20_df = talib.MA(df["close"], timeperiod=20)

for i in range(len(df)):
    if i < 20:
        continue
    price = df.loc[i, "close"]
    date = df.loc[i, "trade_date"]
    # 价格序列平移
    MA10 = ma10_df[i]
    MA20 = ma20_df[i]
    if MA10 >= MA20 and hold == False:
        # 计算开仓数目
        pos = int(capital / price / 100) * 100
        # 剩余资金
        rest = capital - pos * price * (1 + fee)
        # 持仓设置为True
        hold = True
        print("buy at", date, "prece", price, "capital", capital)
    elif MA10 < MA20 and hold == True:
        # 计算平仓后的资金
        capital = pos * price * (1 - fee) + rest
        # 持仓数设置为0
        pos = 0
        # 持仓设置为False
        hold = False
        print("sell at", date, "price", price, "capital", capital)
    # 计算每日的资金数目
    if hold == True:
        # 如果持仓，就记录当前市值
        capital_list.append(rest + pos * price)
    else:
        # 如果没持仓，就记录当前资金
        capital_list.append(capital)

# 计算风险指标
capital_series = pd.Series(capital_list)
# 计算资金序列的简单收益率
capital_returns = ffn.to_returns(capital_series)
# 计算收益率
print(ffn.calc_total_return(capital_series))
# 计算最大回撤率
print(ffn.calc_max_drawdown(capital_series))
# 计算夏普比率
# print(ffn.calc_sharpe(capital_returns))
# 可视化资金曲线
plt.plot(range(len(capital_list)), capital_list)
plt.show()
