@echo off
echo Compiling...

:: Create output directory if not exists
if not exist bin mkdir bin

:: Compile using PowerShell to list .java files recursively
powershell -Command "javac -cp 'lib\\*' -d bin (Get-ChildItem -Recurse -Filter *.java -Path src | ForEach-Object { $_.FullName })"

if %errorlevel%==0 (
  echo Running...
  java -cp "lib\*;bin" Main
) else (
  echo Compilation failed.
)
pause


