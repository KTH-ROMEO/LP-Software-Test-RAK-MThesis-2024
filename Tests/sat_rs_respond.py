import socket

obsw_ip = '127.0.0.1' # sat-rs IP address UNSPECIFIED
obsw_port = 60062

obsw_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

obsw_socket.bind((obsw_ip, obsw_port))
obsw_socket.setblocking(1)
obsw_data, obsw_addr = obsw_socket.recvfrom(1024)
print(obsw_data.hex())


respone = b'\x08\x02\xC0\x00\x00\x0A\x20\x11\x02\x00\x00\x00\x00\x00\x00\xA5\xC5'

send_ip = '127.0.0.1' # sat-rs IP address UNSPECIFIED
send_port = 60061

send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

send_socket.bind((send_ip, send_port))
send_socket.send(respone)

