TITLE

    UltronClock v1.8

------------------------------------------------------------------------------

BUILD DATE

    16/02/2022

------------------------------------------------------------------------------

ORIGINATOR

    Udayathilagan Elamaran
    Apar Innosys 
    Mail ID : udayathilagan.elamaran@aparinnosys.com
------------------------------------------------------------------------------


DEPENDENCY 		:  Buster os , logging and config File

------------------------------------------------------------------------------

CONFIG CHANGES	: Please refer to previous builds for any change in configuration

	ADDED

        N/A

	MODIFIED

        config.json

	DELETED

        N/A


------------------------------------------------------------------------------

Enhancements/Fix IMPLEMENTED : 

------------------------------------------------------------------------------

No.     Type			    Description		

==UltronClock-v1.1==

1		Enhancement 		To avoiding 

2		Feature 			Including new functionality to Set Time To AIN Camera 

3       Fix                 Fixed Rpi Time Validation

4		Feature 			Including new function to Validate RTC Time

5		Feature 			Including new functionality to Set RTC Time

6		Feature 			Including new functionality to Send Data To Mqtt

==UltronClock-v1.2==

1       Fix            		Fixed wrong RTC Time 


2	  	Enhancement 		added Camera Boot Time to Set Time To AIN


==UltronClock-v1.3==


1		Enhancement 		Added EdgeID in Message


==UltronClock-v1.4==

1		Fix 				Fixed CPU Usage

2		Fix 				Fixed UltronClock Inactive

3    	Feature 			Including new function to get camera time for validation

==UltronClock-v1.5==

1		Enhancement 		Added HeartBeat

2		Enhancement 		Including new function to config file validation

==UltronClock-v1.6==

1		Enhancement 		Changed MQTT Topic

==UltronClock-v1.7==

1		Enhancement 		Added New thread for HeartBeat

2		Fix 				Fixed UltronClock HeartBeat time issue

==UltronClock-v1.8==

1		Enhancement 		Modified Time Format In Data Package

2		Enhancement 		Modified HB and Data Topic 

------------------------------------------------------------------------------



HOW TO INSTALL: 

------------------------------------------------------------------------------	

	NEW INSTALLATION:

------------------------------------------------------------------------------

1. UltronClock,Config.json ,UltronClock.service and logging.conf added, please find included file in package

3. Create a new folder named aiultron on \home\pi\edge-controller path

2. Upload the UltronClock,Config.json and logging.conf to \home\pi\edge-controller\aiultron  folder

	* Give Execute Permision for the UltronClock file 

3. Upload the UltronClock.service file in  /etc/systemd/system/   folder
	
	* Enable the UltronClock.service
		sudo systemctl  enable  UltronClock.service
		
	* Start the UltronClock.service
		sudo systemctl  start   UltronClock.service
