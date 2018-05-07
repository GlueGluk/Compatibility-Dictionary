import os
import re
import pymorphy2

d = {}
p = open('./patterns.txt')
for line in p:
    m = re.match(r'^(\S*?) = (.*)$', line)
    if m:
        pname = m.group(1)
        templ = m.group(2)
        m = re.search(r'N1<([^>]*)>', templ)
        if m:
            noun = m.group(1)
            d.update([(pname, noun)])
    else:
        print("Didn't match: ", line)
files = os.listdir('./context')
morph = pymorphy2.MorphAnalyzer()
out = open('./interface_data.txt', 'w')
for f in files:
    print (f)
    fc = open('./context/' + f)
    for line in fc:
        l = re.split('\s+', line)
        verb = l[0].lower()
        if (verb in ['при', 'При', 'ной']) :
            continue
        parsed = morph.parse(verb)
        found = ''
        for p in parsed:
            if (('VERB' in p.tag) or ('INFN' in p.tag)):
                found = p.normal_form
                break
        if found :
            if(d.get(f[:-4])):
                cont = line[:-1].lower()
                cont = re.sub('\s+', ' ', cont)
                out.write(found + ' : ' + d[f[:-4]] + ' : ' + cont + '\n')
    fc.close()
out.close()
