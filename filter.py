#!/usr/bin/python3

import os
import shutil
import pymorphy2
import re

def look_through (fname) :
    f=open(fname)
    flag = True
    counter = 0
    for line in f:
        if(line.find('    ', 20) < 0) :
            counter+=1
            if (counter>20) :
                flag = False
                break
        else:
            counter = 0
    return flag

def del_dash (fname) :
    f=open(fname)
    cont = f.read()
    f.close()
    prev = -1
    dpos = cont.find('-\n', prev+1)
    while (dpos > prev) :
        if (cont[dpos-1] == ' ') :
            prev = dpos
            continue
        stpos = cont.rfind(' ', 0, dpos) + 1
        fpos = dpos+2
        while (cont[fpos] == ' ') :
            fpos += 1
        fpos = cont.find(' ', fpos)
        if (fpos < 0) :
            fpos = len(cont)+1
        wnod = cont[stpos:dpos] + cont[dpos+2:fpos]
   #     print (wnod)
        wwd = cont[stpos:fpos]
        spaces = wwd.count(' ')
        wwd = wwd.replace(' ','')
        wwd = wwd.replace('\n','')
        wnod = wnod.replace(' ','') 
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(wnod)[0]
        if (type(p.methods_stack[0][0]) is pymorphy2.units.by_analogy.KnownSuffixAnalyzer.FakeDictionary) :
            word = wwd
        else :
            word = wnod
  #      print (word +'   '+str(stpos)+'/'+str(fpos))
        cont = cont[:stpos] + word + '\n' +' '*spaces + cont[fpos+1:]
        prev = dpos
        dpos = cont.find('-\n', prev+1)
   #     print(dpos)
    f=open(fname,'wt')
    f.write(cont)
    f.close()
    
	
os.chdir('./textfiles')
arr = os.listdir(path=".")
if not(os.path.isdir("unprocessable")):
    os.mkdir("unprocessable")
for fname in arr:
    if (fname.endswith('.txt')) :
        if look_through(fname) :
	        shutil.move(fname, './unprocessable/' + fname)
arr = os.listdir(path=".")
cnt =1
for fname in arr:
    print (str(cnt) + '   ' + fname)
    if (fname.endswith('.txt')) :
        del_dash(fname)
    cnt+=1
os.chdir('..')
