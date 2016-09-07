#!/usr/bin/python
import socket
if __name__ == '__main__':  
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.connect(('localhost', 8081))  

	name = raw_input("reg name:")
	sock.send("reg#" + name)  
	ret = sock.recv(1024)  
	print(ret)
	msgno = 0
	while True:
		cmd = raw_input("cmd:")
		sid = raw_input("sid or all:")
		if cmd == "exit" or cmd == "quit":
			cmd = "exit"
		else:
			#cmd#all[sid]#adminname#msgno#****	
			cmd = "cmd#%s#%s#%d#%s" % (sid, name, msgno, cmd)
			msgno = msgno + 1
		sock.send(cmd)  
		ret = sock.recv(1024)  
		print(ret)
	sock.close() 