import ast
from collections import Counter

file = open('/path/36kr_result.txt')
s = file.read()
for line in s.splitlines():
    if not line.startswith('2018-01-29'):
        if not line.startswith('result:'):
            with open('/path/36krResult.txt', 'a') as f:
                print(line, file=f)

process = open('/path/36krResult.txt')
sss = process.readlines()
for i in range(len(sss)):
    data = sss[i].split(' Counter(')
    count = Counter()
    for j in range(i,len(sss)):
        dataj = sss[j].split(' Counter(')
        if data[0] == dataj[0]:
            data0 = data[1][:-2]
            data0j = dataj[1][:-2]
            try:
                data1 = ast.literal_eval(data0)
                data1j = ast.literal_eval(data0j)
                # del data1['total']
                inp = [dict(x) for x in (data1, data1j)]
                for y in inp:
                    count += Counter(y)
                    data1 = count
            except:
                pass
    with open('/path/36krFinal.txt', 'a') as f:
        print(data[0], count, file=f)
