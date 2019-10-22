#!/usr/bin/env python3

import subprocess
import optparse
import re

def change_mac(interface, new_mac):

	print ("[+] Changing " + interface + " MAC Address to " + new_mac)

	# subprocess.call("ifconfig "+ interface+" down", shell=True)
	# subprocess.call("ifconfig "+ interface +" hw ether " + new_mac, shell=True)
	# subprocess.call("ifconfig "+ interface +" up", shell=True)


	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])

def get_arguments():
	parser = optparse.OptionParser()

	parser.add_option("-i", "--interface", dest="interface", help="Interface Mac Adress to be changed")
	parser.add_option("-m", "--mac", dest="new_mac", help="New Mac Address")
	# parser.add_option("-n", "--inter", dest="interfaces", help="Print available Interfaces")
	(options, arguments)  = parser.parse_args()

	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more info")

	if not options.new_mac:
		parser.error("[-] Please specify a new mac, use --help for more info")

	return options

def get_current_interfaces():

	interfaces_ifconfig_result = subprocess.check_output(["ifconfig", ])
	result_decode = interfaces_ifconfig_result.decode("utf-8")
	interfaces_search_result = re.findall(r'\n.\w:*', result_decode, flags=0)

	if interfaces_search_result:
		return interfaces_search_result
	else:
		print("[-] Could not get the current interfaces.")


def get_current_mac_address(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	result_decode = ifconfig_result.decode("utf-8")
	mac_address_search_result = re.search(r'[\w{2}:]{17}', result_decode)

	# print(mac_address_search_result)

	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not read Mac Address.")

options = get_arguments()


available_interfaces = get_current_interfaces()

print("[+] Available Interfaces: " + str(available_interfaces))

current_mac = get_current_mac_address(options.interface)

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac_address(options.interface) #overide current_mac varidable with new value

if current_mac == options.new_mac:
	print("[+] Mac Address changed to " + get_current_mac_address(options.interface))
else:
	print("[-] Could not change Mac Address.")
