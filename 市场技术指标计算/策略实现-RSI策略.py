import tushare as ts

# 1.数据准备
ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
ts_pro = ts.pro_api()
df = ts_pro.daily(
    ts_code="000031.SZ",
    start_date="20220101",
    end_date="20231230",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])
# 用到的列
used_cols = ["trade_date", "close"]
df = df[used_cols]
# df.to_csv("./000001.SZ.csv", index=None)

# 策略编写
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ffn
import talib

# 是否持仓
hold = False
# 持仓数
pos = 0
# 回测资金
capital = 100000
rest = 0
# 手续费费率万分之三
fee = 0.0003
# 每日盈亏列表
capital_list = []
# 用于计算RSI指标的数组
rsi6_array = np.zeros(7)
# 读取数据
# df = pd.read_csv("./000001.SZ.csv")
# 遍历历史数据
for i in range(len(df)):
    # 如果小于等于6个数据就跳过
    if i <= 6:
        continue
    price = df.loc[i, "close"]
    date = df.loc[i, "trade_date"]
    # 价格序列平移
    rsi6_array[0:6] = rsi6_array[1:7]
    # 将新数据追加到数组末端
    rsi6_array[-1] = price
    # 计算RSI指标
    rsi6 = talib.RSI(rsi6_array, timeperiod=6)[-1]
    # 判断是否到达开仓信号
    if rsi6 <= 20 and hold == False:
        # 计算开仓数目
        pos = int(capital / price / 100) * 100
        # 剩余资金
        rest = capital - pos * price * (1 + fee)
        # 持仓设置为True
        hold = True
        print("buy at", date, "price", price, "captital", capital)
    elif rsi6 >= 80 and hold == True:
        # 计算平仓后的资金
        capital = pos * price * (1 - fee) + rest
        # 持仓数设置为0
        pos = 0
        # 持仓设置为False
        hold = False
        print("sell at", date, "price", price, "capital", capital)
    # 计算每日的市值
    if hold == True:
        # 如果持仓，就记录当前市值
        capital_list.append(rest + pos * price)
    else:
        # 如果没有持仓，就记录当前资金
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
