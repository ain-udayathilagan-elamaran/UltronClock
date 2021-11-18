# from TimeStone.timestonE import timE
# from FileHand.File import FileHandleR
# from EaseOfUse.Functionalities import Capability
from Mqtt_Module.mqtt import mqtt_mod
from Data_File import Details
username_mqtt=Details["Rpi_TF"]
password_mqtt=Details["password_mqtt"]
mqtt_broker=Details["mqtt_broker"]
mqtt_port=Details["mqtt_port"]
Publish_Topic=Details["Publish_Topic"]

MqTT=mqtt_mod(username_mqtt,password_mqtt,mqtt_broker,mqtt_port,Publish_Topic)
# import json
Message="test1"
MqTT_State,client=MqTT.MQTT_Connect()
print(MqTT_State,client)
if MqTT_State:
    print(Publish_Topic)
    print(MqTT.Publish_Data(client,Message))
 
# # Opening JSON file
# f = open('Config.json',)
 
# # returns JSON object as
# # a dictionary
# data = json.load(f)
# if (data["AparCamera"]):
#     print(data)


# # TimeStonE=timE()

# # TK
# #read_from_file(FileName,permission):
# # FileH=FileHandleR("/home/pi/UltronClock/")
# # d=(timE.ReadHwClockTime())
# # print(d)
# # HW_New_Format=("%Y-%m-%d %X")

# # tm_New_Format=("%a %b %d %X %Y")
# # FileName="DTFile.txt"
# # tm=FileH.read_from_file(FileName=FileName,permission="r")
# # print(tm)
# # timE.check_Which_Greater_Time2_Time1(Time1=d[1],Time1_format=HW_New_Format,Time2=tm[1],Time2_format=tm_New_Format)




# def Main():
#     if Capability.Check_Internet():
#         NtP_Date=Dr_strange.Get_Ntp_Time(Try_Limit=3,Sleep_Time=2)
#         # print(NtP_Date)
#         if NtP_Date[0]:
#             print(NtP_Date[1])
            
#             print(Dr_strange.ReadHwClockTime())
#             # print(Dr_strange.ReadRpiTime())
#             print(Dr_strange.ReadRpiTime())
#             Dr_strange.Set_Rpi_Time("Wed Sep 29 17:46:29 2020")
#             print(Dr_strange.ReadRpiTime())

#             # NtP_Date[1]
#             # check_Which_Greater_Time2_Time1(self,Time1,Time1_format,Time2,Time2_format)
#             # Update_Rpi_Time(self,Time_To_Set)
        
            
        
        
    
    
# # if ff[0]:
# #     print(ff[1])
# # else :
    
# #     print(" th erer df")
    

# # tm_format='%c'
# # seconds_to_add=6000
# # # k=Tk.AddSeconds(tm,"%c",10,New_Format)#AddSeconds(tm,tm_format,seconds_to_add,New_Format)
# # k=Tk.AddSeconds(tm[1],tm_format,seconds_to_add)
# # print(k)
# # kl=FileH.write_on_file(data_To_Write=k[1],FileName=FileName,permission='w')
# # print(kl)
# # FileH.T1_writter("23,8","Change_log.json","w")
# # # Tk.Date_Time_Check(RpiTime=tm[1],Time_format=tm_format)
# # Tk.Time1_Time2_Check(Time1=tm[1],Time1_format=tm_format,Time2=tm[1],Time2_format=tm_format)

    
            
# if __name__ == '__main__':
#     try :
#         Current_version = "0.7"
#         program='''
#         Program name        : UltronClock
#         Author              : Udayathilagan
#         Date created        : 21/07/2021
#         Date last modified  : 21/07/2021
#         Python Version      : 3.9.1
#         Program Version     : {}        
#         Email address       : udayathilagan.elamaran@aparinnosys.com'''.format(Current_version)
        
#         Dr_strange=timE()
#         print("program")
#         Main()
#         # t1=threading.Thread(target=Internet_came_After,args=(10,))
#         # t1.start()
#         # t2=threading.Thread(target=Date_Time_Update)
#         # t2.start()
#     except Exception as ds:
#         print(ds)