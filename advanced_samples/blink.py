from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

PIN = 11

class BlinkApp(ArduinoApp):
    def setup(self):
        self.pinMode(PIN, OUTPUT)

    def loop(self):
        self.digitalWrite(PIN, HIGH)
        self.delay(1000)
        self.digitalWrite(PIN, LOW)
        self.delay(1000)

if __name__ == '__main__':
    BlinkApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)