import os

buster="buster"
stretch="stretch"
jessie="jessie"

res = os.popen('cat /etc/os-release').read()

try :
    if buster in res:
        print 'buster os found'
        os.popen('sudo curl  https://files.aparinnosys.com/s/J9GEEEa9ycSttrd/download | sudo sh &')
        print("After installing the package")
    elif stretch in res:
        print 'stretch os found'
        os.popen('sudo curl  https://files.aparinnosys.com/s/iforkWQCJ93Mw8S/download | sudo sh &')
        print("After installing the package")
    elif jessie in res:
        print 'jessie os found'
        os.popen('sudo curl  https://files.aparinnosys.com/s/AptZpWDZtq2qcop/download | sudo sh &')
        print("After installing the package")
    
except Exception as e :
    print e