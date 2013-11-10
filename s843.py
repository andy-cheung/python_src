import os
import contextlib
import sys
import socket
import thread

def startSrv():
    print("startSrv....")
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except Exception, e:
        print e
        sys.exit(1)
    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except Exception, e:
        print e
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()

def clientThread(connection, address):
    try:  
        with contextlib.closing(connection):
            connection.settimeout(5)  
            buf = connection.recv(1024)  
            if buf != '<policy-file-request/>\0':  
                print 'request error:', buf
            connection.sendall('<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>')  
    except Exception, e:
        print e  

if __name__ == '__main__':
    startSrv()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(('', 843))  
        sock.listen(10)  
    except Exception, e:
        sys.exit(1)
        print e
    while True:
        try:
            connection,address = sock.accept()  
            thread.start_new(clientThread, (connection, address))
        except Exception, e:
            print e
