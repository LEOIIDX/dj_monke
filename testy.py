from tinytag import TinyTag
import music_tag

track = music_tag.load_file("Music/06 - RAM - ACT.flac")
tag = TinyTag.get("Music/06 - RAM - ACT.flac", image = True)
print('This track is by %s.' % tag.artist)
print('It is %f seconds long.' % tag.duration)
