import tushare as ts
import matplotlib.pyplot as plt

ts.set_token("5bc162559b5b797dd8e5ec328db5c0f7ee2a2fc0c7f950652a5706a3")
# 初始化接口,初始化后就可以通过Tushare提供的方法来获取历史数据了
ts_pro = ts.pro_api()
df = ts_pro.daily(
    ts_code="002616.SZ",
    start_date="20190301",
    end_date="20191201",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df = df.reindex(index=df.index[::-1])
df_1 = ts_pro.daily(
    ts_code="300070.SZ",
    start_date="20190301",
    end_date="20191201",
    fields="ts_code, trade_date,open,high,low,close,vol",
)
df_1 = df_1.reindex(index=df_1.index[::-1])
print(df, df_1)
# 可视化
fig = plt.figure()
plt.plot(df["close"])
plt.plot(df_1[["close"]])
plt.show()

# 对他们呢进行一阶差分进行平稳性检验
from statsmodels.tsa.stattools import adfuller
import numpy as np

# 平稳性检验
print(adfuller(np.diff(df["close"])))
print(adfuller(np.diff(df_1["close"])))
"""
根据结果可一看到两者的一阶差分的平稳性检验结果均小于1%的置信度，说明有99%的把我可以拒绝原假设，即两者都满足一阶单整。
(-16.07399351198351, 5.46824765220884e-29, 0, 183, {'1%': -3.466598080268425, '5%': -2.8774669520682674, '10%': -2.5752604356654425}, -179.22489140848012)
(-7.912525574589352, 3.913380211621035e-12, 3, 180, {'1%': -3.4672111510631, '5%': -2.877734766803841, '10%': -2.575403364197531}, -117.76511431240539)
"""
from statsmodels.tsa.stattools import coint

# 协整性检验
print("协整性检验", coint(df["close"], df_1["close"]))
"""
输出结果如下，其返回值分别代表协整性检验的统计值、p-value，以及检验统计值对应的1%、5%和10%置信度下的临界值。可以看到检验统计值-3.39小于5%置信度下的
临界值，并且p-value小于0.05，说明有95%的把握可以拒绝原假设，即两者在一定程度上具有协整关系。
(-3.3939566995972332, 0.043026143216191026, array([-3.95695148, -3.3695386 , -3.06758034]))
"""
