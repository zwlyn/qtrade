"""
# 索提诺比率
索提诺比率（Sortino Ratio）与夏普比率类似，只不过前者表述的是策略在单位下行风险下所能获得的超额收益。这里的下行风险指的是向下波动的风险，也就是策略
亏损的风险。因此，索提诺比率与夏普比率一样，也是比率越高越好。计算公式：索提诺比率=（Rp - Rf） / Od
式中，Rp表示策略的年化收益率，Rf表示无风险收益率，Od表示策略的下行波动率。
"""
import ffn
import pandas as pd

# 累计资产序列
series = pd.Series([10000, 10100, 10300, 10200, 10100, 10200, 10300])
# 计算资产简单收益率
returns = ffn.to_returns(series)
# 计算索提诺比率 报错！
sortino = ffn.calc_sortino_ratio(returns)
print(sortino)
