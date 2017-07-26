#coding=utf-8
print '姓名是三字或更多，请在名后面加-，在-后面添加名的首字母，比如姓名:wangbadan：'
print '姓:wang'
print '名:badan-bd'
print '2字正常输入就可以了'

#信息设置区

str1 = raw_input('姓:')
str2 = raw_input('名:')
str3 = raw_input('手机:')
str4 = raw_input('QQ:')
str5 = str(raw_input('年月日(19890507):'))
str6 = raw_input('域名(www.baidu.com):')
str7 = ('123','123456','000','666','888','8888','888888','123..','!@#','~!@','~!@#','issb','likemakelove','iloveyou','loveyou','admin','system','gl','guanli','manager')#可自行添加
arr1 = {1:'!',2:'@',3:'#',4:'$',5:'%',6:'^',7:'&',8:'*',9:'(',0:')'}
dic = []
tdic = []
ttdic = []
tttdic = []

#信息加工区

if str1!="":
	str1_a=str1[:1]							#截取姓首字母
else:
	print("必须输入姓")
if str2!="":
	if str2.find('-')>0:
		str2_a=str2[str2.find('-')+1:]
		str2=str2[:str2.find('-')]
	else:
		str2_a=str2[:1]						#截取名首字母
if str3!="":
	str3_a=str3[-8:]						#截取后8位
	str3_b=str3[-6:]						#截取后6位
	str3_c=str3[:6]							#截取前6位
else:
	print("必须输入手机或座机")
if str5!="":
	str5_a=str5[:4] 		 				#截取前4为，年
	str5_b=str5[4:8]		 				#截取5-8位，月日
	for i in str5_a: 
		tdic.append(arr1[int(i)]) 		#年对应符号,eg:1986==!(*^
		tt=','
		str5_a1=tt.join(tdic)
	for i in str5_b:
		ttdic.append(arr1[int(i)])		#月日对应符号
		tt=','	
		str5_b1=tt.join(ttdic)
	for i in str5_b.strip('0'):
		tttdic.append(arr1[int(i)])		#没有0的月日对应符号
		tt=','
		str5_b2=tt.join(tttdic)
if str6!="":
	t1=str6.strip('http://').split('.')	#去除[http://]并已点分割域名
	if t1[0]=='www':
		str6_a=''								#如果二级域名是www清除
		str6_b=t1[1]							#截取主域名字符
		str6_c=t1[2] 						#截取域名后缀
	else:
		str6_a=t1[0]							#截取二级域名
		str6_b=t1[1]							#截取主域名字符
		str6_c=t1[2]							#截取域名后缀

#手写规则区

dic.append(str1+str3)									#姓加手机
dic.append(str1+str3_a) 								#姓名加手机后8位
dic.append(str1+str3_b)								#姓名加手机后6为
dic.append(str1+str3_c)								#姓名加手机前6位
dic.append(str1+str4)									#姓加QQ
dic.append(str1+str5)									#姓加生日
dic.append(str1+str5[2:]) 							#姓名加生日不要前2位
dic.append(str1+str5_a+str5_b.replace('0',''))	#姓加生日，日月没0
dic.append(str1+str5_a)								#姓名加年
dic.append(str1+str5_b)								#姓加月日
dic.append(str1+str5_b.replace('0',''))			#姓加日月没0
#
dic.append(str1+str2)						#姓名
dic.append(str1+str2+str3)				#姓名加手机
dic.append(str1+str2+str3_a) 			#姓名加手机后8位
dic.append(str1+str2+str3_b)				#姓名加手机后6为
dic.append(str1+str2+str3_c)				#姓名加手机前6位
dic.append(str1+str2+str4)				#姓名加QQ
dic.append(str1+str2+str5)				#姓名加生日
dic.append(str1+str2+str5[2:]) 			#姓名加生日不要前2位
dic.append(str1+str2+str5_a) 			#姓名加年
dic.append(str1+str2+str5_b) 			#姓名加月日
dic.append(str1+str2+str5_b.replace('0',''))	#姓名加月日没有0
dic.append(str1+str2+str5_a1) 			#姓名加年对应符号
dic.append(str1+str2+str5_b1) 			#姓名加日月对应符号
dic.append(str1+str2+str5_b2) 			#姓名加日月对应符号没有0
dic.append(str1+str2+str6_a) 			#姓名加二级域名
dic.append(str1+str2+str6_b) 			#姓名加主域名字符
#
dic.append(str1_a+str2_a+str3) 			#姓名首字母加手机
dic.append(str1_a+str2_a+str3_a) 		#姓名首字母加手机后8位
dic.append(str1_a+str2_a+str3_b)		#姓名加字母手机后6为
dic.append(str1_a+str2_a+str3_c)		#姓名加字母手机前6位
dic.append(str1_a+str2_a+str4) 			#姓名首字母加QQ
dic.append(str1_a+str2_a+str5) 			#姓名首字母加生日
dic.append(str1_a+str2_a+str5[2:]) 		#姓名首字母加生日不要前2位
dic.append(str1_a+str2_a+str5_a) 		#姓名首字母加年
dic.append(str1_a+str2_a+str5_b)		#姓名首字母加月日
dic.append(str1_a+str2_a+str5_b.replace('0',''))#姓名首字母加月日没有0
dic.append(str1_a+str2_a+str5_a1) 		#姓名首字母加年对应符号
dic.append(str1_a+str2_a+str5_b1) 		#姓名首字母加日月对应符号
dic.append(str1_a+str2_a+str5_b2) 		#姓名首字母加日月对应符号没有0
dic.append(str1_a+str2_a+str6_a) 		#姓名首字母加二级域名
dic.append(str1_a+str2_a+str6_b) 		#姓名首字母加主域名字符
dic.append(str1_a+str2_a+str6_a+str6_b+str6_c)	#姓名首字母加域名不要点
dic.append(str1_a+str2_a+str6_a+'.'+str6_b+'.'+str6_c) #姓名首字母加域名带点
for hz in str7:
	dic.append(str1_a+str2_a+hz)
	dic.append(str1+str2+hz)
	dic.append(str6_b+hz)
print '***************************Mdic start*******************************'
for i in dic:
	print i




