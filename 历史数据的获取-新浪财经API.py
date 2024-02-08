"""
通过一些财经门户网站的接口API获取历史数据，常用的有新浪财经API，雅虎财经API，网易财经API等
"""
import requests
import pandas as pd


# 新浪接口获取股票数据
def get_stock_data(id, scale, data_len):
    """
    id: 股票代码，如sh000001
    scale: 5、15、30、60,代表数据为相应数字的分钟间隔
    data_len: 数据条数，经测试，最大为1970，否则接口失效
    """
    r = requests.get(
        "http://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol={0}&scale={1}&datalen={2}".format(
            id, scale, data_len
        )
    )
    df = pd.DataFrame(r.json())
    df.rename(columns={"day": "date", "volume": "vol"}, inplace=True)
    return df


# 新浪接口获取期货数据
def get_future_data(id, scale):
    """
    id: 期货代码，如rb1910
    scale: 5、15、30、60,代表数据为相应数字的分钟间隔
    """
    r = requests.get(
        "http://stock2.finance.sina.com.cn/futures/api/json_v2.php/IndexService.getInnerFuturesMiniKLine{0}m?symbol={1}".format(
            scale, id
        )
    )
    row_indexs = ["date", "open", "high", "low", "close", "vol"]
    data = r.json()
    data.reverse()
    df = pd.DataFrame(data, columns=row_indexs)
    # df.rename(columns={"day": "date", "volume": "vol"}, inplace=True)
    return df


# 新浪接口获取股指期货数据
def get_cffex_future_data(id, scale):
    """
    id: 股指期货代码，如IF1908
    scale: 5、15、30、60,代表数据为相应数字的分钟间隔
    """
    r = requests.get(
        "http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFuturesMiniKLine{0}m?symbol={1}".format(
            scale, id
        )
    )
    row_indexs = ["date", "open", "high", "low", "close", "vol"]
    data = r.json()
    data.reverse()
    df = pd.DataFrame(data, columns=row_indexs)
    # df.rename(columns={"day": "date", "volume": "vol"}, inplace=True)
    return df


# print(get_future_data("rb1910", "5"))
# print(get_stock_data("sh000001", 5, 5))
# print(get_cffex_future_data("IF1908", 5))
