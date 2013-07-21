import sys
import os

sys.path = [os.path.dirname(os.path.realpath(__file__)) + '/../'] + sys.path

SERIAL_PORT = '/dev/tty.usbmodem1411'
SERIAL_BAUDRATE = 9600