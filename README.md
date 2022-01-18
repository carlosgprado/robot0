# robot0

Domo Arigato, Mr. Robot0


## Access

Per SSH (Raspberry Pi)

* 192.168.1.33 (embedded SOC wlan)
* 192.168.1.34 (TP-Link USB adapter)
* user: pi
* pass: robot0


## L298N Pinout

Raspberry Pi:

* In1 Blue GPIO 23
* In2 Yellow GPIO 24
* In3 Green GPIO 22
* In4 White GPIO 27
* EnA Orange GPIO 12 (PWM)
* EnB Orange GPIO 13 (PWM)


## Compiling the Arduino code

This can be done from inside the Raspberry Pi itself.
Use the `arduino-cli` tool:


```shell
./arduino-cli core update-index
./arduino-cli board list
./arduino-cli core install arduino:avr
./arduino-cli core list
```


## Arduino libraries

```shell
./arduino-cli lib install "HCSR04 ultrasonic sensor"
```

