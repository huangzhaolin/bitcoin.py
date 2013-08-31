__author__ = 'zhaolin.huang'
import MySQLdb as mysql
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import traceback

cnn=mysql.connect(host="localhost",user="root",passwd="5527193",db="bitcoin")
cursor=cnn.cursor()

def doSql(sql):
    log.debug(sql)
    cursor.execute(sql)

LOG_DIR="/home/log"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("filter")
fileTimeHandler = TimedRotatingFileHandler("%s/btc.log"%LOG_DIR, "D", 1)
fileTimeHandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"))
fileTimeHandler.suffix = "%Y-%m-%d.log"
log.addHandler(fileTimeHandler)

class BitCoinTrade(object):
    def __init__(self,parameters):
        for (key,value) in dict(parameters):
            self.__dict__[key]=value

def trades(startTime,endTime,orignal):
    try:
        doSql("select id,date_time,price,num,trade_id,trade_num from trade_data where date_time >= '%(startTime)s' "\
                       "and date_time <='%(endTime)s' and orignal = '%(orignal)s'"%{"startTime":startTime,"endTime":endTime,"orignal":orignal})
        return [zip(("id","date_time","price,num","trade_id","trade_num" ),trade) for trade in cursor.fetchall]
    except Exception:
        log.debug(traceback.format_exc())



