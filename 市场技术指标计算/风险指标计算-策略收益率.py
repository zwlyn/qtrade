"""
策略收益率（Total Return）是一个用于衡量策略好坏最为直观的概念，它代表了策略从开始到结束，总资产的变化率。计算方法如下：
Total Return = (P(end) - P(start)) / P(start) * 100% 式中P(start)和P(end)分别代表策略开始时和结束时的资产数额。
"""
import ffn
import pandas as pd

# 累计资产序列
series = pd.Series([10000, 10100, 10300, 10600])
# 计算收益率
result = ffn.calc_total_return(series)
print(result)
