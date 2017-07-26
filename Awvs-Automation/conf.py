#!/usr/bin/env python
# coding=utf-8

wvs_console = r'H:\Web Vulnerability Scanner 10\wvs_console.exe '  # wvs_console的路径

save_folder = r'H:\Awvs\Result\\'    # 保存记录的目录，后面如果需要对反斜杠转义，否则反斜杠对后面的单引号转义

url_txt = r'H:\Awvs\Url\1_url.txt'  # 待检测url文本

# wvs扫描语句（--不扫描当前目录以上的其他目录（二级目录有效），--启发式扫描）
scan_command = "/Scan %s /Profile default /ExportXML /SaveFolder %s --RestrictToBaseFolder=true " \
              "--ScanningMode=Heuristic"

# 邮箱
mail_host = "smtp.163.com"
mail_user = "123"	#发件帐号
mail_pass = "123"	#发件密码
mail_postfix = "163.com"
mail_list = ['123@qq.com']	#收件人
