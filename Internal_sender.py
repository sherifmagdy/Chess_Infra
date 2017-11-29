import socket
from struct import *
import time

# send state board string to server
# ex: send_state('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq- 0 1', sock)
def send_state(state, hsocket):
    print '[+] sending state : %s' % state
    sz = len(state)
    opcode = 1
    fmt = 'ii ' + str(sz) + 's'
    hsocket.send(pack(fmt, opcode, sz, state))


# connect to server and intialize socket handle
def connect(server,port):
    s = socket.socket()
    s.settimeout(None)
    s.connect((server, port))
    return s

s=connect('127.0.0.1' , 8989)

i=45645654
while 1 :
   time.sleep(1)
   send_state(str(i) , s)
   i+=1


