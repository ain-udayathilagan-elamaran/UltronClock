import os 
import urllib.request
import ssl
class Capability:
    # def __init__():
    #     pass
    

    def Check_Internet(Url_To_Hit): #'https://ipinfo.io/ip'
        try:
            context = ssl._create_unverified_context()
            urllib.request.urlopen(Url_To_Hit, context=context)
            return True
        except Exception as d:
            print(d)
            return False
            