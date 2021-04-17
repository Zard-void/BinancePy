from BinanceApi import *
import json
import pymysql
import time


class Trade:
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
        coinNum = self.freeCoinNum[coinKind]
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()
        prefix = coinKind + "USDT"
        kLineEnum = "15m"
        intervalSec = 15 * 60  # 秒
        leftSecForTrade = 10 #秒
        if lastTradeTime % intervalSec != 0:
            print("上次交易时间与间隔不符")
            return None
        self.waitForTrade(intervalSec, leftSecForTrade)
        t = round(time.time())
        leftSec = t % intervalSec
        while(leftSec < leftSecForTrade and leftSec > 0):
            t = round(time.time())
            leftSec = t % intervalSec
            response = self.bApi.Kline(symbol=prefix, intervalSec=kLineEnum, startTime=str(t) + "000", limit="2")
            print(response)
            # kLineInfoList =
            # TODO

        tradeNum = tradeVolumn / curPrice  # 计算和实际会有差别，价格有波动



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

    def getLatest15Min(self):
        t = round(time.time())  # 秒
        latestTime = t - (t % (15 * 60))
        print(latestTime)

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