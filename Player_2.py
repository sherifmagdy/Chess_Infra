from Client import *

try:
    # create client object
    client = chess_client('127.0.0.1', 7777)

    # connect to sever
    client.srvconnect()

    # wait for other player to connect to get intial board state ; blocks
    client.waitForPlayer()

    print '[+] other Player connected'
    print '=> Has first move : ' + str(client.has_first_move)
    print '=> Initial board : '+client.intial_string

    flag = client.has_first_move

    i=555
    # Main Game loop
    while True :

        # start with sending if we got first play from server
        if (flag):
            flag = 1
            ##############################################################
            ################## SEND BLOCK ################################
            ##############################################################
            raw_input('send new move ? ')

            # While loop to repeat the operation if it failed
            MOVE_SENT= False
            while not MOVE_SENT:

                try :
                    # check the existence of the other player before sending any move
                    if client.probe() == 1 :
                        # other player is already connected
                        print '[+] Sending move : (%d ,%d) ...' % (i, i)
                        # send move to the other player
                        result = client.send_mov(i, i)

                        if result == 0 :
                            print '[-] server did not received the move => server is not reachable'
                            # code to connect again to server
                        else:
                            print '[+] Move sent'
                            MOVE_SENT = True
                            i+=1

                    else :
                        print '[-] other player disconnected'
                        while 1:
                            # busy waiting for the other to connect
                            sleep(2)
                            if client.probe() == 1:
                                print '[++] player came back'
                                break
                            else:
                                print '[--] other player disconnected'
                        # It's up now continue to send again

                except :
                    print '[-] connrction closed'
                    sleep(1)
                    continue
            # SEND BLOCK

        flag = 1


        ##############################################################
        ################## Receive BLOCK #############################
        ##############################################################
        raw_input('Receive Move ? ')
        # While loop to repeat the operation if it failed
        MOVE_RECEIVED= False
        while not MOVE_RECEIVED :
            # waiting for move from the other player
            mov = client.waitformov()

            if mov[0] == 0:
                # Received single move
                print '[+] Receiving single move :' + str(mov)
                MOVE_RECEIVED = True

            elif mov[0] == 1:
                # Received string move
                print '[+] Receiving string move :' + str(mov)
                MOVE_RECEIVED = True

            elif mov[0] == -1:
                # The other player is disconnected
                print '[-] other player disconnected'
                while 1:
                    # busy waiting for the other to connect
                    sleep(2)
                    if client.probe() == 1:
                        print '[++] player came back'
                        break
                    else:
                        print '[--] other player disconnected'
                # It's up now continue to send again

        ##############################################################
        ################## Receive BLOCK #############################
        ##############################################################

        ##############################################################
        ################## Receive BLOCK #############################
        ##############################################################

except Exception, e:
    print e

