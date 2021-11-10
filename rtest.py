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

#Class calling
TimeStonE=timE()
FileHandler=FileHandleR(Main_Location)
CAM=cameraApi(cameraIPSeries=cameraIPSeries)
MqTT=mqtt_mod(username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic)




logging.config.fileConfig('./logging.conf')
logger = logging.getLogger()

cameraIP=206
# Cam_State,Cam_uuid=CAM.Get_UID(cameraIP=cameraIP,username=username,password=password)
# if Cam_State:
#     d,k=CAM.Get_Time(cameraIP=cameraIP,uID=Cam_uuid)
#     # CAM.Set_Mannual_Time(cameraIP=cameraIP,year=year,month=month,day=day,hour=hour,min=min,sec=sec,uID=Cam_uuid)
#     # CAM.Set_NTP_Time(cameraIP,uID=Cam_uuid)
#     print(d,k)
# else :
#     logger.info("Can't Access Cam : "+str(cameraIP))
    
Camera_TF="%Y-%m-%dT%X"


def Read_Cam_Time(cameraIP,username,password):
    Cam_State,Cam_uuid=CAM.Get_UID(cameraIP=cameraIP,username=username,password=password)
    if Cam_State:
        Cam_status,Cam_Time=CAM.Get_Time(cameraIP=cameraIP,uID=Cam_uuid)
        return Cam_status,Cam_Time
    else :
        logger.info("Can't Access Camera : "+str(cameraIP))
        return Cam_State,Cam_uuid

Cam_status,Cam_Time=Read_Cam_Time(cameraIP=206,username=username,password=password)
print(Cam_Time)
ToSet=TimeStonE.TimeFormatChanger(InTime=Cam_Time,INFormat=Camera_TF,OutTimeFormat=Rpi_TF)
print(ToSet)
