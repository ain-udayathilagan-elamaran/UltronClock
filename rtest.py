from TimeStone.timestonE import timE
from FileHand.File import FileHandleR
from EaseOfUse.Functionalities import Capability
from Camera_API.Cam import cameraApi

#Class calling
TimeStonE=timE()
FileHandler=FileHandleR("/home/pi/UltronClock")
CAM=cameraApi(cameraIPSeries="http://192.168.1.")

#Var which need  
Rpi_TF="%a %d %b %X %Z %Y" # Wed 29 Sep 21:21:28 IST 2021
Ntp_TF="%c"     # Thu Sep 30 12:21:32 2021
HwSet_TF="%Y-%m-%d %X"# 2021-09-29 21:20:54
RpiSet_TF="%a %b %d %X %Z %Y"# Mon Aug  12 20:14:11 UTC 2014
Url_To_Hit='https://ipinfo.isdsdso/ip'

DT_File_Name="datetime.txt"
NTP_Server='Asia.pool.ntp.org'
username="admin"
password="123456"
global FlagA
FlagA=0

# print(CAM.Get_UID(206,username,password))



# if Capability.Check_Internet(Url_To_Hit):
#     NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,3,2)
#     print(NtP_State,Ntp_t)
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
            if TimeStonE.check_Time2_Greater_Than_Time1(File_t,Ntp_TF,Hw_t,HwSet_TF):
                print("16")
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=Hw_t,INFormat=HwSet_TF,Zone="IST") 
                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                print("17")
                FileTimeToSet=TimeStonE.TimeFormatChanger(InTime=Hw_t,INFormat=HwSet_TF,OutTimeFormat=Ntp_TF)     
                FileHandler.write_on_file(FileTimeToSet,DT_File_Name,"w")
                print("18")
                FileHandler.T1_writter(T1=RpiTimeToSet,FileName="Change_log.json",permission="w")
                FlagA=2
                #Camera need to set 
            else :
                RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
                TimeStonE.Set_Rpi_Time(RpiTimeToSet)
                HwTimeToSet=TimeStonE.TimeFormatChanger(InTime=File_t,INFormat=Ntp_TF,OutTimeFormat=HwSet_TF)
                TimeStonE.Set_HWClock_Time(HwTimeToSet)
                FileHandler.T1_writter(T1=RpiTimeToSet,FileName="Change_log.json",permission="w")
                FlagA=2
                #Camera need to set 
        else : #Rtc failure
            print("#Rtc failure")
            RpiTimeToSet=TimeStonE.RpiSetFormatChanger(InTime=File_t,INFormat=Ntp_TF,Zone="IST") 
            print(RpiTimeToSet)
            TimeStonE.Set_Rpi_Time(RpiTimeToSet)

       
def T2_Checker(T2,Ntp_time):
    try:
        fl=FileHandler.read_from_file(FileName='Change_log.json',permission='r'))
        # fl = open('Change_log.json',)
        data = json.load(fl)
        # fl.close()
        # To_time=T2
        T1=(data["T1"])
        Duration=TimeStonE.Time1_Time2_check_Difference(Time1=T1,Time1_format=Ntp_TF,Time2=T2,Time2_format=Ntp_TF)
        # Duration=str(delay_Is)
        print("Duration is :"+str(Duration))
        current_Time=df.strptime(Ntp_time,Ntp_TF)
        actual_From_Time=current_Time - Duration
        Change_log_Creater(Duration=Duration, From_Time=From_Time,To_time=To_time,actual_From_Time=actual_From_Time,Ntp_time=Ntp_time)
        logger.warning("Date time was wrong From :{} To :{}".format(From_Time,To_time))
        logger.warning("Actual time was     From :{} To :{}".format(actual_From_Time,Ntp_time))
    except Exception as d:
        logger.warning(d)



def Internet_came_After(tim1): # need to do 
    global FlagA
    while True:
        if FlagA == 2: 
            if Capability.Check_Internet(Url_To_Hit):
                NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(NTP_Server,4,2)
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


# Main()

