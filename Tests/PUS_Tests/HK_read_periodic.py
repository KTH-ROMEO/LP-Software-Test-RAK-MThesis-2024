"""Test used to test the periodic Housekeeping Telemetry sent by the DataHub."""
import PUS_3_test
import serial
from cobs import cobs
import signal
import sys
from SPP_PUS_test import *

print("PUS 3 HK_read_periodic")

ser = serial.Serial('COM3', 115200)

def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        output = ser.read_until(b'\x00')
        output_dec = cobs.decode(output[:-1])
        print("RECV: ", output_dec.hex())
        PUS_3_test.decode_HK_packet(output_dec)
except:
    pass
else:
    pass