import os,sys
import md5

def calMD5ForFile(file):
	a_file = open(file, 'rb')
	m = md5.new(a_file.read())
	a_file.close()
	return m.hexdigest()

def check(rootdir, checkfile):
	f = open(checkfile, 'r')
	list = f.readlines() 
	for line in list:
		arg = line.split(",")
		arg[1] = arg[1].replace('\n','')
		cf = rootdir + arg[1]
		str = calMD5ForFile(cf)
		if str != arg[0]:
			print(arg[1] + ":" + str + "|" + arg[0])
			return False
	return True
succ = check(sys.argv[1], "listdir.txt") 
if succ :
	print("check ok")
else:
	print("check fail")