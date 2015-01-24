import time
if __name__ == '__main__':  
	import socket  
	s = time.time()
	testTimes = 1
	for x in xrange(0,testTimes):

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
		sock.connect(('42.62.59.59', 8001))  
		# sock.connect(('192.168.17.201', 843))  
		import time  
		sock.send('<policy-file-request/>\0')  
		ret = sock.recv(1024)  
		sock.close() 
		if ret != '<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>':
			print 'recv result error!', ret
			
		if x % 100 == 0:
			print x
	e = time.time()
	print s, e
	print testTimes / (e - s)