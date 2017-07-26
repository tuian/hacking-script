import hashlib   
import re

month = ['01','02','03','04','05','06','07','08','09','10','11','12']

def days():
        days_tmp = range(10,32)
        L=[]
        for i in days_tmp:
                tmp = str(i)
                L.append(tmp)
        days = month+L
        return days
def years():
        year = range(2000,2018)
        Y=[]
        for i in year:
                tmp = str(i)
                Y.append(tmp)
        return Y
if __name__ == "__main__":
        year = years()
        day = days()
        A=[]
        for i in year:
                for j in month:
                        for k in day:
                                tmp = i+j+k
                                A.append(tmp)
        for i in A:
                src = i
                m2 = hashlib.md5()   
                m2.update(src)   
                ss = m2.hexdigest()
                if (re.findall(re.compile(r'c5e61e44f8d'), ss)):
                        print ss,src