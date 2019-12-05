import socket
import os
import cPickle as pickle
import random
from thread import *
import platform
import time
import email.utils
import sys

serverPort = 7734
serverName = sys.argv[1]
upload_port_number = 60000 + random.randint(1, 1000)
directory = sys.argv[2]


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((serverName, serverPort))
    return client_socket


client_socket = connect()

print 'Connected to server at: ' + str(serverName) + " and port: " + str(serverPort)
client_hostname = client_socket.getsockname()[0]


def add_request(rfc_number, rfc_title):
    message = "ADD RFC " + str(rfc_number) \
              + " P2P-CI/1.0\r\n" + "Host: " + str(client_hostname) + "\r\n" + "Port: " \
              + str(upload_port_number) \
              + "\r\n" + "Title: " + str(rfc_title) + "\r\n"
    return message


def lookup_request(rfc_number, rfc_title):
    message = "LOOKUP RFC " + str(rfc_number) \
              + " P2P-CI/1.0\r\n" + "Host: " + str(client_hostname) + "\r\n" + "Port: " \
              + str(upload_port_number) \
              + "\r\n" + "Title: " + str(rfc_title) + "\r\n"
    return message


def list_request():
    message = "LIST ALL RFC " + " P2P-CI/1.0\r\n" + "Host: " + str(client_hostname) + "\r\n" + \
              "Port: " + str(upload_port_number) \
              + "\r\n"
    return message


def get_request(rfc_number):
    message = "GET RFC " + str(rfc_number) + " P2P-CI/1.0\r\n" \
                                             "Host: " + str(client_hostname) + "\r\n" \
                                                                               "OS: " + platform.platform() + "\r\n"
    return message


def upload_socket_bind():
    try:
        upload_socket = socket.socket()
        host = '0.0.0.0'
        upload_socket.bind((host, upload_port_number))
        upload_socket.listen(5)
        return upload_socket
    except socket.error as msg:
        print("Socket binding error" + str(msg) + "\n" + "Retrying...")
        upload_socket_bind()


def upload():
    while 1:
        download_socket, download_addr = upload_socket.accept()
        download_message = "Viola! Connected to " + str(client_hostname) + ":" + str(upload_port_number)
        download_socket.sendall(download_message)
        message = download_socket.recv(1024)
        data = message.split('\r\n')

        if len(data) == 4 and "GET RFC " in data[0] and "Host: " in data[1] and "OS: " in data[2]:
            if 'P2P-CI/1.0' in data[0]:
                request = data[0].split(" ")
                if request[0] == 'GET':
                    rfc_number = request[2]
                    rfc_file_path = os.getcwd() + "/" + directory + "/RFC" + rfc_number + ".txt"
                    opened_file = open(rfc_file_path, 'r')
                    file_data = opened_file.read()
                    response = "P2P-CI/1.0 200 OK\r\n" \
                               "Date: " + str(email.utils.formatdate(usegmt=True)) + "\r\n" \
                                                                                     "OS: " + str(
                        platform.platform()) + "\r\n" \
                                               "Last-Modified: " + str(
                        time.ctime(os.path.getmtime(rfc_file_path))) + "\r\n" \
                                                                       "Content-Length: " + str(len(file_data)) + "\r\n" \
                                                                                                                  "Content-Type: text/plain\r\n"
                    response = response + file_data

                    download_socket.sendall(response)
            else:
                response = "505 P2P-CI Version Not Supported\r\n"
                download_socket.send(response)
        else:
            response = "400 Bad Request\r\n"
            download_socket.send(response)


def download_rfc(request, peer_hostname, peer_port, rfc_number):
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peer_socket.connect((peer_hostname, int(peer_port)))
    # print 'Connected to server at: ' + str(peer_hostname) + " and port: " + str(peer_port)
    connect_msg = peer_socket.recv(1024)
    print connect_msg
    peer_socket.sendall(request)
    peer_response = peer_socket.recv(1024)
    if '200 OK' in peer_response.split("\r\n")[0]:
        print 'P2P-CI/1.0 200 OK'
        content_line = (peer_response.split("\r\n"))[4]
        content_length = int(content_line.split(' ')[1])
        peer_response = peer_response + peer_socket.recv(content_length)
        rfc_file_path = os.getcwd() + "/" + directory + "/RFC" + rfc_number + ".txt"
        data = peer_response[peer_response.find('text/plain\r\n') + 12:]

        with open(rfc_file_path, 'w') as file:
            file.write(data)
        print 'File Received from peer and stored locally now'
    elif 'Version Not Supported' in peer_response.split("\r\n")[0]:
        print 'Version Not Supported'
    elif 'Bad Request' in peer_response.split("\r\n")[0]:
        print '400 Bad Request'
    # peer_socket.close()


def client_input():
    print "Enter if you want to: ADD, GET, LIST, LOOKUP or EXIT:"
    service = raw_input()
    if service == 'ADD':
        print("Enter RFC number:")
        rfc_number = raw_input()
        print("Enter Title")
        rfc_title = raw_input()
        rfc_file_path = os.getcwd() + "/" + directory + "/" + "RFC" + rfc_number + ".txt"
        if os.path.isfile(rfc_file_path):
            request = add_request(rfc_number, rfc_title)
            request_list = [request]
            request_message = pickle.dumps(request_list, -1)
            client_socket.sendall(request_message)
            response = client_socket.recv(1024)
            print "ADD Response from the server"
            print response
        else:
            print "File Not Present in the directory"
        client_input()

    elif service == 'LOOKUP':
        print("Enter RFC number:")
        rfc_number = raw_input()
        print("Enter Title")
        rfc_title = raw_input()
        request = lookup_request(rfc_number, rfc_title)
        request_list = [request]
        request_message = pickle.dumps(request_list, -1)
        client_socket.sendall(request_message)
        response = client_socket.recv(1024)
        print "LOOKUP Response from the server"
        print response
        client_input()

    elif service == 'LIST':
        request = list_request()
        request_list = [request]
        request_message = pickle.dumps(request_list, -1)
        client_socket.sendall(request_message)
        response = client_socket.recv(1024)
        print "LIST ALL Response from the server"
        print response
        client_input()

    elif service == 'GET':
        print "Enter RFC Number"
        rfc_number = raw_input()
        print "Enter Title"
        rfc_title = raw_input()
        print "Enter Peer Hostname"
        peer_hostname = raw_input()
        print "Enter Peer Port"
        peer_port = raw_input()

        download_req = get_request(rfc_number)
        print "GET Request to be sent to the peer having the RFC File"
        print download_req

        download_rfc(download_req, peer_hostname, peer_port, rfc_number)
        rfc_file_path = os.getcwd() + "/" + directory + "/" + "RFC" + rfc_number + ".txt"
        if os.path.isfile(rfc_file_path):
            request = add_request(rfc_number, rfc_title)
            request_list = [request]
            request_message = pickle.dumps(request_list, -1)
            client_socket.sendall(request_message)
            response = client_socket.recv(1024)
            print "ADD Response from the server"
            print response
        else:
            print "File Not Present in the directory"
        client_input()

    elif service == 'EXIT':
        message = "EXIT"
        exit_message = pickle.dumps([message], -1)
        client_socket.sendall(exit_message)
        client_socket.close()

    else:
        print ("Wrong option. Try again...")
        client_input()


def send_peer_info(client_socket, directory):
    rfc_numbers = []
    rfc_titles = []
    all_requests = []
    rfc_storage_path = os.getcwd() + "/" + directory
    for file_name in os.listdir(rfc_storage_path):
        if 'RFC' in file_name:
            rfc_number = file_name[file_name.find("C") + 1:file_name.find(".")]
            rfc_title = file_name[:file_name.find(".")]
            req_message = add_request(rfc_number, rfc_title)
            print "ADD Request to be sent to the server"
            print req_message
            #information_list = [req_message]
            all_requests.append(req_message)

    info_add = pickle.dumps(all_requests, -1)
    client_socket.sendall(info_add)
    response_received = client_socket.recv(1024)
    print "ADD Response sent from the server"
    print response_received


data = pickle.dumps([upload_port_number])

client_socket.send(data)
# client_socket.close()

send_peer_info(client_socket, directory)
upload_socket = upload_socket_bind()

start_new_thread(upload, ())

client_input()
