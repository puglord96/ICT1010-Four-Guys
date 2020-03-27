import socket
import sys
from block import Block
from blockchain import BlockChain
import json

# Create a TCP/IP Socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('localhost', 10000)
blockchain = BlockChain()
blockchain.addblock("testingblock")
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)
while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(256)
            print('received {!r}'.format(data))
            if b"query latest" in data:
                data_to_send = json.dumps(blockchain.getlatest())  # Convert latest block to json string and send
                sock.sendall(b"send latest")
                sock.sendall(data_to_send)
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from', client_address)
                break
    finally:
        # Clean up the connection
        connection.close()