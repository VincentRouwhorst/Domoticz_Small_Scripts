#!/usr/bin/python3
#--------------------------------------
#
#              TempFan.py
#  Temperature controled Fan
#
# Author : Vincent Rouwhorst
# Date   : 01/06/2022
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

#trend 1 = trend is stabiel
#trend 2 = trend is warmer
#trend 3 = trend is cooler

import requests, time

DOMOTICZ_IP = 'http://127.0.0.1:8080'

id_name = { 7391 : {"name" : "Temp-licht",                "Tmin" : 40, "Tmax" : 50, "Tread" : 0 },
            333  : {"name" : "Temp Aquarium",             "Tmin" : 24, "Tmax" : 28, "Tread" : 0 },
            332  : {"name" : "Temp Aquarium koeler warm", "Tmin" : 30, "Tmax" : 40, "Tread" : 0 },
            331  : {"name" : "Temp 1",                    "Tmin" : 24, "Tmax" : 30, "Tread" : 0 }}

Tmin = 40
Tmax = 50

def ReadCommand(idx):
    #print(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(idx))
    r = requests.get(DOMOTICZ_IP + "/json.htm?type=devices&rid=" + str(idx))
    siteresponse = r.json()
    print(str(id_name[idx]["name"]) + " = " + str(siteresponse["result"][0]["Temp"]))
    return siteresponse["result"][0]["Temp"]
    if siteresponse["result"][0]["trend"] == 1:
        print("Temp trend is STABIEL")
    elif siteresponse["result"][0]["trend"] == 2:
        print("Temp trend is WARMER")
    elif siteresponse["result"][0]["trend"] == 3:
        print("Temp trend is KOELER")
    #if siteresponse["status"] == 'ERR':
        # Write ERROR to Domoticz log
        #message = "ERROR writing lamp script Aquarium " + str(idx)
        #print(message)
        #requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=addlogmessage&message=" + message)

def ProcesCommand():
    if id_name[7391]["Tread"] > 0 and id_name[333]["Tread"] > 0 and id_name[332]["Tread"] > 0 and id_name[331]["Tread"] > 0 :
        print("complete")
        for x in id_name:
            id_name[x]["Tprocent"] = (id_name[x]["Tread"]-id_name[x]["Tmin"])/((id_name[x]["Tmax"]-id_name[x]["Tmin"])/100)
            print(str(id_name[x]["name"]) + " = " + str(id_name[x]["Tprocent"]) + " %")



def PushCommand(idx, levelx):
    if levelx <= 0:
        levelx = 1 #  minimal value is 1 procent
    elif levelx > 100:
        levelx = 100 # max value is 100 procent
    if levelx in range(101):
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
    while True:
        for x in id_name:
            id_name[x]["Tread"] = ReadCommand(x)
            if x == 7391:
                #Tstep = (Tmax-Tmin)/100
                #print(Tmin)
                Tprocent = (id_name[x]["Tread"]-Tmin)/((Tmax-Tmin)/100)
                print(Tprocent)
                ProcesCommand()
                PushCommand(7716, int(Tprocent))
        time.sleep(60)
