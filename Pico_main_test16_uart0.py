from machine import UART, Pin, PWM
from time import sleep
import ujson

uart0 = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) # UART tx/rx

x = ''
zDict = ''
# Setup all Domoticz IDX numbers and map to internal PIN, name is for ref.
id_name = { 7297 : {"name" : "JMB-C1", "pin" : 15 },
            7298 : {"name" : "JMB-C2", "pin" : 14 },
            7299 : {"name" : "JMB-C3", "pin" : 13 },
            7300 : {"name" : "JMB-C4", "pin" : 12 },
            7301 : {"name" : "JMB-C5", "pin" : 11 },
            7716 : {"name" : "JMB-C6", "pin" : 10 }}

# Setup base freq on all pins
for i in id_name:
    PWM(Pin(id_name[i]["pin"])).freq(200)  

# Setup internal led
led = machine.Pin(25, machine.Pin.OUT) 



def Ledsig(i):
    for i in range(5):
        led.value(1)
        sleep(0.1)
        led.value(0)
        sleep(0.1)

def GetState():
    global zDict
    try:
       if zDict['status'] == 'OK':
           if zDict['result'][0]['Status'] == 'On' or zDict['result'][0]['Status'][0:10] == "Set Level:": # device is ON
               print('Status is ON')
               if type(zDict['result'][0]['Level']) is int and zDict['result'][0]['Level'] in range(101): # levels are in range 0-100
                   print(zDict['result'][0]['Level']) # must be int
                   idx = int(zDict['result'][0]['idx'])
                   level = zDict['result'][0]['Level']
                   return idx, level
               else:
                   print("Error : out of range")
           elif zDict['result'][0]['Status'] == 'Off':
               print('Status is OFF')
               idx = int(zDict['result'][0]['idx'])
               level = 0
               return idx, level
           else:
               print("Error : Oeps")
    except (ValueError):
        print('not oke syntax error in JSON')
        xDict = ''
    except Exception as e:
        print(e)
        
def PWMset(idx, level):
    if idx in id_name.keys() and level in range(101):
        duty = int((65025/100)*level)
        PWM(Pin(id_name[idx]["pin"])).duty_u16(duty)
        print(idx, level)

def IntoJson():
    try:
        global xDict
        global zDict
        zDict = ujson.loads(xDict)
        print('=====')
        #print('JSON is OK')
        #print(zDict['result'][0]['LastUpdate']) # str
        print(zDict['result'][0]['Name']) # str
        #print(zDict['result'][0]['idx'])
        #print(zDict['result'][0]['Level'])
    except (ValueError):
        print('not oke syntax error in JSON')
        xDict = ''
    except Exception as e:
        print(e)

while True:
    try:
        rxData = bytes()
        while uart0.any() > 0:
            rxData += uart0.read(1)
        
        if len(rxData):
            x = x + str(rxData.decode('utf-8'))
            #print(rxData.decode('utf-8'), end='')
            if x.find("HTTP Response code: 200") >= 0 and x.find('"title" : "Devices"') >= 1600:
            #if x[0:23] == "HTTP Response code: 200" and x.find('"title" : "Devices"') > 1000:
                fist_char = x.find("HTTP Response code: 200")
                last_char = x.find('"title" : "Devices"')
                #print("----start----")
                xDict = x[(fist_char+25):(last_char+21)]
                #print(xDict)
                #print("====end====")
                IntoJson()
                #zDict = ujson.loads(xDict)
                print("length : " + str(len(x)))
                x = x[(last_char+21):]
                #GetState()
                a, b = GetState()
                #print(a,b)
                PWMset(a, b)
            elif len(x) > 2400:
                print("to long length : " + str(len(x)))
                Ledsig(3)
                #print(x)
                #print("+++++")
                x = ''
    except Exception as e:
        Ledsig(3)
        x = ''
        print("Oeps an Error")
        print(f"NOT OK: {str(e)}")
