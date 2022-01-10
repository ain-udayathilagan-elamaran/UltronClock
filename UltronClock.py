import logging
import logging.config
# from time import 

from Camera_API.Cam import cameraApi
from EaseOfUse.Functionalities import Capability
from FileHand.File import FileHandleR
from TimeStone.timestonE import timE
import threading
import time
from Mqtt_Module.mqtt import mqtt_mod

from Data_File import Details
import json
global FlagA
FlagA=0

#Var which need  
Rpi_TF=Details["Rpi_TF"] # Wed 29 Sep 21:21:28 IST 2021
Ntp_TF=Details["Ntp_TF"]     # Thu Sep 30 12:21:32 2021
RTC_TF=Details["RTC_TF"] # 2021-09-29 21:20:54
RpiSet_TF=Details["RpiSet_TF"] # Mon Aug  12 20:14:11 UTC 2014
Camera_TF=Details["Camera_TF"] # 2021-10-25T16:44:39
Heart_Beat_TF=Details["Heart_Beat_TF"]#"%d-%m-%Y %H-%M-%S"
Url_To_Hit=Details["Url_To_Hit"] 

DT_File_Name=Details["DT_File_Name"] 
NTP_Server=Details["NTP_Server"] 
username=Details["username"] 
password=Details["password"] 
cameraIPSeries=Details["cameraIPSeries"]
# CameraIP=Details["CameraIP"]
Main_Location=Details["Main_Location"]
Change_File_Name=Details["Change_File_Name"]

username_mqtt=Details["username_mqtt"]
password_mqtt=Details["password_mqtt"]
mqtt_broker=Details["mqtt_broker"]
mqtt_port=Details["mqtt_port"]
Publish_Topic=Details["Publish_Topic"]
HeartBeat_Topic_Suffix=Details["HeartBeat_Topic_Suffix"]
Data_Topic_Suffix=Details["Data_Topic_Suffix"]



#Class calling
TimeStonE=timE()
FileHandler=FileHandleR(Main_Location)
CAM=cameraApi(cameraIPSeries=cameraIPSeries)
MqTT=mqtt_mod(username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic,HeartBeat_Topic_Suffix,Data_Topic_Suffix)




logging.config.fileConfig('./logging.conf')
logger = logging.getLogger()




def Main():
    try :
            
        ConfigData["AparCamera"]
        global FlagA
        if Capability.Check_Internet(Url_To_Hit):
            logger.info("Internet is Here")
            NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,3,2)
            Rpi_Time=TimeStonE.ReadRpiTime()
            if NtP_State:
                if TimeStonE.Time1_Time2_check_equivalent(Ntp_t,Ntp_TF,Rpi_Time,Rpi_TF):
                    logger.info("Rpi time is equal Ntp time")
                    FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
                else:       
                    RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,Zone="IST") 
                    logger.info("Ntp time is Not equal to Rpi time")
                    HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,OutTimeFormat=RTC_TF)
                    TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                    TimeStonE.Set_HWClock_Time(HwTimeToSet)
                    FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
            else:
                logger.info("Can't Get NTP")
        else : #No internet Time
            logger.info("No internet Time")
            RTC_State,RTC_Time=TimeStonE.ReadHwClockTime()
            logger.info("RTC_State is "+str(RTC_State))
            File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
            Rpi_Time=TimeStonE.ReadRpiTime()
            if RTC_State:
                logger.info("RTC is Working")
                if TimeStonE.check_Time2_Greater_Than_Time1(File_t,Ntp_TF,RTC_Time,RTC_TF):# hw CLOCK TIME GREATER 
                    logger.info("RTC Time is greater than File Time")
                    RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=RTC_Time,INFormat=RTC_TF,Zone="IST") 
                    TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                    FileTimeToSet=TimeStonE.TimeFormatChanger(InTime=RTC_Time,INFormat=RTC_TF,OutTimeFormat=Ntp_TF)     
                    FileHandler.write_on_file(FileTimeToSet,DT_File_Name,"w")
                    FileHandler.T1_writter(T1=FileTimeToSet,RTC_State=RTC_State,RTC_Time=RTC_Time,Rpi_Time=Rpi_Time,Camera_Time="NA",FileName="Change_log.json",permission="w")
                    FlagA=2
                    tm=TimeStonE.TimeFormatter(RTC_Time,RTC_TF)
                    if ConfigData["AparCamera"]:    
                        time.sleep(ConfigData["CameraBootTime"])
                        Cam_status,Cam_Time=Read_Cam_Time(cameraIP=206,username=username,password=password)
                        if Cam_status :
                            if TimeStonE.check_Time2_Greater_Than_Time1(RTC_Time,RTC_TF,Cam_Time,Camera_TF):# Camera CLOCK TIME GREATER 
                                logger.info("Camera Time is greater than RTC Time")
                                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,Zone="IST") 
                                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                                FileTimeToSet=TimeStonE.TimeFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,OutTimeFormat=Ntp_TF)     
                                FileHandler.write_on_file(FileTimeToSet,DT_File_Name,"w")
                                FileHandler.T1_writter(T1=FileTimeToSet,RTC_State=RTC_State,RTC_Time=RTC_Time,Rpi_Time=Rpi_Time,Camera_Time=Cam_Time,FileName="Change_log.json",permission="w")
                                FlagA=2
                            else:
                                for ip in ConfigData["CameraIP"]:
                                    logger.info("Camera IP is :"+str(ip))
                                    Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
                        else:
                            for ip in ConfigData["CameraIP"]:
                                logger.info("Camera IP is :"+str(ip))
                                Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
                    #Camera need to set 
                else :# FILE  CLOCK TIME GREATER
                    logger.info("File Time is greater than RTC Time")
                    RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
                    TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                    HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=File_t,INFormat=Ntp_TF,OutTimeFormat=RTC_TF)
                    TimeStonE.Set_HWClock_Time(HwTimeToSet)
                    logger.info("FileHandler.T1_writter")
                    FileHandler.T1_writter(T1=File_t,RTC_State=RTC_State,RTC_Time=RTC_Time,Rpi_Time=Rpi_Time,Camera_Time="NA",FileName=Change_File_Name,permission="w")
                    FlagA=2
                    tm=TimeStonE.TimeFormatter(File_t,Ntp_TF)
                    if ConfigData["AparCamera"]:    
                        time.sleep(ConfigData["CameraBootTime"])
                        Cam_status,Cam_Time=Read_Cam_Time(cameraIP=206,username=username,password=password)
                        if Cam_status :
                            if TimeStonE.check_Time2_Greater_Than_Time1(File_t,Ntp_TF,Cam_Time,Camera_TF):# Camera CLOCK TIME GREATER 
                                logger.info("Camera Time is greater than File Time")
                                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,Zone="IST") 
                                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                                HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,OutTimeFormat=RTC_TF)
                                TimeStonE.Set_HWClock_Time(HwTimeToSet)
                                FileHandler.T1_writter(T1=File_t,RTC_State=RTC_State,RTC_Time=RTC_Time,Rpi_Time=Rpi_Time,Camera_Time=Cam_Time,FileName=Change_File_Name,permission="w")
                                FlagA=2
                            else:
                                for ip in ConfigData["CameraIP"]:
                                    logger.info("Camera IP is :"+str(ip))
                                    Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
                        else:
                            for ip in ConfigData["CameraIP"]:
                                logger.info("Camera IP is :"+str(ip))
                                Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
                    #Camera need to set   
            else : #Rtc failure
                logger.info("Rtc failure")
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                FlagA=2
                FileHandler.T1_writter(T1=File_t,RTC_State=RTC_State,RTC_Time="NA",Rpi_Time=Rpi_Time,Camera_Time="NA",FileName=Change_File_Name,permission="w")
                tm=TimeStonE.TimeFormatter(File_t,Ntp_TF)
                if ConfigData["AparCamera"]:  
                    time.sleep(ConfigData["CameraBootTime"])  
                    Cam_status,Cam_Time=Read_Cam_Time(cameraIP=206,username=username,password=password)
                    if Cam_status :
                        if TimeStonE.check_Time2_Greater_Than_Time1(File_t,Ntp_TF,Cam_Time,Camera_TF):# Camera CLOCK TIME GREATER 
                            logger.info("Camera Time is greater than File Time")
                            RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,Zone="IST")
                            TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                            FlagA=2
                            FileHandler.T1_writter(T1=File_t,RTC_State=RTC_State,RTC_Time="NA",Rpi_Time=Rpi_Time,Camera_Time=Cam_Time,FileName=Change_File_Name,permission="w")
                        else:
                            for ip in ConfigData["CameraIP"]:
                                logger.info("Camera IP is :"+str(ip))
                                Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
                    else:
                        for ip in ConfigData["CameraIP"]:
                            logger.info("Camera IP is :"+str(ip))
                            Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
    except Exception as d :
        logger.error(d)        
def T2_Checker(Ntp_time,EdgeID):
    try:
        From_Time,RTC_State,RTC_Time,Rpi_Time,Camera_Time=FileHandler.T1_Reader(Change_File_Name,"r")
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        DuState,Duration=TimeStonE.Time1_Time2_check_Difference(Time1=From_Time,Time1_format=Ntp_TF,Time2=File_t,Time2_format=Ntp_TF)
        EdgeId=Capability.Get_Edge_Id() # added edge id to pub
        msg=TimeStonE.Data_Creater(EdgeId=EdgeId,Ntp_time=Ntp_time,Ntp_TF=Ntp_TF,Duration=Duration,From_Time=From_Time,To_time=File_t,RTC_State=RTC_State,RTC_Time=RTC_Time,Rpi_Time=Rpi_Time,Camera_Time=Camera_Time)
        logger.info("Duration is :"+str(Duration))
        time.sleep(2)
        MqTT_State,client=MqTT.MQTT_Connect()
        if MqTT_State:
            MqTT.Publish_Data(client,EdgeID,Message=msg)
        else :
            logger.info("MqTT_State is :"+str(MqTT_State))            
        logger.info("Message To Sent:"+str(msg))
    except Exception as d:
        logger.error(d)


def Read_Cam_Time(cameraIP,username,password):
    Cam_State,Cam_uuid=CAM.Get_UID(cameraIP=cameraIP,username=username,password=password)
    if Cam_State:
        Cam_status,Cam_Time=CAM.Get_Time(cameraIP=cameraIP,uID=Cam_uuid)
        return Cam_status,Cam_Time
    else :
        logger.info("Can't Access Camera : "+str(cameraIP))
        return Cam_State,Cam_uuid

def Set_Cam_Time(cameraIP,username,password,year,month,day,hour,min,sec):
    
    Cam_State,Cam_uuid=CAM.Get_UID(cameraIP=cameraIP,username=username,password=password)
    if Cam_State:
        Mstate,mresponse=CAM.Set_Mannual_Time(cameraIP=cameraIP,year=year,month=month,day=day,hour=hour,min=min,sec=sec,uID=Cam_uuid)
        if Mstate:
            logger.info("Set manual time for camera {}".format(str(cameraIP)))
        else:
            logger.error("Error ON Set manual time for camera {}".format(str(cameraIP)))
            logger.error(str(mresponse))
        Nstate,Nresponse=CAM.Set_NTP_Time(cameraIP,uID=Cam_uuid)
        if Nstate:
            logger.info("Set NTP time for camera {}".format(str(cameraIP)))
        else:
            logger.error("Error ON Set NTP time for camera {}".format(str(cameraIP)))
            logger.error(str(Nresponse))
    else :
        logger.info("Can't Access Cam : "+str(cameraIP))

def After_Set(Ntp_t,Ntp_TF,RTC_State):
    RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,Zone="IST") 
    logger.info("After Internetcame setting time")
    TimeStonE.Set_Rpi_Time(RpiTimeToSet)
    FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
    HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,OutTimeFormat=RTC_TF)
    if RTC_State:    
        TimeStonE.Set_HWClock_Time(HwTimeToSet)

def Internet_came_After(tim1): # need to do 
    global FlagA
    while True:
        time.sleep(tim1)
        if FlagA == 2: 
            if Capability.Check_Internet_After_Flag(Url_To_Hit,30):
                NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,4,2)
                logger.info(str(NtP_State))
                logger.info(str(Ntp_t))
                EdgeID=Capability.Get_Edge_Id()
                T2_Checker(Ntp_t,EdgeID)
                RTC_State,RTC_Time=TimeStonE.ReadHwClockTime()
                After_Set(Ntp_t,Ntp_TF,RTC_State)
                #
                FlagA=0
                # break

def Date_Time_Update(Time_To_update): 
    while True :
        time.sleep(Time_To_update)
        ReadRpiTime=TimeStonE.ReadRpiTime()
        EdgeID=Capability.Get_Edge_Id()
        HB_Time=TimeStonE.TimeFormatChanger(InTime=ReadRpiTime,INFormat=Rpi_TF,OutTimeFormat=Heart_Beat_TF)
        HB='{{"STATUS":"{}","VERSION":"{}","TIME":"{}"}}'.format("Online",Current_version,HB_Time)
        MqTT_State,client=MqTT.MQTT_Connect()
        if MqTT_State:
            MqTT.Publish_HeartBeat(client=client,EdgeId=EdgeID,Message=str(HB))
        else :
            logger.info("MqTT_State is :"+str(MqTT_State))
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        if File_State:
            TimeState,AddedTime=TimeStonE.AddSeconds(File_t,Ntp_TF,Time_To_update)
            if TimeState:
                FileHandler.write_on_file(AddedTime,DT_File_Name,"w")
            else:
                logger.error(str(AddedTime))
                if Capability.Check_Internet_After_Flag(Url_To_Hit,10):
                    NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,14,2)
                    if NtP_State:
                        FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
                
        else:
            if Capability.Check_Internet_After_Flag(Url_To_Hit,10):
                NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,14,2)
                if NtP_State:
                    FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")

if __name__ == '__main__':
    try :
        Current_version = "1.6"
        program='''
        Program name        : UltronClock
        Author              : Udayathilagan
        Date created        : 21/07/2021
        Date last modified  : 10/01/2022    
        Python Version      : 3.9.1
        Program Version     : {}        
        Email address       : udayathilagan.elamaran@aparinnosys.com'''.format(Current_version)
        logger.info(program)
        Orgstate,ConfigData,OrgConfigStatus=FileHandleR.Config_Checker_Retrive(File_Name='Org_Config.json',permission='r',Backup_File_Name='Backup_Config.json')
        logger.info("Orginal Config state : "+str(Orgstate))
        logger.info("Orginal Config  Status : "+OrgConfigStatus)
        data="Config file is available"
        if OrgConfigStatus == data  :
            Bakstate,BakConfigData,BakConfigStatus=FileHandleR.Config_Checker_Retrive(File_Name='Backup_Config.json',permission='r',Backup_File_Name='Org_Config.json')
            logger.info("BackUp Config state   : "+str(Bakstate))
            logger.info("BackUp Config  Status : "+BakConfigStatus)
        Main()
        t1=threading.Thread(target=Internet_came_After,args=(ConfigData["InternetCheckInterval"],))
        t1.start()
        t2=threading.Thread(target=Date_Time_Update,args=(ConfigData["TimeUpdateInterval"],))
        t2.start()
    except Exception as ds:
        logger.error(ds)




