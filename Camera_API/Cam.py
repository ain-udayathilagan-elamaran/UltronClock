import requests
import json
class cameraApi:
    def __init__(self,cameraIPSeries):
        self.cameraIPSeries =cameraIPSeries# f"http://192.168.1.{cameraIP}/"
    
    def Get_UID(self,cameraIP,username,password):
        try:    
            
            GetURL=self.cameraIPSeries+str(cameraIP)+f"/cgi-bin/getuid?username={username}&password={password}"
            # print(GetURL)
            response = requests.get(GetURL)#, data=None, headers=None)
            if response.status_code == 200 :
                UID=response.text.split()[3].split(">")[1].split("<")[0]
                return True,UID
            else :
                # print("Status Code: %s" % response.status_code)
                return False,response.text
        except Exception as d:
            print(d)
            return False,d

    def Get_Time(self,cameraIP,uID):
        try :  
            GetURL=self.cameraIPSeries+str(cameraIP)+f"/cgi-bin/time?uid={uID}"
            response = requests.get(GetURL)#, data=None, headers=None)
            if response.status_code == 200 :
                Date=(response.text.split("=")[8].replace('"',"").split()[0].strip())
                Time=(response.text.split("=")[8].replace('"',"").split()[1].split("/")[0].strip())
                return True,Date,Time
            else :
                # print("Status Code: %s" % response.status_code)
                return False,response.text
        except Exception as d:
            return False,d

    def Set_Mannual_Time(self,cameraIP,year,month,day,hour,min,sec,uID):
        try:          
        # http://192.168.1.206/cgi-bin/time?update_method=MANUAL&year=2017&month=11&day=30&hour=8&min=0&sec=0&uid=ffa72511
            GetURL=self.cameraIPSeries+str(cameraIP)+f"/cgi-bin/time?update_method=MANUAL&year={year}&month={month}&day={day}&hour={hour}&min={min}&sec={sec}&uid={uID}"
            # print(GetURL)
            response = requests.get(GetURL)#, data=None, headers=None)
            if response.status_code == 200 :
                # UID=response.text.split()[3].split(">")[1].split("<")[0]
                return True,response.text
            else :
                # print("Status Code: %s" % response.status_code)
                return False,response.text
        except Exception as d:
            return False,d

    def Set_NTP_Time(self,cameraIP,uID):
        try:
            # http://192.168.1.206/cgi-bin/time?update_method=ntp&ntpaddr=asia.pool.ntp.orgport=123&uid=fd2b6673
            GetURL=self.cameraIPSeries+str(cameraIP)+f"/cgi-bin/time?update_method=NTP&ntpaddr=asia.pool.ntp.org&port=123&uid={uID}"
            # print(GetURL)
            response = requests.get(GetURL, data=None, headers=None)
            # print(response)
            if response.status_code == 200 :
                # UID=response.text.split()[3].split(">")[1].split("<")[0]
                return True,response.text
            else :
                # print("Status Code: %s" % response.status_code)
                return True,response.text
        except Exception as d:
            return False,d