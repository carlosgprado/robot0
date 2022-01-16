# ---------------------------------------------
# Serial communications module
# ---------------------------------------------

import serial


class Cereal:
    def __init__(self, device_name="", baud_rate=9600, timeout=1):
        self.dev_name = device_name or "/dev/ttyACM0"
        self.baud_rate = baud_rate
        self.timeout = timeout

        self.ser = None

        self._initialize_serial()

    def _initialize_serial(self):
        self.ser = serial.Serial(
            self.dev_name,
            self.baud_rate,
            timeout=self.timeout
            )

        if not self.ser.readable():
            raise RuntimeError("[-] Serial port NOT readable")

        if not self.ser.writable():
            raise RuntimeError("[-] Serial port NOT writable")

    def send(self):
        raise NotImplemented

    def receive(self):
        raise NotImplemented

    def receive_line(self):
        raise NotImplemented

