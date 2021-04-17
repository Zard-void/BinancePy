import hmac
import hashlib
import time
import requests
import BinanceApi
from BinanceApi import *
import pymysql
from UpdateDataBase import *
from Policy import *
import json
from Trade import *
import datetime
import base64
from hashlib import sha256

if __name__ == "__main__":
    """
    apiKey API KEY 比特数组
    secretKey sercet KEY 比特数组
    
    queryString 交易信息 比特数组
    signature 签名，用于需要签名的API传输
    """

    # f = open("D:\\CodingTools\\Secret\\Binance\\API.txt", "r+")
    # print(f.readlines(1)[0])
    #
    #
    #
    # t = time.time()
    # apiKey = "a9T3mUmkMZh4ljSR4Pt0oFgSUDDEwj1C64ZKcsEH6UNzuUCPbVqeCRAguhF0dL1H"
    # apiKeyByte = str.encode(apiKey)
    # secretKey = "2GyGEi3YqRUkPgxSw2KgBH9o3QVO7ibc0nxv64WYbgQtB0dtduMWj1RZV5WCYdqG"
    # secretKeyByte = str.encode(secretKey)
    # # print(apiKey)
    # timeStamp = int(round(t * 1000))
    # # print(timeStamp)
    # queryString = "symbol=LTCBTC&type=LIMIT&side=BUY&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=" + str(timeStamp)
    # queryStringByte = str.encode(queryString)
    # # print(hashlib.sha256)
    # # print(hmac.new(secretKey, queryString, hashlib.sha256).hexdigest())
    # signature = hmac.new(secretKeyByte, queryStringByte, hashlib.sha256).hexdigest()
    #
    # header = {'X-MBX-APIKEY': apiKey}
    #
    # # print(header)
    # httpUrl = "https://api.binance.com/api/v3/order"
    # httpUrl = httpUrl + "?" + queryString + "&signature=" + str(signature)
    # # print(httpUrl)
    # response = requests.post(headers=header, url=httpUrl)
    #
    # # response = requests.get(url="https://api.binance.com/api/v1/exchangeInfo")
    # print(response.text)

    conn = pymysql.connect(host='localhost', user="root", passwd="123456", db="BINANCE")
    cursor = conn.cursor()
    print(cursor)

    # cursor.execute("show tables")
    # print(cursor.fetchall())

    # update = UpdateDataBase()
    # print(update.isTableCreated("BTCUSDT15MIN"))
    # update.createTable()
    # update.updateTable("BTCUSDT15MIN")
    # update.updateAllTable()

    policy = Policy()
    # policy.policy_03(1613088000, 1614384000, "BTCUSDT")

    bApi = BinanceApi()
    response = bApi.testConnectivity()
    # symbol = LTCBTC & type = LIMIT & side = BUY & timeInForce = GTC & quantity = 1 & price = 0.1 & recvWindow = 5000
    response = bApi.testNewOrder(symbol="BTCUSDT", type="LIMIT", side="BUY", timeInForce="GTC", quantity="1", price="100000", recvWindow="5000")
    response = bApi.accountInformation(recvWindow="5000")
    # print(response)
    infoList = json.loads(response.text)
    # print(infoList[1])
    for key in infoList:
        print(key)
        print(infoList[key])
        print("----")
    print(len(json.loads(response.text)["balances"]))
    # print(len(json.loads(response.text)))

    trade = Trade()
    print(trade.getLatest15Min())
    # print(trade.tradeAsPolicy03("BNB", 10))


