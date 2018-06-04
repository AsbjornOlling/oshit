import socket

""" Open udp socket and print all incoming data """

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 5555))

while True:
    msg, addr = sock.recvfrom(1024)
    print(msg)
