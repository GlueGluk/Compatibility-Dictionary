import os
import re
import pymorphy2

files = os.listdir('./context')
morph = pymorphy2.MorphAnalyzer()
for f in files:
    print (f)
    fc = open('./context/' + f)
    out = open('./cont_res/' + f, 'w')
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
            cont = line[:-1]
            cont = re.sub('\s+', ' ', cont)
            out.write(found + ' : ' + cont + '\n')