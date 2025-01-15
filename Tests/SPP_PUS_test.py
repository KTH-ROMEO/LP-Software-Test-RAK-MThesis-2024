"""Contains SPP and PUS Header Definitions, encoder, decoders and SPP message constructors."""
from crc import Calculator, Crc16
from cobs import cobs

class SPP_header:
    def __init__(self):
        self.spp_version = 0
        self.packet_type = 0
        self.sec_head_flag = 0
        self.apid = 0
        self.seq_flags = 0
        self.sc = 0
        self.data_len = 0
    
    def __str__(self) -> str:
        f_list = [self.spp_version, self.packet_type, self.sec_head_flag, self.apid, self.seq_flags, self.sc, self.data_len]
        n_list = ["spp_version", "packet_type", "sec_head_flag" , "apid", "seq_flags", "sc", "data_len"]
        s_list = []
        for i, f in enumerate(f_list):
            s_list.append(n_list[i] + ": " + str(f))
        res = '\n'.join(s_list)
        res += '\n'
        return res
    
    def simple_TC(self, shf, apid, dl):
        self.packet_type = 1
        self.sec_head_flag = shf
        self.apid = apid
        self.data_len = dl
    
    def SPP_encode(self):
        result_buffer = [0] * 6
        
        result_buffer[0] |=  self.spp_version << 5
        result_buffer[0] |=  self.packet_type << 4
        result_buffer[0] |=  self.sec_head_flag << 3
        result_buffer[0] |= (self.apid & 0x300) >> 8
        result_buffer[1] |=  self.apid & 0x0FF
        result_buffer[2] |=  self.seq_flags << 6
        result_buffer[2] |= (self.sc  & 0x3F00) >> 8
        result_buffer[3] |=  self.sc  & 0x00FF
        result_buffer[4] |= (self.data_len & 0xFF00) >> 8
        result_buffer[5] |=  self.data_len & 0x00FF
        return bytearray(result_buffer)

    
    
class PUS_TC_header:
    def __init__(self):
        self.pus_ver = 0
        self.ack_flags = 0
        self.service_id = 0
        self.subtype_id = 0
        self.source_id = 0
        self.spare = 0
        
    def simple_TC(self, ack, serv_id, sub_id):
        self.pus_ver = 2
        self.ack_flags = ack
        self.service_id = serv_id
        self.subtype_id = sub_id
        self.source_id = 100

    def PUS_TC_encode(self):
        result_buffer = [0] * 5
        
        result_buffer[0] |=  self.pus_ver << 4;
        result_buffer[0] |=  self.ack_flags;
        result_buffer[1] |=  self.service_id;
        result_buffer[2] |=  self.subtype_id;
        result_buffer[3] |= (self.source_id & 0xFF00) >> 8;
        result_buffer[4] |= (self.source_id & 0x00FF);

        return bytearray(result_buffer)

class PUS_TM_header:
    def __init__(self):
        self.pus_ver = 0
        self.sc_t_ref = 0
        self.service_id = 0
        self.subtype_id = 0
        self.msg_cnt = 0
        self.dest_id = 0
        self.time = 0
        self.spare = 0

    def __str__(self) -> str:
        f_list = [self.pus_ver, self.sc_t_ref, self.service_id, self.subtype_id, self.msg_cnt, self.dest_id, self.time]
        n_list = ["pus_ver", "sc_t_ref", "service_id", "subtype_id", "msg_cnt", "dest_id", "time"]
        s_list = []
        for i, f in enumerate(f_list):
            s_list.append(n_list[i] + ": " + str(f))
        res = '\n'.join(s_list)
        res += '\n'
        return res
        

def PUS_TM_decode(raw_header):
    secondary_header = PUS_TM_header()
    secondary_header.pus_ver    = (raw_header[0] & 0xF0) >> 4
    secondary_header.sc_t_ref   = (raw_header[0] & 0x0F)
    secondary_header.service_id =  raw_header[1]
    secondary_header.subtype_id =  raw_header[2]
    secondary_header.msg_cnt    = (raw_header[3] << 8) | raw_header[4]
    secondary_header.dest_id    = (raw_header[5] << 8) | raw_header[6]
    secondary_header.time       = (raw_header[7] << 8) | raw_header[8]
    secondary_header.spare      = 0
    return secondary_header


def SPP_decode(raw_header):
    primary_header = SPP_header()
    primary_header.spp_version	    = (raw_header[0] & 0xE0) >> 5
    primary_header.packet_type 	    = (raw_header[0] & 0x10) >> 4
    primary_header.sec_head_flag	= (raw_header[0] & 0x08) >> 3
    primary_header.apid	            = ((raw_header[0] & 0x03) << 8) | (raw_header[1])
    primary_header.seq_flags		= (raw_header[2] & 0xC0) >> 6
    primary_header.sc	            = ((raw_header[2] & 0x3F) << 8) | (raw_header[3])
    primary_header.data_len		    = (raw_header[4] << 8) | (raw_header[5])
    return primary_header


def data_split(data_size, data_ar):
    el_size = int(data_size / 8)
    s_data = []
    nof_el = int(len(data_ar) / el_size)
    id = 0
    for i in range(nof_el):
        if (id+el_size) >= len(data_ar):
            break
        s_data.append(data_ar[id:id+el_size].hex())
        id += el_size
    return s_data
    


def get_PUS_TC(serv_id, subserv_id, data):
    PUS_TC_HEADER_LEN = 5
    spp_hed = SPP_header()
    spp_hed.simple_TC(1, 321, PUS_TC_HEADER_LEN + len(data) + 1)

    pus_hed = PUS_TC_header()
    pus_hed.simple_TC(0, serv_id, subserv_id)

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
    return cobs_msg
