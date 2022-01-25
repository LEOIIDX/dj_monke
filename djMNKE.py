'''
DJMNKE.py
By: Nanahira Monke Kanade Dev

Internet Radio Stream Bot
'''
import os
import discord
import re
import asyncio
import string
import math
import music_tag
import random

#For metadata command
from mutagen.flac import FLAC, Picture
from mutagen import File
from mutagen.id3 import ID3
import cv2 #pip install opencv-python
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

print('DJ Monke Bot\n')

bot = commands.Bot(command_prefix='mn!',intents=intents)

tVoice = 828667775605669893

async def endbot(ctx): #exits and cleans up after bot is done or forcibly exited
	if os.path.exists("Metadata/currentlyplaying.txt"):
  		os.remove("Metadata/currentlyplaying.txt")
	if os.path.exists("Metadata/cover.png"):
  		os.remove("Metadata/cover.png")
	await ctx.guild.voice_client.disconnect()
		  	
@bot.event
async def on_ready():
	print('Ready!')

@bot.command()
async def play(ctx):
	vc = await bot.get_channel(tVoice).connect()

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
			print(str(check))
			playStatus = vc.is_playing()

		await asyncio.sleep(2)

	#How the next track is picked and played
	async def resetplay(check):
		vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="Music/" + rand))
		with open("Metadata/currentlyplaying.txt", "w", encoding="utf8") as f: 
			f.write("Music/" + rand)
		print(str(check))
	
	#Play all songs until every song in the list from the Music folder is picked, then the bot leaves
	for x in range(Counter):
		rand = random.choice(bigmusiclist)
		await resetplay("reset")
		await currentlyplaying("play")
		bigmusiclist.remove(rand)

	await endbot(ctx)

@bot.command()
async def metadata(ctx):
	#Find what is currently playing
	with open("Metadata/currentlyplaying.txt", "r", encoding="utf8") as f:
		current = f.readlines()
	track = music_tag.load_file(str(current[0]))
	trackstring = str(current[0])

	#Determine if mp3 or flac and extract album art into Metadata folder
	#This also means only mp3 and flac are support unless you want to manually find other methods
	if trackstring[-3:] == "mp3": #mp3
		music = ID3(trackstring)  
		with open("Metadata/cover.png", "wb") as f:
			f.write(music.getall("APIC")[0].data)
	else: #flac
		var = FLAC(trackstring)
		pics = var.pictures
		for p in pics:
			if p.type == 3: #front cover
				with open("Metadata/cover.png", "wb") as f:
					f.write(p.data)

	#Used for embed cover art
	file = discord.File("Metadata/cover.png", filename="cover.png")

	#find the average color of the album art to use as embed color
	myimg = cv2.imread("Metadata/cover.png")
	avg_color_per_row = numpy.average(myimg, axis=0)
	avg_color = numpy.average(avg_color_per_row, axis=0)
	red = int(avg_color[2])
	green = int(avg_color[1])
	blue = int(avg_color[0])

	#Discord embed that is sent
	metaEmbed = discord.Embed(colour = discord.Color.from_rgb(red, green, blue))
	metaEmbed.set_author(name=track['title'])
	metaEmbed.add_field(name='Artist', value=track['artist'])
	metaEmbed.add_field(name='Album', value=track['album'])
	metaEmbed.set_image(url="attachment://cover.png")

	await ctx.channel.send(file=file, embed=metaEmbed)

@bot.command()
async def stop(ctx): #This command will throw out a bunch of errors, too bad!
	if ctx.voice_client: # If the bot is in a voice channel 
		await endbot(ctx) # Leave the channel
	else:
		await ctx.send("I'm not in a voice channel yet")

#this is a placeholder, I have no idea how to make a skip function with current setup
@bot.command()
async def skip(ctx):
	if ctx.voice_client: # If the bot is in a voice channel 
		await endbot(ctx) # Leave the channel
	else:
		await ctx.send("I'm not in a voice channel yet")	

bot.run(TOKEN)