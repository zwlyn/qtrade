"""
Pandas是一个强大的数据分析的工具库，它是在Numpy的基础上进行实现的，
所以也包含了数据运算的基本功能。
Pandas中包含了两种常用数据结构：Series（数组+标签）和DataFrame,可以快速便捷地用于数据的表示
另外Pandas中丰富的函数库为我们提供了很多数据分析和处理方法，所以Pandas也被称为
‘数据分析的瑞士军刀’
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Series（数组+标签）
sr = pd.Series(data=[1, 2, 3], index=["11/01", "11/02", "11/03"])
dict1 = {"11/01": 1, "11/02": 2, "11/03": 3}
sr1 = pd.Series(data=dict1)
# sr = pd.Series(data=[1, 2, 3])

# DataFrame可以看作是一个二维数组，既有行索引又有列索引
# 定义一个二维价格序列数据（Open High Low Close）
ohlc_data = [
    [16.45, 16.48, 16.31, 16.41],
    [16.30, np.nan, 15.70, 15.85],
    [15.75, 15.87, 15.63, 15.86],
    [15.89, 15.91, 15.55, 15.59],
]
# 定义行索引
row_indexs = ["11-1", "11-2", "11-3", "11-4"]
# 定义列索引
column_indexs = ["Open", "High", "Low", "Close"]
df = pd.DataFrame(data=ohlc_data, index=row_indexs, columns=column_indexs)
# print(df)
# 根据DataFrame绘制图像
# df.plot()
# plt.show()

# 绘制具体的列
# df["Close"].plot()
# plt.show()

# 绘制柱状图
# df["Close"].plot(kind="bar")
"""plot函数的参数说明
参数   说明
kind   line(默认),bar,hist,box,pie
figsize 图像的大小，传入一个元组（宽度，高度）
use_index 是否使用索引作为刻度的标签，默认是True
title   图像的标题
legend  是否显示图例
fontsize  文字的大小，int类型
xticks  x轴刻度标签
yticks  y轴刻度标签
grid    图像背景是否加网格，默认False
"""
# plt.show()

# # 去除行中含有nan的行或列，默认axis=0表示删除行,默认how=any表示只要有缺失值就删除
# print(df.dropna())
# # axis=0表示删除行，axis=1表示删除列
# print(df.dropna(axis=0))
# print(df.dropna(axis=1))
# # 删除缺失值所在行，只有都是缺失值才删除
# print(df.dropna(how="all"))

# 填充缺失值
# print(df.fillna(666))
# 按照列进行填充缺失值
df["High"] = df["High"].fillna(df["High"].mean())
# print(df)
