import random
import os

with open("currentlyplaying.txt", "r", encoding="utf8") as f:
	current = f.readlines()

print(str(current[0]))
