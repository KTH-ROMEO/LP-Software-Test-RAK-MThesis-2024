"""Hex String generator for DataHub Telecommands. Takes the bytearray given in 'data' and
    print multiple stages of a Telecommand.
    Prints:
        Hex String SPP Header
        Hex String PUS Header
        Hex String Full Header
        Hex String Packet Data
        Hex String Full Packet (Full Header + Packet Data + Checksum)
        Hex String Full Packet COBS encoded
"""
from SPP_PUS_test import *

PUS_TC_HEADER_LEN = 5

data = bytearray([0x23, 0x00, 0x03, 0x01, 0x00, 0x02, 0xEF, 0x03, 0xEC, 0xDE])

spp_hed = SPP_header()
spp_hed.simple_TC(1, 321, PUS_TC_HEADER_LEN + len(data) + 1)

pus_hed = PUS_TC_header()
pus_hed.simple_TC(0, 8, 1)

enc_spp = spp_hed.SPP_encode()
enc_pus = pus_hed.PUS_TC_encode()

tot_hed = enc_spp + enc_pus
msg_wo_crc = tot_hed + data
crccalc = Calculator(Crc16.IBM_3740)

checksum = crccalc.checksum(msg_wo_crc)
b_checksum = bytearray(checksum.to_bytes(2))

fin_msg = msg_wo_crc + b_checksum
cobs_msg = cobs.encode(fin_msg)
cobs_msg += b'\x00'


print(enc_spp.hex())
print(enc_pus.hex())
print(tot_hed.hex())
print(data.hex())
print(fin_msg.hex())
print(cobs_msg.hex())
