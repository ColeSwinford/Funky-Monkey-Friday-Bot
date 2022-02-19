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

# Startup console message
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Game(name='around'))

# All functionality begins when a message is sent
@client.event
async def on_message(message):

  # if the sender is the bot, return
  if message.author == client.user:
    return

  # if the sender is a server admin, listen for commands
  if message.author.guild_permissions.administrator == True:

    # help command
    if message.content.startswith('!help'):
      await message.channel.send("**You have requested Funky Monkey Assistance**\n!test - preview an alert without tagging everyone\n!config - configure Funky Monkey Friday alerts\n!list timezones - lists all timezones\nCommands timeout after 2 minutes\n`Only administrators can use commands`")

    # test command
    if message.content.startswith('!test'):
      MonkeyTime()
      await message.channel.send("**IT'S FUNKY MONKEY FRIDAY! SEIZE THE DAY!**", file=discord.File("FunkyMonkeyGifs/" + MonkeyTime()))

    # list timezones command
    if message.content.startswith('!list timezones'):
      await message.channel.send('**All Timezones (and country abbreviations)**\nhttps://en.wikipedia.org/wiki/List_of_tz_database_time_zones')
      await message.channel.send('Enter your country abbreviation `Ex. US for United States`')
      country = await client.wait_for("message", timeout=120)
      country
      country = country.content
      await message.channel.send('**{} Timezones**\n`{}`'.format(country, (pytz.country_timezones(country))))

    # configuration command
    if message.content.startswith('!config'):
      h = 'undef'
      m = 'undef'
      ZoneSelection = 'undef'

      # enter hour to alert
      await message.channel.send('Enter your desired alert hour (in 24hr format 00-23) `Ex. 18 = 6:00pm`')
      msg = await client.wait_for("message", timeout=120)
      msg
      msg = int(msg.content)

      # check if the hour input is valid, and if not, let the user know
      if 0 <= msg <= 23:
        h = msg
        await message.channel.send('`You have selected hour {}`'.format(h))
      else:
        await message.channel.send('Stop monkeying around! Funky Monkey Friday requires at least an hour of celebration! You entered an incorrect format, please retry.')
      await message.channel.send('Enter you desired alert minute (00-59)')
      msg2 = await client.wait_for("message", timeout=120)
      msg2
      msg2 = int(msg2.content)

      # check if the minute input is valid, and if not, let the user know
      if 0 <= msg2 <= 59:
        m = msg2
        await message.channel.send('`Your new alert time is {}:{}`'.format(h,m))
      else:
        await message.channel.send('Stop monkeying around! You entered an incorrect format, please retry.')
      
      # timezone prompt and assignment
      await message.channel.send('Enter your timezone in the TZ Database name format (Ex. America/New_York)')
      ZoneSelection = await client.wait_for("message", check=None, timeout=120)
      ZoneSelection
      ZoneSelection = ZoneSelection.content
      dt_new = datetime.datetime.now(tz=pytz.timezone(ZoneSelection))
      print(datetime.datetime.now(tz=pytz.timezone(ZoneSelection)))
      await message.channel.send('`Your timezone has been set to {}`'.format(dt_new))

      # show the user their configuration
      await message.channel.send("You're next Funky Monkey Friday alert is scheduled for {}:{}, {} on the next Friday".format(h, m, ZoneSelection))
      if h != 'undef' and m != 'undef' and ZoneSelection != 'undef':
        @tasks.loop(seconds=5.0)
        async def alerts():
          # weekday() == 4 would be Friday
          ## check if the day and time are equal the configuration
          if datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).weekday() == 4 and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).hour == h and datetime.datetime.now(tz=pytz.timezone(ZoneSelection)).minute ==  m:
            # MonkeyTime() function is called and the alert is sent
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
