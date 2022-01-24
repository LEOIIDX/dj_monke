import random

# Opening a file
file = open("musiclist.txt","r")
Counter = 0
  
# Reading from file
Content = file.read()
music = Content.split("\n")
  
for i in music:
    if i:
        Counter += 1
          
print("This is the number of lines in the file")
print(Counter)
print(music)
rand = str(music[random.randint(0,Counter - 1)])
print(rand)

#with open("musiclist.txt", "r", encoding="utf8") as f:
#	music = [(line.strip()).split() for line in f]
#	x = len(f.readlines())
#	f.close()
#	print(x)