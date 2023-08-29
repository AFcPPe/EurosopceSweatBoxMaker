import json
from geographiclib.geodesic import Geodesic
from numpy import *
import numpy as np


def getHeading(poses):
    ins = Geodesic.WGS84.Inverse(float(poses[0][0]), float(poses[0][1]), float(poses[1][0]), float(poses[1][1]))
    return (ins['azi1'] + 360) % 360


def getpbh(heading):
    p = float(0) * 57.29578 / -360.0
    if p < 0:
        p += 1.0
    p *= 1024.0
    b = float(0) * 57.29578 / -360.0
    if b < 0:
        b += 1.0
    b *= 1024.0
    h = float(heading) * 57.29578 / 360.0 * 1024.0
    return (uint(p) << 22) | (uint(b) << 12) | (uint(h) << 2)


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
                 'HYT', 'CQH', 'EZY', 'BAW', 'RYR', 'CAF', 'OMA', 'CQN', 'CES', 'DKH', 'CNW', 'CJX','USAF']
    call = callsigns[int(np.random.rand() * callsigns.__len__() - 1)]

    sign = str(int(np.random.rand() * 8999 + 1000))
    return call + sign


def randType():
    typesWrong = ['B767', 'B757', 'B747', 'B320', 'A360', 'A738', 'A220', 'A35K', 'B77F']
    rate = int(np.random.rand() * 20)
    types = ['A320', 'A321', 'A319', 'A20N', 'A21N', 'A333', 'A343', 'A344', 'A345', 'A346', 'A359', 'A388',
             'B736', 'B737', 'B738', 'B744', 'B748', 'B752', 'B762', 'B77W', 'B788', 'MD12', 'MD11', 'MD82',
             'E195', 'A320', 'A320', 'B738', 'B738', 'A346', 'A346', 'A359', 'A359','J20','F35','F22']
    if rate == 3:
        types = typesWrong
    st = types[int(np.random.rand() * types.__len__() - 1)]
    return st


def getFP(airport):
    pass


def getPos(callsign, pos, alt, heading,SQK):
    return '@N:' + callsign + ':'+SQK+':1:' + pos[0] + ':' + pos[1] + ':' + str(alt) + ':0:' + getpbh(
        heading).__str__() + ':0'


def randSTAR(airport, runway):
    with open('STARS.json', 'r') as f:
        STARs = json.load(f)
    # print(STARs[airport])
    runwayD = runway[int(np.random.rand() * len(runway))]
    runwaySTAR: dict = STARs[airport][runwayD]
    listS = []
    for e in runwaySTAR:
        listS.append(e)
    if len(listS) == 1:
        return runwaySTAR[listS[0]]
    rander = listS[int(np.random.rand() * len(runwaySTAR))]
    return runwaySTAR[rander]


def getTwoFix(airport, star: str):
    if airport[:2] == 'ZU':
        airport = 'ZP' + airport
    lis = star.split(' ')
    with open('Fixes.json', 'r') as f:
        fixes = json.load(f)
    if len(lis) <= 1:
        return [[convertCord(fixes[airport[:2]][lis[0]][0]), convertCord(fixes[airport[:2]][lis[0]][1])],
                [convertCord(fixes[airport[:2]][lis[0]][0]), convertCord(fixes[airport[:2]][lis[0]][1])]]
    else:
        return [[convertCord(fixes[airport[:2]][lis[0]][0]), convertCord(fixes[airport[:2]][lis[0]][1])],
                [convertCord(fixes[airport[:2]][lis[1]][0]), convertCord(fixes[airport[:2]][lis[1]][1])]]


def setRunway(aip,runs):
    with open('runways.json','r')as f:
        runD = json.load(f)
        text = ''
        for each in runs:
            te = 'ILS'+each+':'+':'.join(runD[aip][each])+'\n'
            text+=te
    return text


def gen(airport, runway, count, sep, alt, aipAlt):
    SQK = 3000
    start = 0
    text = "PSEUDOPILOT:ALL\n"
    text = text + 'AIRPORT_ALT:' + str(int(aipAlt*3.2808399)) + '\n'
    text += setRunway(airport,runway)+'\n\n'
    for i in range(count):
        SQK+=1
        star = randSTAR(airport, runway)
        twoFix = getTwoFix(airport, star)
        cls = randCallsign()
        # print(cls+'   '+str(getHeading(twoFix)))

        text = text + getPos(cls, twoFix[0], alt, getHeading(twoFix),str(SQK)) + '\n'
        text = text + '$FP' + cls + ':*A:I:' + randType() + ':420:' + airport + ':1830:0:19700:' + airport + ':00:00:0:0:::' + star + '\n'
        text = text + '$ROUTE:' + star[star.find(' ') + 1:] + '\n'
        text = text + 'START:' + str(start) + '\n'
        # text = text+'DELAY:6:10\n'
        text = text + 'DELAY:1:2\n'
        text = text + 'REQALT::' + str(alt) + '\n\n\n'
        start += sep
    ressuf = int(np.random.rand() * 15165156165)
    with open('./result/' + airport +'_'+runway.__str__()+ '_APP' + str(ressuf) + '.txt', 'w') as f:
        f.write(text)


for i in range(10):
    gen('ZGGG', ['02R'], 20, 2, 14800, 15)