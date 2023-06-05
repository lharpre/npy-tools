#!/usr/bin/env python3

import subprocess, optparse, re

#return command line arguments
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="The interface to change the MAC address")
    parser.add_option("-m", "--new_mac", dest="new_mac", help="The new MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please Enter An Interface, See --help For Further Information")
    elif not options.new_mac:
        parser.error("[-] Please Enter A MAC Address, See --help For Further Information")
    return options

#update mac address
def update_mac_address(interface, new_mac):
    print("[+] Changing Mac Address For Network Interface " + interface + " to " + new_mac)
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])

#check update success
def get_current_mac(interface):
    result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(result))
    if not mac_search_result:
        print("[-] No MAC Address Found")
        return str(mac_search_result)
    return mac_search_result.group()

options = get_arguments()
update_mac_address(options.interface, options.new_mac)

#check successful operation
if get_current_mac(options.interface) == options.new_mac:
    print("[+] MAC Address Update Successful\n")
else:
    print("[-] MAC Address Not Updated\n")