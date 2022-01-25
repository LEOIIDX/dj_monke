from mutagen.flac import FLAC, Picture
from mutagen import File
from mutagen.id3 import ID3

song = "Music/dogbass.mp3"

print(song[-3:])
if song[-3:] == "mp3":
	music = ID3(song)  
	with open("Metadata/cover.jpg", "wb") as f:
		f.write(music.getall("APIC")[0].data)
else:
	var = FLAC(song)
	pics = var.pictures
	print (pics)
	for p in pics:
		if p.type == 3: #front cover
			print("\nfound front cover") 
			with open("Metadata/cover.jpg", "wb") as f:
				f.write(p.data)