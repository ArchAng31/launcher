#!/usr/bin/env python3

from Service import Service, In_File_Test_Service
from Flag_Server import Flag_Server
from Service_Stand_Alone import Stand_Alone_Service
from Service_Hex_Challenge import Hex_Challenge_Service
from Service_Sha256_Challenge import Sha256_Challenge_Service
import binascii
import os
import threading
import time

round_time_in_seconds = 60
scoring_server_port = 31337
args_dict = {}
args_dict['ip'] = '0.0.0.0'
args_dict['max_threads'] = 20
args_dict['base_dir'] = os.getcwd()
args_dict['exit_file'] = os.path.join(args_dict['base_dir'], 'exit_server.txt')
args_dict['debugging'] = False
args_dict['logging'] = True
args_dict['logging_file'] = os.path.join(args_dict['base_dir'], 'server_log.txt')

#ServiceClass, individual port, service name
service_list = [
    (In_File_Test_Service, 1, "In File Test Service"),
    (Stand_Alone_Service, 2, "Stand Alone Service"),
    (Hex_Challenge_Service, 3, "Hex Challenge Service"),
    (Sha256_Challenge_Service, 4, "Sha256 Challenge Service")
]

#name, directory, auth_string, base_port
teams =  [
    ("R00t Reg", 'team1', 'teamPass1', 40000),
    ("Sh3ll Squad", 'team2', 'teamPass2', 41000),
    ("Pwn Plat00n", 'team3', 'teamPass3', 42000)
]

flags = []
flag_files = []

def add_flag(flag_file):
    with open(flag_file, 'wt') as f:
        flag = "NCX{{{}}}".format(binascii.b2a_hex(os.urandom(16)).decode('utf-8'))
        flags.append(flag)
        f.write(flag)

def create_flag(team_dir, service_name):
    flag_file = os.path.join(team_dir, service_name + '.flag')
    flag_files.append(flag_file)
    add_flag(flag_file)
    return flag_file

def update_flags():
    print("[*] MAIN FILE: Updating Flags")
    for flag_file in flag_files:
        with open(flag_file, 'rt') as f:
            old_flag = f.read().strip()
        add_flag(flag_file)
        flags.remove(old_flag)

def update_flags_and_wait_for_exit():
    while True:
        with open(args_dict['exit_file'], 'rt') as f:
            if f.read().strip() != "":
                os._exit(1)
        time.sleep(round_time_in_seconds)
        update_flags()
#(Service, args_dict, port_base + port, flag_location, service_name, auth_string)

#def launch_service(Service, ip, port, flag_location, name, debug, auth_string):
def launch_service(Service, args_dict, port, flag_location, service_name, auth_string):
    new_service = Service(args_dict, port, flag_location, name, auth_string)
    new_service.run_server()

def create_scoring_server(args_dict, server_port, flags):
    scoring_server = Flag_Server(args_dict, server_port, flags, "Scoring Server")
    scoring_server.run_server()


if __name__ == "__main__":
    print("[*] MAIN FILE: Starting Services")
    with open(args_dict['exit_file'], 'wt') as f:
        f.write('\n')
    #create team directories if they do not exist
    for team_name, team_dir, auth_string, port_base in teams:
        real_team_dir = os.path.join(args_dict['base_dir'], team_dir)
        if not os.path.exists(real_team_dir):
            os.makedirs(real_team_dir)
            print("[*] MAIN FILE: Making " + team_dir)
        #launch the threaded exploits
        for Service, port, name in service_list:
            service_name = "{}'s {}".format(team_name[:3],name)
            flag_location=create_flag(real_team_dir, name)
            t = threading.Thread(
                name="Port "+str(port),
                target=launch_service,
                args=(Service, args_dict, port_base + port, flag_location, service_name, auth_string))
            t.start()
    scoring_server = threading.Thread(
        name="Scoring Server",
        target=create_scoring_server,
        args=(args_dict, scoring_server_port, flags))
    scoring_server.start()
    update_flags_and_wait_for_exit()
