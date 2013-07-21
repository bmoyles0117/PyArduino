import serial
import time

HIGH    = 1
LOW     = 0
OUTPUT  = 1
INPUT   = 0

DEFAULT_BAUDRATE    = 9600

def ensure_connection(func):
    def inner(app, *args, **kwargs):
        app.connect()

        return func(app, *args, **kwargs)

    return inner

def ensure_pin_mode(mode):
    def ensure_pin_mode_wrapper(func):
        def inner(cls, pin, *args, **kwargs):
            if pin not in cls.pins or cls.pins[pin] != OUTPUT:
                cls.pinMode(pin, OUTPUT)

            return func(cls, pin, *args, **kwargs)
        return inner
    return ensure_pin_mode_wrapper

def retry_on_exception(exception, max_attempts=3, retry_delay=0.01):
    def wrapper(func):
        def inner(*args, **kwargs):
            for x in xrange(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exception, e:
                    time.sleep(retry_delay)

            raise e
        return inner
    return wrapper

class ArduinoApp(object):
    DIGITAL_READ    = 1
    DIGITAL_WRITE   = 2
    PIN_MODE        = 3
    ANALOG_READ     = 4
    ANALOG_WRITE    = 5

    def __init__(self, endpoint, baudrate = DEFAULT_BAUDRATE):
        self.endpoint = endpoint
        self.baudrate = baudrate
        self.last_send = None

        self.connect()

        self.setup()

    def analogRead(self, pin, value):
        self.send(self.ANALOG_READ, pin, value)

    def analogWrite(self, pin, value):
        self.send(self.ANALOG_WRITE, pin, value)

    def connect(self):
        if hasattr(self, 'connection') and self.connection.isOpen():
            return self.connection

        self.connection = self.create_connection(self.endpoint, self.baudrate)

        return self.connection

    def create_connection(self, endpoint, baudrate):
        conn = serial.Serial(endpoint, baudrate)
        conn.setTimeout(0.1)
        conn.setWriteTimeout(0.1)

        return conn

    def delay(self, timeout):
        time.sleep(timeout / 1000.)

    @retry_on_exception(ValueError, max_attempts=3)
    def digitalRead(self, pin):
        self.send(self.DIGITAL_READ, pin)

        return int(self.read().strip())

    def digitalWrite(self, pin, value):
        self.send(self.DIGITAL_WRITE, pin, value)

    @classmethod
    def listen(cls, endpoint, baudrate = DEFAULT_BAUDRATE):
        instance = cls(endpoint, baudrate)

        while True:
            instance.loop()

    def pinMode(self, pin, mode):
        self.send(self.PIN_MODE, pin, mode)

    @ensure_connection
    @retry_on_exception(serial.serialutil.SerialException, max_attempts=3)
    def read(self):
        return self.connection.readline()

    @ensure_connection
    def send(self, *args):
        self.last_send = args

        command_str = ','.join(map(str, args))

        # print '%s:%s' % (len(command_str), command_str, )

        self.connection.write('%s:%s' % (len(command_str), command_str, ))

    def setup(self):
        raise NotImplemented("App must define 'setup' method")

class BeginnersArduinoApp(ArduinoApp):
    def __init__(self, *args, **kwargs):
        self.pins = {}

        return super(BeginnersArduinoApp, self).__init__(*args, **kwargs)

    def setup(self):
        pass

    @ensure_pin_mode(OUTPUT)
    def fadePin(self, pin, from_, to, duration):
        delay_duration = duration * 1.0 / abs(to - from_) * 10

        for x in xrange(from_, to, 10 if from_ < to else -10):
            self.analogWrite(pin, x)
            self.delay(delay_duration)

        # Ensure that the brightness makes it to the final point
        self.analogWrite(pin, to)

    @ensure_pin_mode(INPUT)
    def isPinOff(self, pin):
        return self.digitalRead(pin) == LOW

    @ensure_pin_mode(INPUT)
    def isPinOn(self, pin):
        return self.digitalRead(pin) == HIGH

    def pinMode(self, pin, mode):
        super(BeginnersArduinoApp, self).pinMode(pin, mode)

        self.pins[pin] = mode

    @ensure_pin_mode(OUTPUT)
    def turnPinOn(self, pin):
        self.digitalWrite(pin, HIGH)

    @ensure_pin_mode(OUTPUT)
    def turnPinOff(self, pin):
        self.digitalWrite(pin, LOW)