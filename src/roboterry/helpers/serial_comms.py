# ---------------------------------------------
# Serial communications module
# ---------------------------------------------

import serial


class Cereal:
    def __init__(self, device_name="", baud_rate=57600, timeout=1):
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

        # Start from a clean slate
        # Discards the return value
        self.ser.flush()

    def send(self):
        raise NotImplemented

    def receive(self, size=0):
        """Reads the specified number of bytes
           or all remaining bytes on the input buffer.

           Returns a null number of bytes if
           the input buffer is empty
        """

        bytez = b""

        inw = self.ser.in_waiting
        if inw:
            if size:
                bytez = self.ser.read(size=size)
            else:
                bytez = self.ser.readall()

        return bytez

    def receive_line(self):
        """Reads a line waiting on the input buffer
           Usually the Arduino used `Serial.println`
           on its side.
        """

        bytez = b""

        if self.ser.in_waiting:
            bytez = self.ser.readline()

        return bytez


