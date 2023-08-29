import json
import os


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

runwayData = {}
sctList = os.listdir('./sct')
for each in sctList:
    if each[-3:]!='sct':
        continue
    with open('./sct/' + each, mode='r') as f:
        orgData = f.read()

        orgData = orgData[orgData.find('[RUNWAY]') + 9:]
        orgData = orgData[:orgData.find('[')]
        orgData = orgData.split('\n')
        for eo in orgData:
            if eo == '':
                continue
            spl = eo.split(' ')
            if spl[8] not in runwayData:
                runwayData[spl[8]] = {}
            runwayData[spl[8]][spl[0]] = [convertCord(spl[4]),convertCord(spl[5]),convertCord(spl[6]),convertCord(spl[7])]
            runwayData[spl[8]][spl[1]] = [convertCord(spl[6]),convertCord(spl[7]),convertCord(spl[4]), convertCord(spl[5])]

with open('runways.json','w')as f:
    json.dump(runwayData,f)