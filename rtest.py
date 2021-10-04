import logging
import logging.config
# from time import 

from Camera_API.Cam import cameraApi
from EaseOfUse.Functionalities import Capability
from FileHand.File import FileHandleR
from TimeStone.timestonE import timE
import threading
import time
#Class calling
TimeStonE=timE()
FileHandler=FileHandleR("/home/pi/UltronClock")

CAM=cameraApi(cameraIPSeries="http://192.168.1.")

#Var which need  
Rpi_TF="%a %d %b %X %Z %Y" # Wed 29 Sep 21:21:28 IST 2021
Ntp_TF="%c"     # Thu Sep 30 12:21:32 2021
HwSet_TF="%Y-%m-%d %X"# 2021-09-29 21:20:54
RpiSet_TF="%a %b %d %X %Z %Y"# Mon Aug  12 20:14:11 UTC 2014
Url_To_Hit='https://ipinfo.io/ip'

DT_File_Name="datetime.txt"
NTP_Server='Asia.pool.ntp.org'
username="admin"
password="123456"
global FlagA
FlagA=0
CameraIP=[205,206,207,208]



# logging.config.fileConfig('./log.conf')
# logger = logging.getLogger()


# print(CAM.Get_UID(206,username,password))


# if Capability.Check_Internet(Url_To_Hit):
#     NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,3,2)
#     print(NtP_State,Ntp_t)
#     RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,Zone="IST")
#     print(RpiTimeToSet)
#     Rpi_Time=TimeStonE.ReadRpiTime()
#     Hw_Time=TimeStonE.ReadHwClockTime()
    
#     print("1 :",Ntp_t)
#     Chage_Time=TimeStonE.TimeFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,OutTimeFormat=HwSet_TF)#tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
#     print("2 :",Chage_Time)
#         # HwSet_TF
# FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")

# else : 
#     print("df")   
    # if TimeStonE.Time1_Time2_check_equivalent(Ntp_t,Ntp_TF,Rpi_Time,Rpi_TF):
    #     print("yeah")

def Main():
    global FlagA
    if Capability.Check_Internet(Url_To_Hit):
        print("1")
        NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,3,2)
        if NtP_State:
            print("2")
            Rpi_Time=TimeStonE.ReadRpiTime()
            print("3")
            print("This is Rpi Time",Rpi_Time)
            print("This is Ntp_t Time",Ntp_t)           
            if TimeStonE.Time1_Time2_check_equivalent(Ntp_t,Ntp_TF,Rpi_Time,Rpi_TF):
                print("4")
                # print("Rpi and Ntp Time are same")
                FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
                print("5")
            else:       
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,Zone="IST") 
                print("6")
                print("This is RpiTimeToSet Time",RpiTimeToSet)
                HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=Ntp_t,INFormat=Ntp_TF,OutTimeFormat=HwSet_TF)
                print("7")
                print("This is HwTimeToSet Time",HwTimeToSet) 
                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                print("8")
                TimeStonE.Set_HWClock_Time(HwTimeToSet)
                print("9")
                FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
                print("10")
                tm=TimeStonE.TimeFormatter(Ntp_t,Ntp_TF)
                for ip in CameraIP:
                    print(tm.year, tm.month, tm.day, tm.hour, tm.minute,tm.second)
                    Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
    
                #Camera need to set 
    else : #No internet Time
        print("11")
        Hw_State,Hw_t=TimeStonE.ReadHwClockTime()
        print("12")
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        print("13")
        Rpi_Time=TimeStonE.ReadRpiTime()
        print("14")
        if Hw_State:
            print("15")
            if TimeStonE.check_Time2_Greater_Than_Time1(File_t,Ntp_TF,Hw_t,HwSet_TF):# hw CLOCK TIME GREATER 
                print("16")
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Hw_t,INFormat=HwSet_TF,Zone="IST") 
                print(TimeStonE.Set_Rpi_Time(RpiTimeToSet))
                print("17")
                FileTimeToSet=TimeStonE.TimeFormatChanger(InTime=Hw_t,INFormat=HwSet_TF,OutTimeFormat=Ntp_TF)     
                print(FileHandler.write_on_file(FileTimeToSet,DT_File_Name,"w"))
                print("18--",FileTimeToSet)
                print(FileHandler.T1_writter(T1=FileTimeToSet,FileName="Change_log.json",permission="w"))
                FlagA=2
                #Camera need to set 
                tm=TimeStonE.TimeFormatter(Hw_t,HwSet_TF)
                print(tm)
                for ip in CameraIP:
                    print(ip)
                    print(tm.year, tm.month, tm.day, tm.hour, tm.minute,tm.second)
                    Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
    
                #Camera need to set 
            else :# FILE  CLOCK TIME GREATER
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
                print("188")
                print(TimeStonE.Set_Rpi_Time(RpiTimeToSet))
                print("19")
                HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=File_t,INFormat=Ntp_TF,OutTimeFormat=HwSet_TF)
                print("20")
                print(TimeStonE.Set_HWClock_Time(HwTimeToSet))
                print("21")
                print(FileHandler.T1_writter(T1=File_t,FileName="Change_log.json",permission="w"))
                print("22")
                FlagA=2
                print("23")
                tm=TimeStonE.TimeFormatter(File_t,Ntp_TF)
                for ip in CameraIP:
                    print(tm.year, tm.month, tm.day, tm.hour, tm.minute,tm.second)
                    Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
    
                #Camera need to set 
        else : #Rtc failure
            print("#Rtc failure")
            RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
            print("24")
            print(RpiTimeToSet)
            print(TimeStonE.Set_Rpi_Time(RpiTimeToSet))
            FlagA=2
            print("25 OVER")
            tm=TimeStonE.TimeFormatter(File_t,Ntp_TF)
            for ip in CameraIP:
                print(tm.year, tm.month, tm.day, tm.hour, tm.minute,tm.second)
                Set_Cam_Time(cameraIP=ip,username=username,password=password,year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)
    
def T2_Checker(Ntp_time):
    try:
        # fl=FileHandler.read_from_file(FileName='Change_log.json',permission='r')
        # fl = open('Change_log.json',)
        print(Ntp_time)
        # From_Time=FileHandler.T1_Reader(To_Find="T1",FileName='Change_log.json',permission='r')
        To_Find="T1"
        FileName="Change_log.json"
        permission="r"
        From_Time=FileHandler.T1_Reader(To_Find,FileName,permission)
        print("From_Time",From_Time,type(From_Time))
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        print("File_State,File_t",File_State,File_t)
        # T1_Reader
        # data = json.load(fl)
        # fl.close()
        # To_time=T2
        # T1=(data["T1"])
        DuState,Duration=TimeStonE.Time1_Time2_check_Difference(Time1=From_Time,Time1_format=Ntp_TF,Time2=File_t,Time2_format=Ntp_TF)
        # Duration=str(delay_Is)
        msg=TimeStonE.Data_Creater(Ntp_time,Ntp_TF,Duration,From_Time=From_Time,To_time=File_t)
        print("Duration is :"+str(Duration))
        print(msg)
        # current_Time=df.strptime(Ntp_time,Ntp_TF)
        # actual_From_Time=current_Time - Duration
        # Change_log_Creater(Duration=Duration, From_Time=From_Time,To_time=File_t,actual_From_Time=actual_From_Time,Ntp_time=Ntp_time)
        
        # logger.warning("Date time was wrong From :{} To :{}".format(From_Time,To_time))
        # logger.warning("Actual time was     From :{} To :{}".format(actual_From_Time,Ntp_time))
        
        
    except Exception as d:
        print(d)

def Set_Cam_Time(cameraIP,username,password,year,month,day,hour,min,sec):
    Cam_State,Cam_uuid=CAM.Get_UID(cameraIP=cameraIP,username=username,password=password)
    print(Cam_State,Cam_uuid)
    if Cam_State:
        print(CAM.Set_Mannual_Time(cameraIP=cameraIP,year=year,month=month,day=day,hour=hour,min=min,sec=sec,uID=Cam_uuid))
        print(CAM.Set_NTP_Time(cameraIP,uID=Cam_uuid))
    else :
        print ("Can't Access Cam : "+str(cameraIP))


def Internet_came_After(tim1): # need to do 
    print("In interes sadhasdb ",tim1)
    global FlagA
    while True:
        if FlagA == 2: 
            time.sleep(tim1)
            if Capability.Check_Internet_After_Flag(Url_To_Hit,30):
                NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,4,2)
                print(NtP_State,Ntp_t)
                T2_Checker(Ntp_t)
                FlagA=0
                break

def Date_Time_Update(Time_To_update): 
    print("In Date_Time_Update sadhasdb ",Time_To_update)   
    while True :
        time.sleep(Time_To_update)
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        if File_State:
            print("Time to file is :",File_t)   
            TimeState,AddedTime=TimeStonE.AddSeconds(File_t,Ntp_TF,Time_To_update)
            print("Time to update is :",AddedTime)   
            print(FileHandler.write_on_file(AddedTime,DT_File_Name,"w"))
        # dd=read_from_file()
        # b = addSecs(dd, 10)
        # if b=="":
            # logger.error("After adding second file  is emty")
        else:
            if Capability.Check_Internet_After_Flag(Url_To_Hit,10):
                NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,4,2)
                FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")


# File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")  
# tm=TimeStonE.TimeFormatter(File_t,Ntp_TF)      
# print(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
# Set_Cam_Time(cameraIP=207,username="admin",password="123456",year=tm.year,month=tm.month,day=tm.day,hour=tm.hour,min=tm.minute,sec=tm.second)          

# # Main()
# NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,4,2)
# print(NtP_State,Ntp_t)
# T2_Checker(Ntp_t)
            
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
        Main()
        print(program)
        t1=threading.Thread(target=Internet_came_After,args=(10,))
        t1.start()
        t2=threading.Thread(target=Date_Time_Update,args=(10,))
        t2.start()
    except Exception as ds:
        print(ds)
