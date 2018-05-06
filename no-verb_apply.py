import os
import xml.etree.ElementTree as ET
import subprocess

files = os.listdir('./conv')
progr = open('prog_progress.txt', 'w')
#l = m.lemmatize(cont)
for f in files:
    print (f)
    if os.path.isdir('./newcpfull/'+f):
        continue
    xmlres = subprocess.check_output(['../lspl/bin/lspl-find.exe', '-p', '../no-v-pat.txt', '-s', '../pattern_names.txt', '-i', './conv/'+f])
    #open('xml_res.txt', 'w')
    try:
        root = ET.fromstring(xmlres)
        text = root[0]
        for elem in text:
            #print (elem.tag)
            if len(elem):
             #   print ("Has children")
                filename = './fitting_verbs/' + elem.attrib['name'].replace(' ', '') + '.txt'
                fn = open(filename, 'a')
                for ch in elem:
               #     print (ch)
               #     print (ch.text)
               #     print (ch.attrib)
                    s = ch[0].text
                    s = s.replace('\n', ' ').replace('\r', '')
                    sarr = s.split(' ')
                #    print(sarr[0], "-----", v[0])
                    fn.write(sarr[0] + '\n')
                fn.close()
        progr.write(f + "\n")
    except:
        f = open('./find_errors/' + f, 'w')
        f.write(str(xmlres, 'windows-1251'))
        f.close()
        continue
progr.close()

