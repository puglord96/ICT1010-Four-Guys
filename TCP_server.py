import socket
import sys
from blockchain import BlockChain
import pickle
import threading

# Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
blockchain = BlockChain()
blockchain.addblock("Assignment 2")
max_buffer_size = 256000  # kernel receive buffer size of socket
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

# Thread handle for new TCP Connection
def handle_connection(connection, client_address):
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(256)
            print('received {!r}'.format(data))
            if b"query latest" in data:
                data_to_send = pickle.dumps(blockchain.getlatest())  # Convert latest block to json string and send
                connection.sendall(b"send latest")
                connection.sendall(data_to_send)
            if b"query all" in data:
                data_to_send = pickle.dumps(blockchain)
                connection.sendall(b"send all")
                connection.sendall(data_to_send)
                connection.sendall(b"send end")
            if b"update chain" in data:
                received_block_chain_bytes = connection.recv(max_buffer_size)
                # append full bytes string
                full_bytes = received_block_chain_bytes
                while received_block_chain_bytes:
                    received_block_chain_bytes = connection.recv(max_buffer_size)
                    full_bytes += received_block_chain_bytes
                received_block_chain = pickle.loads(full_bytes)
                blockchain.blocks = received_block_chain.blocks
                print("Replaced blockchain")
                blockchain.print_all()
            if b"add block" in data:
                received_block_bytes = connection.recv(1024)
                received_block = pickle.loads(received_block_bytes)
                add_flag = blockchain.addblocktochain(received_block)
                if add_flag:
                    print("Successfully added valid block")
                    print("Data: " + blockchain.getlatest().data)
                    connection.sendall(b"add finish")
                else:
                    print("New block is not valid")
                    connection.sendall(b"add fail")
            if b"query timestamp" in data:
                requested_block_no = int(data.decode()[15:])
                connection.sendall(b"send timestamp")
                connection.sendall(blockchain.timestamp(requested_block_no).encode())
            if b"connection close" in data:
                break
    finally:
        connection.close()


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    # Create new thread per TCP connection
    client_thread = threading.Thread(target=handle_connection,args=(connection,client_address,))
    client_thread.start()
