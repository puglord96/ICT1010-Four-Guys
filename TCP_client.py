import socket
import sys
from blockchain import BlockChain
import pickle

# Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Connect the socket to the port where the sever is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)
exit_flag = False
block_chain = BlockChain()
max_buffer_size = 256000  # kernel receive buffer size of socket
try:
    #on connection, check latest block if equal
    sock.sendall(b"query latest")
    received_string = sock.recv(100).decode()
    if "send latest" in received_string:
        receivedlatestblock_bytes = sock.recv(1024)
        receivedlatestblock = pickle.loads(receivedlatestblock_bytes)
        #if not equal, query entire blockchain from connection
        if receivedlatestblock.index != block_chain.getlatest().index or receivedlatestblock.hash != block_chain.getlatest().hash:
            print("Discrepancy detected, synchronizing...")
            sock.sendall(b"query all")
            received_string = sock.recv(100).decode()
            if "send all" in received_string:
                #store received blockchain for manipulation
                receivedblockchain_bytes = sock.recv(max_buffer_size)
                # append full bytes string
                full_bytes = receivedblockchain_bytes
                while b"send end" not in receivedblockchain_bytes:
                    receivedblockchain_bytes = sock.recv(max_buffer_size)
                    if b"send end" in receivedblockchain_bytes:
                        break
                    else:
                        full_bytes += receivedblockchain_bytes
                receivedblockchain = pickle.loads(full_bytes)
                #transverse backwards for both received and current blockchain until a match
                counterreceived = 0
                countercurrent = 0
                synchronized = 0
                if receivedblockchain.length() == block_chain.length():
                    for i in range(receivedblockchain.length()-1,-1,-1):
                        counterreceived += 1;
                        for j in range(block_chain.length()-1,-1,-1):
                            countercurrent += 1;
                            #if match is found, take the longer blockchain as the current one
                            if receivedblockchain.blocks[i].hash == block_chain.blocks[j].hash:
                                if counterreceived > countercurrent:
                                    block_chain.replacechain(receivedblockchain)
                                    print("Replacing blockchain")
                                elif counterreceived == countercurrent:
                                    block_chain.blocks = receivedblockchain.blocks
                                else:
                                    updateothers = pickle.dumps(block_chain)
                                    sock.sendall(b"update chain")
                                    sock.sendall(updateothers)
                                synchronized = 1
                                break
                elif receivedblockchain.length() > block_chain.length():
                    block_chain.blocks = receivedblockchain.blocks
                    synchronized = 1
                else:
                    data_to_send = pickle.dumps(block_chain)
                    sock.sendall(b"update chain")
                    sock.sendall(data_to_send)
                    synchronized = 1
                #if no match is found, print error message.
                if synchronized == 0:
                     print("Mismatching blockchain, aborting")
                else:
                    print("Synchronization ended")
                    print(block_chain.getlatest().data)
        #else if indexes match and hash match
        else:
            print("Synchronized, proceeding with user input")

    # Loop until user request to exit or close connection
    while exit_flag is not True:
        print("\n? for help")
        user_action = input("Query/Add/List/Exit: ")
        user_input = user_action.split(' ')
        valid_input_flag = False
        list_flag = False
        if user_input[0].lower() == "exit":
            exit_flag = True
            valid_input_flag = True
            sock.sendall(b"connection close")
        elif user_input[0].lower() == "list":
            block_chain.print_all()
            valid_input_flag = True
            list_flag = True
        elif user_input[0].lower() == "?":
            list_flag = True
            valid_input_flag = True
            print("\nQuery timestamp X    [ Whereas X represents the block index                  ]")
            print("Add example data     [ Whereas \"example data\" is the data to add for block   ]")
            print("List                 [ List all contents of the current block chain          ]")
            print("Exit                 [End connection                                         ]\n")
        # If input is less than 2 e.g simply "query" which is unclear
        # Structure of query timestamp of block 5: query timestamp 5
        elif user_input[0].lower() == "query" and len(user_input) >= 2:
            second_input = user_input[1]
            if second_input == "timestamp" and len(user_input) == 3:
                valid_input_flag = True
                sock.sendall(user_action.encode())
        # Structure of add command: add I am new block
        elif user_input[0].lower() == "add":
            valid_input_flag = True
            data_string = user_action[3:]
            add_flag = block_chain.addblock(data=data_string)
            # if successfully added to blockchain, send out the new block
            if add_flag is True:
                data_to_send = pickle.dumps(block_chain.getlatest())
                # Send client command to server
                sock.sendall(b"add block")
                # Send json string of new block
                sock.sendall(data_to_send)
        if exit_flag:
            break
        if valid_input_flag is False:
            print("Invalid Action!")
        elif list_flag is False:
            # Commands received should not be able to exceed 100 bytes
            # For this project assume block chain is small: within 256kb
            received_string = sock.recv(100).decode()
            if "send timestamp" in received_string:
                received_timestamp = sock.recv(256).decode()
                print("Received timestamp: " + received_timestamp)
            elif "add block" in received_string:
                new_block_json = sock.recv(1024)
                new_block = pickle.loads(new_block_json)
                add_flag = block_chain.addblocktochain(new_block)
                if add_flag is True:
                    msg = b"add finish"
                else:
                    msg = b"add fail"
                # Send client command to server
                sock.sendall(msg)
            elif "add finish" in received_string:
                print("Successfully Sent new block")
            elif "add fail" in received_string:
                print("Fail in sending new block")
                print("Starting Synchronization")
                sock.sendall(b"query latest")
                received_string = sock.recv(100).decode()
                if "send latest" in received_string:
                    receivedlatestblock_bytes = sock.recv(1024)
                    receivedlatestblock = pickle.loads(receivedlatestblock_bytes)
                    # if not equal, query entire blockchain from connection
                    if receivedlatestblock.index != block_chain.getlatest().index or receivedlatestblock.hash != block_chain.getlatest().hash:
                        print("Discrepancy detected, synchronizing...")
                        sock.sendall(b"query all")
                        received_string = sock.recv(100).decode()
                        if "send all" in received_string:
                            # store received blockchain for manipulation
                            receivedblockchain_bytes = sock.recv(max_buffer_size)
                            # append full bytes string
                            full_bytes = receivedblockchain_bytes
                            while b"send end" not in receivedblockchain_bytes:
                                receivedblockchain_bytes = sock.recv(max_buffer_size)
                                if b"send end" in receivedblockchain_bytes:
                                    break
                                else:
                                    full_bytes += receivedblockchain_bytes
                            receivedblockchain = pickle.loads(full_bytes)
                            # transverse backwards for both received and current blockchain until a match
                            counterreceived = 0
                            countercurrent = 0
                            synchronized = 0
                            if receivedblockchain.length() == block_chain.length():
                                for i in range(receivedblockchain.length() - 1, -1, -1):
                                    counterreceived += 1;
                                    for j in range(block_chain.length() - 1, -1, -1):
                                        countercurrent += 1;
                                        # if match is found, take the longer blockchain as the current one
                                        if receivedblockchain.blocks[i].hash == block_chain.blocks[j].hash:
                                            if counterreceived > countercurrent:
                                                block_chain.replacechain(receivedblockchain)
                                                print("Replacing blockchain")
                                            elif counterreceived == countercurrent:
                                                block_chain.blocks = receivedblockchain.blocks
                                            else:
                                                updateothers = pickle.dumps(block_chain)
                                                sock.sendall(b"update chain")
                                                sock.sendall(updateothers)
                                            synchronized = 1
                                            break
                            elif receivedblockchain.length() > block_chain.length():
                                block_chain.blocks = receivedblockchain.blocks
                                synchronized = 1
                            else:
                                data_to_send = pickle.dumps(block_chain)
                                sock.sendall(b"update chain")
                                sock.sendall(data_to_send)
                                synchronized = 1
                            # if no match is found, print error message.
                            if synchronized == 0:
                                print("Mismatching blockchain, aborting")
                            else:
                                print("Synchronization ended")
                                print(block_chain.getlatest().data)
finally:
    print('Closing socket connection')
    sock.close()
