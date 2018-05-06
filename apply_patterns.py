import os
import xml.etree.ElementTree as ET
import subprocess
import re

files = os.listdir('./conv')
i = 0
for f in files:
    print (f)
    i +=1
    if os.path.isdir('./conv/'+f):
        continue
    xmlres = subprocess.check_output(['./lspl/bin/lspl-find.exe', '-p', 'patterns.txt', '-s', 'pattern_names.txt', '-i', './conv/'+f])
 #   r = open('xml_res.txt', 'w')
 #   r.write(str(xmlres, 'windows-1251'))
 #   r.close()
    try:
        root = ET.fromstring(xmlres)
        text = root[0]
        for elem in text:
            #print (elem.tag)
            if len(elem):
             #   print ("Has children")
                filename = './found_o/' + elem.attrib['name'].replace(' ', '') + '.txt'
                fn = open(filename, 'a')
                for ch in elem:
               #     print (ch)
               #     print (ch.text)
               #     print (ch.attrib)
                    s = ch[0].text
                    s = s.replace('\n', ' ').replace('\r', '')
                    s = str(i) + " -> " + s
                    fn.write(s + '\n')
                fn.close()
    except:
        f = open('./xml_errors/' + f, 'w')
        f.write(str(xmlres, 'windows-1251'))
        f.close()
        continue
