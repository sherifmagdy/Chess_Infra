Client methods

srvconnect(self)
connect to server and intialize socket handle


waitformov
wait for mov from other palyer
return type : list [type of mov , mov data]
type of move :
     0 => single mov   , mov data (tuple) => (piece , dst)
     1 => state string , mov data (string)=> board string state


send_mov(self, piece, dst):
 send single move to the server
 return  : 1 if acked  0 if failed
 ex: send_move(15 , 12)


send_win(self):
 send win message to the server to end the game
 the server will end the game when it receives that message
 return 1 if acked :  0 otherwise


waitForPlayer(self):
 Probe the existence of the other player
 return  : 1 if other player connected  , otherwise blocks


send_state(self, state)
 send state board string to server
 return  : 1 if acked  0 if failed
 ex: send_state('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq- 0 1')

