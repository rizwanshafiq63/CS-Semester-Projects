# Smart City Resource Management System

## Requirements
- Java 8 or higher
- No external installation needed. GSON library is included in the `lib` folder.

## To Compile and Run:
### On Linux/Mac:
Use the run.sh file.
### On Windows:
Use the run.bat file.

## To Compile and Run:
### On Windows (CMD):
javac -cp 'lib\\*' -d bin (Get-ChildItem -Recurse -Filter *.java -Path src | ForEach-Object { $_.FullName })
java -cp "bin;lib\*" Main
### On Linux/Mac:
```bash
javac -cp "lib/*" -d bin src/**/*.java
java -cp "bin:lib/*" Main
