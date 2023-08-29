import json
import time

import numpy as np

with open('./hxst.json', mode='r') as f:
    stands = json.load(f)

cuzs0 = ['26600', '29100', '31100', '33100', '35100', '37100', '39100', '41100']
cuzs1 = ['25600', '27600', '30100', '32100', '34100', '36100', '38100', '40100']
cuzsx = ['FL300', 'FL310', 'FL320', 'FL330', 'FL340', 'FL350', 'FL360', 'FL370', 'FL380', 'FL390', 'FL250', 'FL260',
         'FL270', 'FL280', 'FL290']

cuz = [cuzs0, cuzs1, cuzsx]

ICAO = 'VHHX'
np.random.seed(int(time.time()))
alt = 23


def convertCord(org: str):
    parts = org.split('.')
    lis1 = float(parts[2] + '.' + parts[3]) / 60
    lis2 = float(lis1 + int(parts[1])) / 60
    lis3 = lis2 + int(parts[0][1:])
    if parts[0][0] == 'N' or parts[0][0] == 'E':
        prefix = ''
    elif parts[0][0] == 'W' or parts[0][0] == 'S':
        prefix = '-'
    return prefix + str(lis3)


def randCallsign():
    callsigns = ['CSZ', 'CCA', 'CBJ', 'CSS', 'KLM', 'CHH', 'CSN', 'CUA', 'CXA', 'CKK', 'CAO', 'CNM', 'CPA', 'CPX',
                 'HYT', 'CQH', 'EZY', 'BAW', 'RYR', 'CAF', 'OMA', 'CQN', 'CES', 'DKH', 'CNW', 'CJX']
    call = callsigns[int(np.random.rand() * callsigns.__len__() - 1)]

    sign = str(int(np.random.rand() * 8999 + 1000))
    return call + sign


def randType():
    typesWrong = ['A737', 'B320', 'B333', 'B346', 'A360', 'A738', 'BMAX', 'B388', 'B77F']
    rate = int(np.random.rand() * 20)
    types = ['A320', 'A321', 'A319', 'A20N', 'A21N', 'A333', 'A343', 'A344', 'A345', 'A346', 'A359', 'A388',
             'B736', 'B737', 'B738', 'B744', 'B748', 'B752', 'B762', 'B77W', 'B788', 'MD12', 'MD11', 'MD82',
             'E195', 'A320', 'A320', 'B738', 'B738', 'A346', 'A346', 'A359', 'A359','F15','F16','FA18','F22',
             'F35','J20','SR22','C700','S92','S76','C40C','CL50']
    if rate <= 3:
        types = typesWrong
    st = types[int(np.random.rand() * types.__len__() - 1)]
    return st


def randPos(st):
    return '@N:' + callsi + ':2000:1:' + convertCord(st[0]) + ':' + convertCord(st[1]) + ':' + str(alt) + ':0:0:0:0'


def randFP():
    with open('ROUTE/'+ICAO+'.json', mode='r') as f:
        fp = json.load(f)[ICAO]

    routeNum = int(np.random.rand() * len(fp))
    altMode = int(np.random.rand() * 9)
    alts = 0
    if altMode >= 2:
        alts = cuz[fp[routeNum]['altType']][int(np.random.rand() * len(cuz[fp[routeNum]['altType']]))]
    if altMode == 0:
        alts = cuz[(fp[routeNum]['altType'] + 1) % 2][
            int(np.random.rand() * len(cuz[(fp[routeNum]['altType'] + 1) % 2]))]
    if altMode == 1:
        alts = cuz[2][int(np.random.rand() * len(cuz[2]))]
    rule = 'I'
    rate = int(np.random.rand() * 20)
    if rate == 5:
        rule = 'V'
    # if decide<3000
    return '$FP' + callsi + ':*A:' + rule + ':' + randType() + ':0:' + fp[routeNum][
        'dep'] + ':0000:0000:' + alts + ':' + fp[routeNum]['arr'] + ':00:00:0:0::/v/:' + fp[routeNum]['routes']

    # '@N:CSC9273:2000:1:40.082540:116.588411:0:0:0:0:0'

requiredNum = int(input('请输入你需要的数量：'))

for num in range(50):
    finalData = 'PSEUDOPILOT:ALL\nAIRPORT_ALT:' + str(alt)
    airp = stands[ICAO]
    standNum = []
    for stt in airp:
        standNum.append(stt)
    print(len(standNum))
    for i in range(requiredNum):
        callsi = randCallsign()
        randppp = int(np.random.rand() * len(standNum))
        posData = randPos(airp[standNum[randppp]])
        del (standNum[randppp])
        finalData += '\n' + posData
        # print(posData)
        FPData = randFP()
        finalData += '\n' + FPData + '\n'
    randsuf = int(np.random.rand() * 15165156165)

    with open('result/'+ICAO + '_TWR'+str(randsuf)+'.txt', mode='w') as f:
        f.write(finalData)

