rem 关闭智能卡服务

net stop SCardSvr

net stop SCPolicySvc

sc config SCardSvr start= disabled

sc config SCPolicySvc start= disabled
rem 开启服务

net start MpsSvc
rem 开机启动

sc config MpsSvc start= auto
rem 启用防火墙

netsh advfirewall set allprofiles state on
rem 屏蔽端口

netsh advfirewall firewall add rule name="deny udp 137 " dir=in protocol=udp localport=137 action=block

netsh advfirewall firewall add rule name="deny tcp 137" dir=in protocol=tcp localport=137 action=block

netsh advfirewall firewall add rule name="deny udp 138" dir=in protocol=udp localport=138 action=block

netsh advfirewall firewall add rule name="deny tcp 138" dir=in protocol=tcp localport=138 action=block

netsh advfirewall firewall add rule name="deny udp 139" dir=in protocol=udp localport=139 action=block

netsh advfirewall firewall add rule name="deny tcp 139" dir=in protocol=tcp localport=139 action=block

netsh advfirewall firewall add rule name="deny udp 445" dir=in protocol=udp localport=445 action=block

netsh advfirewall firewall add rule name="deny tcp 445" dir=in protocol=tcp localport=445 action=block


pause