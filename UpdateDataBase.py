from BinanceApi import *
import pymysql

#1503014400000 2017年8月18日早8点
#1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
class UpdateDataBase:

    def createTable(self):
        conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
        # 获取游标
        cursor = conn.cursor()
        print(cursor)

        suffixMap = {}
        suffixMap["1m"] = "1MIN"
        suffixMap["1d"] = "1DAY"
        suffixMap["1w"] = "1WEK"
        suffixMap["1M"] = "1MON"

        for kLineEnum, suffix in suffixMap.items():
            databaseName = "`" + "BTCUSDT" + suffix + "`"
            sql = "CREATE TABLE IF NOT EXISTS " + databaseName + " (\n"\
                + "`id` int(11) NOT NULL AUTO_INCREMENT,\n"\
                + "`startTime` varchar(255) NOT NULL,\n"\
                + "`high` double(15,6) NOT NULL,\n"\
                + "`low` double(15,6) NOT NULL,\n"\
                + "`begin` double(15,6) NOT NULL,\n"\
                + "`end` double(15,6) NOT NULL,\n"\
                + "`quantity` double(15,6) NOT NULL,\n"\
                + "PRIMARY KEY (`id`)"\
                + ") ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"

            cursor.execute(sql)
        cursor.close()  # 先关闭游标
        conn.close()  # 再关闭数据库连接
        print('创建数据表成功')

    def __init__(self):
        pass
