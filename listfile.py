import os,sys
import md5

def calMD5ForFile(file):
	a_file = open(file, 'rb')
	m = md5.new(a_file.read())
	a_file.close()
	return m.hexdigest()

def listdir(dir,file,rootdir):
	# file.write(dir + '\n')
	fielnum = 0
	# print(dir)
	list = os.listdir(dir) 
	for line in list:
		filepath = os.path.join(dir,line)
		# print(filepath)
		if os.path.isdir(filepath): 
			fielnum = fielnum + listdir(filepath, myfile, rootdir + "/" + line)
		elif os.path:
			myfile.write(calMD5ForFile(filepath)  + ',' +  rootdir + "/" + line + '\n')
			# print(filepath)
			fielnum = fielnum + 1
	return fielnum
# dir = raw_input('please input the path:')
myfile = open('listdir.txt','w')
fielnum = listdir(sys.argv[1], myfile, "")
print("ok:" , fielnum)