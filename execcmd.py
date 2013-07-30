# import MySQLdb
import string
import os, re
import sys
import time
import urllib
import commands

def startSrv():
	print("startSrv....")
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

def loadConfig():
	dbhost = "127.0.0.1"
	dbport = 3306
	dbname = "actor"

	f = open("DBServer.txt", "r")
	list = f.readlines() 
	find = False
	for line in list:
		if line.find("SQL") >= 0:
			find = True
			continue
		if find:
			if line.find("Host") >= 0:
				m = re.search(r"\"[^\"]*\"", line)
				if m:
					dbhost = m.group(0).replace("\"", "")
					print dbhost
				else:
					print "error!!" + line
					exit(-1)
			if line.find("Port") >= 0:
				m = re.search(r"\d+", line)
				if m:
					dbport = m.group(0)
					print dbport
				else:
					print "error!!" + line
					exit(-1)
			if line.find("DBName") >= 0:
				m = re.search(r"\"[^\"]*\"", line)
				if m:
					dbname = m.group(0).replace("\"", "")
					print dbname
				else:
					print "error!!" + line
					exit(-1)
	return dbhost, dbport, dbname

def process(sid, cmdid, cmd, para1, para2):
	print("recv:" + cmd)
	output = ""
	if cmd == "update":
		status, output = commands.getstatusoutput("update.sh")
		#upate:download and unzip
		print(output)

	#send result to web server
	f = urllib.urlopen("http://localhost/servercmd_callback.jsp?cmdid=%d&ret=%s&sid=%d" % (cmdid, output, sid))
	s = f.read()
	print("web result:", s)
	f.close()

if __name__ == '__main__':
	dir = os.getcwd()
	startSrv()
	print "========================="
	print("startSrv success!")
	print "========================="
	
	os.chdir(dir)
	
	# load config
	dbhost, dbport, dbname = loadConfig()

	#connect to mysql
	conn = MySQLdb.Connect(host=dbhost, user='root', passwd="hoolai12", port=string.atoi(dbport), db=dbname)
	print("connect to mysql succ!")

	cur = conn.cursor()
	while True:
		# load cmd from db per 5 sec
		cur.execute("select id,serverid,cmdid, cmd, param1, param2 from servercmd limit 1")
		if cur.rowcount >= 1:
			row = cur.fetchone()
			id = row[0]
			sid = row[1]
			process(sid, row[2], row[3], row[4], row[5])
						
			#after process cmd, should delete from db
			n = cur.execute("delete from servercmd where id=%d" % id)
			if n <= 0:
				exit(-1)	#delete error,exit system

		time.sleep(5)
