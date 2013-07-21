from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

PIN = 11

class DigitalReadApp(BeginnersArduinoApp):
    def loop(self):
        self.turnPinOn(PIN)

        if self.isPinOn(PIN):
            print "Lights on!"

        # This would be an error, being that we just turned it ON
        if self.isPinOff(PIN):
            print "For some reason I also think lights are off... I'm broken!"

        self.delay(1000)

        self.turnPinOff(PIN)

        if self.isPinOff(PIN):
            print "Lights off!"

        # This would be an error, being that we just turned it OFF
        if self.isPinOn(PIN):
            print "Lights are on when they shouldn't be!"

        self.delay(1000)

if __name__ == '__main__':
    DigitalReadApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)