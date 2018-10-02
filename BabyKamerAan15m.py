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


if __name__ == '__main__':
  # Script has been called directly
  idx = '722'
  countdowntimer = 900 # 15 min = 900 sec
  lamplevel = 100 # 0-100

  for x in range(lamplevel):
      print(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + idx + "&switchcmd=Set%20Level&level=" + str(x))
      r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=switchlight&idx=" + idx + "&switchcmd=Set%20Level&level=" + str(x))
      siteresponse = r.json()
      #if siteresponse["status"] == 'OK':
      #print('Response = OK')
      if siteresponse["status"] == 'ERR':
         # Write ERROR to Domoticz log
         message = "ERROR writing lamp script"
         #print(message)
         requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=addlogmessage&message=" + message)
      time.sleep(countdowntimer/lamplevel)
