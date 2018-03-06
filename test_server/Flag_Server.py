#!/usr/bin/env python3

from Service import Service

#example basic exploitable test service inside this same class file
class Flag_Server(Service):
    def __init__(self, ip, port, flags, name="", debug=False, auth_string=""):
        super().__init__(ip, port, None, name, debug, auth_string)
        # this is a pointer to flags from server.py
        self.flags = flags

    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        self.dprint("Opened connection")
        flag = self.recv(1000, client_socket)
        if flag in self.flags:
            msg = "Great Job! Correct Flag.\n"
            print("{} submited flag: {}".format(address[0], flag))
        else:
            msg = "Incorrect Flag.\n"
        self.send_and_close(msg, client_socket)
