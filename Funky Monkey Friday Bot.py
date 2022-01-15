import discord
import os
import random
import discord.client
import datetime
import time
from discord.ext import tasks
import pytz

print(datetime.datetime.now())
print(datetime.datetime.now(tz=pytz.timezone('America/Chicago')).weekday())
print(datetime.datetime.now(tz=pytz.timezone('America/Chicago')).hour)

# 8MB is the API limit for sent files
# Finds a random monkey gif from the FunkyMonkeyGifs folder
def MonkeyTime():
  RandomGif = random.choice(os.listdir("FunkyMonkeyGifs"))
  return RandomGif

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='around'))

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  @tasks.loop(seconds=5.0)
  async def alerts():
    # weekday() == 4 would be Friday
    if datetime.datetime.now(tz=pytz.timezone('America/Chicago')).weekday() == 4 and datetime.datetime.now(tz=pytz.timezone('America/Chicago')).hour == 8:
      print('Initializing Funky Monkey Friday!')
      #MonkeyTime()
      await message.channel.send("@everyone **IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + MonkeyTime()))
      time.sleep(7200)
      print("Happy Funky Monkey Friday!")
    print('Alerts are active!')
  alerts.start()

  if message.author.guild_permissions.administrator == True:

    if message.content.startswith('!help'):
      await message.channel.send("**You have requested Funky Monkey Assistance**\n!test - preview an alert without tagging everyone\nYour next alert will issued on the following Funky Monkey Friday!\n`Only administrators can use commands`")

    if message.content.startswith('!test'):
      MonkeyTime()
      await message.channel.send("**IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + MonkeyTime()))

  else:
    return

client.run(os.getenv('TOKEN'))