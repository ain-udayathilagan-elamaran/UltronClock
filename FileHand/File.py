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
            # logger.error(sd)
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
        except Exception as df:
            print(df)