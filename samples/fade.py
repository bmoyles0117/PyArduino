from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

PIN = 11

class FadeApp(BeginnersArduinoApp):
    def setup(self):
        self.pinMode(PIN, OUTPUT)

    def loop(self):
        self.fadePin(PIN, 0, 255, 1000)
        self.delay(1000)
        self.fadePin(PIN, 255, 0, 1000)
        self.delay(1000)

if __name__ == '__main__':
    FadeApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)