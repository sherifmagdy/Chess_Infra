import socket
from struct import *
from time import *



# order of operation :
# 1- each client need to connect to server and intialize client object
# # create client object
# client = chess_client('127.0.0.1', 7777)
#
# # connect to sever
# client.srvconnect()
#
# 2- wait for the other player to connect so that the server broadcast the intial state and determine who has the first move
# # wait for other player to connect ; blocks
# client.waitForPlayer_Modified()
# print 'first_move flag  : ' + str(client.has_first_move)
# print 'initial board : '+client.intial_string
#
# 3- based on the received flag wait for move or send move .
#
# 4-to send move , signal the other player at first if it still connected if yes then send the move .
# try :
#     if client.probe() == 1 :
#         print '[+] Sending move : (%d ,%d) ...' % (i, i)
#         # send move to the other player
#         client.send_mov(i, i)
#         print '[+] Move sent'
#     else :
#         print '[-] other player disconnected'
#
# except :
#     print '[-] server disconnected'
#
#
# 5- waitformov method blocks to listen for any move from the other player ,if the other player disconnected it will return type of -1 in the list [-1]
#
# mov = client.waitformov()
# print '[+] Receiving move :' + str(mov)
# if mov[0] == -1 :
#     print '[-] other player disconnected'
#     # code to reconnect
#



class chess_client():

    def __init__(self,serv,port):
        self.server = serv
        self.port = port
        self.hsocket = None

        self.has_first_move = None
        self.intial_string = ''

    def __del__(self):
        self.hsocket.close()

    # connect to server and intialize socket handle
    def srvconnect(self):
        s = socket.socket()
        s.settimeout(None)
        s.connect((self.server, self.port))
        self.hsocket = s

    # wait for mov from other palyer
    # return type : list [type of mov , mov data]
    # type of move :
    #     0 => single mov   , mov data (tuple) => (piece , dst)
    #     1 => state string , mov data (string)=> board string state
    def waitformov(self):
        try :
            result = []
            type = None
            type = self.hsocket.recv(4)

            type, = unpack('i', type)

            # single move
            if type == 0:
                move = self.hsocket.recv(8)
                piece, dst = unpack('ii', move)
                result = [0, (piece, dst)]

            # string
            elif type == 1:
                size = self.hsocket.recv(4)
                sz, = unpack('i', size)
                board_state = self.hsocket.recv(sz)
                fmt = str(sz) + 's'
                state, = unpack(fmt, board_state)
                result = [1, state]

            # player disconnected
            elif type == 3:
                result = [-1]

            return result
        except Exception ,e :
            print e

    # send single move to the server
    # return  : 1 if acked  0 if failed
    # ex: send_move(15 , 12)
    def send_mov(self, piece, dst):
        try :
            print '[+] sending single move : piece = %d  | dst = %d' % (piece, dst)
            data = (piece, dst)
            self.hsocket.send(pack('iii', 2, *data))
            data = self.hsocket.recv(4)
            result, = unpack('i', data)
            if result == 1: return 1
            return 0
        except :
            return 0

    # send win message to the server to end the game
    # the server will end the game when it receives that message
    # return 1 if acked :  0 otherwise
    def send_win(self):
        print '[+] Congratulations ...'
        self.hsocket.send(pack('i', 3))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1
        return 0

    # Probe the existence of the other player
    # return  : 1 if other player connected  , otherwise blocks
    def probe(self):
        # print 'probing ...'
        self.hsocket.send(pack('i', 4))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1

    # send state board string to server
    # return  : 1 if acked  0 if failed
    # ex: send_state('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq- 0 1')
    def send_state(self, state):
        print '[+] sending state : %s' % state
        sz = len(state)
        opcode = 1
        fmt = 'ii ' + str(sz) + 's'
        self.hsocket.send(pack(fmt, opcode, sz, state))
        data = self.hsocket.recv(4)
        result, = unpack('i', data)
        if result == 1: return 1
        return 0

    def waitForPlayer(self):

        print 'Waiting for the other player ...'
        # waiting for intial state opcdoe == 12
        data = self.hsocket.recv(4)
        opcode, = unpack('i', data)

        if opcode == 12:
            # receive has_first_move
            data = self.hsocket.recv(4)
            self.has_first_move , = unpack('i', data)

            # recevie intial_string
            data = self.hsocket.recv(4)
            sz, = unpack('i', data)

            board_state = self.hsocket.recv(sz)
            fmt = str(sz) + 's'
            state, = unpack(fmt, board_state)
            self.intial_string = state
            # print '[+] Received intial state from the server : '+state
