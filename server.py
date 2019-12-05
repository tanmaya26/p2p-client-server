import socket
import cPickle as pickle
import random
from thread import *
import platform
import time
import threading

serverPort = 7734
server_name = socket.gethostname()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_name, serverPort))
server_socket.listen(5)
print(server_name)
print('Server running on port 7734...')
active_peers = {}

rfc_index = {}


def add_client_to_list(client_hostname, upload_port):
    active_peers[client_hostname] = upload_port


def add_rfc_index(rfc_number, rfc_host, rfc_title):
    if rfc_number not in rfc_index.keys():
        rfc_index[rfc_number] = []
    rfc_index[rfc_number].append((rfc_host, rfc_title))


def generate_response(rfc_number, rfc_host, rfc_upload_port, rfc_title):
    # P2P - CI / 1.0 200 OK
    # RFC 123 A Proferred Official ICP thishost.csc.ncsu.edu 5678

    message = 'RFC' + ' ' + str(rfc_number) + ' ' + str(rfc_title) + ' ' + str(rfc_host[:rfc_host.find(":")]) + ' ' \
              + str(rfc_upload_port) + '\r\n'
    return message


def lookup_peer(rfc_number, rfc_title):
    message = 'P2P-CI/1.0 200 OK'
    message = message + '\r\n'
    if rfc_number in rfc_index.keys():
        for rfc in rfc_index[rfc_number]:
            if rfc_title == rfc[1]:
                peer_host = rfc[0]
                if peer_host in active_peers.keys():
                    peer_upload_port = active_peers[peer_host]
                    response = generate_response(rfc_number, peer_host, peer_upload_port, rfc_title)
                    message += response
    else:
        message = "P2P-CI/1.0 404 Not Found"
    message += '\r\n'
    return message


def list_peers():
    if len(rfc_index) == 0:
        message = "P2P-CI/1.0 404 Not Found\r\n"
    else:
        message = "P2P-CI/1.0 200 OK"
        message += '\r\n'
        for rfc_number in rfc_index.keys():
            peer_host = rfc_number[0]
            rfc_title = rfc_number[1]
            if peer_host in active_peers.keys():
                peer_upload_port = active_peers[peer_host]
                response = generate_response(rfc_number, peer_host, peer_upload_port, rfc_title)
                message += response
    message += '\r\n'
    return message


def client_connection(connection, addr):
    while 1:
        message_received = connection.recv(1024)
        messages = pickle.loads(message_received)
        flag = 0

        for message in messages:
            if message[0:4] == 'EXIT':
                flag = 1
                break
            elif message[0:3] == 'ADD':
                message_data = message.split('\r\n')
                if (len(message_data) == 5) and "ADD RFC" in message_data[0] and "Host:" in message_data[
                    1] and "Port:" in \
                        message_data[2] and "Title:" in message_data[3]:

                    if 'P2P-CI/1.0' in message_data[0]:
                        rfc_number = message_data[0].split(' ')[2]
                        rfc_upload_port = message_data[2].split(' ')[1]
                        rfc_host = message_data[1].split(' ')[1] + ":" + str(rfc_upload_port)
                        rfc_title = message_data[3].split(' ')[1]
                        add_rfc_index(rfc_number, rfc_host, rfc_title)
                        version = 'P2P-CI/1.0 200 OK'
                        response = version + '\r\n' + generate_response(rfc_number, rfc_host, rfc_upload_port,
                                                                        rfc_title)
                        response += '\r\n'
                        connection.sendall(response)
                    else:
                        response = "505 P2P-CI Version Not Supported\r\n"
                        connection.sendall(response)
                else:
                    response = "400 Bad Request\r\n"
                    connection.sendall(response)

            elif message[0:4] == 'LOOK':
                message_data = message.split('\r\n')
                if (len(message_data) == 5) and "LOOKUP" in message_data[0] and "Host:" in message_data[
                    1] and "Port:" in \
                        message_data[2] and "Title:" in message_data[3]:
                    if 'P2P-CI/1.0' in message_data[0]:
                        rfc_number = message_data[0].split(' ')[2]
                        rfc_title = message_data[3].split(' ')[1]
                        lookup_peer(rfc_number, rfc_title)
                        response = lookup_peer(rfc_number, rfc_title)
                        connection.sendall(response)
                    else:
                        response = "505 P2P-CI Version Not Supported\r\n"
                        connection.sendall(response)
                else:
                    response = "400 Bad Request\r\n"
                    connection.sendall(response)
            elif message[0:4] == 'LIST':
                message_data = message.split('\r\n')
                if (len(message_data) == 5) and "LIST ALL" in message_data[0] and "Host:" in message_data[
                    1] and "Port:" in \
                        message_data[2]:
                    if 'P2P-CI/1.0' in message_data[0]:
                        response = list_peers()
                        connection.sendall(response)
                    else:
                        response = "505 P2P-CI Version Not Supported\r\n"
                        connection.sendall(response)
                else:
                    response = "400 Bad Request\r\n"
                    connection.sendall(response)
        # connection.sendall(response)
        if flag == 1:
            break

    # Remove peer from info lists when peer ends connection
    if active_peers.has_key(client_hostname):
        active_peers.pop(client_hostname, None)
    for rfc in rfc_index.keys():
        for i, item in enumerate(rfc_index[rfc]):
            if item[0] == client_hostname:
                rfc_index[rfc].pop(i)
            if len(rfc_index[rfc]) == 0:
                rfc_index.pop(rfc, None)

    connection.close()


while 1:
    # Receive incoming connection request from client
    connection_socket, addr = server_socket.accept()
    print 'Got incoming connection request from ', addr
    data = connection_socket.recv(1024)
    first_request = pickle.loads(data)
    client_hostname = addr[0] + ":" + str(first_request[0])
    client_upload_port = first_request[0]
    add_client_to_list(client_hostname, client_upload_port)
    # Thread will handle all the incoming requests from clients and respond back to them
    start_new_thread(client_connection, (connection_socket, addr))

server_socket.close()
client_threads = []
# try:
#     while True:
#         conn, addr = server_socket.accept()
#         client_thread = threading.Thread(target=client_connection, args=[conn, addr])
#         client_thread.start()
#         client_threads.append(client_thread)
# finally:
#     server_socket.close()
#     for client_thread in client_threads:
#         client_thread.join()
