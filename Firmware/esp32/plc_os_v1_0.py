import time
import ujson
from machine import Pin, I2C
import mcp23017
#import copy
from copy import deepcopy

# load cofig plc I O
with open('plc_config.txt') as fp:
    plcConfig = ujson.load(fp)

# Ausgang Einstellungen laut Schema GPIO Nr.   (max 12ma belastbar)
'''led1 = Pin(13, Pin.OUT)
led2 = Pin(12, Pin.OUT)
led3 = Pin(14, Pin.OUT)
led4 = Pin(27, Pin.OUT)
led5 = Pin(5, Pin.OUT) # buildin led auf D32
led6 = Pin(2, Pin.OUT) # Programm Wotchdog
led7 = Pin(15, Pin.OUT) # Reset WD IC
led8 = Pin(0, Pin.OUT) # Led RED (Fehler im Programm)
led8.on() #bei program hochfahren ein'''

# Ausgang Einstellungen laut Schema GPIO Nr.   (max 12ma belastbar)
led1 = Pin(13, Pin.OUT)
led2 = Pin(12, Pin.OUT)
led3 = Pin(14, Pin.OUT)
led4 = Pin(27, Pin.OUT)
led5 = Pin(plcConfig["espLedPin"], Pin.OUT) # buildin led auf D32
led6 = Pin(plcConfig["pwdPin"], Pin.OUT) # Programm Wotchdog
led7 = Pin(15, Pin.OUT) # Reset WD IC
led8 = Pin(plcConfig["ledRedPin"], Pin.OUT) # Led RED (Fehler im Programm)
led8.on() #bei program hochfahren ein

# 13, 12, 14, 27

#sw1 = Pin(15, Pin.IN, Pin.PULL_UP)
#sw1 = Pin(18, Pin.IN)
#sw2 = Pin(5, Pin.IN) # alter Wert 5
#sw3 = Pin(4, Pin.IN)
#sw4 = Pin(0, Pin.IN)
#sw5 = Pin(2, Pin.IN)
#sw6 = Pin(15, Pin.IN)
# 15, 2, 0, 4, 5, 18

# encrypt
def sxor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def decrypt(text, pw):
    textListe = list(text)
    pwListShort = list(pw)
    encListe = []
    
    textLen = int(len(textListe) / len(pwListShort) + 1)

    password = ''
    for a in range(1, textLen+ 1):
        password += pw
    pwListe = list(password)
    
    while textListe:
        char = textListe.pop(0)
        pwChar = pwListe.pop(0)
        encChar = sxor(char, pwChar)
        encListe.append(encChar)

    enc = ''.join(encListe)
    return enc

# lade blockprogramm
# ohne encrypt
'''sd_0 = []
sd = []
with open('blockprogramm.json') as fp:
            sd_0 = ujson.load(fp)

sd = sd_0[1]
config = sd_0[0]'''

# mit encrypt
encText = ''
with open('plc_blockprogram.plc') as fp:
    encText = ujson.load(fp)

password = 'welt'
text = decrypt(encText, password)
textDict = ujson.loads(text)

sd = textDict[1]
config = textDict[0]

# PWD augang einschalten (PED signal null)
led6.on()
led6.off()

tonTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}

ton = {}
item = {}
if config['maxTon'] > 0:
    for number in range(1, config['maxTon'] + 1):
        item[('TON'+ str(number))] = {}
        item[('TON'+ str(number))] = dict(tonTyp)
        ton.update(item)

tofTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}

tof = {}
item = {}
if config['maxTof'] > 0:
    for numberTof in range(1, config['maxTof'] + 1):
        item[('TOF'+ str(numberTof))] = {}
        item[('TOF'+ str(numberTof))] = dict(tofTyp)
        tof.update(item)

countTyp = {'presetValue': 0, 'setValue': 0, 'actualValue': 0,
            'countUpFlanke': '0', 'countDownFlanke': '0', 'init': '0'}
cud = {}
item = {}
if config['maxCud'] > 0:
    for numberCud in range(1, config['maxCud'] + 1):
        item[('CUD'+ str(numberCud))] = {}
        item[('CUD'+ str(numberCud))] = dict(countTyp)
        cud.update(item)
    
# init Programm hochlauf
#block = {'B1': '0', 'B2': '0', 'B3': '0'}
# init Programm hochlauf
block = {}
if config['maxBlock'] > 0:
    for nummer in range(1, config['maxBlock'] + 1):
        item = {('B' + str(nummer)): '0'}
        block.update(item)

ip = {}
if config['maxIp'] > 0:
    for nummer in range(1, config['maxIp'] + 1):
        item = {('IP' + str(nummer)): '0'}
        ip.update(item)

sr = {}
if config['maxSr'] > 0:
    for nummer in range(1, config['maxSr'] + 1):
        item = {('SR' + str(nummer)): '0'}
        sr.update(item)

mw = {}
if config['maxMw'] > 0:
    for nummer in range(1, config['maxMw'] + 1):
        item = {('MW' + str(nummer)): 0}
        mw.update(item)
    
#input = {'I1': '0', 'I2': '0', 'I3': '1', 'I4': '1', 'I5': '0', 'I6': '0'}
#output = {'Q1': '0', 'Q2': '0', 'Q3': '0', 'Q4': '0', 'Q5': '0', 'Q6': '0'}

input = {}
if config['maxInput'] > 0:
    for nummer in range(1, config['maxInput'] + 1):
        item = {('I' + str(nummer)): '0'}
        input.update(item)

output = {}
if config['maxOutput'] > 0:
    for nummer in range(1, config['maxOutput'] + 1):
        item = {('Q' + str(nummer)): '0'}
        output.update(item)

print(input)

# Block Program
'''sd = [{'B1':'ZUW', 'OUT':'Q1', 'IN1': 'B2'},
      {'B2':'OR', 'OUT':'B1-I1', 'IN1': 'B3', 'IN2': 'B6'},
    {'B6':'GT', 'OUT':'B2-I2', 'IN1': 'MW1', 'IN2': 'CUD1'},
    {'B3':'TON', 'OUT':'B2-I1', 'IN1': 'B4', 'TONNR': 'TON1', 'PARAMETER1': 1500},
    {'B4':'INPUT', 'OUT':'B3-I1', 'IN1': 'I1'},
      {'B10':'ZUW', 'OUT':'Q2', 'IN1': 'B13'},
      {'B13':'TOF', 'OUT':'B12-I1', 'IN1': 'B14', 'TOFNR': 'TOF1', 'PARAMETER1': 1000},
      {'B14':'SR', 'OUT':'B13-I1', 'IN1': 'B17', 'IN2': 'B16', 'SRNR': 'SR1'},
      {'B16':'INPUT', 'OUT':'B14-I2', 'IN1': 'I1'},
      {'B17':'CUD', 'OUT':'B14-I1', 'IN1': 'I2', 'IN2': 'I1', 'IN3': '',
       'CUDNR': 'CUD1', 'PARAMETER1': 0, 'PARAMETER2': 3},
       {'B18':'MOVE', 'OUT':'MW1', 'IN1': 'B19', 'IN2': 3},
       {'B19':'INPUT', 'OUT':'B18-I1', 'IN1': 'I2'}]'''

# PWD augang einschalten (PED signal null)
led6.on()
led6.off()
time.sleep(0.4)
# i2c Bus aktivieren
#i2c = I2C(scl=Pin(22), sda=Pin(21))
i2c = I2C(scl=Pin(plcConfig["sclPin"]), sda=Pin(plcConfig["sdaPin"]))
print(i2c.scan())
#mcp = mcp23017.MCP23017(i2c, 0x20)
mcp = mcp23017.MCP23017(i2c, plcConfig["icAdress"])
# property interface 8-bit
mcp.porta.mode = 0xff # Port A als Eingänge
mcp.portb.mode = 0x00 # Port B als Ausgänge

# PWD augang einschalten (PED signal null)
#led6.on()

# merker für toggle Bit
ledEin = 0
led8.off() # LED RED hochfahren Aus

def abfrage():
    #print(mcp.pin(0))
    
    #if not mcp.pin(0):
        #mcp.pin(8, value = 1)
    #else:
        #mcp.pin(8, value = 0)
    #global input

    if 'I1' in input:
        if not mcp.pin(5):
            input['I1'] = '1'
        else:
            input['I1'] = '0'
         
    #if sw2.value() == 0:
        #input['I2'] = '1'
    #else:
        #input['I2'] = '0'
    
    if 'I2' in input:
        if not mcp.pin(4):
            input['I2'] = '1'
        else:
            input['I2'] = '0'
    
    if 'I3' in input:
        if not mcp.pin(3):
            input['I3'] = '1'
        else:
            input['I3'] = '0'
    
    if 'I4' in input:
        if not mcp.pin(2):
            input['I4'] = '1'
        else:
            input['I4'] = '0'
    
    if 'I5' in input:
        if not mcp.pin(1):
            input['I5'] = '1'
        else:
            input['I5'] = '0'
    
    if 'I6' in input:
        if not mcp.pin(0):
            input['I6'] = '1'
        else:
            input['I6'] = '0'
    
    if 'Q1' in output:
        if output['Q1'] == '1':
            led1.on()
            mcp.pin(8, value = 1)
        else:
            led1.off()
            mcp.pin(8, value = 0)
    
    if 'Q2' in output:
        if output['Q2'] == '1':
            led2.on()
            mcp.pin(9, value = 1)
        else:
            led2.off()
            mcp.pin(9, value = 0)
    
    if 'Q3' in output:
        if output['Q3'] == '1':
            led3.on()
            mcp.pin(10, value = 1)
        else:
            led3.off()
            mcp.pin(10, value = 0)
    
    if 'Q4' in output:
        if output['Q4'] == '1':
            led4.on()
            mcp.pin(11, value = 1)
        else:
            led4.off()
            mcp.pin(11, value = 0)
    # Led RED neben grün    
    if 'Q5' in output:
        if output['Q5'] == '1':
            led8.on()
        else:
            led8.off()
            
    global ledEin
    if ledEin == 0:
        led5.off()
        led6.off()
        ledEin = 1
        return None
    if ledEin == 1:
        led5.on()
        led6.on()
        ledEin = 0
        return None
    
    led7.off()
    
    
def block_and(blockNr ,daten):
    l_add= []
    for key in daten:
        if key[:1] == 'B':
            #print(key)
            global block
            value = block[key]
        if key[:1] == 'I':
            #print(key)
            global input
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        l_add.append(value)

    result = l_add.count('1')

    if result == len(l_add):
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_or(blockNr ,daten):
    l_add= []
    for key in daten:
        if key[:1] == 'B':
            #print(key)
            global block
            value = block[key]
        if key[:1] == 'I':
            #print(key)
            global input
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        l_add.append(value)

    result = l_add.count('1')

    if result > 0:
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_compare(blockNr, daten, art):
    global block, cud, ton, tof, mw
    in1 = 0
    in2 = 0
    
    # IN1 daten[0]
    strIn1 = str(daten[0])
    if strIn1.isdigit():
        in1 = int(daten[0])
    else:
        if 'MW' in daten[0]:     
            in1 = mw[daten[0]]
        if 'CUD' in daten[0]:     
            in1 = cud[daten[0]]['actualValue']
        if 'TON' in daten[0]:     
            in1 = ton[daten[0]]['actualTime']
        if 'TOF' in daten[0]:     
            in1 = tof[daten[0]]['actualTime']
    
    # IN2 daten[1]
    strIn2 = str(daten[1])
    if strIn2.isdigit():
        in2 = int(daten[1])
    else:
        if 'MW' in daten[1]:     
            in2 = mw[daten[1]]
        if 'CUD' in daten[1]:
            in2 = cud[daten[1]]['actualValue']
        if 'TON' in daten[1]:     
            in2 = ton[daten[1]]['actualTime']
        if 'TOF' in daten[1]:     
            in2 = tof[daten[1]]['actualTime']
    
    # Ausgang
    if art == 'LT':
        if in1 < in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}
    if art == 'LIT':
        if in1 <= in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}
    if art == 'GT':
        if in1 > in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}
    if art == 'GIT':
        if in1 >= in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}
    if art == 'IT':
        if in1 == in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}
    if art == 'NIT':
        if in1 != in2:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

def block_aritmetic(blockNr, daten, art, out):
    global block, cud, ton, tof, mw
    in2 = 0
    in3 = 0
    value = ''
    # abfrage Eingang 1
    if daten[0]:
        if 'B' in daten[0]:
            value = block[daten[0]]
    
    if value == '0':
        return { blockNr: '0'}
        
    # IN2 daten[1]
    strIn2 = str(daten[1])
    if strIn2.isdigit():
        in2 = int(daten[1])
    else:
        if 'MW' in daten[1]:     
            in2 = mw[daten[1]]
        if 'CUD' in daten[1]:     
            in2 = cud[daten[1]]['actualValue']
        if 'TON' in daten[1]:     
            in2 = ton[daten[1]]['actualTime']
        if 'TOF' in daten[1]:     
            in2 = tof[daten[1]]['actualTime']
    
    # IN3 daten[2]
    strIn3 = str(daten[2])
    if strIn3.isdigit():
        in3 = int(daten[2])
    else:
        if 'MW' in daten[2]:     
            in3 = mw[daten[2]]
        if 'CUD' in daten[2]:
            in3 = cud[daten[2]]['actualValue']
        if 'TON' in daten[2]:     
            in3 = ton[daten[2]]['actualTime']
        if 'TOF' in daten[2]:     
            in3 = tof[daten[2]]['actualTime']
    
    # Ausgang
    if art == 'ADD':
        mw[out] = int(in2 + in3)
        return { blockNr: '1'}
    if art == 'SUB':
        mw[out] = int(in2 - in3)
        return { blockNr: '1'}
    if art == 'MUL':
        mw[out] = int(in2 * in3)
        return { blockNr: '1'}
    if art == 'DIV':
        # neu 1.11.21
        if in2 == 0 or in3 == 0:
            mw[out] = 0
            return { blockNr: '1'}
        mw[out] = int(in2 / in3)
        return { blockNr: '1'}

def block_move(blockNr, daten, out):
    global block, cud, ton, tof, mw
    in2 = ''
    value = ''
    # abfrage Eingang 1
    if daten[0]:
        if 'B' in daten[0]:
            value = block[daten[0]]
    # neu 1.11.21
    if not daten[0]:
        value = '0'
    
    if value == '0':
        return { blockNr: '0'}
        
    # IN2 daten[1]
    strIn2 = str(daten[1])
    if strIn2.isdigit():
        in2 = int(daten[1])
    else:
        if 'MW' in daten[1]:     
            in2 = mw[daten[1]]
        if 'CUD' in daten[1]:     
            in2 = cud[daten[1]]['actualValue']
        if 'TON' in daten[1]:     
            in2 = ton[daten[1]]['actualTime']
        if 'TOF' in daten[1]:     
            in2 = tof[daten[1]]['actualTime']
    
    # Ausgang
    if 'MW' in out:
        mw[out] = int(in2)
        return { blockNr: '1'}
    if 'CUD' in out:
        cud[out]['setValue'] = int(in2)
        return { blockNr: '1'}
    if 'TON' in out:     
        ton[out]['paramter'] = int(in2)
        return { blockNr: '1'}
    if 'TOF' in out:     
        tof[out]['paramter'] = int(in2)
        return { blockNr: '1'}
    # neu 10.11.21 wenn keine Angebe
    return { blockNr: '0'}

def block_ip(blockNr ,daten, ipNr):
    global block, input, ip
    inputListe= []
    for key in daten:
        if key[:1] == 'B':
            value = block[key]
        if key[:1] == 'I':
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        inputListe.append(value)

    if inputListe[0] == '0':
        ip[ipNr] = '0'
        
    if ip[ipNr] == '0' and inputListe[0] == '1':
        ip[ipNr] = '1'
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_cud(blockNr ,daten, cudNr, parameter1, parameter2):
    global block, input, cud
    inputListe= []
    for key in daten:
        if key[:1] == 'B':
            value = block[key]
        if key[:1] == 'I':
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        inputListe.append(value)
    # init
    if cud[cudNr]['init'] == '0':
        cud[cudNr]['presetValue'] = parameter1
        cud[cudNr]['actualValue'] = cud[cudNr]['presetValue']
        cud[cudNr]['init'] = '1'
    
    # reset
    if inputListe[2] == '1':
        cud[cudNr]['presetValue'] = parameter1
        cud[cudNr]['actualValue'] = cud[cudNr]['presetValue']
        cud[cudNr]['init'] = '1'
        
    # flanke count UP
    if inputListe[0] == '0':
        cud[cudNr]['countUpFlanke'] = '0'
    
    # flanke count DOWN
    if inputListe[1] == '0':
        cud[cudNr]['countDownFlanke'] = '0'
    
    # count UP
    if cud[cudNr]['countUpFlanke'] == '0' and inputListe[0] == '1':
        cud[cudNr]['countUpFlanke'] = '1'
        cud[cudNr]['actualValue'] += 1
    
    # count DOWN
    if cud[cudNr]['countDownFlanke'] == '0' and inputListe[1] == '1':
        cud[cudNr]['countDownFlanke'] = '1'
        cud[cudNr]['actualValue'] -= 1
    
    # Block Output
    cud[cudNr]['setValue'] = parameter2
    if cud[cudNr]['actualValue'] >= cud[cudNr]['setValue']:
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_inv(blockNr ,daten):
    l_add= []
    for key in daten:
        if key[:1] == 'B':
            #print(key)
            global block
            value = block[key]
        if key[:1] == 'I':
            #print(key)
            global input
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        l_add.append(value)

    result = l_add.count('1')

    if result > 0:
        return { blockNr: '0'}
    else:
        return { blockNr: '1'}

def block_sr(blockNr ,datenInput, srNr):
    global block, input, sr
    inputListe= []
    for key in datenInput:
        if key[:1] == 'B':
            value = block[key]
        if key[:1] == 'I':
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        inputListe.append(value)
        
    if inputListe[0] == '1':
        sr[srNr] = '1'
    if inputListe[1] == '1':
        sr[srNr] = '0'
        
    if sr[srNr] == '1':
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_ton(blockNr ,daten, tonNr, parameter1):
    global block, input, ton
    l_add= []
    tonEin = False
    for key in daten:
        if key[:1] == 'B':
            value = block[key]
        if key[:1] == 'I':
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        l_add.append(value)

    result = l_add.count('1')

    if result == len(l_add):
        #return { blockNr: '1'}
        tonEin = True
    else:
        #return { blockNr: '0'}
        tonEin = False
    # init Wert vom plc proramm kann dann überschrieben werden
    if not ton[tonNr]['paramter']:
        ton[tonNr]['paramter'] = parameter1
    ton[tonNr]['setTime'] = ton[tonNr]['paramter']

    if not tonEin and ton[tonNr]['isWork'] == '1':
        ton[tonNr]['isWork'] = '0'
        
    # alt
    '''if tonEin and ton[tonNr]['isWork'] == '0':
        ton[tonNr]['actualTime']  = 0
        ton[tonNr]['startTime'] = time.ticks_ms()
        ton[tonNr]['isWork'] = '1'

    if tonEin and ton[tonNr]['isWork'] == '1':
        if ton[tonNr]['actualTime'] <= ton[tonNr]['setTime']:
            ton[tonNr]['actualTime'] = time.ticks_ms() - ton[tonNr]['startTime']'''
    
    # neu 4.11.21
    if tonEin and ton[tonNr]['isWork'] == '0':
        ton[tonNr]['actualTime']  = 0
        ton[tonNr]['startTime'] = 0
        ton[tonNr]['isWork'] = '1'

    if tonEin and ton[tonNr]['isWork'] == '1':
        if ton[tonNr]['actualTime'] <= ton[tonNr]['setTime']:
            ton[tonNr]['actualTime'] += cyklus_ms
    
    if tonEin and ton[tonNr]['actualTime'] >= ton[tonNr]['setTime']:
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}

def block_tof(blockNr ,daten, tofNr, parameter1):
    global block, input, tof
    l_add= []
    tofEin = False
    for key in daten:
        if key[:1] == 'B':
            value = block[key]
        if key[:1] == 'I':
            value = input[key]
        # neu 1.11.21
        if not key:
            value = '0'
        l_add.append(value)

    result = l_add.count('1')

    if result == len(l_add):
        #return { blockNr: '1'}
        tofEin = True
    else:
        #return { blockNr: '0'}
        tofEin = False
    # init Wert vom plc proramm kann dann überschrieben werden
    if not tof[tofNr]['paramter']:
        tof[tofNr]['paramter'] = parameter1
    tof[tofNr]['setTime'] = tof[tofNr]['paramter']

    if not tofEin and tof[tofNr]['isWork'] == '1' and tof[tofNr]['actualTime'] >= tof[tofNr]['setTime']:
        tof[tofNr]['isWork'] = '0'

    if tofEin and tof[tofNr]['isWork'] == '0':
        tof[tofNr]['actualTime']  = 0
        #tof[tofNr]['startTime'] = time.ticks_ms()
        tof[tofNr]['isWork'] = '1'
        #print("tof ein")
    
    # alt
    '''if tofEin:
        tof[tofNr]['startTime'] = time.ticks_ms()
        
    if not tofEin and tof[tofNr]['isWork'] == '1':
        if tof[tofNr]['actualTime'] <= tof[tofNr]['setTime']:
            tof[tofNr]['actualTime'] = time.ticks_ms() - tof[tofNr]['startTime']'''

    # neu 4.11.21
    if tofEin:
        tof[tofNr]['startTime'] = 0
        
    if not tofEin and tof[tofNr]['isWork'] == '1':
        if tof[tofNr]['actualTime'] <= tof[tofNr]['setTime']:
            tof[tofNr]['actualTime'] += cyklus_ms
    
    if tofEin or tof[tofNr]['isWork'] == '1':
        return { blockNr: '1'}
    else:
        return { blockNr: '0'}
    
def output_update(blockNr, outputNr, value):
     global output, block
     # neu 1.11.21 wenn in1 keine daten enhält
     if not value:
         wert = {outputNr: '0'}
         output.update(wert)
         return { blockNr: '0'} 
     
     wert = {outputNr: block[value]}
     output.update(wert)
     if block[value] == '1':
         return { blockNr: '1'}
     else:
         return { blockNr: '0'}
         
# Bearbeitung Block Programm

fertig = True
#sd2 = copy.deepcopy(sd)
sd2 = deepcopy(sd)

print("start")

timeCyklusStart = time.ticks_ms()
cyklusCounter = 0
cyklusListe = []
cyklus_ms = 0

while fertig:
    #print("start")
    abfrage()
    
    if sd2:
        daten = sd2.pop()
        #Liste erzeugen
        liste_input = []
        blArt = ''
        blNr = ''
        tonNr = ''
        tofNr = ''
        parameter1 = ''
        parameter2 = ''
        srNr = ''
        ipNr = ''
        cudNr = ''
        out = ''
        #print(daten)
        if 'IN1' in daten:
            liste_input.append(daten['IN1'])
        if 'IN2' in daten:
            liste_input.append(daten['IN2'])
        if 'IN3' in daten:
            liste_input.append(daten['IN3'])
        if 'OUT' in daten:
            out = daten['OUT']
        if 'TONNR' in daten:
            tonNr = daten['TONNR']
            parameter1 = daten['PARAMETER1']
        if 'TOFNR' in daten:
            tofNr = daten['TOFNR']
            parameter1 = daten['PARAMETER1']
        if 'SRNR' in daten:
            srNr = daten['SRNR']
            #print(daten)
        if 'IPNR' in daten:
            ipNr = daten['IPNR']
        if 'CUDNR' in daten:
            cudNr = daten['CUDNR']
            parameter1 = daten['PARAMETER1']
            parameter2 = daten['PARAMETER2']
        for key, value in daten.items():
            if value == 'AND':
                blArt = value
                blNr = key
            if value == 'OR':
                blArt = value
                blNr = key
            if value == 'ZUW':
                blArt = value
                blNr = key
            if value == 'INPUT':
                blArt = value
                blNr = key
            if value == 'TON':
                blArt = value
                blNr = key
            if value == 'TOF':
                blArt = value
                blNr = key
            if value == 'SR':
                blArt = value
                blNr = key
            if value == 'INV':
                blArt = value
                blNr = key
            if value == 'IP':
                blArt = value
                blNr = key
            if value == 'CUD':
                blArt = value
                blNr = key
            if value == 'LT':
                blArt = value
                blNr = key
            if value == 'LIT':
                blArt = value
                blNr = key
            if value == 'GT':
                blArt = value
                blNr = key
            if value == 'GIT':
                blArt = value
                blNr = key
            if value == 'IT':
                blArt = value
                blNr = key
            if value == 'NIT':
                blArt = value
                blNr = key
            if value == 'ADD':
                blArt = value
                blNr = key
            if value == 'SUB':
                blArt = value
                blNr = key
            if value == 'MUL':
                blArt = value
                blNr = key
            if value == 'DIV':
                blArt = value
                blNr = key
            if value == 'MOVE':
                blArt = value
                blNr = key
        if blArt == 'AND':
            bl = block_and(blNr, liste_input)
            block.update(bl)
        if blArt == 'OR':
            bl = block_or(blNr, liste_input)
            block.update(bl)
        if blArt == 'INPUT':
            bl = block_and(blNr, liste_input)
            block.update(bl)
        if blArt == 'TON':
            bl = block_ton(blNr, liste_input, tonNr, parameter1)
            block.update(bl)
        if blArt == 'TOF':
            bl = block_tof(blNr, liste_input, tofNr, parameter1)
            block.update(bl)
        if blArt == 'SR':
            bl = block_sr(blNr, liste_input, srNr)
            block.update(bl)
        if blArt == 'INV':
            bl = block_inv(blNr, liste_input)
            block.update(bl)
        if blArt == 'IP':
            bl = block_ip(blNr, liste_input, ipNr)
            block.update(bl)
        if blArt == 'CUD':
            bl = block_cud(blNr, liste_input, cudNr, parameter1, parameter2)
            block.update(bl)
        if blArt == 'LT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'LIT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'GT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'GIT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'IT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'NIT':
            bl = block_compare(blNr, liste_input, blArt)
            block.update(bl)
        if blArt == 'ADD':
            bl = block_aritmetic(blNr, liste_input, blArt, out)
            block.update(bl)
        if blArt == 'SUB':
            bl = block_aritmetic(blNr, liste_input, blArt, out)
            block.update(bl)
        if blArt == 'MUL':
            bl = block_aritmetic(blNr, liste_input, blArt, out)
            block.update(bl)
        if blArt == 'DIV':
            bl = block_aritmetic(blNr, liste_input, blArt, out)
            block.update(bl)
        if blArt == 'MOVE':
            bl = block_move(blNr, liste_input, out)
            block.update(bl)
        if blArt == 'ZUW':
            bl = output_update(blNr, daten['OUT'], daten['IN1'])
            block.update(bl)
    
    #time.sleep(0.05)
              
    if not sd2:
        sd2 = deepcopy(sd)
        
        # zyklus ms
        # wenn tick_ms overflow
        if time.ticks_ms() < timeCyklusStart:
            pass
        else:
            cyklus_ms = time.ticks_ms() - timeCyklusStart
            
        cyklusListe.append(cyklus_ms)
        timeCyklusStart = time.ticks_ms()
        cyklusCounter += 1
        
        if cyklusCounter >= 1:
            print(cyklusListe)
            cyklusListe = []
            cyklusCounter = 0
            
        #sd2 = copy.deepcopy(sd)
        #fertig = False
    #print(sr['SR1'])
    #print(time.clock())
    #print(output['Q1'])