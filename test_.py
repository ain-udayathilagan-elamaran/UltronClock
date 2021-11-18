from TimeStone.timestonE import timE
from FileHand.File import FileHandleR
from EaseOfUse.Functionalities import Capability



TimeStonE=timE()
FileHandler=FileHandleR()

# TK
#read_from_file(FileName,permission):
# FileH=FileHandleR("/home/pi/UltronClock/")
# d=(timE.ReadHwClockTime())
# print(d)
# HW_New_Format=("%Y-%m-%d %X")

# tm_New_Format=("%a %b %d %X %Y")
# FileName="DTFile.txt"
# tm=FileH.read_from_file(FileName=FileName,permission="r")
# print(tm)
# timE.check_Which_Greater_Time2_Time1(Time1=d[1],Time1_format=HW_New_Format,Time2=tm[1],Time2_format=tm_New_Format)


DT_File_Name="datetime.txt"

def Main():
    if Capability.Check_Internet():
        NtP_State,Ntp_t=TimeStonE.Get_Ntp_Time(3,2)
        if NtP_State:
            print(Ntp_t)
            Rpi_Time=TimeStonE.ReadRpiTime()
            if TimeStonE.Time1_Time2_check_equivalent(Ntp_t,"%c",Rpi_Time[1],"%c"):
                FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
            else:        
                TimeStonE.Update_Rpi_Time(Ntp_t)
                TimeStonE.Update_HwClock_Time(Ntp_t)
                FileHandler.write_on_file(Ntp_t,DT_File_Name,"w")
    
    else : #No internet Time
        Hw_State,Hw_t=TimeStonE.ReadHwClockTime()
        File_State,File_t=FileHandler.read_from_file(DT_File_Name,"r")
        Rpi_Time=TimeStonE.ReadRpiTime()
        if Hw_State:
            if TimeStonE.check_Which_Greater_Time2_Time1(File_t,"%c",Hw_t,"%c"):
                TimeStonE.Update_Rpi_Time(Hw_t)
                TimeStonE.Update_HwClock_Time(Hw_t)          
                #Camera need to set 
        else : #Rtc failure
            if TimeStonE.check_Which_Greater_Time2_Time1(Rpi_Time,"%c",File_t,"%c"):
                TimeStonE.Update_Rpi_Time(File_t)
                TimeStonE.Update_HwClock_Time(File_t)
            
                #Camera need to set 
    
    
# if ff[0]:
#     print(ff[1])
# else :
    
#     print(" th erer df")
    

# tm_format='%c'
# seconds_to_add=6000
# # k=Tk.AddSeconds(tm,"%c",10,New_Format)#AddSeconds(tm,tm_format,seconds_to_add,New_Format)
# k=Tk.AddSeconds(tm[1],tm_format,seconds_to_add)
# print(k)
# kl=FileH.write_on_file(data_To_Write=k[1],FileName=FileName,permission='w')
# print(kl)
# FileH.T1_writter("23,8","Change_log.json","w")
# # Tk.Date_Time_Check(RpiTime=tm[1],Time_format=tm_format)
# Tk.Time1_Time2_Check(Time1=tm[1],Time1_format=tm_format,Time2=tm[1],Time2_format=tm_format)

    
            
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
        
        print("program")
        Main()
        # t1=threading.Thread(target=Internet_came_After,args=(10,))
        # t1.start()
        # t2=threading.Thread(target=Date_Time_Update)
        # t2.start()
    except Exception as ds:
        print(ds)