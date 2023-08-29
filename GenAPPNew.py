import json

import numpy as np
from geographiclib.geodesic import Geodesic
from numpy import uint

cuzs = [['26600', '29100', '31100', '33100', '35100', '37100', '39100', '41100'],
        ['25600', '27600', '30100', '32100', '34100', '36100', '38100', '40100']]


def getHeading(poses):
    ins = Geodesic.WGS84.Inverse(float(poses[0][0]), float(poses[0][1]), float(poses[1][0]), float(poses[1][1]))
    return (ins['azi1'] + 360) % 360


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


def randType():
    typesWrong = ['B767', 'B757', 'B747', 'B320', 'A360', 'A738', 'A220', 'A35K', 'B77F']
    rate = int(np.random.rand() * 20)
    types = ['A320', 'A321', 'A319', 'A20N', 'A21N', 'A333', 'A343', 'A344', 'A345', 'A346', 'A359', 'A388',
             'B736', 'B737', 'B738', 'B744', 'B748', 'B752', 'B762', 'B77W', 'B788', 'MD12', 'MD11', 'MD82',
             'E195', 'A320']
    if rate == 3:
        types = typesWrong
    st = types[int(np.random.rand() * types.__len__() - 1)]
    return st


def randCallsign():
    callsigns = ['CSZ', 'CCA', 'CBJ', 'CSS', 'KLM', 'CHH', 'CSN', 'CUA', 'CXA', 'CKK', 'CAO', 'CNM', 'CPA', 'CPX',
                 'HYT', 'CQH', 'EZY', 'BAW', 'RYR', 'CAF', 'OMA', 'CQN', 'CES', 'DKH', 'CNW', 'CJX']
    call = callsigns[int(np.random.rand() * callsigns.__len__() - 1)]

    sign = str(int(np.random.rand() * 8999 + 1000))
    return call + sign


def replaceILS(data: dict, ICAO, runway) -> dict:
    retData = {}
    for each in data:
        rStr = data[each].replace(ICAO, f'ILS{runway}')
        retData[each] = rStr
    return retData


def getRelatedRouteAndSTAR(ICAO, runwayList):
    with open('TerminalLegs.json', 'r') as f:
        tmaData = json.load(f)
        STARs = {}
        for eachRunway in runwayList:
            STARs[eachRunway] = replaceILS(tmaData[ICAO]['STAR'][eachRunway], ICAO, eachRunway)
        # print(STARs)
    sieList = set()
    for each in STARs:
        eRunway = STARs[each]
        for eo in eRunway:
            sieList.add(eRunway[eo][:eRunway[eo].find(' ')])
    with open('./ROUTE/all.json', 'r') as f:
        routeData = json.load(f)
        routes = []
        for each in routeData:
            inR = routeData[each]
            if ICAO not in inR:
                continue
            for eachRoute in inR[ICAO]:
                sie = eachRoute['routes'][eachRoute['routes'].rfind(' ') + 1:]
                if sie in sieList and len(eachRoute['dep']) == 4:
                    routes.append(eachRoute)
    return STARs, routes


def getPos(callsign, pos, alt, heading, SQK):
    return '@N:' + callsign + ':' + SQK + ':1:' + pos[0] + ':' + pos[1] + ':' + str(alt) + ':0:' + getpbh(
        heading).__str__() + ':0'


def getFP(route, star, rwyName, starName, callsign):
    # print(route,star,rwyName,starName)
    crz = cuzs[route['altType']][int(np.random.rand() * len(cuzs[route['altType']]))]
    r = f"{route['routes']} {starName}/{rwyName}"
    return '$FP' + callsign + ':*A:I:' + randType() + ':0:' + route[
        'dep'] + ':0000:0000:' + crz + ':' + route['arr'] + ':00:00:0:0::/v/:' + r
    # pass


def getRoute(star):
    route = star[star.find(' ') + 1:]
    return f'$ROUTE:{route}'


def setRunway(aip, runs):
    with open('runways.json', 'r') as f:
        runD = json.load(f)
        text = ''
        for each in runs:
            te = 'ILS' + each + ':' + ':'.join(runD[aip][each]) + '\n'
            text += te
    return text


def gen(text, airplaneCount):
    for ii in range(airplaneCount):
        sqk = oct(SQK + ii)[2:]
        apid = int(np.random.rand() * len(airport))
        rwyid = int(np.random.rand() * len(stars[apid]))
        rwyName = list(stars[apid].keys())[rwyid]
        starid = int(np.random.rand() * len(stars[apid][rwyName]))
        starName = list(stars[apid][rwyName].keys())[starid]
        routeids = []
        starSie = stars[apid][rwyName][starName][:stars[apid][rwyName][starName].find(' ')]
        for j in range(len(route[apid])):
            r = route[apid][j]['routes']
            sie = r[r.rfind(' ') + 1:]
            if sie == starSie:
                routeids.append(j)
        if len(routeids) == 0:
            ii -= 1
            continue
        routeid = routeids[int(np.random.rand() * len(routeids))]
        twoFix = getTwoFix(airport[apid], stars[apid][rwyName][starName])
        callsign = randCallsign()

        textPos = getPos(callsign, twoFix[0], inAlt, getHeading(twoFix), sqk)
        textFP = getFP(route[apid][routeid], stars[apid][rwyName][starName], rwyName, starName, callsign)
        textRoute = getRoute(stars[apid][rwyName][starName])
        textStart = f'START:{start + ii * interval}'
        textDelay = 'DELAY:1:2'
        textReq = f'REQALT::{inAlt}'
        text += f'{textPos}\n{textFP}\n{textRoute}\n{textStart}\n{textDelay}\n{textReq}\n\n'
    ressuf = int(np.random.rand() * 15165156165)
    with open('./result/' + airport.__str__() + '_' + runwayList.__str__() + '_APP' + str(ressuf) + '.txt', 'w') as f:
        f.write(text)


if __name__ == '__main__':
    airport = ['ZGGG']
    runwayList = [['01','02R']]
    airplaneCount = 50
    count = 20
    interval = 2
    inAlt = 19700
    alt = 15.2
    # stars,route = getRelatedRouteAndSTAR(airport,runwayList)
    stars = []
    route = []
    SQK = 3000
    start = 0
    text = "PSEUDOPILOT:ALL\n"
    text = text + 'AIRPORT_ALT:' + str(int(alt * 3.2808399)) + '\n'
    for i in range(len(airport)):
        text += setRunway(airport[i], runwayList[i])
        dataS, dataR = getRelatedRouteAndSTAR(airport[i], runwayList[i])
        stars.append(dataS)
        route.append(dataR)
    text += '\n\n'
    for i in range(count):
        gen(text, airplaneCount)
