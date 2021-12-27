import os 
import urllib.request
import ssl
import json


class Capability:
    # def __init__():
    #     pass
    

    def Check_Internet(Url_To_Hit): #'https://ipinfo.io/ip'
        try:
            context = ssl._create_unverified_context()
            urllib.request.urlopen(Url_To_Hit, context=context)
            return True
        except Exception as d:
            # print(d)
            return False

    def Get_Edge_Id():
        try:  
            with open('/home/pi/edge-controller/config/edge-controller.json', 'r') as res   :  
            #res = os.popen('cat /home/pi/edge-controller/config/edge-controller.json').read()
                kl=json.loads(res.read())
                edge=kl["VBOXID"]
                return edge
        except Exception as d:
            return d

            
    def Check_Internet_After_Flag(Url_To_Hit,Sleep_Time): #'https://ipinfo.io/ip'
        try:
            context = ssl._create_unverified_context()
            urllib.request.urlopen(Url_To_Hit, context=context)
            return True
        except Exception as d:
            # print(d)
            return False
            