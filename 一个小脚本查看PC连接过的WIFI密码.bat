@echo off

echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo +    0.请使用管理员权限运行,运行完请查看C盘的WifiPassword文件夹。 +              
echo +    1.WifiPassword中的文件请使用文本编辑工具打开。               +
echo +    2.打开WifiPassword中的文件后,keyMaterial标签里就是无线密码。 +
echo +    3.这是一个查询历史连接成功过的无线密码小程序,不是无线破解！  +
echo +                                           by:www.3ecurity.com   +
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ipconfig | find "无线局域网适配器 "
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

set /p WifiName=请输入【无线局域网适配器】后面的字符串:

md C:\WifiPassword

netsh wlan export  profile interface=%WifiName% key=clear folder=C:\WifiPassword

echo 请按任意键退出:)

Set /p Enter=""