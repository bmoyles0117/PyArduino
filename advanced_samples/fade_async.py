from settings import SERIAL_PORT, SERIAL_BAUDRATE
from arduino import *

GREEN_PIN = 11
RED_PIN = 10
LOOP_DELAY = 50
MAX_VALUE = 255

class FadeAsyncApp(ArduinoApp):
    def setup(self):
        self.pinMode(GREEN_PIN, OUTPUT)
        self.pinMode(RED_PIN, OUTPUT)

        self.fade_trackers = {}

    def fadePinAsync(self, pin, duration):
        if pin not in self.fade_trackers:
            self.fade_trackers[pin] = 0

        if self.fade_trackers[pin] > MAX_VALUE:
            self.fade_trackers[pin] = 0

        self.fade_trackers[pin] += float(MAX_VALUE) / duration * LOOP_DELAY

        self.analogWrite(pin, int(self.fade_trackers[pin]))

    def loop(self):
        self.fadePinAsync(RED_PIN, 1000)
        self.fadePinAsync(GREEN_PIN, 2000)

        self.delay(LOOP_DELAY)

if __name__ == '__main__':
    FadeAsyncApp.listen(SERIAL_PORT, SERIAL_BAUDRATE)