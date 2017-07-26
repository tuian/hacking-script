@echo off
setlocal ENABLEDELAYEDEXPANSION

:get_USERDNSDOMAIN

if "%USERDOMAIN%"=="WORKGROUP" (
    echo [-] WORKGROUP environment
    set domain_type=workgroup
    goto :eof
)

if defined USERDOMAIN (
    if defined USERDNSDOMAIN (
        echo [-] current domain: %USERDOMAIN% [%USERDNSDOMAIN%]
        set domain_type=domain
        goto :eof
    )
)

call :del tmp
net config workstation /n>tmp 2>&1
findstr /c:"System error 1312 has occurred" tmp >nul && (
    echo [-] logon session does not exist, try next...
) || (
    findstr /c:"Workstation service is not started" tmp >nul && (
        echo [-] Workstation service is not started, try next...
    ) || (
        for /f "tokens=1-5" %%a in ('findstr /b /i /c:"workstation domain" tmp') do (
            if /i "%%a %%b %%c %%d"=="workstation domain dNS name" (
                set USERDNSDOMAIN=%%e
            ) else (
                set USERDOMAIN=%%c
            )
        )
        call :del tmp
        
        if "!USERDOMAIN!"=="WORKGROUP" (
            echo [-] WORKGROUP environment
            set domain_type=workgroup
            goto :eof
        )
        
        if defined USERDOMAIN (
            if defined USERDNSDOMAIN (
                echo [-] current domain: !USERDOMAIN! [!USERDNSDOMAIN!]
                set domain_type=domain
                goto :eof
            )
        )
    )
)
call :del tmp

call :found_under_path nltest.exe nltest
if defined nltest (
    "%nltest%" /domain_trusts >tmp 2>&1
    findstr /c:"Status = 1717" tmp >nul && (
        call :del tmp
        set USERDOMAIN=WORKGROUP
        echo [-] seems in WORKGROUP environment
        set domain_type=workgroup
        goto :eof
    ) || (
        for /f "tokens=2,3,4,5 delims=() " %%i in ('findstr /c:"(Primary Domain)" tmp') do (
            if "%%i"=="" (
                echo [-] could not get domain trust via nltest, try next...
            ) else (
                if "%%k %%l"=="NT 5" (
                    set USERDNSDOMAIN=%%j
                    set USERDOMAIN=%%i
                ) else if "%%j %%k"=="NT 4" (
                    if not defined USERDNSDOMAIN set USERDNSDOMAIN=%%i
                    if not defined USERDOMAIN set USERDOMAIN=%%i
                ) else if "%%j"=="MIT" (
                    if not defined USERDNSDOMAIN set USERDNSDOMAIN=%%i
                    if not defined USERDOMAIN set USERDOMAIN=%%i
                ) else if "%%j"=="DCE" (
                    if not defined USERDNSDOMAIN set USERDNSDOMAIN=%%i
                    if not defined USERDOMAIN set USERDOMAIN=%%i
                ) else (
                    echo [#] unknown trust type
                )
            )
            call :del tmp
            if defined USERDOMAIN (
                if defined USERDNSDOMAIN (
                    echo [-] current domain: !USERDOMAIN! [!USERDNSDOMAIN!]
                    set domain_type=domain
                    goto :eof
                )
            )
        )
    )
) else (
    echo [#] could not find nltest.exe
)

ipconfig /all>tmp 2>&1
findstr /c:"Primary Dns Suffix" tmp >nul && (
    for /f "tokens=2 delims=:" %%a in ('findstr /c:"Primary Dns Suffix" tmp') do (
        set ip_userdnsdomain=%%a
        set ip_userdnsdomain=!ip_userdnsdomain: =!
    )
    if defined USERDNSDOMAIN (
        if /i "%USERDNSDOMAIN%"=="!ip_userdnsdomain!" (
            set ip_userdnsdomain=
        ) else (
            echo [-] seems in %USERDNSDOMAIN% or !ip_userdnsdomain! domain
        )
    ) else (
        echo [-] maybe in !ip_userdnsdomain! domain
    )
) || (
    call :del tmp
    set USERDOMAIN=WORKGROUP
    echo [-] WORKGROUP environment
    set domain_type=workgroup
    goto :eof
)
call :del tmp

ver|findstr /c:"5." >nul && (
    echo [-] skip wmic method...
) || (
    for /f %%i in ('wmic computersystem get domain^|findstr /v /i domain') do (
        if not "%%i"=="" (
            if /i "%%i"=="WORKGROUP" (
                set USERDOMAIN=WORKGROUP
            ) else (
                set USERDNSDOMAIN=%%i
            )
        )
    )
)
call :del tmp

if "%USERDOMAIN%"=="WORKGROUP" (
    echo [-] WORKGROUP environment
    set domain_type=workgroup
    goto :eof
)

if defined USERDOMAIN (
    if defined USERDNSDOMAIN (
        echo [-] current domain: %USERDOMAIN% [%USERDNSDOMAIN%]
        goto :eof
    )
)

for /f %%a in ('reg query HKU^|findstr /v "DEFAULT S-1-5-18 S-1-5-19 S-1-5-20 Classes"^|findstr HKEY_USERS') do (
     for /f "tokens=1,3" %%i in ('reg query "%%a\Volatile Environment" 2^>nul^|findstr "USERDNSDOMAIN USERDOMAIN"') do (
        if not defined registry_line (
            set registry_line=1
        ) else (
            set /a registry_line=!registry_line!+1 >nul
        )
        if "%%i"=="USERDNSDOMAIN" (
            set /a DOMAIN_line=!registry_line!+1 >nul
            set DNS_temp=%%j
        )
        if "!DOMAIN_line!"=="!registry_line!" (
            if "%%i"=="USERDOMAIN" (
                if defined USERDOMAIN (
                    if /i "%%j"=="%USERDOMAIN%" set USERDNSDOMAIN=!DNS_temp!
                ) else (
                    set USERDOMAIN=%%j
                    set USERDNSDOMAIN=!DNS_temp!
                )
            )
        )
    )
)


if not defined USERDNSDOMAIN (
    if "%USERDOMAIN%"=="WORKGROUP" (
        echo [-] WORKGROUP environment
        set domain_type=workgroup
        goto :eof
    ) else if "%USERDOMAIN%"=="%COMPUTERNAME%" (
        echo [-] seems in a WORKGROUP environment
        set domain_type=workgroup
        goto :eof
    ) else (
        echo [-] current domain: %USERDOMAIN%
        echo [-] could not find any other domain info
        if defined ip_userdnsdomain (
            echo [-] maybe domain dns is %ip_userdnsdomain%
        )
        echo [-] regard as WORKGROUP environment
        set domain_type=workgroup
        goto :eof
    )
) else (
    if defined USERDOMAIN (
        echo [-] current domain: %USERDOMAIN% [%USERDNSDOMAIN%]
        set domain_type=domain
        goto :eof
    ) else (
        echo [-] current domain: %USERDNSDOMAIN%
        echo [-] could not find domain name, use %COMPUTERNAME% instead
        set USERDOMAIN=%COMPUTERNAME%
        set domain_type=domain
        goto :eof
    )
)
goto :eof


:del
if "%~1"=="" goto :eof
if exist %~1 del /f /q %~1 2>nul
shift /1
goto :del

:found_under_path
rem set %~2=%~f$PATH:1
rem goto :eof
for /l %%a in (1,1,20) do call :get_seperate_path %1 %2 %%a %2_tmp%random%
goto :eof
:get_seperate_path
for /f "delims=; tokens=%3" %%a in ("%path%") do (
        set %4=%%~fa
    if not defined %2 (
        if defined %4 (
            if "!%4:~-1!"=="\" set %4=!%4:~,-1!
            if exist "!%4!\%~1" (
                echo [-] found %~1 under !%4!
                set %2=!%4!\%~1
            )
        )
    )
    set %4=
)
goto :eof