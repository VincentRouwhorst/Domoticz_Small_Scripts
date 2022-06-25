#!/usr/bin/python3
#--------------------------------------
#
#              AquariumUit.py
#  Switch Hue Light Off in 45 min
#
# Author : Vincent Rouwhorst
# Date   : 31/05/2022
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

import requests
import time

DOMOTICZ_IP = 'http://127.0.0.1:8080'

id_name = { 7301 : {"name" : "JMB-C5" }}

def PushCommand(idx, levelx):
    print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(idx) + "&switchcmd=Set%20Level&level=" + str(levelx))
    r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + str(idx) + "&switchcmd=Set%20Level&level=" + str(levelx))
    siteresponse = r.json()
    if siteresponse["status"] == 'ERR':
        # Write ERROR to Domoticz log
        message = "ERROR writing lamp script Aquarium " + str(idx)
        #print(message)
        requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=addlogmessage&message=" + message)


if __name__ == '__main__':
  # Script has been called directly
  countdowntimer = 45 * 60 # 45 min = 2700 sec
  lamplevel = 101 # 0-100

  for x in reversed(range(lamplevel)):  # range=On, reversed=Off script
      for z in id_name.keys():
          PushCommand(z, x)
      time.sleep(countdowntimer/lamplevel)
