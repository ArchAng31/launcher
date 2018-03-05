#!/usr/bin/env python3

from socket import *
from binascii import b2a_hex
from os import urandom
from threading import Thread

class Service():
    def __init__(self, ip, port, flag_location, name="", debug=False, auth_string=""):
        self.ip = ip
        self.port = port
        self.flag_location = flag_location
        self.name = name
        self.debug = debug
        self.auth_string = auth_string
        self.max_threads = 20
        self.dprint("Launching Server")
        self.server_socket = self.create_socket()

    #this is a debug print. Set debug to True to see
    #set debug to false to turn off
    def dprint(self, text):
        if self.debug:
            print(self.name + ': ' + text)

    #create basic server socket
    def create_socket(self):
        self.dprint("binding to " + str(self.port))
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        return server_socket

    #listen to socket in a threaded manner
    def run_server(self):
        self.server_socket.listen(self.max_threads)
        counter = 0
        while True:
            (client_socket, address) = self.server_socket.accept()
            print(address)
            t = Thread(name="Thread "+str(counter), target=self.handle_client, args=(client_socket, address))
            counter += 1
            t.start()

    #basic client_recv example
    def client_recv(self, sock):
        data = sock.recv(1000)
        while data == "":
            data = sock.recv(1000)
        return data

    def get_flag(self):
        with open(self.flag_location, 'rt') as f:
            return f.read().strip()


#example basic exploitable test service inside this same class file
class ServiceTest(Service):
    def __init__(self, ip, port, flag_location, name="", debug=False, auth_string=""):
        super().__init__(ip, port, flag_location, name, debug, auth_string)


    def handle_client(self, client_socket, address):
        add_str = address[0] + ':' + str(address[1])
        self.dprint(add_str + " - opened connection")
        random_hex = b2a_hex(urandom(3)).decode('utf-8')
        self.dprint(random_hex)
        msg = "Send me a string that starts with " + random_hex + ".\n"
        client_socket.send(msg.encode('utf-8'))
        #hex_string = hashlib.sha256(client_socket.recv(1000).strip()).hexdigest()[:6]
        hex_string = client_socket.recv(1000).decode('utf-8').strip()[:6]
        if hex_string != random_hex:
            self.dprint(add_str + ": Not valid hex string: " + hex_string + ', ' + random_hex)
            client_socket.close()
            return None
        client_socket.send("Congrats! Here is your flag\n".encode('utf-8'))
        client_socket.send(self.get_flag().encode('utf-8'))
        client_socket.close()
        self.dprint(add_str + " - closed connection")
