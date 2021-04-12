from BinanceApi import *
import pymysql
import json

#1503014400000 2017年8月18日早8点
#1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
class UpdateDataBase:

    def updateAllTable(self):
        for kLineEnum, suffix in self.__suffixMap.items():
            for prefix, prefix in self.__prefixMap.items():
                self.updateTable(prefix + suffix)

    def updateTable(self):
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()


    def updateTable(self, tableName):
        if "BTCUSDT" in tableName:
            prefix = "BTCUSDT"
        elif "BNBUSDT" in tableName:
            prefix = "BNBUSDT"
        elif "ETHUSDT" in tableName:
            prefix = "ETHUSDT"
        else:
            print("数据库未建立")
            return
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM " + tableName + " WHERE id=1")
        except:
            print(tableName + "数据表不存在")
            cursor.close()
            conn.close()
            return
        isDatabaseEmpty = cursor.fetchone() is None
        for kLineEnum, suffix in self.__suffixMap.items():
            if tableName == prefix + suffix:
                if isDatabaseEmpty:
                    startTime = 1503014400
                else:
                    cursor.execute("SELECT * FROM " + tableName + " where id=(select max(id) from " + tableName + ")")
                    startTime = int(cursor.fetchone()[2])
                isLatestData = False
                while(not isLatestData):
                    bApi = BinanceApi()
                    response = bApi.Kline(symbol=prefix, interval=kLineEnum, startTime=str(startTime) + "000", limit="1000")
                    kInfoList = json.loads(response.text)
                    if len(kInfoList) > 1:
                        for kInfo in kInfoList:
                            existInTable = False
                            startTime = int(int(kInfo[0]) / 1000)
                            timeArray = time.localtime(startTime)
                            date = "'" + time.strftime("%Y-%m-%d %H:%M:%S", timeArray) + "'"
                            # print(date)
                            beginPrice = kInfo[1]
                            highPrice = kInfo[2]
                            lowPrice = kInfo[3]
                            endPrice = kInfo[4]
                            quantity = kInfo[5]
                            if kInfo == kInfoList[0]:
                                isFirstKLineInfo = True
                            else:
                                isFirstKLineInfo = False
                            if isFirstKLineInfo:
                                cursor.execute(
                                    "SELECT * FROM " + tableName + " where startTime=" + str(startTime))
                                existInTable = not (cursor.fetchone() is None)
                            if not existInTable:
                                sql = "INSERT INTO " + tableName + "(date, startTime, \
                                       highPrice, lowPrice, beginPrice, endPrice, quantity) \
                                       VALUES (%s, %d, %s, %s, %s, %s, %s)" % \
                                       (date, startTime, highPrice, lowPrice, beginPrice, endPrice, quantity)
                                cursor.execute(sql)
                                conn.commit()
                            else:
                                sql = "UPDATE " + tableName + " SET date=" + date + ", startTime=" + str(startTime) + \
                                      ", highPrice=" + highPrice + ", lowPrice=" + lowPrice + ", beginPrice=" + beginPrice + \
                                      ", endPrice=" + endPrice + ", quantity=" + quantity + " WHERE startTime=" + str(startTime)
                                cursor.execute(sql)
                                conn.commit()
                    elif len(kInfoList) == 1:
                        kInfo = kInfoList[0]
                        startTime = int(int(kInfo[0]) / 1000)
                        timeArray = time.localtime(startTime)
                        date = "'" + time.strftime("%Y-%m-%d %H:%M:%S", timeArray) + "'"
                        # print(date)
                        beginPrice = kInfo[1]
                        highPrice = kInfo[2]
                        lowPrice = kInfo[3]
                        endPrice = kInfo[4]
                        quantity = kInfo[5]
                        sql = "UPDATE " + tableName + " SET date=" + date + ", startTime=" + str(startTime) + \
                              ", highPrice=" + highPrice + ", lowPrice=" + lowPrice + ", beginPrice=" + beginPrice + \
                              ", endPrice=" + endPrice + ", quantity=" + quantity + " WHERE startTime=" + str(startTime)
                        # print(sql)
                        cursor.execute(sql)
                        conn.commit()

                        isLatestData = True
                    else:
                        print("sql查询有误")
                        isLatestData = True
        cursor.close()
        conn.close()

    def createTable(self, prefix):
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()

        for kLineEnum, suffix in self.__suffixMap.items():
            tableName = "`" + prefix + suffix + "`"
            sql = "CREATE TABLE IF NOT EXISTS " + tableName + " (\n"\
                + "`id` int(11) NOT NULL AUTO_INCREMENT,\n"\
                + "`date` varchar(100) NOT NULL,\n"\
                + "`startTime` int(11) NOT NULL,\n"\
                + "`highPrice` double(15,6) NOT NULL,\n"\
                + "`lowPrice` double(15,6) NOT NULL,\n"\
                + "`beginPrice` double(15,6) NOT NULL,\n"\
                + "`endPrice` double(15,6) NOT NULL,\n"\
                + "`quantity` double(15,6) NOT NULL,\n"\
                + "PRIMARY KEY (`id`)"\
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"
            cursor.execute(sql)
        cursor.close()  # 先关闭游标
        conn.close()  # 再关闭数据库连接

    def initSuffixMap(self):
        self.__suffixMap = {}
        self.__suffixMap["1m"] = "1MIN"
        self.__suffixMap["3m"] = "3MIN"
        self.__suffixMap["5m"] = "5MIN"
        self.__suffixMap["15m"] = "15MIN"
        self.__suffixMap["30m"] = "30MIN"
        self.__suffixMap["1h"] = "1HOUR"
        self.__suffixMap["2h"] = "2HOUR"
        self.__suffixMap["4h"] = "4HOUR"
        self.__suffixMap["6h"] = "6HOUR"
        self.__suffixMap["8h"] = "8HOUR"
        self.__suffixMap["12h"] = "12HOUR"
        self.__suffixMap["1d"] = "1DAY"
        self.__suffixMap["3d"] = "3DAY"
        self.__suffixMap["1w"] = "1WEK"
        self.__suffixMap["1M"] = "1MON"
        pass

    def initPrefixMap(self):
        self.__prefixMap = {}
        self.__prefixMap["BTCUSDT"] = "BTCUSDT"
        self.__prefixMap["BNBUSDT"] = "BNBUSDT"
        self.__prefixMap["ETHUSDT"] = "ETHUSDT"

    def __init__(self):
        self.initSuffixMap()
        self.initPrefixMap()
        self.createTable("BTCUSDT")
        self.createTable("BNBUSDT")
        self.createTable("ETHUSDT")
        pass
