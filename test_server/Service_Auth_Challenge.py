#!/usr/bin/env python3

from Service import Service
import binascii
import hashlib
import os

#example new exploitable service in a seperate class file
class Auth_Challenge_Service(Service):
    def __init__(self, args_dict, port, flag_location, name="", auth_string=""):
        super().__init__(args_dict, port, flag_location, name, auth_string)

    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        #increase timeout due to proof of work
        client_socket.settimeout(20)
        self.dprint("Opened connection")
        msg = "Send me your authentication string xored with a one-time pad.\n"
        self.send(msg, client_socket)
        xored_auth_string = self.recv(1000, client_socket, None)
        if len(xored_auth_string) < 12:
            self.send_and_close("Sorry. That auth string is not long enough.\n", client_socket)
        self.send("Send me your one-time pad.\n", client_socket)
        one_time_pad= self.recv(1000, client_socket)
        if len(xored_auth_string) <= len(one_time_pad):
            self.send_and_close("Your auth string and one time pad lengths do not match.\n", client_socket)
        auth_string = ''.join([ chr(a ^ ord(b)) for (a,b) in zip(xored_auth_string, one_time_pad) ])
        if auth_string != self.auth_string:
            msg = "The resulting auth_string {} is incorrect.\n".format(auth_string)
        else:
            msg = "Congrats! Here is your flag: {}\n".format(self.get_flag())
        self.send_and_close(msg, client_socket)
