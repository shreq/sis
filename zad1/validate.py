import os
import re

directory = os.fsencode('./output/')
regex = re.compile('^(astr|bfs).+(stats).+')

isGood = True
badSolutions = ''

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if regex.match(filename):
        with open('output/' + filename) as fi:
            length = fi.readline()
            fln = filename.split('_')
            if int(length) != int(fln[4]):
                isGood = False
                badSolutions += (filename + '\n')

if not isGood:
    print(badSolutions)
else:
    print('All good')
