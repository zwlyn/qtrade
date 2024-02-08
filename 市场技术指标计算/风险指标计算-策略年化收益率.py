"""
# 策略年化收益率
策略年化收益率（Total Annualized Return）也是一个常用的风险指标。它是把当前的收益率换算成年收益率来计算的，当前的收益率可能是一周的
收益率，也可能是一个月的收益率，它是真正获取到的收益率，而年化收益率是一种理论收益率，并不是真正获取到的收益率。年化收益率是变动的，
它通常不会和年收益率相等，一般情况下，年化收益率都是要高于实际的年收益率。
Total Annualized Returns = ((1+P)^(250/n) -1)* 100% 式中n为策略执行的时间，P为这段时间内的策略收益率
"""
import ffn
import pandas as pd

# 累计资产序列
series = pd.Series([10000, 10100, 10300, 10600])
# 计算收益率
result = ffn.calc_total_return(series)
# 将日收益率转换为年化收益率
ann_result = ffn.annualize(result, 4, one_year=250)
print(ann_result)
