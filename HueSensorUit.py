#!/usr/bin/python3
#--------------------------------------
#
#              HueSensor.py
#  Switch Hue Sensor Off
#
# Author : Vincent Rouwhorst
# Date   : 25/06/2022
#
#--------------------------------------

import requests
import time

HUE_IP = 'http://192.168.5.28/api/hqJbo66WmQkEtRx3NA5qIgNuZBOhBsAye114-7EH/sensors/19'


def ReadCommand():
    print(HUE_IP)
    r = requests.get(HUE_IP)
    siteresponse = r.json()
    print(siteresponse)

def PutCommand():
    # Making a PUT request
    print(HUE_IP)
    data = '{"config": {"on":false }}'
    print(data)
    r = requests.put(HUE_IP, data)
    # check status code for response received
    # success code - 200
    print(r)
    # print content of request
    print(r.content)



if __name__ == '__main__':
  # Script has been called directly
    #ReadCommand()
    PutCommand()
