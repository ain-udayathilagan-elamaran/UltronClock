import os 
import json

class FileHandleR:
    def __init__(self,Main_path):
        self.Main_path =Main_path+"/"
        
    def read_from_file(self,FileName,permission):
        try:   
            f = open(self.Main_path+FileName, permission)
            kc=f.read()
            f.close()
            return True,kc.strip()
        except Exception as kc:
            return False,kc


    def write_on_file(self,data_To_Write,FileName,permission):
        try:
            f = open(self.Main_path+FileName,permission)
            # print(self.Main_path+FileName)
            f.write(data_To_Write)
            f.close()
            return True
        except Exception as sd:
            return False
            print(sd)
            # DateTimeSetter(30)


    def T1_writter(self,T1,FileName,permission):
        try :
            change_log={
            "T1":T1 ,
            "T2":""
            }
            json_ob = json.dumps(change_log, indent = 4)
            with open(FileName, permission) as outfile:
                outfile.write(json_ob) 
                return True  
        except Exception as df:
            return False
            print(df)
            
            
    def T1_Reader(self,To_Find,FileName,permission):
        try:
            print(To_Find)
            # fl=FileHandler.read_from_file(FileName='Change_log.json',permission='r')
            fl = open(FileName,permission)
            data = json.load(fl)
            fl.close()
            # To_time=T2
            T1=(data[To_Find])
            print(T1)
            return T1
            # Duration=TimeStonE.Time1_Time2_check_Difference(Time1=T1,Time1_format=Ntp_TF,Time2=T2,Time2_format=Ntp_TF)
            # # Duration=str(delay_Is)
            # print("Duration is :"+str(Duration))
            # current_Time=df.strptime(Ntp_time,Ntp_TF)
            # actual_From_Time=current_Time - Duration
            # Change_log_Creater(Duration=Duration, From_Time=From_Time,To_time=To_time,actual_From_Time=actual_From_Time,Ntp_time=Ntp_time)
            # logger.warning("Date time was wrong From :{} To :{}".format(From_Time,To_time))
            # logger.warning("Actual time was     From :{} To :{}".format(actual_From_Time,Ntp_time))
        except Exception as d:
            print(d)
            return False
