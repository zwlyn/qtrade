"""
# 最大回撤率
最大回撤率（Maximum Drawdown）同夏普比率一样，也是用于衡量策略风险的指标。它描述的是策略的最大亏损情况，即在一段时间内，资产从高峰跌落至低估的幅度。
因此，最大回撤率通常越小越好。计算方法：  最大回撤率 = （Px - Py） / Px  式中，Px和Py分别表示资产一段时间的最高值和最低值。
"""
import ffn
import pandas as pd

# 累计资产序列
series = pd.Series([10000, 10100, 10300, 10200, 10100, 10200, 10300])
# 计算最大回撤率
max_drawdown = ffn.calc_max_drawdown(series)
print(max_drawdown)
