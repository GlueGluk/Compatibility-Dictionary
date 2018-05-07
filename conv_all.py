import os
import subprocess

if not(os.path.isdir("converted")):
    os.mkdir("converted")
files = os.listdir('./textfiles')
for f in files:
    print (f)
    if os.path.isdir('./textfiles/'+f):
        continue
    subprocess.run(['perl', './ext_convert_to.pl', './textfiles/'+f, './converted/'+f])
