#!/usr/bin/env python3

from Exploit import Exploit, In_File_Test_Exploit
from Exploit_Stand_Alone import Stand_Alone_Exploit
import random
import threading
import time

debug = True
debug_chaff = False
round_time_in_seconds = 60
chaff_to_real_ratio = 3

#exploit list in format (ExploitClass, exploit_port, exploit_name)
exploit_list = [
    (In_File_Test_Exploit, 40001, "In File Test Exploit"),
    (Stand_Alone_Exploit, 40002, "Stand Alone Exploit")
]

def submit_flag(name, flag):
    #write some code to connect to the flag server and summit your flags.
    print("{}Received Flag: {}".format(name, flag))

def launch_exploit(Exploit, ip, port, name, debug, debug_chaff):
    new_exploit = Exploit(ip, port, name, debug, debug_chaff)
    chaff_array = [False]*chaff_to_real_ratio
    chaff_array.append(True)
    random.shuffle(chaff_array)
    #this is not threaded to prevent DOSing server, but also do not make
    #chaff_to_real_ratio so big it takes longer than a round
    for value in chaff_array:
        if value:
            target, flag = new_exploit.get_flag()
            submit_flag(target, flag)
        else:
            new_exploit.send_chaff()


if __name__ == "__main__":
    print("[*] Starting Launcher")
    #get the list of ips
    with open('ips.txt', 'rt') as f:
        ips = f.read().strip().split('\n')
    #launch the threaded exploits
    while True:
        for ip in ips:
            for Exploit, port, name in exploit_list:
                t = threading.Thread(
                    name=name+ " against " + ip,
                    target=launch_exploit,
                    args=(Exploit, ip, port, name, debug, debug_chaff))
                t.start()
        time.sleep(round_time_in_seconds)
