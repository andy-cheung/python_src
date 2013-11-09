import os
import sys
import socket

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
            try:  
                connection.settimeout(1)  
                buf = connection.recv(1024)  
                if buf == '<policy-file-request/>':  
                    connection.send('<?xml version="1.0"?><cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>')  
            except Exception, e:
                print e  
                
            connection.close() 
        except Exception, e:
            print e
