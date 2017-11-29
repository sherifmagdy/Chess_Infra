import socket
from struct import *


# return type : string
def waitforstr(hsocket):
    try :
        result = []
        type = None
        type = hsocket.recv(4)
        type, = unpack('i', type)

        # string
        if type == 1:
            size = hsocket.recv(4)
            sz, = unpack('i', size)
            board_state = hsocket.recv(sz)
            fmt = str(sz) + 's'
            state, = unpack(fmt, board_state)

        return state
    except Exception ,e :
        print e

def listenForConn(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(5)

    client, address = sock.accept()
    client.settimeout(999999)
    return client




client = listenForConn('127.0.0.1', 8989)
while 1 :
    strr = waitforstr(client)
    print '[+] Received string : '+strr


