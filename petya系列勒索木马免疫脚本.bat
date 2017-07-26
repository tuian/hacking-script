@echo off
echo 请以管理员权限启动该免疫脚本..
echo.
                net session >nul 2>&1

if %errorLevel% == 0 (
        if exist C:\Windows\perfc (
                echo 已经创建过*Petya免疫文件.
                echo.
        ) else (
                echo 这是一个免疫NotPetya/Petya/Petna/SortaPetya勒索病毒的文件，不要删除，能避免电脑中招 by x > C:\Windows\perfc
                echo 这是一个免疫NotPetya/Petya/Petna/SortaPetya勒索病毒的文件，不要删除，能避免电脑中招 by x > C:\Windows\perfc.dll
                echo 这是一个免疫NotPetya/Petya/Petna/SortaPetya勒索病毒的文件，不要删除，能避免电脑中招 by x > C:\Windows\perfc.dat

                attrib +R C:\Windows\perfc
                attrib +R C:\Windows\perfc.dll
                attrib +R C:\Windows\perfc.dat

                echo 免疫类型：NotPetya/Petya/Petna/SortaPetya.
                echo.
        )
) else (
        echo 失败：请以管理员身份运行改程序
)
  
pause