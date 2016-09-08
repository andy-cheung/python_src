#!/usr/bin/python
import socket
import thread
import Queue
import time

def processrecv(ret):
	retlist = ret.split("#")
	#ret#sid#adminname#msgno#****
	if len(retlist) < 5:
		print("recv:" + ret)
		return
	print("sid:" + retlist[1])
	print("result:" + retlist[4])
		
def run(sock, name):
	while True:
		try:
			ret = sock.recv(1024 * 10)
			processrecv(ret)
		except socket.error:
			print("socket closed")
			exit(0)

if __name__ == '__main__':  
	name = ""
	msgno = 0
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.connect(('localhost', 8081))  

	name = raw_input("reg name:")
	sock.send("reg#" + name)  
	ret = sock.recv(1024)  
	print("reg:" + ret)
	
	thread.start_new_thread(run, (sock, name))

	while True:
		cmd = raw_input("")

		if cmd == "exit" or cmd == "quit":
			exit(0)

		msgno = msgno + 1	
		# all[sid]#****
		cmdlist = cmd.split("#")
		if len(cmdlist) < 2:
			print("cmd error!arg is not enough")
			continue
		sid = cmdlist[0]
		if not sid.isalnum() and sid != "all":
			print("sid is error")
			continue

		cmd = cmdlist[1]
		#cmd#all[sid]#adminname#msgno#****	
		allcmd = "cmd#%s#%s#%d#%s" % (sid, name, msgno, cmd)
		sock.send(allcmd) 
		# print(allcmd)

	sock.close() 