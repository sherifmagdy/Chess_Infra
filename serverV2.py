import socket
import threading
from struct import *
import select
import time
from random import randint


def log(txt):
    f = open("log.txt", "a")
    f.write(txt + "\n")
    f.close()


class ThreadedServer(object):
    def __init__(self, host, port, game_mode, intial_state, player1_time, player2_time, force_start=0):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        self.opcodes = [None, 'board state string', 'single move', 'win message', 'check probe']
        self.players = [False, False]

        self.hsockets = [None, None]

        # start timestamp for each player waiting for it's move
        self.timers = [0, 0]
        # total time used for each player
        self.total_time = [0, 0]

        self.game = False
        self.first_play = True

        self.game_mode = game_mode

        self.turn = 0

        # initial parameters for the class
        self.initial_state = intial_state
        self.force_start = force_start

    def listen(self):
        self.sock.listen(5)
        while 1:
            if not self.players[0] or not self.players[1]:
                print 'waiting ... '

                client, address = self.sock.accept()
                client.settimeout(999999)
                if not self.players[0]:
                    print '==================='
                    print 'player 1 registered'
                    print '==================='
                    log('Player 1 registered!')
                    self.players[0] = True
                    self.hsockets[0] = client
                    threading.Thread(target=self.listenToClient, args=(0,)).start()

                elif self.players[0] and not self.players[1]:
                    print '==================='
                    print 'player 2 registered'
                    print '==================='
                    log('Player 2 registered!')
                    self.players[1] = True
                    self.hsockets[1] = client
                    threading.Thread(target=self.listenToClient, args=(1,)).start()

                # Start counting time base as soon as the two players are already registered
                if self.first_play and self.players[0] and self.players[1]:

                    # broadcast initial state and the starter
                    sock1 = self.hsockets[0]
                    sock2 = self.hsockets[1]

                    # first player has the move randomly or if force start set
                    if self.force_start == 0:
                        # check who will have the first move randomly
                        starter = randint(0, 1)
                        if starter == 0:
                            first_player = 1
                            second_player = 0
                            self.turn = 0
                        else:
                            first_player = 0
                            second_player = 1
                            self.turn = 1

                    else:
                        # for given force start
                        if self.force_start == 1:
                            first_player = 1
                            second_player = 0
                            self.turn = 0

                        elif self.force_start == 2:
                            first_player = 0
                            second_player = 1
                            self.turn = 1

                    # length of str
                    sz = len(self.initial_state)
                    # initial msg opcode == 12
                    opcode = 12

                    # format of initial message
                    fmt = 'iii' + str(sz) + 'si'
                    sock1.send(pack(fmt, opcode, first_player, sz, self.initial_state, int(self.game_mode)))
                    sock2.send(pack(fmt, opcode, second_player, sz, self.initial_state, int(self.game_mode)))

                    self.timers[self.turn] = time.time()
                    self.first_play = False
                    print '[Server] starting timers'
                    print '[Player_1] first move flag :' + str(first_player)
                    print '[Player_2] first move flag :' + str(second_player)

                    log('[Server] starting timers')
                    log('[Player_1] first move flag :' + str(first_player))
                    log('[Player_2] first move flag :' + str(second_player))

    def listenToClient(self, player):
        # opcode size
        size = 4

        if player == 0:
            print '[player 1 thread]'
            log('[player 1 thread]')
        elif player == 1:
            print '[player 2 thread]'
            log('[player 2 thread]')

        sock = self.hsockets[player]

        try:
            while 1:

                if not self.players[0] or not self.players[1]:
                    continue

                if self.turn == player:
                    if self.timers[player] == 0:
                        self.timers[player] = time.time()
                    current = time.time() - self.timers[player]
                    c = current + self.total_time[player]

                    # print player
                    # print c
                    # print self.timers[player]
                    # print self.total_time[player]

                    sock.settimeout(900 - int(c))
                data = sock.recv(size)
                opcode, = unpack('i', data)
                # Debug Msg
                # print '[Server] Received opcode [%s] from player %d' %(self.opcodes[opcode],player+1)

                # board state string == ' Size | S-T-R-I-N-G'

                # single move
                if opcode == 2:
                    data = sock.recv(4)
                    if player != self.turn:
                        print "not his turn"
                        continue
                    # piece = unpack('4s', data)
                    # print("data at server is", piece)
                    # print '[Player%d] Recieved move : piece = %d  dst = %d'%(player+1 ,piece , dst)

                    y, = unpack('4s', data)
                    piece = y[0:2]
                    dest = y[2:4]

                    log('[Player' + str(player + 1) + '] Recieved move : piece = ' + str(piece) + '  dst = ' + str(
                        dest))

                    # Start time for other player
                    self.start_timer((player + 1) % 2)
                    # stop my timer
                    self.stop_timer(player)
                    self.turn = (player + 1) % 2
                    sock.settimeout(None)

                    try:
                        Othersock = self.hsockets[(player + 1) % 2]
                        Othersock.sendall(pack('i', 2))
                        Othersock.sendall(data)
                    except Exception, e:
                        # any exception for the other palyer thread should not hang the current thread
                        print '[-] failed to send single move to player %d' % (
                            (player + 1) % 2 + 1)  # just show the other player num from it's index
                        log('[-] failed to send single move to player ' + str((player + 1) % 2 + 1))
                        print e
                        continue

                # single move with promotion
                elif opcode == 6:
                    data = sock.recv(5)
                    if player != self.turn:
                        continue
                    # piece , dst  = unpack('5s', data)
                    # print '[Player%d] Recieved move : piece = %d  dst = %d'%(player+1 ,piece , dst)

                    y, = unpack('5s', data)
                    piece = y[0:2]
                    dest = y[2:4]
                    prom = y[4:5]

                    log('[Player' + str(player + 1) + '] Recieved move with promotion : piece = ' + str(
                        piece) + '  dst = ' + str(dest) + ' prom = ' + str(prom))

                    # Start time for other player
                    self.start_timer((player + 1) % 2)
                    # stop my timer
                    self.stop_timer(player)
                    self.turn = (player + 1) % 2
                    sock.settimeout(None)

                    try:
                        Othersock = self.hsockets[(player + 1) % 2]
                        Othersock.sendall(pack('i', 6))
                        Othersock.sendall(data)
                    except Exception, e:
                        # any exception for the other palyer thread should not hang the current thread
                        print '[-] failed to send single move with promotion to player %d' % (
                            (player + 1) % 2 + 1)  # just show the other player num from it's index
                        log('[-] failed to send single move with promotion to player ' + str((player + 1) % 2 + 1))
                        print e
                        continue


                # check other player : each client is responsible for checking the availability of the other player
                elif opcode == 4:
                    if self.players[(player + 1) % 2]:
                        x = pack('i', 1)
                    else:
                        x = pack('i', 0)
                    sock.sendall(x)

                # get remaining time
                elif opcode == 5:
                    if self.turn == player:
                        current = time.time() - self.timers[player]
                        c = current + self.total_time[player]
                    else:
                        c = self.total_time[player]
                    print c
                    sock.sendall(pack('i', 900 - int(c)))

        except Exception, e:
            print e
            if e == "timed out":
                sock.sendall(pack('is', 3, 'L'))
                Othersock.sendall(pack('is', 3, 'W'))
                log('Player ' + str((player + 1) % 2 + 1) + ' won!')
        finally:
            # if any thread killed , disconnect it's corresponding player
            print '************************************************'
            print '[-] closing connection for player %d' % (player + 1)
            print '************************************************'
            log('Player ' + str(player + 1) + ' disconnected!')
            log('[-] closing connection for player ' + str(player + 1))
            sock.close()
            self.players[player] = False
            self.hsockets[player] = None

            if not self.players[0] and not self.players[1]:
                self.first_play = True

            # send message to notify other player the player disconnected
            Othersock = self.hsockets[(player + 1) % 2]
            try:
                Othersock.sendall(pack('i', 10))
            except:
                print '[-] both players disconnected'
                log('[-] both players disconnected')

    def start_timer(self, player):
        self.timers[player] = time.time()

    def stop_timer(self, player):
        current = time.time()
        c = current - self.timers[player]
        self.total_time[player] += int(c)

        print '[Player%d_Timing] Move took : %d sec , total time elasped : %d sec' % (
            player + 1, c, self.total_time[player])
        log('[Player' + str(player + 1) + '] Move took : ' + str(c) + ' sec , total time elapsed : ' + str(
            self.total_time[player]) + ' sec')
        max = 900  # 15 minutes
        if int(self.total_time[player]) >= max:
            print '[Timing] Player %d lose => timeout !!' % player + 1
            log('[Timing] Player ' + str(player + 1) + ' lose => timeout !!')


if __name__ == "__main__":
    # BoardState = open('board.txt', 'r').readlines()[0]
    BoardState = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'




    f = open("log.txt", "w")
    f.write("")
    f.close()
    log('Server is starting...')

    ThreadedServer('127.0.0.1', 7777, 1, str(BoardState), 0, 0, 0).listen()
    # force parameter 1 : player one has first move
    #     force parameter 2 : player two has first move