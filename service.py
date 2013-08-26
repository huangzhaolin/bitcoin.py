__author__ = 'zhaolin.huang'
import MySQLdb as mysql

cnn=mysql.connect(host="jolinhuang.com",user="root",passwd="5527193",db="bitcoin")
cursor=cnn.cursor()

class BitCoinTrade(object):
    def __init__(self,parameters):
        for (key,value) in dict(parameters):
            self.__dict__[key]=value

def trades(startTime,endTime,orignal):
    cursor.execute("select id,date_time,price,num,trade_id,trade_num from trade_data where date_time >= '%(startTime)s' \ "
                   "and date_time <='%(endTime)s' and orignal = '%(orignal)s'"%{"startTime":startTime,"endTime":endTime,"orignal":orignal})
    return [zip(("id","date_time","price,num","trade_id","trade_num" ),trade) for trade in cursor.fetchall]



