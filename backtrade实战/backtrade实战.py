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
        self.fromdate = datetime(2023, 6, 1)
        self.todate = datetime(2023, 12, 30)
        self.cash = 100000
        self.stake = 3000  # 每笔交易使用的固定交易量
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


class 双均线策略(bt.Strategy):
    """
    框架在调用init时，该策略已经具有一个数据列表datas,
    这是标准的python列表，可以按插入顺序访问数据。列表中
    的第一个数据self.datas[0]是用于交易操作，并且策略中的
    所有元素都是由框架的系统时钟同步的。由于只需要访问收盘
    价数据，于是使用self.dataclose=self.datas[0].close将
    第一条价格数据的收盘价赋值给新变量。系统时钟当经过一个K
    线柱的时候，策略的next()方法就会被调用一次。这个一过程
    将一直循环，直到其他指标信号出现为止。此时，便会输出最终
    结果。
    """

    # 策略名称
    name = "双均线策略"

    def __init__(self):
        # 是否打印
        self.doPrint = False
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        # 双均线策略相关指标计算
        self.ma10_df = talib.MA(np.array(list(self.datas[0].close)), timeperiod=10)
        self.ma20_df = talib.MA(np.array(list(self.datas[0].close)), timeperiod=20)

        # # 绘制图形时候用到的指标
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

    def next(self):
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.双均线策略()

    def 双均线策略(self):
        index = len(self) - 1
        if index < 20:
            return
        # 价格序列平移
        MA10 = self.ma10_df[index]
        MA20 = self.ma20_df[index]
        if MA10 >= MA20 and not self.position:
            self.buy()
        elif MA10 < MA20 and self.position:
            self.sell()

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


class 三连跌购买策略(bt.Strategy):
    """
    框架在调用init时，该策略已经具有一个数据列表datas,
    这是标准的python列表，可以按插入顺序访问数据。列表中
    的第一个数据self.datas[0]是用于交易操作，并且策略中的
    所有元素都是由框架的系统时钟同步的。由于只需要访问收盘
    价数据，于是使用self.dataclose=self.datas[0].close将
    第一条价格数据的收盘价赋值给新变量。系统时钟当经过一个K
    线柱的时候，策略的next()方法就会被调用一次。这个一过程
    将一直循环，直到其他指标信号出现为止。此时，便会输出最终
    结果。
    """

    # 策略名称
    name = "三连跌购买策略"

    def __init__(self):
        # 是否打印
        self.doPrint = False
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None

    def next(self):
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.三连跌购买策略()

    def 三连跌购买策略(self):
        """如果K线收盘价出现三连跌，则买入
        如果已经持仓，并且当前交易数据量在买入后5个单位后，则卖出"""
        # 如果没有持仓则买入
        if not self.position:
            trade_date = self.datas[0].datetime.date(0)
            today_colse_price = self.dataclose[0]
            yestoday_close_price = self.dataclose[-1]
            before_yestoday_close_price = self.dataclose[-2]
            if (
                today_colse_price < yestoday_close_price
                and yestoday_close_price < before_yestoday_close_price
            ):
                self.order = self.buy()
                # 记录当前交易数量
                self.bar_executed = len(self)
                if self.doPrint:
                    print(trade_date, "买入：", today_colse_price)
        else:
            self.持有5天卖()

    def 持有5天卖(self):
        """如果已经持仓，并且当前交易数据量在买入后5个单位后，则卖出"""
        if len(self) >= (self.bar_executed + 5):
            if self.doPrint:
                print("卖出", self.dataclose[0])
            # 跟踪订单避免重复
            self.order = self.sell()

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


class RSI购买策略(bt.Strategy):
    # 策略名称
    name = "RSI购买策略"

    def __init__(self):
        # 是否打印
        self.doPrint = False
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        # 用于计算RSI指标的数组
        self.rsi6_array = np.zeros(7)

    def next(self):
        index = len(self) - 1
        if index < 6:
            return
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.RSI购买策略()

    def RSI购买策略(self):
        """如果未持仓且rsi6<=20，则买入
        如果已经持仓，并且rsi6 >= 80，则卖出"""
        # 价格序列平移
        self.rsi6_array[0:6] = self.rsi6_array[1:7]
        # 将新数据追加到数组末端
        self.rsi6_array[-1] = self.dataclose[0]
        # 计算RSI指标
        rsi6 = talib.RSI(self.rsi6_array, timeperiod=6)[-1]
        # 如果没有持仓则买入
        if not self.position and rsi6 <= 20:
            trade_date = self.datas[0].datetime.date(0)
            today_colse_price = self.dataclose[0]
            self.order = self.buy()
            # 记录当前交易数量
            self.bar_executed = len(self)
            if self.doPrint:
                print(trade_date, "买入：", today_colse_price)
        elif self.position and rsi6 >= 80:
            self.order = self.sell()
            if self.doPrint:
                print(trade_date, "卖出：", today_colse_price)

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


class 短线购买策略(bt.Strategy):
    # 策略名称
    name = "短线购买策略"

    def __init__(self):
        # 是否打印
        self.doPrint = True
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        # 用于计算RSI指标的数组
        self.rsi6_array = np.zeros(7)
        # 上次交易的股价
        self.lastPrice = None

    def next(self):
        index = len(self) - 1
        if index < 6:
            return
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.RSI购买策略()

    def RSI购买策略(self):
        """如果未持仓且rsi6<=20，则买入
        如果已经持仓，并且rsi6 >= 80，则卖出"""
        # 价格序列平移
        self.rsi6_array[0:6] = self.rsi6_array[1:7]
        # 将新数据追加到数组末端
        self.rsi6_array[-1] = self.dataclose[0]
        # 计算RSI指标
        rsi6 = talib.RSI(self.rsi6_array, timeperiod=6)[-1]
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        # 如果没有持仓则买入
        if not self.position and rsi6 <= 20:
            self.order = self.buy()
            self.lastPrice = today_colse_price
            # 记录当前交易数量
            self.bar_executed = len(self)
            if self.doPrint:
                print(trade_date, "买入：", today_colse_price)
        elif self.position and rsi6 >= 80:
            self.order = self.sell()
            if self.doPrint:
                print(trade_date, "卖出：", today_colse_price)
        else:
            self.止损策略()

    def 止损策略(self):
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        # 止损
        if (
            self.position
            and self.lastPrice
            and self.lastPrice * 0.95 > today_colse_price
        ):
            self.order = self.sell()
            self.lastPrice = None
            if self.doPrint:
                print(trade_date, "止损卖出：", today_colse_price)

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


class KDJ策略(bt.Strategy):
    # 策略名称
    name = "KDJ策略"

    def __init__(self):
        # 是否打印
        self.doPrint = True
        # 获取数据中close的数据列表
        self.dataclose = self.datas[0].close
        # 获取数据中volume的数据列表
        self.datavol = self.datas[0].volume
        # 跟踪挂单
        self.order = None
        # 用于计算RSI指标的数组
        self.rsi6_array = np.zeros(7)
        # 上次交易的股价
        self.lastPrice = None
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        self.rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(self.rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot=False)

    def next(self):
        index = len(self) - 1
        if index < 6:
            return
        trade_date = self.datas[0].datetime.date(0)
        close_price = self.dataclose[0]
        # 打印收盘价格
        if self.doPrint:
            print(trade_date, "[Close]", close_price)
        self.KDJ策略()

    def KDJ策略(self):
        """一般情况下K、D、J值都大于50则为多头市场，后期看涨；反之，如果K、D、J值都小于50，则为空头市场，后期看跌，
        但是，当KDJ值大于或小于一定范围容易出现钝化现象，也就是变化不明显，所以就需要结合其他指标进行分析。
        或者从三条线的关系上个来看，多头情况下，当J线大于K线，K线大于D线并出现金叉时，意味着上涨趋势，反之下跌"""
        print(list(self.datas[0]), "debug")
        # 价格序列平移
        self.rsi6_array[0:6] = self.rsi6_array[1:7]
        # 将新数据追加到数组末端
        self.rsi6_array[-1] = self.dataclose[0]
        # 计算RSI指标
        rsi6 = self.rsi[0]  # talib.RSI(self.rsi6_array, timeperiod=6)[-1]
        print(self.rsi[0], rsi6, "debug rsi")
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        # 如果没有持仓则买入
        if not self.position and rsi6 <= 20:
            self.order = self.buy()
            self.lastPrice = today_colse_price
            # 记录当前交易数量
            self.bar_executed = len(self)
            if self.doPrint:
                print(trade_date, "买入：", today_colse_price)
        elif self.position and rsi6 >= 80:
            self.order = self.sell()
            if self.doPrint:
                print(trade_date, "卖出：", today_colse_price)
        else:
            self.止损策略()

    def 止损策略(self):
        trade_date = self.datas[0].datetime.date(0)
        today_colse_price = self.dataclose[0]
        # 止损
        if (
            self.position
            and self.lastPrice
            and self.lastPrice * 0.95 > today_colse_price
        ):
            self.order = self.sell()
            self.lastPrice = None
            if self.doPrint:
                print(trade_date, "止损卖出：", today_colse_price)

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


class 金叉死叉策略(bt.Strategy):

    name = "金叉死叉策略"

    def log(self, txt, dt=None, doprint=False):
        """日志函数，用于统一输出日志格式"""
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):

        # 初始化相关数据
        self.dataclose = self.datas[0].close
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
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy()
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()

    def stop(self):
        self.log(
            "(金叉死叉有用吗) Ending Value %.2f" % (self.broker.getvalue()),
            doprint=True,
        )


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
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 五日移动平均线
        self.sma5 = bt.indicators.SimpleMovingAverage(self.datas[0], period=3)
        # 十日移动平均线
        self.sma10 = bt.indicators.SimpleMovingAverage(self.datas[0], period=12)

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
            if self.sma5[0] > self.sma10[0]:
                self.order = self.buy()
        else:
            # 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.sma5[0] < self.sma10[0]:
                self.order = self.sell()

    def stop(self):
        self.log(
            "Ending Value %.2f" % (self.broker.getvalue()),
            doprint=True,
        )


test_strategy = TestStrategy()
# 双均线策略, 三连跌购买策略, RSI购买策略
test_strategy.compare([ZW策略])
