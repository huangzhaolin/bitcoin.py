#!/bin/env python
#coding=utf-8
'''
Created on 2013-7-19
@author: zhaolin.huang
收集bitcoin的交易数据
'''
import MySQLdb
import urllib
import json
import threading
import time

cnnPool =[MySQLdb.connect(host="localhost", user="root", passwd="5527193", db="bitcoin"),MySQLdb.connect(host="localhost", user="root", passwd="5527193", db="bitcoin"),MySQLdb.connect(host="localhost", user="root", passwd="5527193", db="bitcoin")]
URL={"trade":"http://info.btc123.com/lib/jsonProxyEx.php?type=btcchinaTrade2","buyAndSell":"http://info.btc123.com/lib/jsonProxyEx.php?type=btcchinaDepth","mtGox":"http://info.btc123.com/lib/jsonProxyEx.php?type=MtGoxTradesv2NODB"}
class TradeData(object):
     """docstring for TradeData"""
     datetime=""
     price=""
     num=""
     orignal=""
     trade_num=""
     trade_id=""
     def __init__(self, parameters):
          for key in dict(parameters).keys():
               self.__dict__[key]=dict(parameters).get(key)
     def insert_to_db(self,cnn):
          print "insert into trade_data(date_time,price,num,orignal,trade_num,trade_id) values('%s',%s,%s,'%s',%s,%s)"%(self.datetime,self.price,self.num,self.orignal,self.trade_num,self.trade_id)
          cnn.cursor().execute("insert into trade_data(date_time,price,num,orignal,trade_num,trade_id) values('%s',%s,%s,'%s',%s,%s)"%(self.datetime,self.price,self.num,self.orignal,self.trade_num,self.trade_id))
          cnn.commit()
class BaseData(object):
     """docstring for BaseData"""
     datetime=""
     price=""
     num=""
     def __init__(self, parameters):
          for key in dict(parameters).keys():
               self.__dict__[key]=dict(parameters).get(key)
class BuyData(BaseData):
     """docstring for BuyData"""
     def __init__(self, parameters):
          super(BuyData, self).__init__(parameters)
     def insert_to_db(self,cnn):
          cnn.cursor().execute("insert into buy_data(date_time,price,num) values('%s',%s,%s)"%(self.datetime,self.price,self.num))
          cnn.commit()
class SellData(BaseData):
     """docstring for SellData"""
     def __init__(self, parameters):
          super(SellData, self).__init__(parameters)
     def insert_to_db(self,cnn):
          #print("insert into sell_data(date_time,price,num) values('%s',%s,%s)"%(self.datetime,self.price,self.num))
          cnn.cursor().execute("insert into sell_data(date_time,price,num) values('%s',%s,%s)"%(self.datetime,self.price,self.num))
          cnn.commit()
class DataCollectorFactory(object):
     """docstring for DataCollectorFactory"""
     data_url=None
     data_type=None
     cnn=None
     def __init__(self, data_url,data_type,cnn):
          self.data_url=data_url
          self.data_type=data_type
          self.cnn=cnn
     def trade_data_handle(self,json_data,orignal="BITCCHINA"):
          cursor=self.cnn.cursor()
          cursor.execute("select max(trade_id) from trade_data where orignal='%s'"%orignal)
          max_trade_id=cursor.fetchone()[0]
          max_trade_id=max_trade_id if max_trade_id else 0
          for data in json_data:
               tradeData=TradeData(zip(["datetime","price","num","orignal","trade_num","trade_id"],[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data.get("date","")))),data.get("price",""),data.get("amount",0),\
                                                                                                    orignal,0,data.get("tid",0)]))
               if tradeData.trade_id==0 or int(max_trade_id) < int(tradeData.trade_id):
                    tradeData.insert_to_db(self.cnn)
     def buy_data_handle(self,json_data):
          for data in json_data:
               buyData=BuyData(zip(["datetime","price","num"],[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),data[0],data[1]]))
               buyData.insert_to_db(self.cnn)
     def sell_data_handle(self,json_data):
          for data in json_data:
               sellData=SellData(zip(["datetime","price","num"],[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),data[0],data[1]]))
               sellData.insert_to_db(self.cnn)
     def collect_data(self,orignal="BITCCHINA"):
          print orignal
          json_data=json.loads(list(urllib.urlopen(self.data_url))[0])
          if self.data_type == TradeData:
               self.trade_data_handle(json_data,orignal)
          if self.data_type == BuyData:
               self.buy_data_handle(json_data["asks"])
          if self.data_type==SellData:
               self.sell_data_handle(json_data["bids"])
if __name__ == "__main__":
    while True:
        threading.Thread(target=DataCollectorFactory(URL["trade"],TradeData,cnnPool[0]).collect_data()).start()
        #threading.Thread(target=DataCollectorFactory(URL["mtGox"],TradeData,cnnPool[0]).collect_data("MTGOX")).start()
        threading.Thread(target=DataCollectorFactory(URL["buyAndSell"],SellData,cnnPool[2]).collect_data()).start()
        threading.Thread(target=DataCollectorFactory(URL["buyAndSell"],BuyData,cnnPool[1]).collect_data()).start()
        time.sleep(20)
