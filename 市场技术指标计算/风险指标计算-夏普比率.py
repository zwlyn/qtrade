"""
# 夏普比率
对量化投资来说，往往高收益伴随着高风险，很多人希望可以做到风险和收益的平衡。夏普比例就是用于衡量每承担一个单位的风险的情况下，所获得的无风险收益率
的超额回报是多少的指标。夏普比率越高，说明在承担一定风险的情况下，所获得的超额回报也就越高；反之，夏普比例越低甚至为负时，说明在承担一定风险的情况下，
所获得的超额回报越少或没有。所以，一般情况下，夏普比率越高越好。计算方法：
Sharpe Rate = (Rp - Rf) / Op  式中Rp表示策略的年华收益率，Rf表示无风险利率，Op表示策略收益的波动率（策略收益率的年化标准差）
"""
import ffn
import pandas as pd

# 累计资产序列
series = pd.Series([10000, 10100, 10300, 10200, 10100, 10200, 10300])
# 计算资产简单收益率
returns = ffn.to_returns(series)
print(returns)
# 计算夏普比率 报错了ypeError: unsupported operand type(s) for /: 'float' and 'str'
sharpe = ffn.calc_sharpe(returns)
print(sharpe)
