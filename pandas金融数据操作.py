import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ohlc_data = [
    ["2021-11-01", 16.45, 16.48, 16.31, 16.41],
    ["2021-11-02", 16.30, 16.32, 15.70, 15.85],
    ["2021-11-03", 15.75, 15.87, 15.63, 15.86],
    ["2021-11-04", 15.89, 15.91, 15.55, 15.59],
]
column_indexs = ["Datetime", "Open", "High", "Low", "Close"]
df = pd.DataFrame(data=ohlc_data, columns=column_indexs)
# 计算RSI(Relative Strength Index，相对强弱指标)，它可以表示市场一定时期的景气程度。RSI可以用来估计多空力量的强弱程度，
# 所以它可以作为一种超买超卖指标，N日的RSI=(N日收盘涨幅)/(N日涨跌幅)
# df["RSI"] = talib.RSI(df["Close"], timeperiod=2)

# 使用DateFrame的resample()进行多周期K线数据合成,5T表示对元数据每间隔5个单位进行一次转换操作（即每5分钟进行合并）
df["Datetime"] = pd.to_datetime(df["Datetime"])
# 将Datetime作为索引
df = df.set_index("Datetime")
rule_dict = {"Open": "first", "High": "max", "Low": "min", "Close": "last"}
result = df.resample("2880T", closed="left", label="right").apply(rule_dict)
df.to_csv("sample.csv")
