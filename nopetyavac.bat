@echo off
REM Administrative check from here: https://stackoverflow.com/questions/4051883/batch-script-how-to-check-for-admin-rights
REM Vaccination discovered by twitter.com/0xAmit/status/879778335286452224
REM Batch file created by Lawrence Abrams of BleepingComputer.com. @bleepincomputer @lawrenceabrams

echo Administrative permissions required. Detecting permissions...
echo.
		
net session >nul 2>&1

if %errorLevel% == 0 (
	if exist C:\Windows\perfc (
		echo Computer already vaccinated for NotPetya/Petya/Petna/SortaPetya.
		echo.
	) else (
		echo This is a NotPetya/Petya/Petna/SortaPetya Vaccination file. Do not remove as it protects you from being encrypted by Petya. > C:\Windows\perfc
                echo This is a NotPetya/Petya/Petna/SortaPetya Vaccination file. Do not remove as it protects you from being encrypted by Petya. > C:\Windows\perfc.dll
                echo This is a NotPetya/Petya/Petna/SortaPetya Vaccination file. Do not remove as it protects you from being encrypted by Petya. > C:\Windows\perfc.dat

		attrib +R C:\Windows\perfc
                attrib +R C:\Windows\perfc.dll
                attrib +R C:\Windows\perfc.dat

		echo Computer vaccinated for current version of NotPetya/Petya/Petna/SortaPetya.
		echo.
	)
) else (
	echo Failure: You must run this batch file as Administrator.
)
  
pause
