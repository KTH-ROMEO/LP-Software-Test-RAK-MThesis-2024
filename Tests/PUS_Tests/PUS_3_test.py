"""Contains Offsets, and multipliers for correctly decoding Houskeeping Report data sent by the DataHub
    Also contains predefined test messages used by HK_toggle_periodic.py and a Housekeeping packet decode function used by HK_*.py tests
"""
from SPP_PUS_test import *
import struct



def get_PUS_3_TC(subserv_id, data : bytearray):
    return get_PUS_TC(3, subserv_id, data)



UC_SID = b'\xaa\xaa'
FPGA_SID = b'\x55\x55'

par_id = {
    UC_SID: {
        1 : "uc_vbat",
        2 : "amb_temp",
        3 : "uc_3v",
    },
    FPGA_SID: {
        1 : "fpga_1v5",
        2 : "fpga_3v",
    },
}

par_mult = {
    UC_SID: {
        "uc_vbat"  : 0.00146484375,
        "amb_temp" : 0.000732421875,
        "uc_3v"    : 0.00097412109,
    },
    FPGA_SID: {
        "fpga_1v5"  : 0.000732421875,
        "fpga_3v"   : 0.00097412109,
        
    },
}

par_offset = {
    UC_SID: {
        "uc_vbat"  : 0,
        "amb_temp" : 20,
        "uc_3v"    : 0,
    },
    FPGA_SID: {
        "fpga_1v5"  : 0,
        "fpga_3v"   : 0,
    },
}

HK_PERIODIC_UC = HK_ONESHOT_UC_PARS      = [0x01, 0x00, 0xAA, 0xAA]
HK_ONESHOT_UC_PARS_COBS = get_PUS_3_TC(27, bytearray(HK_ONESHOT_UC_PARS))

HK_EN_PERIODIC_UC_COBS   = get_PUS_3_TC(5, bytearray(HK_PERIODIC_UC))
HK_DIS_PERIODIC_UC_COBS  = get_PUS_3_TC(6, bytearray(HK_PERIODIC_UC))


HK_PERIODIC_FPGA = HK_ONESHOT_FPGA_PARS      = [0x01, 0x00, 0x55, 0x55]
HK_ONESHOT_FPGA_PARS_COBS = get_PUS_3_TC(27, bytearray(HK_ONESHOT_FPGA_PARS))

HK_EN_PERIODIC_FPGA_COBS = get_PUS_3_TC(5, bytearray(HK_PERIODIC_FPGA))
HK_DIS_PERIODIC_FPGA_COBS = get_PUS_3_TC(6, bytearray(HK_PERIODIC_FPGA))



def decode_HK_packet(output_dec):
    spp_header = SPP_decode(output_dec)
    print(spp_header)
    if spp_header.sec_head_flag:
        pus_tm_header = PUS_TM_decode(output_dec[6:])
        print(pus_tm_header)
        if pus_tm_header.service_id == 3:
            data = output_dec[6+9:]
            sid_bytes = data[0:2]
            sid_str = sid_bytes.hex()
            print(f"SID: {sid_bytes} {sid_str}")
            data = data[2:]
            out = data_split(32, data)
            print("HK params:")
            for i, e in enumerate(out):
                raw_num_val = struct.unpack('<i', bytes.fromhex(e))[0] # "<" means little endian
                i += 1 # ids are 1-indexed

                id_name =   par_id[sid_bytes][i]
                mutiplier = par_mult[sid_bytes][id_name]
                offset =    par_offset[sid_bytes][id_name]
                
                real_num_val = raw_num_val * mutiplier + offset
                print(real_num_val)
            
            print()