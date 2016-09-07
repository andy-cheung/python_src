#!/usr/bin/python
import socket
if __name__ == '__main__':  
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
	sock.connect(('localhost', 8081))  
	sock.send("reg#admin")  
	ret = sock.recv(1024)  
	print(ret)
	sock.close() 