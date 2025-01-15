"""Test to continually wait for and decode telemetry packets from the DataHub.
    Contains a hk mode, which specifies that the data received from the DataHub
    is Housekeeping data. In this mode the data is decoded. This Test is deprecated,
    use PUS_Tests/HK_*.py
"""

import serial
import codecs
from cobs import cobs
import signal
import sys
import struct
from SPP_PUS_test import *

ser = serial.Serial('COM3', 115200, timeout=1)

def signal_handler(sig, frame):
    ser.close()
    sys.exit(0)

def pad_msg(msg, pad_to):
    msg_len = len(msg)
    diff = pad_to - msg_len
    for i in range(0, diff):
        msg += b'\x00'
    return msg


signal.signal(signal.SIGINT, signal_handler)

if len(sys.argv) > 1:
    spp_message = bytearray.fromhex(sys.argv[1])
    msg_len = len(spp_message)
    ser.write(spp_message)
    print(f"Sent Message ({msg_len})")
    

while True:
    try:
        output = ser.read(256)
        output_list = output.split(b'\x00')
        for output in output_list:
            if len(output) == 0:
                continue
            output_decoded = cobs.decode(output)
            rep_len = len(output_decoded)
            
            if len(sys.argv) > 1  and sys.argv[1] == "hk":
                print(f"Reply ({rep_len})")
                print("Raw:", output_decoded.hex())
                spp_header = SPP_decode(output_decoded)
                print(spp_header)
                if spp_header.sec_head_flag:
                    pus_tm_header = PUS_TM_decode(output_decoded[6:])
                    print(pus_tm_header)
                    if pus_tm_header.service_id == 3:
                        data = output_decoded[6+9:]
                        sid = (data[0:2]).hex()
                        print(f"SID: {sid}")
                        data = data[2:]
                        out = data_split(32, data)
                        print("HK params:")
                        for e in out:
                            print(struct.unpack('<f', bytes.fromhex(e))[0]) # "<" means little endian
    except:
        pass
    else:
        pass
