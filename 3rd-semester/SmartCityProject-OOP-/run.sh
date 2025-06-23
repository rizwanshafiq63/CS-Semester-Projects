#!/bin/bash

# Compile all .java files in src using Gson library
echo "Compiling Java files..."
javac -cp "lib/*" -d bin $(find src -name "*.java")

# If compilation was successful, run Main
if [ $? -eq 0 ]; then
  echo "Running Smart City Project..."
  java -cp "lib/*:bin" Main
else
  echo "Compilation failed."
fi

