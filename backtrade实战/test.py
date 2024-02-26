from __future__ import absolute_import, division, print_function, unicode_literals

import backtrader as bt
from datetime import datetime
import pandas as pd
import backtrader.feeds as btfeeds
import talib
import os
import random
import numpy as np
from sklearn.svm import SVC

random.seed(1)


# class KDJ(bt.Indicator):
#     lines = ("K", "D", "J")
#     params = (("period", 9),)

#     def __init__(self):
#         self.high_nine = bt.indicators.Highest(self.data.high, period=9)
#         # 9个交易日内最低价
#         self.low_nine = bt.indicators.Lowest(self.data.low, period=9)
#         # 计算rsv值
#         self.rsv = 100 * bt.DivByZero(
#             self.data_close - self.low_nine, self.high_nine - self.low_nine, zero=None
#         )
#         # 计算rsv的3周期加权平均值，即K值
#         self.K = bt.indicators.EMA(self.rsv, period=3)
#         # D值=K值的3周期加权平均值
#         self.D = bt.indicators.EMA(self.K, period=3)
#         # J=3*K-2*D
#         self.J = 3 * self.K - 2 * self.D


class KDJ(bt.Indicator):
    lines = ("K", "D", "J")

    params = (
        ("period", 9),  # KDJ周期
        ("slow_period", 3),  # 慢速线周期
        ("smooth_d", 1),  # 平滑因子
    )

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        if len(self) < self.params.period:
            return

        highest_high = self.data.high.get(size=self.params.period)
        lowest_low = self.data.low.get(size=self.params.period)
        close = self.data.close[0]

        rsv = (close - lowest_low) / (highest_high - lowest_low) * 100

        # 计算K值
        if len(self) == self.params.period:
            self.lines.K[0] = 50  # 初始K值为50
        else:
            self.lines.K[0] = (
                self.lines.K[-1]
                * (self.params.slow_period - 1)
                / self.params.slow_period
                + rsv / self.params.slow_period
            )

        # 计算D值
        if len(self) == self.params.period + self.params.slow_period - 1:
            self.lines.D[0] = 50  # 初始D值为50
        else:
            self.lines.D[0] = (
                self.lines.D[-1] * (self.params.smooth_d - 1) / self.params.smooth_d
                + self.lines.K[0] / self.params.smooth_d
            )

        # 计算J值
        self.lines.J[0] = 3 * self.lines.K[0] - 2 * self.lines.D[0]


class 测试策略(bt.Strategy):
    # 策略名称
    name = "测试策略"
    params = (
        # 持仓够5个单位就卖出
        ("exitbars", 5),
    )

    def __init__(self):
        # 是否打印
        self.doPrint = False
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        self.high_nine = bt.indicators.Highest(self.data.high, period=9)
        # 9个交易日内最低价
        self.low_nine = bt.indicators.Lowest(self.data.low, period=9)
        # 计算rsv值
        self.rsv = 100 * bt.DivByZero(
            self.data_close - self.low_nine, self.high_nine - self.low_nine, zero=None
        )
        # 计算rsv的3周期加权平均值，即K值
        self.K = bt.indicators.EMA(self.rsv, period=3)
        # D值=K值的3周期加权平均值
        self.D = bt.indicators.EMA(self.K, period=3)
        # J=3*K-2*D
        self.J = 3 * self.K - 2 * self.D

        me1 = bt.indicators.EMA(self.data, period=12)
        me2 = bt.indicators.EMA(self.data, period=26)
        self.macd = me1 - me2
        self.signal = bt.indicators.EMA(self.macd, period=9)
        bt.indicators.MACDHisto(self.data)
        self.kdj = bt.indicators.KDJ()

    # 交易状态通知，一买一卖算交易
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        print("交易利润, 毛利润 %.2f, 净利润 %.2f" % (trade.pnl, trade.pnlcomm))

    def next(self):
        print(self.KDJ.K[0], self.KDJ.D[0], self.KDJ.J[0])
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.混合策略()

    def KDJ策略(self):
        """当K线突破D线为买进信号;K线跌破D线为卖出信号"""
        # 如果没有持仓则买入
        if not self.position:
            condition1 = self.K[-1] - self.D[-1]
            condition2 = self.K[0] - self.D[0]
            if not self.position:
                if condition1 < 0 and condition2 > 0:
                    print("BUY CREATE, %.2f" % self.dataclose[0])
                    self.order = self.buy()

            elif condition1 > 0 or condition2 < 0:
                print("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()

    def 混合策略(self):
        """基于MACD策略的买入信号进行买入，KDJ策略的卖出信号进行卖出"""
        if not self.position:
            # 买入基于MACD策略
            condition1 = self.macd[-1] - self.signal[-1]
            condition2 = self.macd[0] - self.signal[0]
            if condition1 < 0 and condition2 > 0:
                print("BUY CREATE, %.2f" % self.dataclose[0])
                self.order = self.buy()

        else:
            # 卖出基于KDJ策略
            condition1 = self.J[-1] - self.D[-1]
            condition2 = self.J[0] - self.D[0]
            if condition1 > 0 or condition2 < 0:
                print("SELL CREATE, %.2f" % self.dataclose[0])
                self.order = self.sell()


class ZW策略(bt.Strategy):

    name = "ZW策略"

    def log(self, txt, dt=None, doprint=False):
        """日志函数，用于统一输出日志格式"""
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):

        # 初始化相关数据
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 五日移动平均线
        self.sma5 = bt.indicators.SimpleMovingAverage(self.datas[0], period=5)
        # 十日移动平均线
        self.sma10 = bt.indicators.SimpleMovingAverage(self.datas[0], period=10)

    def notify_order(self, order):
        """
        订单状态处理

        Arguments:
            order {object} -- 订单状态
        """
        if order.status in [order.Submitted, order.Accepted]:
            # 如订单已被处理，则不用做任何事情
            return

        # 检查订单是否完成
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)

        # 订单因为缺少资金之类的原因被拒绝执行
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

        # 订单状态处理完成，设为空
        self.order = None

    def notify_trade(self, trade):
        """
        交易成果

        Arguments:
            trade {object} -- 交易状态
        """
        if not trade.isclosed:
            return

        # 显示交易的毛利率和净利润
        self.log(
            "OPERATION PROFIT, GROSS %.2f, NET %.2f" % (trade.pnl, trade.pnlcomm),
            doprint=True,
        )

    def next(self):
        """下一次执行"""

        # 记录收盘价
        self.log("Close, %.2f" % self.dataclose[0])

        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return

        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.sma5[0] > self.sma10[0] and self.sma5[-1] <= self.sma10[-1]:
                self.order = self.buy()
        elif self.position:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()
            # 止盈 7%
            elif (
                self.buyprice
                and ((self.dataclose[0] - self.buyprice) / self.buyprice) >= 0.07
            ):
                self.order = self.sell()
            # 止损 2%
            elif (
                self.buyprice
                and ((self.dataclose[0] - self.buyprice) / self.buyprice) <= -0.02
            ):
                self.order = self.sell()
            # 高位是一周内的最高（天）量卖出
            elif (
                len(self) > 7
                and self.datavol[0] > np.max(self.datavol.get(ago=-1, size=7)) * 1.5
                and self.dataclose[0] > np.max(self.dataclose.get(ago=-1, size=7))
            ):
                self.order = self.sell()
            # 量价格背离卖出
            elif (
                self.dataclose[0] > self.dataclose[-1]
                and self.datavol[0] < self.datavol[-1]
            ):
                self.order = self.sell()

    def stop(self):
        self.log(
            "Ending Value %.2f" % (self.broker.getvalue()),
            doprint=True,
        )


class TestStrategy:
    def __init__(self):
        self.fromdate = datetime(2023, 6, 1)
        self.todate = datetime(2023, 12, 30)
        self.cash = 100000
        self.stake = 2000  # 每笔交易使用的固定交易量
        self.stock_num = 1  # 测试使用的股票数目
        self.doPlot = True

    def runStrategy(self, dataPath, strategy):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy)
        # 设置佣金为0.001,除以100去掉%号
        cerebro.broker.setcommission(commission=0.005)
        print("Starting Portfolio value:", cerebro.broker.getvalue())
        df = pd.read_csv(dataPath)
        df.trade_date = pd.to_datetime(df.trade_date.apply(str))
        data = btfeeds.PandasData(
            dataname=df,
            fromdate=self.fromdate,
            todate=self.todate,
            datetime="trade_date",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="vol",
            openinterest=-1,
        )
        cerebro.adddata(data)
        cerebro.broker.setcash(self.cash)
        # 每笔交易使用固定交易量
        cerebro.addsizer(bt.sizers.FixedSize, stake=self.stake)
        cerebro.run()
        # 可视化:绘图
        if self.doPlot:
            cerebro.plot(
                style="candle",
                plotdist=0.1,  # 设置图形之间的间距
                barup="#ff9896",
                bardown="#98df8a",  # 设置蜡烛图上涨和下跌的颜色
                volup="#ff9896",
                voldown="#98df8a",  # 设置成交量在行情上涨和下跌情况下的颜色
            )
        print(
            "{} {} Final Portfolio value:".format(dataPath, strategy.name),
            cerebro.broker.getvalue(),
        )
        return cerebro.broker.getvalue()

    def random_stocks(self):
        filenames = os.listdir("./data")
        stock_choices = random.choices(filenames, k=self.stock_num)
        return ["./data/{}".format(filename) for filename in stock_choices]

    def compare(self, strategys):
        stock_choices = self.random_stocks()
        # {策略1:[股票1收益，股票2收益...], 策略2:[股票1收益，股票2收益...]}
        income_map = {}
        for strategy in strategys:
            income_map[strategy.name] = []
            for stock_path in stock_choices:
                income_map[strategy.name].append(self.runStrategy(stock_path, strategy))
        avg_map = {}
        for key, value in income_map.items():
            avg_map[key] = np.average(value)
        print("策略收益列表：", income_map)
        print("策略平均收益：", avg_map)


test_strategy = TestStrategy()
# 双均线策略, 三连跌购买策略, RSI购买策略
test_strategy.compare([ZW策略])
