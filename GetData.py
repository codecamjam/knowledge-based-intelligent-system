
def getAttributes(file):
    count = 1
    attList = []
    for line in file:
        cur = [x.strip() for x in line.split()]
        if len(cur) == 3 and cur[0][-1].endswith(':'):
            binPos = {cur[1]: count}
            binNeg = {cur[2]: -count}
            attList.append(binPos)
            attList.append(binNeg)
        count+=1
    return attList






def getConstraints(file):
    print ("")

def getPreferences(file):
    print ("")


try:
    file1 = open("att.txt", 'r')
    dicList = getAttributes(file1)
    print(dicList)
except IOError:
    print 'Cannot open attFile'


def truthtable (n):
  if n < 1:
    return [[]]
  subtable = truthtable(n-1)
  return [ row + [v] for row in subtable for v in [0,1] ]

r = truthtable(5)

for i in r:
    print (i)