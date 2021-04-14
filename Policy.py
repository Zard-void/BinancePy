import pymysql
import json

class Policy:

    def policy_02(self, startTime, endTime):
        prefix = "BNBUSDT"
        suffix = "15MIN"
        coinKind = "BNB"
        tableName = prefix + suffix

        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(startTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            startId = kInfoList[0][0]
            # print(startId)
        else:
            print("获取信息错误")
            print("开始时间：" + str(startTime))
            return
        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(endTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            endId = kInfoList[0][0]
            # print(endId)
        else:
            print("获取信息错误")
            print("结束时间：" + str(endTime))
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
                        self.sell(curBeginPrice)
                        self.sell(curBeginPrice)
                        print("Sell")
                    elif self.coinNum[coinKind] == 0:
                        self.sell(curBeginPrice)
                        print("Sell")
                else:
                    if self.coinNum[coinKind] == 0:
                        self.buy(curBeginPrice)
                        print("Buy")
                    elif self.coinNum[coinKind] < 0:
                        self.buy(curBeginPrice)
                        self.buy(curBeginPrice)
                        print("Buy")

            else:
                print("逻辑错误")

            curTotalPrice = self.coinNum[coinKind] * curBeginPrice + self.usableMoney[coinKind]
            print("持仓" + str(self.coinNum[coinKind]) + "开盘价格：" + str(curBeginPrice) + "可用资金：" + str(
                self.usableMoney[coinKind]) + "当前总价值：" + str(curTotalPrice))
            curId = curId + 1
            preId = preId + 1

    '''
    前15分钟涨，买入，前15分钟跌，卖出
    '''
    def policy_01(self, startTime, endTime):
        prefix = "BNBUSDT"
        suffix = "15MIN"
        coinKind = "BNB"
        tableName = prefix + suffix

        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(startTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            startId = kInfoList[0][0]
            # print(startId)
        else:
            print("获取信息错误")
            print("开始时间：" + str(startTime))
            return
        sql = "SELECT ID FROM " + tableName + " where startTime=" + str(endTime)
        cursor.execute(sql)
        kInfoList = cursor.fetchall()
        if len(kInfoList) == 1:
            endId = kInfoList[0][0]
            # print(endId)
        else:
            print("获取信息错误")
            print("结束时间：" + str(endTime))
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
                        self.sell(curBeginPrice)
                        print("Sell")
                else:
                    if self.coinNum[coinKind] == 0:
                        self.buy(curBeginPrice)
                        print("Buy")
            else:
                print("逻辑错误")

            curTotalPrice = self.coinNum[coinKind] * curBeginPrice + self.usableMoney[coinKind]
            print("持仓" + str(self.coinNum[coinKind]) + "开盘价格：" + str(curBeginPrice) + "可用资金：" + str(self.usableMoney[coinKind]) +"当前总价值：" + str(curTotalPrice))
            curId = curId + 1
            preId = preId + 1



    def sell(self, currentPrice):
        sellNum = 1
        coinKind = "BNB"
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

    def buy(self, currentPrice):
        buyNum = 1
        coinKind = "BNB"
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