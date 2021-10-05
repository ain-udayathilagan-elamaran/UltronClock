import datetime
from datetime import datetime as df
import logging
import logging.config
import time
import os
import urllib.request
from time import ctime
import json
import threading
import ntplib

global FlagA
FlagA=0
logging.config.fileConfig('./log.conf')
logger = logging.getLogger()

def addSecs(tm, secs):
    try:
        New_Format=("%a %b %d %X %Y")
        tm =  df.strptime(tm, "%c")
        fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
        fulldate = fulldate + datetime.timedelta(seconds=secs)
        fuc=(fulldate.strftime(New_Format))
        return fuc
    except Exception as dfs:
        logger.error(dfs)

def read_from_file():
    try:   
        f = open("datetime.txt", "r")
        kc=f.read()
        f.close()
        filetim=kc.split()
        return kc
    except Exception as sd:
        logger.error(sd)

def write_on_file(data_To_Write):
    try:
        f = open("datetime.txt", "w")
        f.write(data_To_Write)
        f.close()
    except Exception as sd:
        logger.error(sd)
        DateTimeSetter(30)

def check_internet():
    try:
        urllib.request.urlopen('https://ipinfo.io/ip')
        Date_Time_Check()
    except Exception as d:
        logger.warning("No internet")
        logger.error(d)
        Read_and_update()

def Read_and_update():
    global FlagA
    try:    
        kc=read_from_file()
        os.system("sudo date -s '"+kc+"'")
        FlagA=2
        T1_writter(kc)
    except Exception as sd:
        logger.error(sd)

def Chenage_Time_From_File():
    global FlagA
    try:
        logger.warning("")
        kc=read_from_file()
        if kc.strip() == "":
            logger.error("datetime File  is emty")
        else :
            os.system("sudo date -s '"+kc+"'")
            T1_writter(kc)
            FlagA=2
    except Exception as sfd:
        logger.error(sfd)

def T1_writter(T1):
    try :
        change_log={
        "T1":T1 ,
        "T2":""
        }
        json_ob = json.dumps(change_log, indent = 4)
        with open("Change_log.json", "w") as outfile:
            outfile.write(json_ob)   
    except Exception as df:
        logger.warning(df)

def Date_Time_Check():
    try:
        client = ntplib.NTPClient()
        response = client.request('Asia.pool.ntp.org', version=4)
        ntptime=str(ctime(response.tx_time))
        res = os.popen('sudo date').read().strip()
        ntptim=ntptime.split()
        Rpitim=res.split()
        Nday=ntptim[0]
        Rday=Rpitim[0]
        Nmonth=ntptim[1]
        Rmonth=Rpitim[2]
        Ndate=ntptim[2]
        Rdate=Rpitim[1]
        Nyear=ntptim[4]
        Ryear=Rpitim[5]
        Ntime=ntptim[3]
        Rtime=Rpitim[3]
        if Ntime == Rtime and Nyear == Ryear and Nday == Rday and Ndate == Rdate and Nmonth == Rmonth:
            logger.warning("Ntp time and Rpi time are same ")
            write_on_file(ntptime)
        else :
            logger.warning("Time mismatch on Rpi")
            logger.warning("Time on Rpi:"+res)
            logger.warning("Time on NTP:"+ntptime)
            os.system("sudo date -s '"+ntptime+"'")
            write_on_file(ntptime) # Changed on  27/07/2021
    except Exception as df:
        logger.error(df)
 
def Get_Ntp_Time():
    tr =0
    while True:
        try:
            if tr > 3:
                break
            client = ntplib.NTPClient()
            response = client.request('Asia.pool.ntp.org', version=4)
            ntptime=str(ctime(response.tx_time))  
            return ntptime
        except Exception as df:
            tr=tr+1
            time.sleep(2)
            logger.error(df)

def DateTimeSetter(tim1):
    while True:
        time.sleep(tim1)
        try:
            urllib.request.urlopen('https://ipinfo.io/ip')
            client = ntplib.NTPClient()
            response = client.request('Asia.pool.ntp.org', version=4)
            ntptime=str(ctime(response.tx_time))
            write_on_file(ntptime)
            break
        except Exception as d:
            logger.error("No internet")

def Internet_came_After(tim1):
  global FlagA
  while True:
    if FlagA == 2: 
      time.sleep(tim1)
      try:
        urllib.request.urlopen('https://ipinfo.io/ip')
        ntpttime=Get_Ntp_Time()
        T2=read_from_file()
        T2_Checker(T2,ntpttime)
        write_on_file(ntpttime)
        change_log={
            "T1":"" ,
            "T2":""
              }
        json_ob = json.dumps(change_log, indent = 4)
        with open("Change_log.json", "w") as outfile:
          outfile.write(json_ob)
        FlagA=0
        break
      except Exception as d:
        logger.error("No internet")

def Change_log_Creater(Duration,From_Time,To_time,actual_From_Time,Ntp_time):
    try:
        kc1=("\n\t Duration is :{}\Log time was wrong From :{} To :{} \nActual Date time was     From :{} To :{}".format(Duration,From_Time,To_time,actual_From_Time,Ntp_time))
        f = open("Correction_time.txt", "a")
        f.write(str(kc1))
        f.close()
    except Exception as sd:
        logger.error(sd)
           
def T2_Checker(T2,Ntp_time):
  try:    
    fl = open('Change_log.json',)
    data = json.load(fl)
    fl.close()
    To_time=T2
    From_Time=(data["T1"])
    To_Time =  df.strptime(To_time, "%c")
    From_Time =  df.strptime(From_Time, "%c")
    delay_Is= To_Time - From_Time
    Duration=str(delay_Is)
    logger.warning("Duration is :"+Duration)
    current_Time=df.strptime(Ntp_time,"%c")
    actual_From_Time=current_Time - delay_Is
    Change_log_Creater(Duration=Duration, From_Time=From_Time,To_time=To_time,actual_From_Time=actual_From_Time,Ntp_time=Ntp_time)
    logger.warning("Date time was wrong From :{} To :{}".format(From_Time,To_time))
    logger.warning("Actual time was     From :{} To :{}".format(actual_From_Time,Ntp_time))
  except Exception as d:
    logger.warning(d)
    
def Date_Time_Update():    
    while True :
        time.sleep(10)
        dd=read_from_file()
        b = addSecs(dd, 10)
        if b=="":
            logger.error("After adding second file  is emty")
        else:
            write_on_file(data_To_Write=b)
            
            
if __name__ == '__main__':
    try :
        Current_version = "0.7"
        program='''
        Program name        : UltronClock
        Author              : Udayathilagan
        Date created        : 21/07/2021
        Date last modified  : 21/07/2021
        Python Version      : 3.9.1
        Program Version     : {}        
        Email address       : udayathilagan.elamaran@aparinnosys.com'''.format(Current_version)
        check_internet()
        logger.info(program)
        t1=threading.Thread(target=Internet_came_After,args=(10,))
        t1.start()
        t2=threading.Thread(target=Date_Time_Update)
        t2.start()
    except Exception as ds:
        logger.error(ds)