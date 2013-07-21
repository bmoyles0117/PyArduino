from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

PIN = 11

class BlinkApp(BeginnersArduinoApp):
    def setup(self):
        self.pinMode(PIN, OUTPUT)

    def loop(self):
        self.turnPinOn(PIN)
        self.delay(1000)
        self.turnPinOff(PIN)
        self.delay(1000)

if __name__ == '__main__':
    BlinkApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)