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


class TestStrategy:
    def __init__(self):
        self.fromdate = datetime(2000, 1, 1)
        self.todate = datetime(2023, 12, 30)
        self.cash = 100000
        self.stake = 800  # 每笔交易使用的固定交易量
        self.stock_num = 1  # 测试使用的股票数目
        self.doPlot = True

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


class SVM策略(bt.Strategy):
    # 策略名称
    name = "SVM策略"

    def __init__(self):
        # 是否打印
        self.doPrint = True
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中open的数据列表
        self.dataopen = self.datas[0].open
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        # 用于训练SVM的数据
        self.data = []
        self.train_x = []
        self.label = []
        self.svm = SVC(kernel="linear")
        self.predict = -1
        self.records = []

    def next(self):
        index = len(self) - 1
        # 收集训练数据
        window_len = 20  # 滑动窗口大小
        self.data.append(self.dataclose[0])
        if (index + 1) > 21:
            self.train_x.append(self.data[-21:-1])
            if self.dataclose[0] - self.dataopen[0] > 0:
                self.label.append(1)
                if self.predict == 1:
                    self.records.append(1)
                elif self.predict == 0:
                    self.records.append(0)
            else:
                self.label.append(0)
                if self.predict == 0:
                    self.records.append(1)
                elif self.predict == 1:
                    self.records.append(0)
        if index < 3650:
            return
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.SVM策略(window_len)
        print(np.average(self.records))

    def SVM策略(self, window_len):
        """通过SVM训练预测"""
        # 实例化SVM模型
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        # 模型训练
        self.svm = SVC(kernel="linear")
        self.svm.fit(self.train_x, self.label)
        current_x = self.data[-window_len:]
        prediction = self.svm.predict([current_x])
        self.predict = prediction[0]
        print(prediction)
        if prediction[0] == 1 and not self.position:
            self.order = self.buy()
            if self.doPrint:
                print(trade_date, "买入：", today_colse_price)
        elif self.position and prediction[0] == 0:
            self.order = self.sell()
            if self.doPrint:
                print(trade_date, "卖出：", today_colse_price)


test_strategy = TestStrategy()
# 双均线策略, 三连跌购买策略, RSI购买策略
test_strategy.compare([SVM策略])
