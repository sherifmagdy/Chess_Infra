Client methods

# connect to server and intialize socket handle
srvconnect(self):

# wait for mov from other palyer
# return type : list [type of mov , mov data]
# type of move :
#     0 => single mov   , mov data (tuple) => (piece , dst)
#     1 => state string , mov data (string)=> board string state
waitformov


# send single move to the server
# return  : 1 if acked  0 if failed
# ex: send_move(15 , 12)
send_mov(self, piece, dst):


# send win message to the server to end the game
# the server will end the game when it receives that message
# return 1 if acked :  0 otherwise
send_win(self):


# Probe the existence of the other player
# return  : 1 if other player connected  , otherwise blocks
waitForPlayer(self):


# send state board string to server
# return  : 1 if acked  0 if failed
# ex: send_state('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq- 0 1')
send_state(self, state)
