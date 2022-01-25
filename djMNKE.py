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
from mutagen import File

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

@bot.event
async def on_ready():
	print('Ready!')

@bot.command()
async def play(ctx):
	vc = await bot.get_channel(tVoice).connect()

	bigmusiclist = os.listdir("Music")
	Counter = 0
	for i in bigmusiclist:
		if i:
			Counter += 1

	async def currentlyplaying(check):
		playStatus = vc.is_playing()
		while playStatus:
			await asyncio.sleep(1)
			print(str(check))
			playStatus = vc.is_playing()

		await asyncio.sleep(2)

	async def resetplay(check):
		vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="Music/" + rand))
		with open("Metadata/currentlyplaying.txt", "w", encoding="utf8") as f: 
			f.write("Music/" + rand)
		print(str(check))
	
	for x in range(Counter):
		rand = random.choice(bigmusiclist)
		await resetplay("reset")
		await currentlyplaying("play")
		bigmusiclist.remove(rand)

	await ctx.guild.voice_client.disconnect()

@bot.command()
async def metadata(ctx):
	with open("Metadata/currentlyplaying.txt", "r", encoding="utf8") as f:
		current = f.readlines()
	f = music_tag.load_file(str(current[0]))
	artwork = f.tags['APIC:'].data
	with open('image.jpg', 'wb') as img:
   		img.write(artwork)
	art = f['artwork']
	metaEmbed = discord.Embed(colour = discord.Color.gold())

	metaEmbed.set_author(name=f['title'])
	metaEmbed.set_image(image = artwork)
	metaEmbed.add_field(name='Artist', value=f['artist'])
	metaEmbed.add_field(name='Album', value=f['album'])

	await ctx.channel.send(embed=metaEmbed)

@bot.command()
async def stop(ctx):
	if ctx.voice_client: # If the bot is in a voice channel 
		await ctx.guild.voice_client.disconnect() # Leave the channel
	else:
		await ctx.send("I'm not in a voice channel yet")
	if os.path.exists("currentlyplaying.txt"):
  		os.remove("currentlyplaying.txt")
	if os.path.exists("currentlyplaying.txt"):
  		os.remove("currentlyplaying.txt")
	exit()

bot.run(TOKEN)