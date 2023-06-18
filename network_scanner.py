#!/usr/bin/env python3

import scapy.all as scapy
import argparse

#Reading Command Line Arguments
def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="target_network", help="Network Address To Be Scanned")
	options = parser.parse_args()
	if not options.target_network:
		parser.error("[-] Network Address Not Supplied")
	return options
	
#Scan Network For IP MAC Addresses
def scan(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	arp_request_broadcast = broadcast/arp_request
	#Index 0 - Answered List. Index 1 = Unanswered List.
	answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

	client_list = []
	for i in answered_list:
		client = {"ip":i[1].psrc, "mac":i[1].hwsrc}
		client_list.append(client)
	return client_list

def print_result(clients):
	print("IP\t\t\tMAC Address\n------------------------------------------")
	for client in clients:
		print(client["ip"] + "\t\t" + client["mac"])

print("[+] Scanning For Clients On The Network\n")

options = get_arguments()
scan_result = scan(options.target_network)
print_result(scan_result)