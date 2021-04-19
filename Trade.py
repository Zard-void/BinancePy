from BinanceApi import *
import json
import pymysql
import time


class Trade:
    # tradeVolumn 交易额，单位USDT，暂定10
    # lastTradeTime 上次交易时间，实际为上次交易时的最近时间点，例如11:21交易，则入参为11:15（15分钟为例）
    def tradeAsPolicy03(self, coinKind, tradeVolumn, lastTradeTime):
        if not self.testIsConnected():
            return None
        coinKindList = self.getAllCoinInfoInWallet()
        if coinKindList is None:
            return None
        if not(coinKind in coinKindList):
            print("当前交易币种有误")
            return None

        # lastTradeTime为0代表为首次交易，此时默认上次交易为最近的15Min，即当前时间所在K线已交易，等待下次K线进行再次交易
        if lastTradeTime == 0:
            lastTradeTime = self.getLatest15Min(time.time())
            # print(lastTradeTime)

        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()
        prefix = coinKind + "USDT"
        kLineEnum = "15m"
        intervalSec = 15 * 60  # 秒
        leftSecForTrade = 5 #秒
        if lastTradeTime % intervalSec != 0:
            print("上次交易时间与间隔不符")
            return None
        self.waitForTrade(intervalSec, leftSecForTrade)
        t = round(time.time())
        leftSec = intervalSec - t % intervalSec
        # 如果剩余时间在(0, leftSecForTrade)内，则未到下个周期，如果为0或从周期内最大值开始，则代表到达下个周期
        # 当前周期内始终循环获取时间，并获取最近一次的整点时刻(与K线有关)，退出循环代表进入下个周期，开始交易
        # 以lastTradeTime作为startTime，如果startTime为11：15，证明上次交易时间在11：30之前
        # 以lastTradeTime作为startTime，理论只能获取1个K线数据，如果获取到两个，证明已经到达下个周期
        # 在获取两个K线数据的情况下，检查第二个数据的开始时间，应该为lastTradeTime + 900
        # 检查剩余时间是否大于leftSecForTrade或等于0(因为非首次交易的话，此时应该是前一个周期刚结束，后一个周期刚开始)
        while(leftSec < leftSecForTrade + 1 and leftSec > 0):
            t = round(time.time())
            leftSec = intervalSec - t % intervalSec
            response = self.bApi.Kline(symbol=prefix, interval=kLineEnum, startTime=str(lastTradeTime) + "000", limit="2")
            # print(response)
            kLineInfoList = json.loads(response.text)
        # print("leftSec : " + str(leftSec))
        # print("curTime : " + str(time.time()))
        # t = int(round(time.time()))
        response = self.bApi.Kline(symbol=prefix, interval=kLineEnum, startTime=str(lastTradeTime) + "000", limit="2")
        kLineInfoList = json.loads(response.text)

        curBeginPrice = 0

        for kLineInfo in kLineInfoList:
            if kLineInfo[0] == lastTradeTime * 1000:
                preKLineInfo = kLineInfoList[0]
                preStartTime = int(preKLineInfo[0])
                preBeginPrice = float(preKLineInfo[1])
                preHighPrice = float(preKLineInfo[2])
                preLowPrice = float(preKLineInfo[3])
                preEndPrice = float(preKLineInfo[4])
                preQuantity = float(preKLineInfo[5])
                curBeginPrice = float(preEndPrice)

        # if len(kLineInfoList) != 1:
        #     print(response)
        #     print(len(kLineInfoList))
        #     print(json.loads(response.text))
        #     print("获取信息错误")
        # else:
        #     # timeArray = time.localtime(startTime)
        #     # date = "'" + time.strftime("%Y-%m-%d %H:%M:%S", timeArray) + "'"
        #     # # print(date)
        #     response = self.bApi.Kline(symbol=prefix, interval=kLineEnum, startTime=str(lastTradeTime) + "000", limit="2")
        #     kLineInfoList = json.loads(response.text)
        #     preKLineInfo = kLineInfoList[0]
        #     preStartTime = preKLineInfo[0]
        #     preBeginPrice = preKLineInfo[1]
        #     preHighPrice = preKLineInfo[2]
        #     preLowPrice = preKLineInfo[3]
        #     preEndPrice = preKLineInfo[4]
        #     preQuantity = preKLineInfo[5]
        #
        #     curKLineInfo = kLineInfoList[1]
        #     curStartTime = curKLineInfo[0]
        #     curBeginPrice = curKLineInfo[1]

        tradeNum = tradeVolumn / curBeginPrice
        tradeNum = float('%.2f' % tradeNum)

        response = self.bApi.testConnectivity()
        if (preBeginPrice >= preEndPrice):
            # 开始大于结束，下跌，卖
            coinNum = float(self.freeCoinNum[coinKind])
            coinNum =  self. cutFloat(coinNum, 2)
            if coinNum > 0:
                print("enterSell")
                print("当前时间:" + round(time.time()))
                response = self.bApi.newOrder(symbol=coinKind + "USDT", type="MARKET", side="SELL",
                                              quantity=str(coinNum), recvWindow="5000")
        else:
            #开始小于结束，上涨，买
            coinNum = float(self.freeCoinNum[coinKind])
            coinNum = self. cutFloat(coinNum, 2)
            if coinNum == 0:
                print("enterBuy")
                print("当前时间:" + round(time.time()))
                response = self.bApi.newOrder(symbol=coinKind + "USDT", type="MARKET", side="BUY",
                                              quantity=str(tradeNum), recvWindow="5000")

        print(json.loads(response.text))




        # tradeNum = tradeVolumn / curPrice  # 计算和实际会有差别，价格有波动

    def cutFloat(self, num, n):
         n = 10**(-n)
         return (num//n)*n

    '''
    makerCommission
    takerCommission
    buyerCommission
    sellerCommission
    canTrade
    canWithdraw
    canDeposit
    updateTime
    accountType
    balances
    permissions
    '''
    def getAllCoinInfoInWallet(self):
        if not self.testIsConnected():
            return None
        response = self.bApi.accountInformation(recvWindow="5000")
        infoList = json.loads(response.text)
        coinInfoList = infoList["balances"]
        for coinInfo in coinInfoList:
            coinKind = coinInfo["asset"]
            self.coinKind.append(coinKind)
            self.freeCoinNum[coinKind] = coinInfo["free"]
            self.lockedCoinNum[coinKind] = coinInfo["locked"]
        return self.coinKind


    def testIsConnected(self):
        response = self.bApi.testConnectivity()
        if json.loads(response.text) == {}:
            return True
        else:
            return False

    def getLatest15Min(self, t):
        latestTime = t - (t % (15 * 60))
        return int(latestTime)

    def waitForTrade(self, intervalSec, leftSecForTrade):
        t = round(time.time())
        timeToWait = intervalSec - t % intervalSec
        if timeToWait - leftSecForTrade > 0:
            time.sleep(timeToWait - leftSecForTrade)



    def __init__(self):
        self.bApi = BinanceApi()
        self.coinKind = []
        self.freeCoinNum = {}
        self.lockedCoinNum = {}