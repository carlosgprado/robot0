#!/bin/sh

./arduino-cli upload -p /dev/ttyAMA0 --fqbn arduino:avr:uno $1

