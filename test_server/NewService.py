#!/usr/bin/env python3

from binascii import b2a_hex
from os import urandom
from Service import Service

#example new exploitable service in a seperate class file
class NewService(Service):
    def __init__(self, ip, port, flag_location, name="", debug=False):
        super().__init__(ip, port, flag_location, name, debug)


    def handle_client(self, client_socket, address):
        add_str = address[0] + ':' + str(address[1])
        self.dprint(add_str + " - opened connection")
        random_hex = b2a_hex(urandom(3)).decode('utf-8')
        self.dprint(random_hex)
        msg = "Send me a string whos sha256 hash starts with " + random_hex + ".\n"
        client_socket.send(msg.encode('utf-8'))
        hex_string = hashlib.sha256(client_socket.recv(1000).strip()).hexdigest()[:6]
        if hex_string != random_hex:
            self.dprint(add_str + ": The hex_string does not match: " + hex_string + ', ' + random_hex)
            client_socket.send("The hash does not match the hex string\n".encode('utf-8'))
            client_socket.close()
            return None
        msg = "Send me your 12 character auth string xored with the random_hex (" + random_hex + ").\n"
        client_socket.send(msg.encode('utf-8'))
        auth_string = client_socket.recv(1000).strip().decode('utf-8')
        if len(auth_string) != 12:
            client_socket.send("Not a valid auth code\n".encode('utf-8'))
            self.dprint(add_str + ": Not valid auth code: " + auth_code)
        else:
            client_socket.send("Congrats! Here is your flag\n".encode('utf-8'))
            client_socket.send(self.get_flag().encode('utf-8'))
        client_socket.close()
        self.dprint(add_str + " - closed connection")
