#!/usr/bin/env python3

import socket
import sys
import threading
import datetime

class Service():
    def __init__(self, args_dict, port, flag_location, name="", auth_string=""):
        self.ip = args_dict['ip']
        self.port = port
        self.flag_location = flag_location
        self.name = "{:30}".format(name[:30])
        self.client_string = self.name
        self.auth_string = auth_string
        self.debugging = args_dict['debugging']
        self.logging = args_dict['logging']
        self.logging_file = args_dict['logging_file']
        self.max_threads = args_dict['max_threads']
        self.dprint("Launching Server")
        self.server_socket = self.create_socket()


    #this is a debug print. Set debug to True to see
    #set debug to false to turn off
    def dprint(self, text):
        msg = self.client_string + ' - ' + text
        if self.debugging:
            print(msg)
        if self.logging:
            with open(self.logging_file, 'at+') as debug_file:
                timestamp = '[{0:%m-%d %H:%M:%S}] '.format(datetime.datetime.now())
                debug_file.write(timestamp + msg + '\n')

    #create basic server socket
    def create_socket(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #enable port reuse incase lazy killed
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except OSError as e:
            self.dprint("ERROR establishing socket")
            sys.exit(1)
        try:
            server_socket.bind((self.ip, self.port))
            self.dprint("Bounding to port {}".format(self.port))
            return server_socket
        except OSError as e:
            self.dprint("ERROR binding to port : {}".format(e))
            sys.exit(1)


    #listen to socket in a threaded manner
    def run_server(self):
        self.server_socket.listen(self.max_threads)
        counter = 0
        while True:
            try:
                (client_socket, address) = self.server_socket.accept()
                #set a timeout of 10 so cannot open all sockets
                client_socket.settimeout(10)
                t = threading.Thread(name="threading.Thread "+str(counter), target=self.handle_client, args=(client_socket, address))
                counter += 1
                t.start()
            except OSError as e:
                self.dprint("ERROR accepting connection: {}".format(e))


    def get_flag(self):
        with open(self.flag_location, 'rt') as f:
            flag = f.read().strip()
            print("{} got flag: {}".format(self.client_string, flag))
            return flag

    def send(self, msg, socket):
        self.dprint(msg.strip())
        try:
            socket.send(msg.encode('utf-8'))
        except OSError as e:
            self.dprint("ERROR sending data: {}".format(e))
            sys.exit(1)

    def send_and_close(self, msg, socket):
        self.send(msg, socket)
        socket.close()
        self.dprint("Closed connection")

    #basic client_recv example
    def recv(self, msg_len, client_socket, decode_string='utf-8'):
        try:
            chunk = client_socket.recv(msg_len)
            if chunk == b'':
                self.dprint("ERROR received no data")
                #raise RuntimeError("socket connection broken - no data")
            recv_msg = chunk.decode(decode_string).strip()
            self.dprint("Received: " + recv_msg)
            return recv_msg
        except OSError as e:
            client_socket.send("Timeout exceeded.\n".encode(decode_string))
            client_socket.close()
            self.dprint("ERROR receiving data: {}".format(e))
            sys.exit(1)

#example basic exploitable test service inside this same class file
class In_File_Test_Service(Service):
    def __init__(self, args_dict, port, flag_location, name="", auth_string=""):
        super().__init__(args_dict, port, flag_location, name, auth_string)

    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        self.dprint("Opened connection")
        self.send("Great Job Connecting to the In File Test Service!\n", client_socket)
        self.send_and_close("Here is your flag: {}\n".format(self.get_flag()), client_socket)
