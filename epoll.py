#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, select
import Queue
 
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
message_queues = {}
 
fd_to_socket = {serversocket.fileno():serversocket,}
while True:
	print("waiting for new connection.....")
	timeout = 10
	#轮询注册的事件集合
	events = epoll.poll(timeout)
	if not events:
		continue
	for fd, event in events:
		socket = fd_to_socket[fd]
		#可读事件
		elif event & select.EPOLLIN:
			#如果活动socket为服务器所监听，有新连接
			if socket == serversocket:
				connection, address = serversocket.accept()
				print "new connection" , address
				connection.setblocking(0)
				#注册新连接fd到待读事件集合
				epoll.register(connection.fileno(), select.EPOLLIN)
				fd_to_socket[connection.fileno()] = connection
				message_queues[connection]	= Queue.Queue()
			#否则为客户端发送的数据
			else:
				closefd = False
				try:
					data = socket.recv(1024)
				except socket.error:
					if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN): # since this is a non-blocking socket..
						closefd = True
				if data:
					print "recv data", data , "client:" , socket.getpeername()
					message_queues[socket].put(data)
					#修改读取到消息的连接到等待写事件集合
					epoll.modify(fd, select.EPOLLOUT)
				else:
					closefd = True

				if closefd:
					epoll.unregister(fd)
					fd_to_socket[fd].close()
					del fd_to_socket[fd]
		#可写事件
		elif event & select.EPOLLOUT:		
			try:
				msg = message_queues[socket].get_nowait()
			except Queue.Empty:
				print socket.getpeername() , " queue empty"
				epoll.modify(fd, select.EPOLLIN)
			else :
				print "send data" , msg , "client:" , socket.getpeername()
				socket.send(msg)
		
epoll.unregister(serversocket.fileno())
epoll.close()
serversocket.close()