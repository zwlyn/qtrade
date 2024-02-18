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

# random.seed(2)


class TestStrategy:
    def __init__(self):
        self.fromdate = datetime(2000, 1, 1)
        self.todate = datetime(2023, 12, 30)
        self.cash = 100000
        self.stake = 100  # 每笔交易使用的固定交易量
        self.stock_num = 100  # 测试使用的股票数目
        self.doPlot = False

    def runStrategy(self, dataPath, strategy):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(strategy)
        # 设置佣金为0.001,除以100去掉%号
        cerebro.broker.setcommission(commission=0.001)
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
            cerebro.plot()
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


class K线组合型量化策略(bt.Strategy):
    # 策略名称
    name = "K线组合型量化策略"

    def __init__(self):
        # 是否打印
        self.doPrint = False
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中open的数据列表
        self.dataopen = self.datas[0].open
        # 获取数据中low的数据列表
        self.datalow = self.datas[0].low
        # 获取数据中high的数据列表
        self.datahigh = self.datas[0].high
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        self.stopLossPrice = None

    def next(self):
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        # if self.doPrint:
        #     print(trade_date, "[Close]", close_price)
        self.K线组合型量化策略()

    def downSignal(self):
        """当第五根阴线收盘于前四根上升趋势K线实体下方，则进场追空,止损为5根k线的最高点"""
        close_price_5 = self.dataclose[0]
        open_price_5 = self.dataopen[0]
        close_price_4 = self.dataclose[-1]
        open_price_4 = self.dataopen[-1]
        close_price_3 = self.dataclose[-2]
        open_price_3 = self.dataopen[-2]
        close_price_2 = self.dataclose[-3]
        open_price_2 = self.dataopen[-3]
        close_price_1 = self.dataclose[-4]
        open_price_1 = self.dataopen[-4]
        up_4 = (
            close_price_4 > close_price_3 > close_price_2 > close_price_1
            or close_price_4 > close_price_2 > close_price_3 > close_price_1
        )
        k5_close_min = close_price_5 < np.min(
            [
                open_price_5,
                close_price_4,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
                open_price_1,
            ]
        )
        k4_close_max = close_price_4 > np.max(
            [
                close_price_5,
                open_price_5,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
                open_price_1,
            ]
        )
        k1_open_min = open_price_1 < np.min(
            [
                close_price_4,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
            ]
        )
        k1_close_min = close_price_1 < np.min(
            [
                close_price_4,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
            ]
        )
        if k5_close_min and up_4:  # and k4_close_max and k1_open_min and k1_close_min:
            self.stopLossPrice = np.max(
                [
                    self.datahigh[0],
                    self.datahigh[-1],
                    self.datahigh[-2],
                    self.datahigh[-3],
                    self.datahigh[-4],
                ]
            )
            return True
        return False

    def upSignal(self):
        """当第五根阳线收盘于前4根下跌趋势K线实体上方，则进场追多，止损为5根K线的最低点"""
        close_price_5 = self.dataclose[0]
        open_price_5 = self.dataopen[0]
        close_price_4 = self.dataclose[-1]
        open_price_4 = self.dataopen[-1]
        close_price_3 = self.dataclose[-2]
        open_price_3 = self.dataopen[-2]
        close_price_2 = self.dataclose[-3]
        open_price_2 = self.dataopen[-3]
        close_price_1 = self.dataclose[-4]
        open_price_1 = self.dataopen[-4]
        down_4 = (
            close_price_4 < close_price_3 < close_price_2 < close_price_1
            or close_price_4 < close_price_2 < close_price_3 < close_price_1
        )
        k5_close_max = close_price_5 > np.max(
            [
                open_price_5,
                close_price_4,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
                open_price_1,
            ]
        )
        k4_close_min = close_price_4 < np.min(
            [
                close_price_5,
                open_price_5,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
                open_price_1,
            ]
        )
        # k1 open除了k5close，比其他都大
        k1_open_max = open_price_1 > np.max(
            [
                open_price_5,
                close_price_4,
                open_price_4,
                close_price_3,
                open_price_3,
                close_price_2,
                open_price_2,
                close_price_1,
            ]
        )
        if k5_close_max and down_4:  # and k4_close_min and k1_open_max:
            self.stopLossPrice = np.min(
                [
                    self.datalow[0],
                    self.datalow[-1],
                    self.datalow[-2],
                    self.datalow[-3],
                    self.datalow[-4],
                ]
            )
            return True
        return False

    def K线组合型量化策略(self):
        """如果K线收盘价出现三连跌，则买入
        如果已经持仓，并且当前交易数据量在买入后5个单位后，则卖出"""
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        if self.position and self.downSignal():
            self.order = self.sell()
            if self.doPrint:
                print(trade_date, "卖出：", today_colse_price)
        elif not self.position and self.upSignal():
            self.order = self.buy()
            if self.doPrint:
                print(trade_date, "买入：", today_colse_price)
        else:
            # 止损策略
            """up:当第五根阳线收盘于前4根下跌趋势K线实体上方，则进场追多，止损为5根K线的最低点"""
            """down:当第五根阴线收盘于前四根上升趋势K线实体下方，则进场追空,止损为5根k线的最高点"""
            if not self.stopLossPrice:
                return
            if self.position and today_colse_price < self.stopLossPrice:
                self.order = self.sell()
                self.stopLossPrice = None
                # self.stopLossPrice = np.max(
                #     [
                #         self.datahigh[0],
                #         self.datahigh[-1],
                #         self.datahigh[-2],
                #         self.datahigh[-3],
                #         self.datahigh[-4],
                #     ]
                # )
                if self.doPrint:
                    print(trade_date, "止损卖出：", today_colse_price)
            elif not self.position and today_colse_price > self.stopLossPrice:
                self.order = self.buy()
                self.stopLossPrice = None
                # self.stopLossPrice = np.min(
                #     [
                #         self.datalow[0],
                #         self.datalow[-1],
                #         self.datalow[-2],
                #         self.datalow[-3],
                #         self.datalow[-4],
                #     ]
                # )
                if self.doPrint:
                    print(trade_date, "止损买入：", today_colse_price)

    def notify_order(self, order):
        """当执行订单操作时会执行该函数"""
        if order.status in [order.Submitted, order.Accepted]:
            # broker 提交/接受了，买/卖订单则什么都不做
            return

        # 检查一个订单是否完成
        # 注意: 当资金不足时，broker会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                if self.doPrint:
                    print(
                        "已买入, 价格: %.2f, 费用: %.2f, 佣金 %.2f"
                        % (
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm,
                        )
                    )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                if self.doPrint:
                    print(
                        "已卖出, 价格: %.2f, 费用: %.2f, 佣金 %.2f"
                        % (
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm,
                        )
                    )
            # 记录当前交易数量
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            if self.doPrint:
                print("订单取消/保证金不足/拒绝")

        # 其他状态记录为：无挂起订单
        self.order = None


test_strategy = TestStrategy()
# 双均线策略, 三连跌购买策略, RSI购买策略
test_strategy.compare([K线组合型量化策略])
