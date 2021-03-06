import os
import datetime
from datetime import datetime as df
import ntplib
import time
from time import ctime

class timE:
    
    def __init__(self):
        pass
    
    def Data_Creater(self,EdgeId,Ntp_time,Ntp_TF,Duration,From_Time,From_Time_TF,To_time,To_time_TF,RTC_State,RTC_Time,RTC_Time_TF,Rpi_Time,Rpi_Time_TF,Camera_Time,Camera_Time_TF,Std_Time):
        current_Time=df.strptime(Ntp_time,Ntp_TF)
        actual_From_Time=current_Time - Duration
        From_Time=self.TimeFormatChanger(From_Time,From_Time_TF,Std_Time)
        To_time=self.TimeFormatChanger(To_time,To_time_TF,Std_Time)
        # actual_From_Time=self.TimeFormatChanger(actual_From_Time,Ntp_TF,Std_Time) 
        Ntp_time=self.TimeFormatChanger(Ntp_time,Ntp_TF,Std_Time)
        if RTC_Time == "NA":
            RTC_Time="NA"
        else:
            RTC_Time=self.TimeFormatChanger(RTC_Time,RTC_Time_TF,Std_Time)
        Rpi_Time=self.TimeFormatChanger(Rpi_Time,Rpi_Time_TF,Std_Time)
        if Camera_Time == "NA":
            Camera_Time="NA"
        else:
            Camera_Time=self.TimeFormatChanger(Camera_Time,Camera_Time_TF,Std_Time)
        # Change_log_Creater(Duration=Duration, From_Time=From_Time,To_time=To_time,actual_From_Time=actual_From_Time,Ntp_time=Ntp_time)
        # msg='{{"Edge_Id":"{}","Duration":"{}","Time_Was_Wrong_From":"{}","Time_Was_Wrong_To":"{}","Actual_Date_time_was_From":"{}","Actual_Date_time_was_Till":"{}","RTC_State":"{}","RTC_Time":"{}","Rpi_Time":"{}","Camera_Time":{}}}'.format(EdgeId,Duration,From_Time,To_time,actual_From_Time,Ntp_time,RTC_State,RTC_Time,Rpi_Time,Camera_Time)
        msg='{{"Edge_Id":"{}","Duration":"{}","Time_Was_Wrong_From":"{}","Time_Was_Wrong_To":"{}","Actual_Date_time_was_From":"{}","Actual_Date_time_was_Till":"{}","RTC_State":"{}","RTC_Time":"{}","Rpi_Time":"{}","Camera_Time":"{}"}}'.format(
                EdgeId,Duration,From_Time,To_time,actual_From_Time,Ntp_time,RTC_State,RTC_Time,Rpi_Time,Camera_Time)
        return msg
    def RpiSetFormatChanger(self,InTime,INFormat,Zone): 
        try :    
            Time =  df.strptime(InTime, INFormat)#tm_format="%c"
            ODT=Time.strftime("%a %b %d %X ")
            OY=Time.strftime(" %Y")
            OUT=ODT+Zone+OY
            # fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
            return OUT
        except Exception as dfs:
            return dfs


    def TimeFormatChanger(self,InTime,INFormat,OutTimeFormat): 
        try :    
            Time =  df.strptime(InTime, INFormat)#tm_format="%c"
            OUT=Time.strftime(OutTimeFormat)
            # fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
            return OUT
        except Exception as dfs:
            return dfs


    def TimeFormatter(self,InTime,INFormat): 
        try :    
            Time =  df.strptime(InTime, INFormat)#tm_format="%c"
            # OUT=Time.strftime(OutTimeFormat)
            # fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
            return Time
        except Exception as dfs:
            return dfs


    def ReadHwClockTime(self): 
        try :    
            HData=os.popen('sudo hwclock  -r').read().strip().split('.')[0]
            RTC_TF="%Y-%m-%d %X"
            HTime =  df.strptime(HData, RTC_TF)
            return True,HData
        except Exception as dfs:
            return False,dfs
            
    def ReadRpiTime(self): 
        try :    
            fuc=os.popen('date').read().strip()
            return fuc
        except Exception as dfs:
            return dfs
            # sudo hwclock --set --date="2011-08-14 16:45:05"


    def Set_Rpi_Time(self,Time_To_Set):
        try:    
            os.system("sudo date -s '"+Time_To_Set+"'")
            return True
        except Exception as sd:
            return False

    def Set_HWClock_Time(self,Time_To_Set):
        '''Format Need To Like this 2011-08-14 16:45:05'''
        try:    
            os.system('sudo hwclock --set --date='+'"'+Time_To_Set+'"')
            return True,Time_To_Set
        except Exception as sd:
            return False,sd




    def AddSeconds( self,tm,tm_format,seconds_to_add):#,New_Format):
        try:
            fuc=""
            # New_Format=("%a %b %d %X %Y")
            tm =  df.strptime(tm, tm_format)#tm_format="%c"
            fulldate = datetime.datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, tm.second)
            fulldate = fulldate + datetime.timedelta(seconds=seconds_to_add)
            fuc=(fulldate.strftime(tm_format))
            return True,fuc
        except Exception as dfs:
            return False,dfs



    def Ntp_And_Local_Time_Check(self,RpiTime,Time_format):
        try:
            RpiTime =  df.strptime(RpiTime, Time_format)
            # print(RpiTime)
            client = ntplib.NTPClient()
            response = client.request('Asia.pool.ntp.org', version=4)
            ntptime=str(ctime(response.tx_time))
            NtpTime=df.strptime(ntptime,Time_format)
            # print(NtpTime)
            if RpiTime == NtpTime :
                print("Ntp time and Rpi time are same ")
                # write_on_file(ntptime)
                # print(ntp)
            else :
                print("Time mismatch on Rpi")
                # print("Time on Rpi: "+str(RpiTime))
                # print("Time on NTP: "+str(NtpTime))
                # #os.system("sudo date -s '"+ntptime+"'")
                #write_on_file(ntptime) # Changed on  27/07/2021
        except Exception as fs:
            print(fs)
    


    def Time1_Time2_check_equivalent(self,Time1,Time1_format,Time2,Time2_format):
        try:
            Time1 =  df.strptime(Time1, Time1_format)
            Time2 =  df.strptime(Time2, Time2_format)
            dif=Time1-Time2
            seconds = round(dif.total_seconds())
            if seconds >50  :
                # print("Time deferent is :"+str(seconds))
                # print("Ntp time and Rpi time are same ")
                return False
                # write_on_file(ntptime)
                # print(ntp)
            else :
                # print("Time deferent is More :"+str(dif))
                return True
        except Exception as fs:
            print(fs)

    def check_Time2_Greater_Than_Time1(self,Time1,Time1_format,Time2,Time2_format):
        try:
            Time1 =  df.strptime(Time1, Time1_format)
            Time2 =  df.strptime(Time2, Time2_format)
            dif=Time2-Time1
            seconds = round(dif.total_seconds())
            if  seconds > 50 :
                return True
            else :
                return False
        except Exception as fs:
            print(fs)




    def Time1_Time2_check_Difference(self,Time1,Time1_format,Time2,Time2_format):
        try:
            Time1 =  df.strptime(Time1, Time1_format)
            Time2 =  df.strptime(Time2, Time2_format)
            duration=Time2 -Time1 
            return True,duration
        except Exception as fs:
            print(fs)
            return False,fs




    
    
    def Get_Ntp_Time(self,NTP_Server,Try_Limit,Sleep_Time):
        tr =0
        while True:
            time.sleep(0.1)
            try:
                if tr > Try_Limit:
                    return False,None
                    # break
                client = ntplib.NTPClient()
                response = client.request(NTP_Server, version=4)
                ntptime=str(ctime(response.tx_time))  
                return True,ntptime
            except Exception as df:
                tr=tr+1
                time.sleep(Sleep_Time)
                print(df)