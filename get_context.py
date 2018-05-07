import os
import xml.etree.ElementTree as ET
import subprocess

if not(os.path.isdir("context")):
    os.mkdir("context")
files = os.listdir('./converted')
for f in files:
    print (f)
    if os.path.isdir('./converted/'+f):
        continue
    xmlres = subprocess.check_output(['./lspl/bin/lspl-find.exe', '-p', './no-v-pat.txt', '-s', './pattern_names.txt', '-i', './converted/'+f])
    try:
        root = ET.fromstring(xmlres)
        text = root[0]
        for elem in text:
            if len(elem):
                filename = './context/' + elem.attrib['name'].replace(' ', '') + '.txt'
                fn = open(filename, 'a')
                for ch in elem:
                    s = ch[0].text
                    s = s.replace('\n', ' ').replace('\r', '')
                    fn.write(s + '\n')
                fn.close()
    except:
        continue
    print(f)

