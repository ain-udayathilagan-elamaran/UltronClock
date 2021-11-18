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

    def Update_Config(self,File_Name,Backup_File_Name):
        with open(Backup_File_Name, "r") as fl:
            f = open(File_Name,"w")
            f.write(fl.read())
            f.close()
    
    def Config_Checker_Retrive(File_Name,permission,Backup_File_Name):
        try :
            if not os.path.exists(File_Name):#if file not available
                data= ("File Not found ")
                with open(Backup_File_Name, "r") as fl:
                    f = open(File_Name,"w")
                    f.write(fl.read())
                    f.close()
                # Update_Config(File_Name,Backup_File_Name)
                fl = open(File_Name,permission)
                ConfigData = json.load(fl)  
                return True,ConfigData,data

            elif len(open(File_Name).read()) == 0 :#if file available and emty 
                data=("File is empty bro")
                with open(Backup_File_Name, "r") as fl:
                    f = open(File_Name,"w")
                    f.write(fl.read())
                    f.close()
                fl = open(File_Name,permission)
                ConfigData = json.load(fl)  
                return True,ConfigData,data

            else :
                data="Config file is available"
                fl = open(File_Name,permission)
                ConfigData = json.load(fl)  
                return True,ConfigData,data
                # Update_Config(File_Name,Backup_File_Name)
        except Exception as df :
            data=""
            return False,df,data
              
            

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


    def T1_writter(self,T1,RTC_State,RTC_Time,Rpi_Time,Camera_Time,FileName,permission):
        try :
            change_log={
            "T1":T1 ,
            "T2":"",
            "RTC_State":RTC_State,
            "RTC_Time":RTC_Time,
            "Rpi_Time":Rpi_Time,
            "Camera_Time":Camera_Time
            
            
            }
            json_ob = json.dumps(change_log, indent = 4)
            with open(FileName, permission) as outfile:
                outfile.write(json_ob) 
                return True  
        except Exception as df:
            return False
            print(df)
            
            
    def T1_Reader(self,FileName,permission):
        try:
            # print(To_Find)
            # fl=FileHandler.read_from_file(FileName='Change_log.json',permission='r')
            fl = open(FileName,permission)
            data = json.load(fl)
            fl.close()
            # To_time=T2
            T1=data["T1"]
            RTC_State=data["RTC_State"]
            RTC_Time=data["RTC_Time"]
            Rpi_Time=data["Rpi_Time"]
            Camera_Time=data["Camera_Time"]
            
            return T1,RTC_State,RTC_Time,Rpi_Time,Camera_Time
        except Exception as d:
            print(d)
            return False
