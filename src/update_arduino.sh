#!/bin/bash

echo "[+] Compiling robotino..."
./arduino-compile.sh robotino

echo "[+] Uploading..."
./arduino-upload.sh robotino

echo "[+] Finished"

