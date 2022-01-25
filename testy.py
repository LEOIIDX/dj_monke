import random
import os

bigmusiclist = os.listdir("Music")
Counter = 0
for i in bigmusiclist:
	if i:
		Counter += 1

rand = random.choice(bigmusiclist)
print(rand)
print(bigmusiclist)
bigmusiclist.remove(rand)
print(bigmusiclist)
# list of items
List = [10, 20, 30, 40, 50, 60,
        70, 80, 90]
  
# using the sample() method
UpdatedList = random.sample(List, 3)
  
# displaying random selections from 
# the list without repetition
print(UpdatedList)