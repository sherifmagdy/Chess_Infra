from Client import *

client = chess_client('127.0.0.1', 7777)
player_no = client.srvconnect()

client.waitForPlayer()
try:
    print 'other Player connected'
    print 'first_move falge : ' + str(client.has_first_move)
    i = 0
    while 1:

        mov = client.waitformov()

        print '[+] Receiving move :' + str(mov)
        if mov[0] == -1 :
            print '[-] other player disconnected'
            # code to reconnect

        sleep(222)

        client.send_mov(i, i)
        print '[+] Sending move : (%d ,%d)' %(i,i)

        i += 1

except Exception, e:
    print e
