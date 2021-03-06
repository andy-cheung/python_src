#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select
import Queue
import os
import sys
import string

message_queues = {}
sidlist = {}
adminlist = {}

def startSrv():
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 1 fail")
		sys.exit(1)
	os.chdir("/")
	os.setsid()
	os.umask(0)

	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 2 fail")
		sys.exit(1)

	sys.stdout.flush()
	sys.stderr.flush()

def clear(fd):
	print("socket closed:%d" % fd)
	if adminlist.get(fd):
		name = adminlist.pop(fd)
		print("%s exit" % name)
	for k,v in sidlist.items():
		if v == fd:
			sid = sidlist.pop(k)	
			print("server %s exit" % sid)

def sendDataToFD(fd, msg): 
	if not fd:
		return	
	ql = message_queues.get(fd)
	if not ql:
		return
	ql.put(msg)
	#修改读取到消息的连接到等待写事件集合
	epoll.modify(fd, select.EPOLLOUT)

def sendData(sid, msg):
	fd = sidlist.get(sid)
	if not fd: 
		print("sid error %s" % sid)
		return
	sendDataToFD(fd, msg)

def sendAll(msg):
	for i in sidlist:
		sendData(i, msg)

def regclient(regname):
	if regname.find("admin") >= 0:
		for k,v in adminlist.items():
			if v == regname:
				clear(k)
		adminlist[fd] = regname
	elif regname.isalnum():
		if sidlist.get(regname):
			clear(sidlist[regname])
		#sid
		sidlist[regname] = fd
	print("%s reg!%d" % (regname, fd))
	sendDataToFD(fd, "ok")

def process(fd, msg):
	if msg == "heart":
		return

	cmdlist = msg.split("#")
	if len(cmdlist) < 0:
		return

	#msg="reg#****"
	cmd = cmdlist[0] 
	if cmd not in ["cmd", "ret", "reg"]:
		return

	if cmd == "reg":
		if len(cmdlist) < 2:
			return
		regname = cmdlist[1]
		regclient(regname)

	elif cmd == "cmd":
		#cmd#all[sid]#adminname#msgno#****
		if (len(cmdlist) < 5):
			return
		sid = cmdlist[1]
		if sid == "all":
			sendAll(msg)
		else:
			sendData(sid, msg)
		sendDataToFD(fd, "send ok")
		
	elif cmd == "ret":
		#ret#sid#adminname#msgno#****
		if (len(cmdlist) < 5):
			return	
		adminname = cmdlist[2]
		for k, v in adminlist.items():
			if v == adminname:
				sendDataToFD(k, msg)

if __name__ == '__main__':
	
	startSrv()

	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address = ("0.0.0.0", 8081)
	serversocket.bind(server_address)
	serversocket.listen(1)
	print "server start..." , server_address
	serversocket.setblocking(0)

	#新建epoll事件对象，后续要监控的事件添加到其中
	epoll = select.epoll()
	#添加服务器监听fd到等待读事件集合
	epoll.register(serversocket.fileno(), select.EPOLLIN)
	
	fd_to_socket = {serversocket.fileno():serversocket,}
	while True:
		timeout = 10
		#轮询注册的事件集合
		events = epoll.poll(timeout)
		if not events:
			continue
		for fd, event in events:
			socket = fd_to_socket[fd]
			#可读事件
			if event & select.EPOLLIN:
				#如果活动socket为服务器所监听，有新连接
				if socket == serversocket:
					connection, address = serversocket.accept()
					print "new connection" , address
					connection.setblocking(0)
					#注册新连接fd到待读事件集合
					epoll.register(connection.fileno(), select.EPOLLIN)
					fd_to_socket[connection.fileno()] = connection
					message_queues[connection.fileno()]	= Queue.Queue()
				#否则为客户端发送的数据
				else:
					closefd = False
					try:
						msg = socket.recv(1024)
					except socket.error:
						if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN): # since this is a non-blocking socket..
							closefd = True
					if msg:
						print "recv msg", msg , "client:" , socket.getpeername()
						process(fd, msg) 
					else:
						closefd = True

					if closefd:
						epoll.unregister(fd)
						fd_to_socket[fd].close()
						del fd_to_socket[fd]
						clear(fd)
			#可写事件
			elif event & select.EPOLLOUT:		
				try:
					msg = message_queues[fd].get_nowait()
				except Queue.Empty:
					epoll.modify(fd, select.EPOLLIN)
				else :
					socket.send(msg)
					print "send data:" , msg 

			
	epoll.unregister(serversocket.fileno())
	epoll.close()
	serversocket.close()