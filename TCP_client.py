import socket
import sys
from block import Block
from blockchain import BlockChain
import json

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
    # Loop until user request to exit or close connection
    while exit_flag is not True:
        user_action = input("Query or Add: ")
        user_input = user_action.split(' ')
        valid_input_flag = False
        if user_input[0].lower() is "close" or user_input[0] is "exit":
            exit_flag = True
        # If input is less than 2 e.g simply "query" which is unclear
        # Structure of query timestamp of block 5: query timestamp 5
        elif user_input[0].lower() is "query" and len(user_input) >= 2:
            second_input = user_input[1]
            if second_input is "all":
                valid_input_flag = True
                sock.sendall(b"query all")
            elif second_input is "latest":
                valid_input_flag = True
                sock.sendall(b"query latest")
            elif second_input is "timestamp" and len(user_input) == 3:
                valid_input_flag = True
                sock.sendall(user_action.encode())
        # Structure of add command: add I am new block
        elif user_input[0].lower() is "add":
            data_string = user_action[3:]
            add_flag = block_chain.addblock(data=data_string)
            # if successfully added to blockchain, send out the new block
            if add_flag is True:
                data_to_send = json.dumps(block_chain.getlatest())
                # Send client command to server
                sock.sendall(b"add block")
                # Send json string of new block
                sock.sendall(data_to_send)
        if valid_input_flag is False:
            print("Invalid Action!")
        # Commands received should not be able to exceed 100 bytes
        # For this project assume block chain is small: within 256kb
        received_string = sock.recv(100).decode()
        if "send all" in received_string:
            new_block_chain_json = sock.recv(max_buffer_size)
            new_block_chain = json.loads(new_block_chain_json)
            print("Received all blocks")
            block_chain.replacechain(new_block_chain)
        # Latest block is only 1 block. Assume the block will not be very big
        elif "send latest" in received_string:
            new_block_json = sock.recv(1024)
            new_block = json.loads(new_block_json)
            print("Received latest block")
            print("Latest block data: " + new_block.data + " timestamp: " + new_block.timestamp)
        # Timestamp is small in general so 256 bytes is more than enough
        elif "send timestamp" in received_string:
            received_timestamp = sock.recv(256).decode()
            print("Received timestamp: " + received_timestamp)
        elif "add block" in received_string:
            new_block_json = sock.recv(1024)
            new_block = json.loads(new_block_json)
            add_flag = block_chain.addblocktochain(new_block)
            data_to_send = json.dumps(block_chain.getlatest())
            # Send client command to server
            sock.sendall(b"add block")
            # Send json string of new block
            sock.sendall(data_to_send)
        elif "query all" in received_string:
            data_to_send = json.dumps(block_chain)
            sock.sendall(b"send all")
            sock.sendall(data_to_send)
        elif "query latest" in received_string:
            data_to_send = json.dumps(block_chain.getlatest())
            sock.sendall(b"send latest")
            sock.sendall(data_to_send)
        elif "query timestamp" in received_string:
            pass

finally:
    print('Closing socket connection')
    sock.close()
