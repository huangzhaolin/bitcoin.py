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
        searchdata=self.cursor.execute("select date_time,price,num from trade_data where orignal='%s' and date_time>'%s'"%(self.orignal,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-15))))
        return [ dict(zip(("date_time,price,num"),row)) for row in searchdata.fetchall() ]
    def sendAlarm(self,**message):
        cmd="echo %(message)s | mail -s %(subject)s 228939139@163.com"
        os.system(cmd%message)
    def hanlde(self):
        alarmData=self.searchData()
        alarmMessage=[]
        if len(alarmData)>10:
            alarmData.append("trade count this 15 seconds > 10 it's:%s"%len(alarmData))
        moreThan10=[]
        for data in alarmData:
            if dict(data).get("num")>10:
                moreThan10.append("price is :%(price)s num is:%(num)s"%dict(data))
        if len(moreThan10) > 0:
            alarmData.append("num > 10 \n :%s"%"\n".join(moreThan10))
        lowest=0
        hightest=0
        for data in alarmData:
            rowData=dict(data)
            if lowest==0 and hightest==0:
                lowest=rowData.get("price")
                hightest=rowData.get("price")
                continue
            if rowData.get("price") < lowest:
                lowest=rowData.get("price")
            if rowData.get("price") > hightest:
                hightest=rowData.get("price")
        if hightest-lowest > 1.5:
            alarmData.append("high - low is >1.5 high is :%s and low is : %s"%(hightest,lowest))
        self.sendAlarm({"subject":"bitcoin trade alarm","message":"\n".join(alarmData)})

if __name__=="__main__":
    import threading
    while True:
        threading.Thread(target=Alarm("BITCCHINA").hanlde).start()
        time.sleep(15)


