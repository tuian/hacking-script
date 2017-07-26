#coding=utf-8
'python版本小葵转化工具'
import base64
import md5
import urllib

def toHex(input):
    payload = ""
    for i in input:
        payload += hex(ord(i))[2:]
#hex(ord(i))为\0x68,0x64的形式，每个字符用1个字节存储
    return "0x"+payload

def toAscii(input):
    payload = ""
    for i in input:
        payload += str((ord(i)))+" "
    return payload

def toURL(input):
    payload = ""
    for i in input:
        payload += "%"+hex(ord(i))[2:]
    return payload

def toMd5(input):
    m = md5.new()
    m.update(input)
    payload = m.hexdigest()
    return payload

def toBase64(input):
    return base64.b64encode(input)

def Base64_decode(input):
    missing_padding = 4 - len(input) % 4
    if missing_padding:
        input += b'='* missing_padding
    return base64.decodestring(input)
    
if __name__=="__main__":
    while True:
        input = raw_input("please input the string:")
        print "Hex:",toHex(input)
        print "Ascii:",toAscii(input)
        print u"URL格式:",toURL(input)
        print "MD5_32:",toMd5(input)
        print "Base64:",toBase64(input)
        print u"Base64解密",Base64_decode(input)
        raw_input("please click 'enter' key ")