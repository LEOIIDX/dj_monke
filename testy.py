import os,sys
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

song_path = os.path.join(sys.argv[0])
track = MP3("Music/dogbass.mp3")
tags = ID3("Music/dogbass.mp3")
print("ID3 tags included in this song ------------------")
print(tags.pprint())
print("-------------------------------------------------")
pict = tags.get("APIC")
print(pict)