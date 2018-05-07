import os
import shutil
import re
import subprocess

if not(os.path.isdir("textfiles")):
    os.mkdir("textfiles")
dirs = os.listdir("./library")
for dir in dirs:
	print("============", dir)
	os.chdir("./textfiles")
	files = os.listdir("../library/"+dir)
	for f in files:
		print(dir, "---", f)
		m = re.match(r'.*\.(.*)', f)
		if m:
			print(m.group(1))
			if m.group(1) == 'pdf':
				subprocess.call(["pdftotext", "-enc", "UTF-8", "-layout", "../library/"+dir+"/"+f])
			elif m.group(1) == 'doc' or m.group(1) == 'docx':
				subprocess.call(["soffice", "-headless", "-convert-to", "txt:Text", "../library/"+dir+"/"+f])
		else:
			print ("Err1", f)
	files = os.listdir("../library/"+dir)
	for f in files:
		m = re.match(r'.*\.(.*)', f)
		if m:
			if m.group(1) == 'txt':
				shutil.move("../library/"+dir+"/"+f, "./"+f)
		else:
			print ("Err2", f)
	os.chdir("../")
	break



