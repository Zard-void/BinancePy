import time
import hmac
import hashlib
import requests

class BinanceApi:

    """
    testConnectivity 测试能否联通
    Get方法
    """
    def testConnectivity(self):
        header = self.__header
        httpUrl = self.createUrl("testConnectivity")
        response = requests.get(headers=header, url=httpUrl)
        return response

    def checkServerTime(self):
        header = self.__header
        httpUrl = self.createUrl("checkServerTime")
        response = requests.get(headers=header, url=httpUrl)
        return response

    def exchangeInformation(self):
        header = self.__header
        httpUrl = self.createUrl("exchangeInformation")
        response = requests.get(headers=header, url=httpUrl)
        return response

    def orderBook(self, **kwargs):
        # kwargs["signature"] = self.getSignature()
        # kwargs["timestamp"] = self.__getTimeStamp()
        header = self.__header
        httpUrl = self.createUrl("orderBook", **kwargs)
        response = requests.get(headers=header, url=httpUrl)
        return response

    def createUrl(self, apiName, **kwargs):
        print(kwargs)
        self.setQueryString(**kwargs)
        queryString = self.getQueryString()
        print(queryString)
        if apiName in self.__apiDict:
            if not bool(kwargs):
                httpUrl = self.__binanceApiUrl + self.__apiDict[apiName]
            else:
                httpUrl = self.__binanceApiUrl + self.__apiDict[apiName] + "?" + queryString
            print(httpUrl)
            return httpUrl
        else:
            raise Exception("Invalid API")

    def getSignature(self):
        queryStringByte = str.encode(self.getQueryString())
        secretKeyByte = self.__secretKeyByte
        signature = str(hmac.new(secretKeyByte, queryStringByte, hashlib.sha256).hexdigest())
        return signature

    def getQueryString(self):
        return self.queryString

    """
    设置queryString的值，用于后续构造url
    kwargs : 动态参数，用于设置__argDict字典中的值
    """
    def setQueryString(self, **kwargs):
        self.__clearArgDict()
        self.queryString = ""
        self.queryStringByte = None
        for kwargsKey, kwargsValue in kwargs.items():
            # print("Key : {0}, Value : {1}".format(kwargsKey, kwargsValue))
            if kwargsKey in self.__argDict:
                self.__argDict[kwargsKey] = kwargsValue
            else:
                print("{0}参数setQueryString失败".format(kwargsKey))
        for argDictKey, argDictValue in self.__argDict.items():
            if argDictValue is not None:
                if self.queryString == "":
                    self.queryString = self.queryString + argDictKey + "=" + argDictValue
                else:
                    self.queryString = self.queryString + "&" + argDictKey + "=" + argDictValue

    @staticmethod
    def __getTimeStamp():
        t = time.time()
        timeStamp = int(round(t * 1000))
        return str(timeStamp)

    def __clearArgDict(self):
        self.__argDict["symbol"] = None
        self.__argDict["type"] = None
        self.__argDict["side"] = None
        self.__argDict["timeInForce"] = None
        self.__argDict["quantity"] = None
        self.__argDict["price"] = None
        self.__argDict["recvWindow"] = None
        self.__argDict["limit"] = None
        self.__argDict["signature"] = None
        self.__argDict["timestamp"] = None

    def __init__(self):
        # 初始化ApiKey和SecretKey
        self.f = open("D:\\CodingTools\\Secret\\Binance\\API.txt", "r+")
        data = self.f.read().splitlines()
        self.__apiKey = data[0]
        self.__apiKeyByte = str.encode(self.__apiKey)
        self.__secretKey = data[1]
        self.__secretKeyByte = str.encode(self.__secretKey)
        # self.__signature = None

        # 初始化时间戳，使用时获取
        # self.timeStamp = ""

        # 初始化queryString，使用时构造
        self.queryString = ""
        self.queryStringByte = None

        # 初始化http头
        self.__header = {'X-MBX-APIKEY': self.__apiKey}

        # 初始化币安API链接
        self.__binanceApiUrl = "https://api.binance.com"

        # 初始化参数字典
        self.__argDict = {}
        self.__clearArgDict()

        # 初始化API字典
        self.__apiDict = {}
        self.__apiDict["testConnectivity"] = "/api/v3/ping"  # 测试服务器连通性
        self.__apiDict["checkServerTime"] = "/api/v3/time"  # 获取服务器时间
        self.__apiDict["exchangeInformation"] = "/api/v3/exchangeInfo"  # 交易规范信息
        self.__apiDict["orderBook"] = "/api/v3/depth"  # 深度信息
        self.__apiDict["recentTradesList"] = "/api/v3/trades"  # 近期成交
        self.__apiDict["oldTradeLookup"] = "/api/v3/historicalTrades"  # 查询历史成交
        self.__apiDict["compressed"] = "/api/v3/aggTrades"  # 近期成交(归集)
        self.__apiDict["Kline"] = "/api/v3/klines"  # K线数据
        self.__apiDict["currentAveragePrice"] = "/api/v3/avgPrice"  # 当前平均价格
        self.__apiDict["24hrTickerPriceChangeStatistics"] = "/api/v3/ticker/24hr"  # 24hr价格变动情况
        self.__apiDict["symbolPriceTicker"] = "/api/v3/ticker/price"  # 最新价格接口
        self.__apiDict["symbolOrderBookTicker"] = "/api/v3/ticker/bookTicker"  # 最优挂单接口
        self.__apiDict["newOrder"] = "/api/v3/order"  # 下单
        self.__apiDict["testNewOrder"] = "/api/v3/order/test"  # 测试下单接口
        self.__apiDict["queryOrder"] = "/api/v3/order"  # 查询订单
        self.__apiDict["cancelOrder"] = "/api/v3/order"  # 撤销订单
        self.__apiDict["cancelAllOpenOrdersOnASymbol"] = "/api/v3/openOrders"  # 关闭账户当前挂单
        self.__apiDict["currentOpenOrders"] = "/api/v3/openOrders"  # 查看账户当前挂单
        self.__apiDict["allOrders"] = "/api/v3/allOrders"  # 查询所有订单（包括历史订单）
        self.__apiDict["newOCO"] = "/api/v3/order/oco"  # 下选择性委托订单
        self.__apiDict["cancelOCO"] = "/api/v3/orderList"  # 关闭OCO订单
        self.__apiDict["queryOCO"] = "/api/v3/orderList"  # 查询单条指定OCO订单
        self.__apiDict["queryAllOCO"] = "/api/v3/allOrderList"  # 查询所有指定OCO订单
        self.__apiDict["queryOpenOCO"] = "/api/v3/openOrderList"  # 查询当前进行总OCO订单
        self.__apiDict["accountInformation"] = "/api/v3/account"  # 账户信息
        self.__apiDict["accountTradeList"] = "/api/v3/myTrades"  # 账户成交历史
        """
        self.__apiDict["startUserDataStream"] = "/api/v3/userDataStream"  # 新建用户数据流
        self.__apiDict["keepaliveUserDataStream"] = "/api/v3/userDataStream"  # Keepalive
        self.__apiDict["closeUserDataStream"] = "/api/v3/userDataStream"  # 关闭用户数据流
        """



