import json
import os

files = os.listdir('./sct/')
result = {}
for each in files:
    if each[-3:]=='sct':
        with open('sct/'+each) as f:
            data = f.read()
        data = data[data.find('[FIX')+7:]
        data = data[:data.find('[')]
        data = data.split('\n')
        result[each[:2]] = {}
        for e in data:
            if len(e)==0:
                continue
            if e[0] ==';':
                continue
            line = e.split(' ')
            result[each[:2]][line[0]] = [line[1],line[2]]
with open('Fixes.json','w')as f:
    json.dump(result,f)
