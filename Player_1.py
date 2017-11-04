from Client import *



client = chess_client('127.0.0.1', 7777)
client.srvconnect()

if client.waitForPlayer() == 1:
    try:
        print 'other Player connected'
        i=555
        while 1 :

            sleep(3)
            client.send_mov(i, i)
            print '[+] Sending move : (%d ,%d)' % (i, i)

            mov = client.waitformov()
            print '[+] Receiving move :' + str(mov)

            i+=1
            # raw_input('Next Mov ?')


    except Exception, e:
        print e

