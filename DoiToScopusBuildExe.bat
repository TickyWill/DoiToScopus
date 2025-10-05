:: Creation: A. Chabli 2025-10-05
:: Refactoring: ................

@echo off 
Title DoiToScopus.exe making

:: Setting development branches
echo:
set /p "bp_branch=Enter BiblioParsing branch to import: "
echo:
set /p "bm_branch=Enter BiblioMeter branch to import: "
echo:
set /p "dts_branch=Enter DoiToScopus branch to import: "

:: Setting name of python program to launch the application
echo:
set /p "app_py=Enter name of program to launch application (case sensitive, ex: app.py or App.py): "

:: Setting exe version
echo:
set /p "exe_version=Enter DoiToScopus version (#.#.#): "
echo:

:: Setting useful editing parameters
set "TAB=   "

:: Setting useful directories
set "working_dir=%TEMP%\DoiToScopus.exe"
:: set "save_dir=C:\Program"
set "save_dir=%USERPROFILE%\DoiToScopus.exe"

:: Setting the name of the log file to debbug the executable making
set "LOG=%working_dir%\log.txt"

:: Creating a clean %working_dir%
echo Creating a clean %working_dir% directory
if exist %working_dir% (
    echo %TAB%%working_dir% exists and will be removed - Please wait...
    rmdir /s /q %working_dir%
    if not exist %working_dir% (
        echo %TAB%Existing %working_dir% removed
        ) else (
            echo %TAB%Unable to remove existing %working_dir%
            GOTO FIN
            ))
mkdir %working_dir%
if exist %working_dir% (
    echo ******* REPORT ON DoiToScopus EXECUTABLE MAKING ******* > %LOG%
    echo %working_dir% successfully created >> %LOG% 
    echo %TAB%%working_dir% successfully created
    echo:
) else (
    echo %TAB%Unable to create %working_dir%
    GOTO FIN)

:: Creating a venv
:: adapted from https://stackoverflow.com/questions/45833736/how-to-store-python-version-in-a-variable-inside-bat-file-in-an-easy-way?noredirect=1
echo Creating a virtual environment
cd %working_dir%
set "python_dir=%userprofile%\PyVersions\python3.9.7"
if exist %python_dir% ( 
    echo %TAB%%python_dir% will be used to build the venv
    echo:
    %python_dir%\python -m venv venv
) else (
    echo %TAB%Unable to access %python_dir% so we will use the default python version
    echo:
    python -m venv venv)
    
:: Upgrading pip version
echo Upgrading pip version
venv\Scripts\python.exe -m pip install --upgrade pip
echo %TAB%Upgraded pip to latest version
echo:

:: Activating the venv
echo Activating the virtual environment
set "virtual_env=%working_dir%\venv"
call %virtual_env%\Scripts\activate.bat

:: Getting and displaying the python version used
for /F "tokens=* USEBACKQ" %%F in (`python --version`) do (set var=%%F)
if exist %working_dir%\venv (
    echo A virtual environment created with %var% and activated >> %LOG%
    echo %TAB%A virtual environment created with %var% and activated
    echo:
) else (
    echo Unable to create a virtual environment >> %LOG%
    echo %TAB%Unable to create a virtual environment
    GOTO FIN)

:: Installing packages
echo Installing BiblioParsing package
echo:
pip install git+https://github.com/TickyWill/BiblioParsing.git@%bp_branch%
cls
echo The package BiblioParsing successfully installed >> %LOG%
echo:
echo The package BiblioParsing successfully installed
echo:
echo Installing BiblioMeter packages
echo:
pip install git+https://github.com/TickyWill/BiblioMeter.git@%bm_branch%
cls
echo The package BiblioMeter successfully installed >> %LOG%
echo:
echo The BiblioMeter packages successfully installed
echo:
echo Installing DoiToScopus packages
echo:
pip install git+https://github.com/TickyWill/DoiToScopus.git@%dts_branch%
cls
echo The package DoiToScopus successfully installed >> %LOG%
echo:
echo The DoiToScopus packages successfully installed
echo:
echo Installing ScopusApyJson packages
echo:
pip install ScopusApyJson
cls
echo The package ScopusApyJson successfully installed >> %LOG%
echo:
echo The package ScopusApyJson successfully installed
echo:     
echo Installing auto-py-to-exe packages
echo:
pip install auto-py-to-exe
cls
echo The package auto-py-to-exe successfully installed >> %LOG%
echo:
echo The package auto-py-to-exe successfully installed
echo:    

:: Getting the python program to launch the application
echo Getting the python program to launch the application
set "PGM=%working_dir%\%app_py%"
set "prefixe=https://raw.githubusercontent.com/TickyWill/DoiToScopus/"
if %dts_branch%==main (
    set "pgm_origin=%prefixe%%dts_branch%/%app_py%"
) else (
    set "pgm_origin=%prefixe%refs/heads/%dts_branch%/%app_py%"
)
curl.exe  -o %PGM% %pgm_origin%
if exist %PGM% (
    echo The python program %PGM% successfully found >> %LOG%
    echo %TAB%The python program %PGM% successfully found
    echo:         
) else ( 
    echo Unable to get the python program %PGM% >> %LOG%
    echo %TAB%Unable to get the python program %PGM%
    GOTO FIN)

:: Setting the icon and the directories to add
set "ICON=%working_dir%/venv/Lib/site-packages/dtsfuncts/ConfigFiles/BM-logo.ico"
set "DTSFUNC=%working_dir%/venv/Lib/site-packages/dtsfuncts;dtsfuncts/"
set "DTSGUI=%working_dir%/venv/Lib/site-packages/dtsgui;dtsgui/"
set "PARSE=%working_dir%/venv/Lib/site-packages/BiblioParsing;BiblioParsing/"
set "BMFUNC=%working_dir%/venv/Lib/site-packages/bmfuncts;bmfuncts/"
set "BMGUI=%working_dir%/venv/Lib/site-packages/bmgui;bmgui/"
set "STJ=%working_dir%/venv/Lib/site-packages/ScopusApyJson;ScopusApyJson/"

:: Making the executable app.exe to be located in dist
cls
echo Making the executable app.exe to be located in dist
echo:
pyinstaller --noconfirm --onefile --console^
 --icon="%ICON%"^
 --add-data "%DTSFUNC%"^
 --add-data "%DTSGUI%"^
 --add-data "%PARSE%"^
 --add-data "%BMFUNC%"^
 --add-data "%BMGUI%"^
 --add-data "%STJ%"^
 "%PGM%"
if exist %working_dir%\dist\app.exe (
    echo The executable app.exe successfully made in dist directory >> %LOG%
    echo:
    echo %TAB%The executable app.exe successfully made in dist directory
    cls
) else (
    echo Making of the executable app.exe failed >> %LOG%
    echo:
    echo %TAB%Making of the executable app.exe failed
    GOTO FIN)

:: Renaming the directory dist to aaaa_mm_jj DoiToScopus 
:: adapted from http://stackoverflow.com/a/10945887/1810071
echo Renaming the directory dist
for /f "skip=1" %%x in ('wmic os get localdatetime') do if not defined MyDate set MyDate=%%x
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set fmonth=00%Month%
set fday=00%Day%
set dir_name="%Year%-%fmonth:~-2%-%fday:~-2% DoiToScopus"
rename %working_dir%\dist %dir_name%
if not exist %working_dir%\dist (
    echo The executable directory successfully renamed to %dir_name% >> %LOG%
    echo %TAB%The executable directory successfully renamed to %dir_name%
    echo:
) else (
    echo The executable directory renaming failed >> %LOG%
    echo %TAB%The executable directory renaming failed
    GOTO FIN)

:: Cleaning the working dir
:: Removing delating the directories and the files used only for making the executable (except venv)
echo Cleaning the working dir
rmdir /s /q %working_dir%\build
if not exist %working_dir%\build (echo %TAB%%TAB%build dir successfully removed)
if exist %working_dir%\app.spec (del /f %working_dir%\app.spec)
if not exist %working_dir%\app.spec (echo %TAB%%TAB%app.spec file successfully delated)
echo %working_dir% cleaned successfully >> %LOG%
echo %TAB%%working_dir% cleaned successfully 
echo:

:: Renaming the built exe to DoiToScopus-#.#.#
echo Renaming the built exe
set "exe_file_name=DoiToScopus-%exe_version%.exe"
ren %dir_name%\app.exe %exe_file_name%
if exist %dir_name%\%exe_file_name% (
    echo The executable is renamed to %exe_file_name% >> %LOG%
    echo The executable is located in the directory: %working_dir%\%dir_name% >> %LOG%
    echo %TAB%The executable is renamed to %exe_file_name%    
    echo %TAB%The executable is located in the directory:
    echo %TAB%%TAB%%working_dir%\%dir_name%
) else (
    echo The executable still named app.exe >> %LOG%
    echo The executable is located in %working_dir%\%dir_name% >> %LOG%
    echo %TAB%The executable still named app.exe and is located in the directory:
    echo %TAB%%TAB%%working_dir%\%dir_name%)

:: Copying the built exe to a user directory
echo:
echo Copying the built exe to a user directory
echo:
set "rep=n"
set /p "rep=Do you want to save the exe directory in an other directory than %save_dir% (y/n)? "
if %rep%==y goto OTHER
set "output_dir=%save_dir%\%dir_name%"
goto COPY
:OTHER
echo:
set /p "new_dir=Enter the other full path for saving the exe directory: "
echo:
set "output_dir="%new_dir%"\%dir_name%"
:COPY
echo:
if exist %output_dir% (
    rmdir /s /q %output_dir%
    echo Existing %output_dir% directory removed before creation >> %LOG%
    echo %TAB%Existing %output_dir% directory removed before creation
    )
echo:
mkdir %output_dir%
if exist %output_dir% (
    echo %output_dir% directory successfully created >> %LOG%
    echo %TAB%%output_dir% directory successfully created
    goto COPY_FILE
) else (
    echo:
    echo Unable to create %output_dir% directory >> %LOG%
    echo %TAB%Unable to create %output_dir% directory
    goto RETRY)
:COPY_FILE
echo %TAB%Please wait while copying the built exe...
set "input_file=%working_dir%\%dir_name%\%exe_file_name%"
set "output_file=%output_dir%\%exe_file_name%"
copy %input_file% %output_file%
if %ERRORLEVEL% == 0 (
    echo %exe_file_name% file successfully saved in %output_dir% directory >> %LOG%
    echo %TAB%%exe_file_name% file successfully saved in %output_dir% directory
    goto FIN
) else (
    echo %TAB%Errors encountered during copy of exe file.  Copy canceled with status: %errorlevel%
    echo Errors encountered during copy of exe file.  Copy canceled with status: %errorlevel% >> %LOG%
)
:RETRY
echo:
set "rep=n"
set /p "rep=Do you want to try an other full path for saving the exe directory (y/n)? "
if  %rep%==y goto OTHER
:FIN
echo:
set "rep=n"
set /p "rep=Do you want to use an other full path for saving the exe directory (y/n)? "
if  %rep%==y goto OTHER
echo:
echo The report on the executable building is available in the file:
echo %TAB%%LOG%
echo:

pause