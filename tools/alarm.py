#! /bin/env python2.7
__author__ = 'zhaolinhuang'
import  MySQLdb
import smtplib
import os
import time
class Alarm(object):
    dbCnn=MySQLdb.connect(host="localhost", user="root", passwd="5527193", db="bitcoin")
    cursor=dbCnn.cursor()
    def __init__(self,orignal):
        self.orignal=orignal
    def searchData(self):
        self.cursor.execute("select date_time,price,num from trade_data where orignal='%s' and date_time>'%s'"%(self.orignal,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-15))))
        return [ dict(zip(("date_time","price","num"),row)) for row in self.cursor.fetchall() ]
    def sendAlarm(self,**message):
        cmd="echo %(message)s | mail -s %(subject)s 228939139@163.com"
        os.system(cmd%message)
    def hanlde(self):
        alarmData=self.searchData()
        alarmMessage=[]
        if len(alarmData)>5:
            alarmMessage.append("trade count this 15 seconds > 5 it's:%s"%len(alarmData))
        moreThan10=[]
        for data in alarmData:
            if data.get("num")>10:
                moreThan10.append("price is :%(price)s num is:%(num)s"%data)
        if len(moreThan10) > 0:
            alarmMessage.append("num > 10 \n :%s"%"\n".join(moreThan10))
        lowest=0
        hightest=0
        for data in alarmData:
            if lowest==0 and hightest==0:
                lowest=data.get("price")
                hightest=data.get("price")
                continue
            if data.get("price") < lowest:
                lowest=data.get("price")
            if data.get("price") > hightest:
                hightest=data.get("price")
        if hightest-lowest > 1.5:
            alarmMessage.append("high - low is >1.5 high is :%s and low is : %s"%(hightest,lowest))
        if len(alarmMessage):
            print "\n".join(alarmMessage)
            self.sendAlarm(**{"subject":"bitcoin trade alarm","message":"\n".join(alarmMessage)})

if __name__=="__main__":
    import threading
    while True:
        threading.Thread(target=Alarm("BITCCHINA").hanlde).start()
        time.sleep(15)


