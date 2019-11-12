import pandas as pd
import re

# sched = pd.read_excel('final spelling 11-17 2018 nutcracker cast list.xlsx').fillna('')
sched = pd.read_excel('nccastrev.xlsx').fillna('')
dates = [k for k in sched.keys() if k[:2] == 'De']

people = set()
for date in dates:
    pset = set(sched[date])
    people = people.union(pset)
    sched[date] = [l.replace(' ', '').replace('-','') for l in list(sched[date])]
people = [p for p in people if type(p)==str]
people = [p for p in people if '12' not in p]
people = [p for p in people if 'Cast' not in p]
people = [p.split('*')[0] for p in people]
people = [p.split(':')[-1] for p in people]
people = [p.replace(' ','') for p in people]
people = [p.replace('.','') for p in people]
people = [p.replace('-','') for p in people]
slashes = [p.split('/') for p in people if '/' in p]
slashpeople = [p for s in slashes for p in s]
people = [p for p in people if '/' not in p]
people = sorted(list(set(people).union(slashpeople)))

def findsubset(key, search):
    return sched.loc[sched[key].str.contains(search, case=False)]

def findroles(person, disp=True):
    if disp:
        print('###############')
        print(person)
    retstr = ''
    for date in dates:
        roles = list(findsubset(date, person.replace(' ', ''))['Role'])
        roles = [r for r in roles if r != '']
        print(date)
        print(roles)
        retstr += '; '.join(roles) + ','
    if disp:
        print('###############')
    return retstr

def sepnames(names):
    if type(names) != list:
        names = [names]
    return [' '.join(re.findall('[A-Z][^A-Z]*' , person)) for person in names]

def findpeople(role):
    print('###############')
    print(role)
    for date in dates:
        people = list(findsubset('Role', role)[date])
        people = [r for r in people if r != '']
        print(date)
        print(sepnames(people))
        # print('\n'*1)
    print('###############')


findroles('isab')
findpeople('arabian')

with open('ncpeoplelist.csv' ,'w') as f:
    f.write(',' + ','.join([str(d).replace('\n',' ') for d in dates]))
    f.write('\n')
    for person in people:
        if person:
            personspace = ' '.join(re.findall('[A-Z][^A-Z]*' , person))
            f.write(personspace + ',' + findroles(person, disp=False))
            f.write('\n')

# sched['Role']
# findsubset('Role', 'pani')
# np.array(findsubset(date, 'Matt')['Role'])









#####################
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
import numpy as np

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

simscore = np.zeros(len(people)-1)
for pindex in range(1, len(people)):
    p1 = people[pindex-1]
    p2 = people[pindex]
    # minlen = min(len(p1), len(p2))
    # thisscore = similar(p1[:minlen], p2[:minlen])
    thisscore = fuzz.partial_ratio(p1, p2)/100
    simscore[pindex-1] = thisscore
    if thisscore > 0.8:
        print(p1, p2, thisscore)

mlist = []
for p1 in people:
    for p2 in people:
        if [p2,p1] not in mlist:
            thisscore = fuzz.partial_ratio(p1, p2)/100
            if thisscore > 0.8 and p1 != p2:
                print(p1, p2, thisscore)
                mlist.append([p1,p2])


##############################scratch

import numpy as np

sched.keys()
[print(p) for p in people]
list(people)

sched.loc[ sched['December 8\nSat. 2pm'].str.contains('Matt', case=False)]

me = sched.loc[ sched['December 8\nSat. 2pm'].str.contains('Matt', case=False)]

print(np.array(me))


key = 'Role'; search = 'Spanish'
sched.loc[ sched[key].str.contains(search, case=False)]

findsubset('Role', 'Spanish')

sched.iloc[94]

person = 'Matt'

def findsubset(key, search):
    return sched.loc[ sched[key].str.contains(search, case=False)]

def findroles(person):
    for date in dates:
        roles = list(findsubset(date, person)['Role'])
        roles = [r for r in roles if r != '']
        print(date)
        print(roles)
        print('\n'*1)

date = dates[0]
roles = list(findsubset(date, person)['Role'])

findroles('hean')

date = dates[1]
findsubset(date, 'Hea')

