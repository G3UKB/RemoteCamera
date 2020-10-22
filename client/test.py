#!/usr/bin/env python3

import os, sys
import socket
import pickle

CMD_PORT = 10002
#RESPONSE_PORT = 10003
SERVER_IP = '192.168.1.107'

# Create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind to the response port
#sock.bind(('', RESPONSE_PORT))
#sock.settimeout(20)

# Send a move command
sock.sendto(pickle.dumps(['CMD_MOVE', 0, 20]), (SERVER_IP, CMD_PORT))
sock.sendto(pickle.dumps(['CMD_MOVE', 1, 20]), (SERVER_IP, CMD_PORT))

sock.sendto(pickle.dumps(['CMD_MOVE', 0, 0]), (SERVER_IP, CMD_PORT))
sock.sendto(pickle.dumps(['CMD_MOVE', 1, 0]), (SERVER_IP, CMD_PORT))

