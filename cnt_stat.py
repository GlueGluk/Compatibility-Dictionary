import os

f = open('pattern_names.txt')
d = {}
for line in f:
    fn = line.replace(' ', '')
    fn = fn.replace('\n', '')
    fn = './found_o/' + fn + '.txt'
    if (os.path.isfile(fn)):
        num_lines = sum(1 for l in open(fn))
        if (num_lines > 50):
            print (num_lines, fn)
        if (d.get(num_lines)) :
            d[num_lines] += 1
        else:
            d.update([(num_lines, 1)])
    else :
        if (d.get(0)):
            d[0] += 1
        else:
            d.update([(0, 1)])
res = open('stat_o.txt', 'w')
for i in sorted (d.keys()):
    s = str(i) + ' -> ' + str(d[i])
    res.write(s+'\n')
res.close()