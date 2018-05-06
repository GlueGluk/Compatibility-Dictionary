import os
import pymorphy2

files = os.listdir('./fitting_verbs')
morph = pymorphy2.MorphAnalyzer()
for f in files:
    print (f)
    fc = open('./fitting_verbs/' + f)
    d = {}
    for line in fc:
        l = line
        l = l.replace(' ','').replace('\n','')
        if (l in ['при', 'При', 'ной']) :
            continue
        parsed = morph.parse(l)
        found = ''
        for p in parsed:
            if (('VERB' in p.tag) or ('INFN' in p.tag)):
                found = p.normal_form
                break
        if found :
            if (d.get(found)):
                d[found] += 1
            else:
                d.update([(found,1)])
    out = open('./result/' + f, 'w')
    for r in sorted(d, key=d.get, reverse=True):
        key = r
        val = d[r]
        if val>50:
            print(f, key, val)
        out.write(key + ' : ' + str(val) + '\n')