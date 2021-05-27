import socket
import os
import sys
import hashlib

try:
    if len(sys.argv) == 2:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('', int(sys.argv[1])))
    else:
        sys.exit()
except socket.error:
    print("failed to create socket")
    sys.exit()

def checksum(chunk_file):
    data = 0
    for i in range(0, len(chunk_file), 2):
        data1 = chunk_file[i] * 256 + chunk_file[i+1]
        data = data + data1
        if data > 0xffff:
            data = data & 0xffff
            data += 1
    data = ~data
    data = data & 0xffff
    return bytes([data//256, data%256])

def sender_send(file_name):
	#
	# Implement in the order mentioned in the silde and video.
	#
    s.sendto("valid".encode(), client_addr)
    print("valid list command")
    if os.path.isfile(file_name):
        s.sendto("file".encode(), client_addr)
    file_size = os.stat(file_name).st_size
    size = int(file_size/984)
    read_file = open(file_name, 'rb')
    s.sendto(str(size).encode(), client_addr)
    src_ip = bytes(map(int, '168.188.129.169'.split('.')))
    dst_ip = bytes(map(int, '13.209.70.238'.split('.')))
    zero = bytes([0x0])
    protocol = bytes([17])
    udp_len = bytes([(8+file_size)//256, (8+file_size)%256])
    src_port = bytes([8000//256, 61598%256])
    dst_port = bytes([53109//256, 8111%256])
    length = bytes([(8+file_size)//256, (8+file_size)%256])
    cnt = 0
    while cnt < size:
            chunk_file = read_file.read(984)
            header = src_ip + dst_ip + zero + protocol + udp_len + src_port + dst_port + length + checksum(chunk_file)
            s.sendto(header + chunk_file, client_addr)
            print("packet number ",cnt)
            cnt += 1

if __name__ == "__main__":
    try:
    	data, client_addr = s.recvfrom(1024)
    except ConnectionResetError:
        print("error. port number not matching.")
        sys.exit()

    text = data.decode('utf8')
    handler = text.split()

    if handler[0] == 'receive':
        sender_send(handler[1])
    elif handler[1] == 'exit':
        socket.close()
        sys.exit()
