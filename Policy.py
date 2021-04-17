import pymysql
import json
import UpdateDataBase as upDB
import math

class Policy:

    def policy_03(self, startTime, endTime, prefix):
        suffix = "15MIN"
        tableName = prefix + suffix
        coinKind = self.getCoinKind(prefix)
        status = self.policyPrepare(prefix, suffix, tableName, coinKind)
        if status == False:
            print("交易终止")
            return
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        startId = self.getStartId(cursor, startTime, tableName)
        endId = self.getEndId(cursor, endTime, tableName)
        if startId == None or endId == None:
            return

        curId = startId
        preId = curId - 1
        while curId != endId:
            sql = "SELECT * FROM " + tableName + " where id=" + str(preId)
            cursor.execute(sql)
            preKInfoList = cursor.fetchall()
            sql = "SELECT * FROM " + tableName + " where id=" + str(curId)
            cursor.execute(sql)
            curKInfoList = cursor.fetchall()
            if len(preKInfoList) == 1 and len(curKInfoList) == 1:
                preBeginPrice = preKInfoList[0][5]
                preEndPrice = preKInfoList[0][6]
                curBeginPrice = curKInfoList[0][5]
                if preBeginPrice > preEndPrice:
                    if self.coinNum[coinKind] > 0:
                        self.sell(coinKind, curBeginPrice, tradeNum)
                        print("Sell")
                else:
                    if self.coinNum[coinKind] == 0:
                        tradeNum = math.floor(self.totalMoney[coinKind] / curBeginPrice)
                        self.buy(coinKind, curBeginPrice, tradeNum)
                        print("Buy")
            else:
                print("逻辑错误")

            curTotalPrice = self.coinNum[coinKind] * curBeginPrice + self.usableMoney[coinKind]
            self.totalMoney[coinKind] = curTotalPrice
            print("持仓" + str(self.coinNum[coinKind]) + "开盘价格：" + str(curBeginPrice) + "场内资产" + str(
                curBeginPrice * self.coinNum[coinKind]) + "可用资金：" + str(
                self.usableMoney[coinKind]) + "当前总价值：" + str(curTotalPrice))
            curId = curId + 1
            preId = preId + 1

    def policy_02(self, startTime, endTime, prefix, tradeNum):
        suffix = "15MIN"
        tableName = prefix + suffix
        coinKind = self.getCoinKind(prefix)
        status = self.policyPrepare(prefix, suffix, tableName, coinKind)
        if status == False:
            print("交易终止")
            return

        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        startId = self.getStartId(cursor, startTime, tableName)
        endId = self.getEndId(cursor, endTime, tableName)
        if startId == None or endId == None:
            return


        curId = startId
        preId = curId - 1
        while curId != endId:
            sql = "SELECT * FROM " + tableName + " where id=" + str(preId)
            cursor.execute(sql)
            preKInfoList = cursor.fetchall()
            sql = "SELECT * FROM " + tableName + " where id=" + str(curId)
            cursor.execute(sql)
            curKInfoList = cursor.fetchall()
            if len(preKInfoList) == 1 and len(curKInfoList) == 1:
                preBeginPrice = preKInfoList[0][5]
                preEndPrice = preKInfoList[0][6]
                curBeginPrice = curKInfoList[0][5]
                if preBeginPrice > preEndPrice:
                    if self.coinNum[coinKind] > 0:
                        self.sell(coinKind, curBeginPrice, tradeNum)
                        self.sell(coinKind, curBeginPrice, tradeNum)
                        print("Sell")
                    elif self.coinNum[coinKind] == 0:
                        self.sell(coinKind, curBeginPrice, tradeNum)
                        print("Sell")
                else:
                    if self.coinNum[coinKind] == 0:
                        self.buy(coinKind, curBeginPrice, tradeNum)
                        print("Buy")
                    elif self.coinNum[coinKind] < 0:
                        self.buy(coinKind, curBeginPrice, tradeNum)
                        self.buy(coinKind, curBeginPrice, tradeNum)
                        print("Buy")

            else:
                print("逻辑错误")

            curTotalPrice = self.coinNum[coinKind] * curBeginPrice + self.usableMoney[coinKind]
            self.totalMoney[coinKind] = curTotalPrice
            print("持仓" + str(self.coinNum[coinKind]) + "开盘价格：" + str(curBeginPrice) + "可用资金：" + str(
                self.usableMoney[coinKind]) + "当前总价值：" + str(curTotalPrice))
            curId = curId + 1
            preId = preId + 1

    '''
    前15分钟涨，买入，前15分钟跌，卖出
    '''
    def policy_01(self, startTime, endTime, prefix, tradeNum):
        suffix = "15MIN"
        tableName = prefix + suffix
        coinKind = self.getCoinKind(prefix)
        status = self.policyPrepare(prefix, suffix, tableName, coinKind)
        if status == False:
            print("交易终止")
            return

        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        startId = self.getStartId(cursor, startTime, tableName)
        endId = self.getEndId(cursor, endTime, tableName)
        if startId == None or endId == None:
            return

        curId = startId
        preId = curId - 1
        while curId != endId:
            sql = "SELECT * FROM " + tableName + " where id=" + str(preId)
            cursor.execute(sql)
            preKInfoList = cursor.fetchall()
            sql = "SELECT * FROM " + tableName + " where id=" + str(curId)
            cursor.execute(sql)
            curKInfoList = cursor.fetchall()
            if len(preKInfoList) == 1 and len(curKInfoList) == 1:
                preBeginPrice = preKInfoList[0][5]
                preEndPrice = preKInfoList[0][6]
                curBeginPrice = curKInfoList[0][5]
                if preBeginPrice > preEndPrice:
                    if self.coinNum[coinKind] > 0:
                        self.sell(coinKind, curBeginPrice, tradeNum)
                        print("Sell")
                else:
                    if self.coinNum[coinKind] == 0:
                        self.buy(coinKind, curBeginPrice, tradeNum)
                        print("Buy")
            else:
                print("逻辑错误")

            curTotalPrice = self.coinNum[coinKind] * curBeginPrice + self.usableMoney[coinKind]
            self.totalMoney[coinKind] = curTotalPrice
            print("持仓" + str(self.coinNum[coinKind]) + "开盘价格：" + str(curBeginPrice) + "可用资金：" + str(self.usableMoney[coinKind]) +"当前总价值：" + str(curTotalPrice))
            curId = curId + 1
            preId = preId + 1



    def sell(self,coinKind, currentPrice, sellNum):
        coinNumAferTrade = self.coinNum[coinKind] - sellNum
        coinValueAfterTrade = coinNumAferTrade * currentPrice
        feesForTrade = self.fees[coinKind]  # 预留手续费算法
        usableMoneyAfterTrade = self.usableMoney[coinKind] + sellNum * currentPrice - feesForTrade
        # if coinNumAferTrade < 0 or coinValueAfterTrade < 0 or feesForTrade < 0 or usableMoneyAfterTrade < 0:
        if usableMoneyAfterTrade < 0:
            print("卖出失败！")
            print("当前交易币：" + coinKind)
            print("交易后持币数量：" + str(coinNumAferTrade))
            print("交易后场内资产：" + str(coinValueAfterTrade))
            print("交易所需手续费：" + str(feesForTrade))
            print("交易后可用资金：" + str(usableMoneyAfterTrade))
            return False
        else:
            self.coinNum[coinKind] = coinNumAferTrade
            self.coinValue[coinKind] = coinValueAfterTrade
            self.usableMoney[coinKind] = usableMoneyAfterTrade
            self.totalMoney[coinKind] = self.coinValue[coinKind] + self.usableMoney[coinKind]
            return True

    def buy(self,coinKind, currentPrice, buyNum):
        coinNumAferTrade = self.coinNum[coinKind] + buyNum
        coinValueAfterTrade = coinNumAferTrade * currentPrice
        feesForTrade = self.fees[coinKind]  # 预留手续费算法
        usableMoneyAfterTrade = self.usableMoney[coinKind] - buyNum * currentPrice - feesForTrade
        # if coinNumAferTrade < 0 or coinValueAfterTrade < 0 or feesForTrade < 0 or usableMoneyAfterTrade < 0:
        if usableMoneyAfterTrade < 0:
            print("买入失败！")
            print("当前交易币：" + coinKind)
            print("交易后持币数量：" + str(coinNumAferTrade))
            print("交易后场内资产：" + str(coinValueAfterTrade))
            print("交易所需手续费：" + str(feesForTrade))
            print("交易后可用资金：" + str(usableMoneyAfterTrade))
            return False
        else:
            self.coinNum[coinKind] = coinNumAferTrade
            self.coinValue[coinKind] = coinValueAfterTrade
            self.usableMoney[coinKind] = usableMoneyAfterTrade
            self.totalMoney[coinKind] = self.coinValue[coinKind] + self.usableMoney[coinKind]
            return True

    def getStartId(self, cursor, startTime, tableName):
        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(startTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            startId = kInfoList[0][0]
        else:
            startId = None
            print("获取信息错误")
            print("开始时间：" + str(startTime))
        return startId

    def getEndId(self, cursor, endTime, tableName):
        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(endTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            endId = kInfoList[0][0]
            # print(endId)
        else:
            endId = None
            print("获取信息错误")
            print("结束时间：" + str(endTime))
        return endId

    def policyPrepare(self, prefix, suffix, tableName, coinKind):
        if not prefix in upDB.UpdateDataBase().prefixMap.values():
            print("交易错误-前缀不存在")
            return False
        if not suffix in upDB.UpdateDataBase().suffixMap.values():
            print("交易错误-后缀不存在")
            return False
        if not upDB.UpdateDataBase().isTableCreated(tableName):
            print("交易错误-数据表未创建")
            return False
        self.initArguments(coinKind)
        return True

    def getCoinKind(self, prefix):
        coinKind = prefix.split("USDT")[0]
        return coinKind

    def initArguments(self, coinKind):
        print("coinKind:" + coinKind)
        self.coinNum[coinKind] = 0
        self.coinValue[coinKind] = 0
        self.usableMoney[coinKind] = 60000000
        self.totalMoney[coinKind] = 60000000
        self.fees[coinKind] = 0

    def __init__(self):
        self.coinNum = {}
        self.coinValue = {}
        self.usableMoney = {}
        self.fees = {}
        self.totalMoney = {}
        self.coinNum["BNB"] = 0
        self.coinValue["BNB"] = 0
        self.usableMoney["BNB"] = 1000
        self.totalMoney["BNB"] = 1000
        self.fees["BNB"] = 0
        pass