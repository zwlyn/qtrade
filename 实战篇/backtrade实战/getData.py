import tushare as ts
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1.数据准备
pro = ts.pro_api("20231208200557-1a9c3fbc-4615-474e-8445-26c2a0019fc0")
pro._DataApi__http_url = "http://tsapi.majors.ltd:7000"
df = pro.daily(
    ts_code="000001.SZ",
    start_date="20000101",
    end_date="20240207",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])
df.to_csv("./data/000001.SZ.csv", index=None)
