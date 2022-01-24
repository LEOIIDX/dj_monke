import random
import os

bigmusiclist = os.listdir("Music")
Counter = 0
for i in bigmusiclist:
	if i:
		Counter += 1

print(Counter)