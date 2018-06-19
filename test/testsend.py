#!/usr/bin/env python

import socket
# import time
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 5555))
sock.connect(("127.0.0.1", 6666))


def print_incoming(sock):
    print("Starting threaded read.")
    while True:
        data, ancdata, msg_flags, addr = sock.recvmsg(1024)
        print("Received: " + str(data))


threading.Thread(target=print_incoming, args=([sock])).start()


def hello_world(sock):
    for i in range(6):
        print("Sending " + str(i))
        # seq no + an empty byte
        header = bytes([i, 0])
        payload = bytes("Hello world! " + str(i) + "\n", "utf-8")
        packetbytes = header + payload
        sock.sendall(packetbytes)
        # time.sleep(1)


# hello_world(sock)


def swapped_packets(sock):
    # send dumb packets
    # swap packets three and four
    for i in range(10):
        if i == 3:
            i = 4
        elif i == 4:
            i = 3
        header = bytes([i, 0])
        print("Sending: " + str(i))
        payload = bytes("Swap packets test: " + str(i) + "\n", "utf-8")
        sock.sendall(header + payload)


swapped_packets(sock)
