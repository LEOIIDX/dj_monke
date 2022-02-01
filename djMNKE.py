'''
djMNKE.py
By: Nanahira Monke Kanade Dev

Internet Radio Stream Bot

TODO List
#TODO Create a base playlist (ill take care of that - leo)
#TODO Create a debug functionality
'''
import os
import discord
import re
import asyncio
import string
import math
import music_tag
import random
import sys

#For metadata command
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from tinytag import TinyTag
import datetime

import cv2 #*pip install opencv-python
import numpy

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#intents
intents = discord.Intents.default()
intents.members = True
intents.emojis = True
intents.reactions = True

os.system('clear')

print('DJ Monke Bot\n')

mode = input('Select Mode\n(0) Normal\n(1) Debug\n')

if int(mode) >= 1:
	bot = commands.Bot(command_prefix='mnt!',intents=intents)
else:
	bot = commands.Bot(command_prefix='mn!',intents=intents)

bot.remove_command('help')

global metaOut, metaOut_TEST

metaOut_TEST = 841586692640735242
metaOut = 936204500434296883

@bot.event
async def on_ready():
	global stopStatus
	stopStatus = 0
	print('Ready!')
	os.system('cp cover.png Metadata/cover.png')

async def endbot(vc): #exits and cleans up after bot is done or forcibly exited
	if os.path.exists("Metadata/currentlyplaying.txt"):
  		os.remove("Metadata/currentlyplaying.txt")
	if os.path.exists("Metadata/cover.png"):
  		os.remove("Metadata/cover.png")

	await bot.change_presence(status=discord.Status.online, activity=discord.Game('Nothing'))
	await vc.disconnect()

	await player()

async def player():
	vc = await bot.get_channel(targetVoice).connect()

	#Counts the amount of files in the Music directory
	bigmusiclist = os.listdir("Music")
	Counter = 0
	for i in bigmusiclist:
		if i:
			Counter += 1

	#What plays the music
	async def currentlyplaying(check):
		playStatus = vc.is_playing()
		while playStatus:
			await asyncio.sleep(1)
			playStatus = vc.is_playing()

		await asyncio.sleep(2)

	#How the next track is picked and played
	async def resetplay(check):
		vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="Music/" + rand))
		with open("Metadata/currentlyplaying.txt", "w", encoding="utf8") as f: 
			f.write("Music/" + rand)
		os.system('cp cover.png Metadata/cover.png')
		await metadata()
	
	#Play all songs until every song in the list from the Music folder is picked (know from counter), then the bot leaves
	for x in range(Counter):
		rand = random.choice(bigmusiclist)
		await resetplay("reset")
		await currentlyplaying("play")
		bigmusiclist.remove(rand)

	if int(mode) >= 1:
		await bot.get_channel(metaOut_TEST).send('Restarting')
	else:
		await bot.get_channel(metaOut).send('Restarting')
	
	await endbot(vc)

async def metadata():
	#Find what is currently playing
	with open("Metadata/currentlyplaying.txt", "r", encoding="utf8") as f:
		current = f.readlines()
	track = music_tag.load_file(str(current[0]))
	trackstring = str(current[0])

	#Determine if mp3 or flac and extract album art into Metadata folder
	#This also means only mp3 and flac are support unless you want to manually find other methods
	#haha nope - leo
	if trackstring[-3:] == "mp3": #mp3
		music = ID3(trackstring)  
		with open("Metadata/cover.png", "wb") as f:
			f.write(music.getall("APIC")[0].data)
		musictype = "mp3"
	else: #flac
		var = FLAC(trackstring)
		pics = var.pictures
		for p in pics:
			if p.type == 3: #front cover
				with open("Metadata/cover.png", "wb") as f:
					f.write(p.data)
		musictype = "FLAC"

	#find the average color of the album art to use as embed color
	myimg = cv2.imread("Metadata/cover.png")
	avg_color_per_row = numpy.average(myimg, axis=0)
	avg_color = numpy.average(avg_color_per_row, axis=0)
	red = int(avg_color[2])
	green = int(avg_color[1])
	blue = int(avg_color[0])

	#* Discord embed that is sent
	track = music_tag.load_file(str(current[0]))
	tag = TinyTag.get(str(current[0]))

	#? New random phrase list? Just using a few from iidx bot command right now -zep
	TitleList = ["The next respect", "The escaping of the music beat.", "WELCOME TO THE CYBER-beat-NATION", "TRIP THE DEEP", "IIDX OF THE NEW CENTURY", "THE PRIMARY VIVID IIDX", "JEWEL SHOWER", "Break the Future", "Revolutionary Energetic Diversification", "Just Got Splash Beats!", "You're the DJ of this gig!", "Are You Ready Come on! It's Party Time!", "Blaze through the resort party!", "FEAR THE SAFARI", "Your mom calls me an animal.", "STREAM RIDING.", "This brand-new hour lets you cast and share your beat! Have a GREAT \"CastHour\" !!", "Go over with glaring sounds!", "Ride the sound flux! Record line of \"pleasure\"!", "This sound, this is the shinoBUZZ world", "Every day is the first station to shine yourself", "Next Link Various Tunes Change the World [ TRI ] For The Future !!!", "Lovely × Drive = New Lincle.", "The echo of sound, the shine of light.", "Super Sparkling Crown and Butterflies", "Do not pull the \"trigger\". Beat the \"war\"", "The ultimate system beatmania deluxe version."]

	metaEmbed = discord.Embed(title=tag.title, description=tag.artist, color= discord.Color.from_rgb(red, green, blue))
	metaEmbed.set_author(name="\"" + random.choice(TitleList) + "\"", icon_url="https://i.imgur.com/4T55IR4.png")
	file = discord.File("Metadata/cover.png", filename="cover.png")
	metaEmbed.set_thumbnail(url="attachment://cover.png")
	metaEmbed.set_footer(text=tag.album + "\n" +  str(tag.samplerate) + "Hz | " + str(int(tag.bitrate)) + " kbps | " + musictype)

	if int(mode) >= 1:
		await bot.get_channel(metaOut_TEST).send(file=file, embed=metaEmbed)
	else:
		await bot.get_channel(metaOut).send(file=file, embed=metaEmbed)

	await bot.change_presence(status=discord.Status.online, activity=discord.Game(str(track['title']) + ' - ' + str(track['artist'])))

@bot.command()
@commands.has_any_role('Admin', 'Mod', 'DJ')
async def play(ctx): #Allows the above on_ready call to be used on command (like if you do mn!stop)
	global targetVoice
	if not ctx.author.voice:
		await ctx.channel.send('Please join a Voice Channel.')
	else:
		targetVoice = ctx.author.voice.channel.id
		await player()

@bot.command()
@commands.has_any_role('Admin', 'Mod', 'DJ')
async def stop(ctx): #*This command will throw out a bunch of errors, too bad!
	if ctx.voice_client: # If the bot is in a voice channel
		if os.path.exists("Metadata/currentlyplaying.txt"):
	  		os.remove("Metadata/currentlyplaying.txt")
		if os.path.exists("Metadata/cover.png"):
	  		os.remove("Metadata/cover.png")
		await ctx.voice_client.disconnect()
		os.execv(sys.executable, ['python'] + sys.argv)
	else:
		await ctx.send("I'm not in a voice channel yet")

#Literally just kills the ffmpeg process. large brain af - leo
@bot.command()
@commands.has_any_role('Admin', 'Mod', 'DJ')
async def skip(ctx):
	if ctx.voice_client:
		os.system('killall ffmpeg')
		await ctx.channel.send('Song Skipped')
	else:
		await ctx.send("I'm not in a voice channel yet")

@bot.command()
async def help(ctx):
	helpEmbed = discord.Embed()
	file = discord.File('cover.png', filename='cover.png')

	helpEmbed.set_author(name='DJ MONKE Help')
	helpEmbed.set_thumbnail(url='attachment://cover.png')
	helpEmbed.add_field(name='play', value='mn!play || Starts playback (Only available to DJ role)', inline=False)
	helpEmbed.add_field(name='stop', value='mn!stop || Stops playback (Only available to DJ role)', inline=False)
	helpEmbed.add_field(name='skip', value='mn!skip || Skips the current song (Only avialible to DJ role', inline=False)

	await ctx.channel.send(file=file, embed = helpEmbed)

bot.run(TOKEN)