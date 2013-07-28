import MySQLdb
import os
import sys
import time
import urllib
import commands

def startSrv():
	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 1 fail -->%d --> %s\n" % (e.errno, e.strerror))
		sys.exit(1)
	os.chdir("/")
	os.setsid()
	os.umask(0)

	try:
		pid = os.fork()
		if pid > 0:
			sys.exit(0)
	except Exception, e:
		sys.stderr.write("fork 2 fail -->%d --> %s\n" % (e.errno, e.strerror))
		sys.exit(1)

	sys.stdout.flush()
	sys.stderr.flush()

def process(sid, cmdid, cmd, para1, para2):
	if cmd == "update":
		status, output = commands.getstatusoutput("update.sh")
		#upate:download and unzip
		print(output)
		if output == "update ok":
			ret = "ok"
		else:
			ret = "fail"

	#send result to web server
	f = urllib.urlopen("http://localhost/test.jsp?cmdid="+cmdid+"&ret="+ret+"&sid="+sid)
	s = f.read()
	print("web result:", s)
	f.close()

if __name__ == '__main__':
	startSrv()
	print "========================="
	print("startSrv success!")
	print "========================="

	#connect to mysql
	conn = MySQLdb.Connect(host='localhost',user='root', pwaswd='', port=3306)
	cur = conn.curosr()
	while True:
		# load cmd from db per 5 sec
		cur.execute("select id,sid,cmdid, cmd, para1, para2 from servercmd limit 1")
		if cur.rowcount >= 1:
			row = cur.fetchone()
			id = row[0]
			sid = row[1]
			process(sid, row[2], row[3], row[4], row[5])
						
			#after process cmd, should delete from db
			n = cur.execute("delete servercmd where id="+id)
			if n <= 0:
				exit(-1)	#delete error,exit system

		time.sleep(5)


