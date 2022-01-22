import discord
import os
import random
import discord.client
import datetime
import time
from discord.ext import tasks
import pytz

print(datetime.datetime.now())

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

  if message.author.guild_permissions.administrator == True:

    if message.content.startswith('!help'):
      await message.channel.send("**You have requested Funky Monkey Assistance**\n!test - preview an alert without tagging everyone\n!config - configure Funky Monkey Friday alerts\n!list timezones - lists all timezones\nCommands timeout after 2 minutes\n`Only administrators can use commands`")

    if message.content.startswith('!test'):
      MonkeyTime()
      await message.channel.send("**IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + MonkeyTime()))

    if message.content.startswith('!list timezones'):
      await message.channel.send('**All Timezones (and country abbreviations)**\nhttps://en.wikipedia.org/wiki/List_of_tz_database_time_zones')
      await message.channel.send('Enter your country abbreviation `Ex. US for United States`')
      country = await client.wait_for("message", timeout=120)
      country
      country = country.content
      await message.channel.send('**{} Timezones**\n`{}`'.format(country, (pytz.country_timezones(country))))

    if message.content.startswith('!config'):
      h = 'undef'
      m = 'undef'
      ZoneSelection = 'undef'

      await message.channel.send('Enter your desired alert hour (in 24hr format 00:00-23:00) `Ex. 5:00pm is 17:00`')
      msg = await client.wait_for("message", timeout=120)
      msg
      msg = int(msg.content)

      if 0 <= msg <= 23:
        h = msg
        await message.channel.send('`You have selected hour {}`'.format(h))
      else:
        await message.channel.send('Stop monkeying around! Funky Monkey Friday requires at least an hour of celebration! You entered an incorrect format, please retry.')
      await message.channel.send('Enter you desired alert minute (00-59)')
      msg2 = await client.wait_for("message", timeout=120)
      msg2
      msg2 = int(msg2.content)

      if 0 <= msg2 <= 59:
        m = msg2
        #await message.channel.send('`You have selected minute {}`'.format(m))
        await message.channel.send('`Your new alert time is {}:{}`'.format(h,m))
      else:
        await message.channel.send('Stop monkeying around! You entered an incorrect format, please retry.')
      
      await message.channel.send('Enter your timezone in the TZ Database name format (Ex. America/New_York)')
      ZoneSelection = await client.wait_for("message", check=None, timeout=120)
      ZoneSelection
      ZoneSelection = ZoneSelection.content
      dt_new = datetime.datetime.now(tz=pytz.timezone(ZoneSelection))
      print(datetime.datetime.now(tz=pytz.timezone(ZoneSelection)))
      await message.channel.send('`Your timezone has been set to {}`'.format(dt_new))

      await message.channel.send("You're next Funky Monkey Friday alert is scheduled for {}:{}, {} on the next Friday".format(h, m, ZoneSelection))
      if h != 'undef' and m != 'undef' and ZoneSelection != 'undef':
        @tasks.loop(seconds=5.0)
        async def alerts():
          # weekday() == 4 would be Friday
          if datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).weekday() == 4 and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).hour == h and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).minute ==  m:
            print('tried')
            #MonkeyTime()
            await message.channel.send("@everyone **IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + MonkeyTime()))
            time.sleep(60)
            print("Sent!")
          print('Day: {}'.format(datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).weekday()))
          print('Time: {}'.format(datetime.datetime.now(tz=pytz.timezone(ZoneSelection))))
          print('alerts are active for {}:{}, {}'.format(h, m, ZoneSelection))
        alerts.start()

  else:
    return

client.run(os.getenv('TOKEN'))