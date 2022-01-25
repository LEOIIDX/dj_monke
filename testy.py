from mutagen.flac import FLAC, Picture
from mutagen import File
from mutagen.id3 import ID3

current = "Music/Think.flac"

print(current[-3:])
if current[-3:] == "mp3":
	music = ID3(current)  
	with open("Metadata/cover.jpg", "wb") as f:
		f.write(music.getall("APIC")[0].data)
else:
	var = FLAC(current)
	pics = var.pictures
	print (pics)
	for p in pics:
		if p.type == 3: #front cover
			print("\nfound front cover") 
			with open("Metadata/cover.jpg", "wb") as f:
				f.write(p.data)