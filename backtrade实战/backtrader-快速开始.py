import datetime  #
import os.path  # 路径管理
import sys  # 获取当前运行脚本的路径 (in argv[0])

# 导入backtrader框架
import backtrader as bt


# 创建策略继承bt.Strategy
class TestStrategy(bt.Strategy):

    def __init__(self):
        # 保存收盘价的引用
        self.dataclose = self.datas[0].close

    def next(self):
        # 记录收盘价
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        print("Close,", close_price, trade_date)


# 创建Cerebro引擎
cerebro = bt.Cerebro()
# Cerebro引擎在后台创建broker(经纪人)，系统默认资金量为10000
# 为Cerebro引擎添加策略
cerebro.addstrategy(TestStrategy)
# 拼接加载路径
datapath = os.path.join("./orcl-1995-2014.txt")
# 创建交易数据集
data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    # 数据必须大于fromdate
    fromdate=datetime.datetime(2000, 1, 1),
    # 数据必须小于todate
    todate=datetime.datetime(2000, 12, 31),
    reverse=False,
)
# 加载交易数据

cerebro.adddata(data)
# 设置投资金额100000.0
cerebro.broker.setcash(100000.0)
# 引擎运行前打印期出资金
print("组合期初资金: %.2f" % cerebro.broker.getvalue())
cerebro.run()
# 引擎运行后打期末资金
print("组合期末资金: %.2f" % cerebro.broker.getvalue())
