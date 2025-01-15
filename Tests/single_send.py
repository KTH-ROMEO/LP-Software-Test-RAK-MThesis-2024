"""Sends a premade spp_message to a Given Serial port."""
import serial
import codecs
from cobs import cobs
import socket
import signal
import sys


'''
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
'''
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

def send_single(spp_message):
    signal.signal(signal.SIGINT, signal_handler)
    msg_len = len(spp_message)
    ser.write(spp_message)
    print(f"Sent Message ({msg_len})")
    print(spp_message.hex())

def read_inf():
    while True:
        s = ser.read(256)
        yield s