"""DataHub Telemetry decode test used in conjunction with sat-rs"""
import serial
import codecs
from cobs import cobs
import socket
import signal
import sys



obsw_ip = '127.0.0.1' # sat-rs IP address UNSPECIFIED
obsw_port = 60062

obsw_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

obsw_socket.bind((obsw_ip, obsw_port))
obsw_socket.setblocking(0)

send_ip = '127.0.0.1' # sat-rs IP address UNSPECIFIED
send_port = 60061

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

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

while True:
    try:
        obsw_data, obsw_addr = obsw_socket.recvfrom(1024)
    except:
        pass
    else:
        spp_message = obsw_data
        msg_len = len(spp_message)
        print(f"Sent Message ({msg_len})")
        print(spp_message.hex())
        spp_message = cobs.encode(spp_message)
        spp_message += b'\x00'
        ser.write(spp_message)
    
        output = ser.read(256)
        output_list = output.split(b'\x00')
        for output in output_list:
            if len(output) == 0:
                continue
            output_decoded = cobs.decode(output)
            rep_len = len(output_decoded)
            print(f"Reply ({rep_len})")
            print(output_decoded.hex())
            obsw_socket.sendto(output_decoded, (send_ip, send_port))
