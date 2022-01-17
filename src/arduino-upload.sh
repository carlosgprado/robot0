#!/bin/sh

./arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno $1

