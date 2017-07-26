# coding:utf-8

routeList = []
with open('data.txt', mode='r') as file:
    for line in file:
        if 'Â·ÓÉµØÖ·' in line:
            if line.split(':')[1].strip('\n') not in routeList:
                routeList.append(line.split(':')[1].strip('\n'))
print len(routeList)
print routeList

routeFile = open('routeFile.txt', mode='a')
for route in routeList:
    routeFile.write(route + '\n')
routeFile.close()