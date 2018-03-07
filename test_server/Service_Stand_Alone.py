#!/usr/bin/env python3

from Service import Service

#example new exploitable service in a seperate class file
class Stand_Alone_Service(Service):
    def __init__(self, args_dict, port, flag_location, name="", auth_string=""):
        super().__init__(args_dict, port, flag_location, name, auth_string)

    def handle_client(self, client_socket, address):
        self.client_string = self.name + ' ' + address[0] + ':' + str(address[1])
        self.dprint("Opened connection")
        self.send("Great Job Connecting to the Stand Alone Service!\n", client_socket)
        self.send_and_close("Here is your flag: {}\n".format(self.get_flag()), client_socket)
