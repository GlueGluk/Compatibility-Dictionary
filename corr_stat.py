import os
import re

d = {}
p = open('../patterns.txt')
for line in p:
    m = re.match(r'^(\S*?) = (.*)$', line)
    if m:
        d.update([(m.group(1), m.group(2))])
    else:
        print("Didn't match: ", line)
files = os.listdir('./result')
for f in files:
    cont = open('./cont_res/' + f).read()
    m = re.match(r'V', cont)
    if not m:
        m = re.match(r'{', cont)
        if not m:
            print (f)
            fh = open('./cont_res/' + f, 'w')
            if(d.get(f[:-4])):
                fh.write(d[f[:-4]] + '\n')
            else:
                print("No such key in dict: ", f[:-4])
            fh.write(cont)
            fh.close()
