"""
Pandas_datareader 它可以从国内外很多数据源中抓取数据，并将它们转换为Pandas中的DataFrame格式
安装：pip install pandas_datareader
# 被墙了
"""
import pandas_datareader.data as web

data = web.DataReader(
    "600789.SS", data_source="yahoo", start="2019-01-01", end="2019-10-01"
)
print(data)
