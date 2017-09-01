@echo off
TITLE Set forced through the VPN to the Internet , plz run as administrator!  by t00ls.net
:menu
echo.
echo ===============================================================================
echo.
echo 1. Set forced through the VPN to the Internet , plz run as administrator
echo 2. Delete your setttings in 1 , plz run as administrator
echo 3. Query your settings IP
echo 4. exit
echo.                                                                by t00ls.net
echo.

set /p select=plz select:  
if /i "%select%"=="1" goto 1
if /i "%select%"=="2" goto 2
if /i "%select%"=="3" goto 3
if /i "%select%"=="4" goto 4
echo error select&pause&%0
:1
echo.
echo  Examples:
echo          10.0.0.1 or 10.0.0.1-10.0.0.254 or 10.0.0.1/24
echo          10.0.0.1,192.168.1.1,10.10.10.0/24
echo          use , to separate multiple IPs
echo.
set /p ip=Set Your IP Address: 
echo netsh advfirewall set allprofiles firewallpolicy allowinbound,blockoutbound
netsh advfirewall set allprofiles firewallpolicy allowinbound,blockoutbound
echo netsh advfirewall firewall add rule name="allowvpn1" dir=out action=allow enable=yes remoteip="%ip%"
netsh advfirewall firewall add rule name="allowvpn1" dir=out action=allow enable=yes remoteip="%ip%"
echo netsh advfirewall firewall add rule name="allowvpnremote1" dir=out action=allow enable=yes interfacetype=ras
netsh advfirewall firewall add rule name="allowvpnremote1" dir=out action=allow enable=yes interfacetype=ras
goto menu

:2
echo.
echo netsh advfirewall set allprofiles firewallpolicy allowinbound,allowoutbound
netsh advfirewall set allprofiles firewallpolicy allowinbound,allowoutbound
echo netsh advfirewall firewall delete rule name="allowvpn1"
netsh advfirewall firewall delete rule name="allowvpn1"
echo netsh advfirewall firewall delete rule name="allowvpnremote1"
netsh advfirewall firewall delete rule name="allowvpnremote1"
goto menu

:3
echo.
echo You have set the IP
netsh advfirewall firewall show rule name="allowvpn1" |findstr IP
if %errorlevel% NEQ 0 (echo.
echo ----Not Found IP----
echo.
echo.) else echo.
goto menu

:4
exit