"""Tests used to send a Houskeeping oneshot request Telecommand to the DataHub, receive and decode the Telemetry response."""
import PUS_3_test
import serial
from cobs import cobs
import signal
import sys
import struct
from SPP_PUS_test import *

print("PUS 3 HK_OneShot_test")

ser = serial.Serial('COM3', 115200, timeout=1)

def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    msg_full = PUS_3_test.HK_ONESHOT_UC_PARS_COBS
    print("SENT: ", cobs.decode(msg_full[:-1]).hex())
    ser.write(msg_full)

    output = ser.read(256)
    output_dec = cobs.decode(output[:-1])
    print("RECV: ", output_dec.hex())
    PUS_3_test.decode_HK_packet(output_dec)
except:
    pass
else:
    pass