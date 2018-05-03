import os
import subprocess

files = os.listdir('./textfiles1')
for f in files:
    print (f)
    if os.path.isdir('./textfiles1/'+f):
        continue
    subprocess.run(['perl', '../perl_scripts/ext_convert_to.pl', './textfiles1/'+f, './conv/'+f])
