@echo off
cd /d "%~dp0"
del *.ncb *.plg *.opt *.positions
del /q debug\*.*
del /q release\*.*
del /q bin\*.ilk bin\*.bsc bin\*.pdb
goto :eof
