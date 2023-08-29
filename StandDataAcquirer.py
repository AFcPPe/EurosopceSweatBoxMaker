import json
import os

standData = {}

sctList = os.listdir('./sct')
for each in sctList:
    with open('./sct/' + each, mode='r') as f:
        orgData = f.read()

        orgData = orgData[orgData.find('[FREETEXT]') + 11:]
        orgData = orgData[:orgData.find('[')]
        orgData = orgData.split('\n')
        for aee in orgData:
            if aee == '':
                continue
            splData = aee.split(':')

            if len(splData) != 4:
                continue
            if len(splData[2]) != 4:
                continue
            if not splData[3].isdigit():
                continue
            if splData[2] not in standData:
                standData[splData[2]] = {}

            standData[splData[2]][splData[3]] = [splData[0], splData[1]]
with open('./stands.json', mode='w') as f:
    json.dump(standData, f)
