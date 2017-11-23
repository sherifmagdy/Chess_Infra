from Client import *



# create client object
client = chess_client('127.0.0.1', 7777)

# connect to sever
client.srvconnect()

# wait for other player to connect ; blocks
client.waitForPlayer()
try:
    print '[+] other Player connected'
    print 'first_move flag  : ' + str(client.has_first_move)
    print 'initial board : '+client.intial_string
    i=555
    while 1 :

        sleep(3)

        raw_input('bb1')
        try :
            if client.probe() == 1 :
                print '[+] Sending move : (%d ,%d) ...' % (i, i)
                # send move to the other player
                result = client.send_mov(i, i)
                print '[+] Move sent'
                if result == 0 :
                    print '[-] server error'
                    # code to connect again and continue
            else :
                print '[-] other player disconnected'
                # code to connect again and continue

        except :
            print '[-] server disconnected'

        raw_input('bb2')



        # wait for the move from the other player ; blocks
        mov = client.waitformov()
        print '[+] Receiving move :' + str(mov)

        i+=1


except Exception, e:
    print e

