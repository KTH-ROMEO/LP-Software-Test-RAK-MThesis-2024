"""Basic script to test the details of how the python cobs library decodes an SPP header."""

from cobs import cobs
from SPP_PUS_test import *

recv_msg = b'\x04\x03\xba\xc0\x01\x04\x01\x0b\xe5'
output = cobs.decode(recv_msg)

spp_header = SPP_decode(output)
print(spp_header)
print(output.hex())