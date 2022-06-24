#!/usr/bin/python
#--------------------------------------
#
#              BabyKamerUit5m.py
#  Switch Hue Light off in 5 min
#
# Author : Vincent Rouwhorst
# Date   : 27/09/2018
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

import requests
import time

DOMOTICZ_IP = 'http://127.0.0.1:8080'

id_name = { 722  : {"name" : "Hue Babykamer", "min" : 5, "max" : 85 }}


def ReadCommand(idx):
    #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(idx))
    r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(idx))
    siteresponse = r.json()
    print(str(id_name[idx]["name"]) + " = " + str(siteresponse["result"][0]["Status"]))
    if siteresponse['status'] == 'OK':
        if siteresponse['result'][0]['Status'] == 'On' or siteresponse['result'][0]['Status'][0:10] == "Set Level:": # device is ON
            print('Status is ON')
            if type(siteresponse['result'][0]['Level']) is int and siteresponse['result'][0]['Level'] in range(101): # levels are in range 0-100
                print(siteresponse['result'][0]['Level']) # must be int
                #idx = int(siteresponse['result'][0]['idx'])
                level = siteresponse['result'][0]['Level']
                return level
            else:
                print("Error : out of range")
        elif siteresponse['result'][0]['Status'] == 'Off':
            print('Status is OFF')
            #idx = int(siteresponse['result'][0]['idx'])
            level = id_name[idx]["max"]
            return level
        else:
            print("Error : Oeps")


if __name__ == '__main__':
  # Script has been called directly
  idx = 722
  countdowntimer = 300 # 5 min = 300 sec
  lampstartlevel = ReadCommand(idx)

  for x in reversed(range(id_name[idx]["min"], lampstartlevel)):  # level 7 is the minimum level for the light to dim to
      print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(idx) + "&switchcmd=Set%20Level&level=" + str(x))
      r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(idx) + "&switchcmd=Set%20Level&level=" + str(x))
      siteresponse = r.json()
      #if siteresponse["status"] == 'OK':
      #print('Response = OK')
      if siteresponse["status"] == 'ERR':
         # Write ERROR to Domoticz log
         message = "ERROR writing lamp script"
         #print(message)
         requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=addlogmessage&message=" + message)
      time.sleep(countdowntimer/lampstartlevel)
