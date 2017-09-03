::合并所有表
@echo off
del /f /q 1.sql
setlocal Enabledelayedexpansion
set  p=0
for /l %%i in (1,1,11) do (
        for /l %%j in (1,1,10) do (
                set /a p=!p!+1
                echo INSERT INTO qqinfo.dbo.quninfo^([QunNum],[MastQQ],[CreateDate],[Title],[Class],[QunText]^) SELECT [QunNum],[MastQQ],[CreateDate],[Title],[Class],[QunText] FROM QunInfo%%i.dbo.QunList!p!>>1.sql
                echo go>>1.sql
                )
        
        ) 
        
osql -E -i 1.sql