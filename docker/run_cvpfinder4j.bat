@echo off

set SRC=%1%
set REPORT=report

if not exist "%REPORT%" (
  mkdir %REPORT%
)
docker container run -it -v %CD%:/data -v %CD%\%REPORT%:/cvpfinder/report amanhirohisa/cvpfinder /cvpfinder/cvpfinder4j /data/%SRC:\=/%

echo == Note ============================================
echo "/data/%SRC:\=/% --> %SRC%"
echo "/cvpfinder/report/report.csv --> report/report.csv"
