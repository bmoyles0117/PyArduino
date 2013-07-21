from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

BUTTON_PIN = 10
LED_PIN = 11

class ButtonApp(BeginnersArduinoApp):
    def setup(self):
        self.pinMode(BUTTON_PIN, INPUT)
        self.pinMode(LED_PIN, OUTPUT)

    def loop(self):
        if self.isPinOn(BUTTON_PIN):
            self.turnPinOn(LED_PIN)
        else:
            self.turnPinOff(LED_PIN)

        self.delay(100)

if __name__ == '__main__':
    ButtonApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)