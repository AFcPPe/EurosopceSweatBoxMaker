import json

def isRNAV(each):
    star = each[4]
    star = star.split(' ')
    if len(star)<2:
        return False
    if len(star[-2])<2:
        return False
    if star[-2][:2] !='FI' and star[-2][:2] !='FF':
        return False
    return True

with open('sct/ZBBB.ese','r')as f:
    data = f.read()
    data = data[data.find('[SIDSSTARS]')+11:].split('\n')

result = {}

for each in data:
    if each == '':
        continue
    if each[:3]=='SID':
        continue
    if each[:3]=='STA':
        each = each.split(':')
        if each[1] not in result:
            result[each[1]]={}
        if each[2] not in result[each[1]]:
            result[each[1]][each[2]] = {}
        if not isRNAV(each):
            continue
        if each[3]=='RV':
            continue
        result[each[1]][each[2]][each[3]] = each[4]
with open('STARS.json','w')as f:
    json.dump(result,f)
