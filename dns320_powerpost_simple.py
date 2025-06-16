#!/usr/bin/env python3
######################
#	dns320_powerpost_simple.py: une execution de shutdown/restart pour NAS DNS320
#	en utilisant les requetes GET/POST en simple HTTP
#	puisqu'impossible rentrer avec le SSH boudiou nom de diou
#
#	LAFONTAINE Cédric Camille 2025
#	contact@codelibre.fr
#
#           _        _ _ _             ___
#  ___ ___ _| |___   | |_| |_ ___ ___  |  _|___
# |  _| . | . | -_|  | | | . |  _| -_|_|  _|  _|
# |___|___|___|___|  |_|_|___|_| |___|_|_| |_|
#
# ASCII art generator: http://patorjk.com/software/taag/
#
# VERSION 0.2 ASPERGE BAVEUSE
#
#	SETTINGS SHOULD BE SET MANUALLY IN THE HEAD OF THIS SCRIPT
#	I LEFT MINE
#
#	example usage:
#		- fill the settings
#		- uncomment the desired line at the bottom of this script
#
# PLEASE NOTE: do not give internet access to DNS320 NAS. There is a firmware breach revealed in 2020.
#
# TODO::
# detectdangerous needs improvments
# add forced_shutdown (bypass dangerous)?
######################
import requests
import base64

# NAS IP and port
ip_address = '192.168.8.101'
port = 80  # HTTP port. Maybe implement SSL?

# Login URL
login_url = f'http://{ip_address}:{port}/cgi-bin/login_mgr.cgi'
# URL of the 'API' endpoint
COMMAND_URL = f'http://{ip_address}:{port}/cgi-bin/hd_config.cgi'
POWER_URL = f'http://{ip_address}:{port}/cgi-bin/system_mgr.cgi'

# Your credentials
username = 'admin'
password = 'admin'

# Prepare POST data
payload = {
	'cmd': 'login',
	'username': username,
	'pwd': base64.b64encode(password.encode()).decode(),
	'port': str(port)
}
# Create session
session = requests.Session()
# Send POST request to login
response = session.post(login_url, data=payload)

def DetectDangerous():
	"""
	Returns True if dangerous, False otherwise.
	"""
	######################################################################
	##### Command implemented from the original javascript code
	##### /web/function/function.js $("#home_restart") $("#home_shutdown") .click(function()
	######################################################################
	data = {'cmd': 'cgi_Detect_Dangerous'}
	response = session.post(COMMAND_URL, data=data)

	# Assuming server returns a JSON or plain text indicating danger
	# Adjust parsing based on actual response format
	if response.status_code == 200:
		# Example: if response.text contains 'dangerous' or similar
		# You'll need to adapt this based on actual response
		if 'danger' in response.text.lower():
			return True
		else:
			return False
	else:
		print(f"Failed to detect danger: {response.status_code}")
		return True  # Be cautious and assume dangerous if detection fails

def WhatWeWant(cmd):
	if DetectDangerous():
		print("Operation aborted: Dangerous operations detected.")
		return
	# Check command
	if (cmd != "shutdown" and cmd != "restart"):
		return ("WRONG COMMAND (" + cmd + "). shutdown or restart only")
	# Send command
	data = {'cmd': 'cgi_restart'}
	msg = "PLEASE WAIT FOR RESTART"
	if (cmd == "shutdown"):
		data = {'cmd': 'cgi_shutdown'}
		msg = "SHUTTING DOWN NOW"
	response = session.post(POWER_URL, data=data)
	if response.status_code == 200:
		print(f"{cmd} command sent successfully.")
		print(msg)
	else:
		print(f"Failed to send command: {response.status_code}")
		
if response.ok:
	# You may need to inspect response.text or response.status_code
	print("Login request sent. Proceeding command::")
	# Usage example, uncomment:
	# WhatWeWant("restart")
	# or
	# WhatWeWant("shutdown")
else:
	print("HTTP session error.")
