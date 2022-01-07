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
RandomGif = 'undef'
# Date vars
h = 00
m = 00
ZoneSelection = 'UTC'

# Finds a random monkey gif from the FunkyMonkeyGifs folder
def MonkeyTime():
  global RandomGif
  RandomGif = random.choice(os.listdir("FunkyMonkeyGifs"))

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='around'))

@client.event
async def on_message(message):
  global RandomGif, h, m

  if message.author == client.user:
    return

  if message.author.guild_permissions.administrator == True:

    if message.content.startswith('!help'):
      await message.channel.send("**You have requested Funky Monkey Assistance**\n!config timezone - configure timezone (default is UTC)\n!time - configure time to send alert (in 24hr format 00:00-23:00; default is 00:00)\n!test - preview an alert without tagging everyone\n!enable - enable Funky Monkey Friday alerts\n!disable - disable Funky Monkey Friday alerts\n!list timezones - lists all timezones\n!setting - displays alert time and timezone configuration\n`Only users with admin permissions can use commands`")

    if message.content.startswith('!test'):
      MonkeyTime()
      await message.channel.send("**IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + RandomGif))

    if message.content.startswith('!time'):
      await message.channel.send('Enter your desired alert time (in 24hr format 00-23')
      msg = await client.wait_for("message", timeout=60)
      msg
      msg = int(msg.content)

      if 0 <= msg <= 23:
        h = msg
        await message.channel.send('You have selected hour {}'.format(h))
      else:
        await message.channel.send('Stop monkeying around! Funky Monkey Friday requires at least an hour of celebration! You entered an incorrect format, please retry.')
      await message.channel.send('Enter you desired alert minute (00-59)')
      msg2 = await client.wait_for("message", timeout=120)
      msg2
      msg2 = int(msg2.content)

      if 0 <= msg2 <= 59:
        m = msg2
        await message.channel.send('You have selected minute {}'.format(m))
        await message.channel.send('Your new alert time is {}:{}'.format(h,m))
      else:
        await message.channel.send('Stop monkeying around! You entered an incorrect format, please retry.')

    if message.content.startswith('!list timezones'):
      await message.channel.send('**US Timezones**\n`{}`'.format(pytz.country_timezones('US')))
      await message.channel.send('**All Timezones**\nhttps://en.wikipedia.org/wiki/List_of_tz_database_time_zones')

    if message.content.startswith('!config timezone'):
      global ZoneSelection
      await message.channel.send('Enter your timezone in the TZ Database name format (Ex. America/New_York)')
      ZoneSelection = await client.wait_for("message", check=None, timeout=120)
      ZoneSelection
      ZoneSelection = ZoneSelection.content
      dt_new = datetime.datetime.now(tz=pytz.timezone(ZoneSelection))
      print(datetime.datetime.now(tz=pytz.timezone(ZoneSelection)))
      await message.channel.send('Your timezone has been set to {}'.format(dt_new))

    if message.content.startswith('!enable'):
      await message.channel.send("You're next Funky Monkey Friday alert is scheduled for {}:{}, {} on the next Friday".format(h, m, ZoneSelection))
      @tasks.loop(seconds=5.0)
      async def alerts():
        # weekday() == 4 would be Friday
        if datetime.datetime.now().today().weekday() == 4 and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).hour == h and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).minute ==  m:
          MonkeyTime()
          await message.channel.send("@everyone **IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + RandomGif))
          time.sleep(60)
          print("Sent!")
        print(datetime.datetime.now(tz=pytz.timezone(ZoneSelection)))
        print('alerts are active for {}:{}, {}'.format(h, m, ZoneSelection))
      alerts.start()

    if message.content.startswith('!disable'):
      h = 'undef'
      m = 'undef'
      await message.channel.send('Alerts have been disabled!')

    if message.content.startswith('!setting'):
      await message.channel.send("Timezone: {}\nTime: {}:{}".format(ZoneSelection, h, m))

  else:
    print('Only administrators can use commands.')

client.run(os.getenv('TOKEN'))