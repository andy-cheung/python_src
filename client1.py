#!/usr/bin/python
import socket
import thread
import Queue
import time

msglist = Queue.Queue()
name = ""

def run():
	msgno = 0
	while True:
		try:
			cmd = msglist.get_nowait()
		except Queue.Empty:
			time.sleep(1)
		else:
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

			try:
				sock.send(allcmd)  
				ret = sock.recv(1024 * 10)
				print(ret)
			except socket.error:
				print("socket closed")
				exit(0)

if __name__ == '__main__':  
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.connect(('localhost', 8081))  

	name = raw_input("reg name:")
	sock.send("reg#" + name)  
	ret = sock.recv(1024)  
	print(ret)
	
	thread.start_new_thread(run, ())

	while True:
		cmd = raw_input("cmd:")

		if cmd == "exit" or cmd == "quit":
			exit(0)

		msglist.put(cmd)

	sock.close() 