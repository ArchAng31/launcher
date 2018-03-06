#!/usr/bin/env python3

from Service import Service
from socket import *
from binascii import b2a_hex
from os import urandom
from threading import Thread

#example basic exploitable test service inside this same class file
class Hex_Challenge_Service(Service):
    def __init__(self, ip, port, flag_location, name="", debug=False, auth_string=""):
        super().__init__(ip, port, flag_location, name, debug, auth_string)

    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        self.dprint("Opened connection")
        random_hex = b2a_hex(urandom(3)).decode('utf-8')
        msg = "Send me a string that starts with the following random hex: {}\n".format(random_hex)
        self.send(msg, client_socket)
        received_hex_string = self.recv(1000, client_socket)[:6]
        if received_hex_string != random_hex:
            msg = "The hex strings {} and {} do not match.".format(random_hex, received_hex_string)
        else:
            msg = "Congrats! Here is your flag: {}\n".format(self.get_flag())
        self.send_and_close(msg, client_socket)
