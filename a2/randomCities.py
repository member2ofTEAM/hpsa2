import math
import random

for i in range(1000):
	random.seed()
	f = open('tests/Test'+str(i), 'w')
	for j in range(1000):
		f.write(str(j+1)+' '+str(random.randrange(30000))+' '+str(random.randrange(30))+' '+str(random.randrange(30000))+'\n')
