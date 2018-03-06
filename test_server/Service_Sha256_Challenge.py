#!/usr/bin/env python3

from Service import Service
import binascii
import hashlib
import os

#example new exploitable service in a seperate class file
class Sha256_Challenge_Service(Service):
    def __init__(self, ip, port, flag_location, name="", debug=False, auth_string=""):
        super().__init__(ip, port, flag_location, name, debug, auth_string)


    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        #increase timeout due to proof of work
        client_socket.settimeout(20)
        self.dprint("Opened connection")
        random_hex = binascii.b2a_hex(os.urandom(2)).decode('utf-8')
        msg = "Send me a string that whose resulting sha256 hash starts with the following random hex: {}\n".format(random_hex)
        self.send(msg, client_socket)
        received_string = self.recv(1000, client_socket)
        sha256_hash = hashlib.sha256(received_string.encode('utf-8')).hexdigest()[:4]
        if sha256_hash != random_hex:
            msg = "The provided string {} starting hash {} does not match {}.".format(received_string, random_hex, sha256_hash)
        else:
            msg = "Congrats! Here is your flag: {}\n".format(self.get_flag())
        self.send_and_close(msg, client_socket)
