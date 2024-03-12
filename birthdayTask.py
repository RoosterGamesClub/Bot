import discord
from discord.ext import commands, tasks
from datetime import date

from settings import GUILD_ID, NEWS_CHANNEL_ID, MAIN_COLOR

""" the birthays dictionary has the following structure """
"""

birthdays = {
  "month-day" : {
    "member_id" : discord's member_id,
    "name" : some text that identifies this person
  }
}

"""

birthdays = {
  #"3-11" : {"member_id" : 334016584093794305, "name" : "test-event"}, #maybe aqui agregar el cumpleaños de posho
  "8-27" : {"member_id" : 334016584093794305, "name" : "leo aka wissens"},
  "11-2" : {"member_id" : 637770445172768768, "name" : "leslie aka bistraw"},
  "7-13" : {"member_id" : 985700030130315284, "name" : "feruk"},
  "9-9"  : {"member_id" : 842438155508252675, "name" : "diegongi"}
}

# events for the day will be stored here so they dont repeat
already_notified_events = []

@tasks.loop(minutes=30)
async def birthdayNotification(bot : commands.Bot):
  today = date.today()

  today_str = f"{today.month}-{today.day}"

  for birthday in birthdays:
    if birthday in already_notified_events: #check if the event has been notified already
      continue

    if birthday != today_str: #check if today is the day
      continue

    already_notified_events.append(birthday)

    if today_str in birthdays:
      event = birthdays[today_str]

      member_id = event["member_id"]

      description_ = f"Feliz cumpleaños <@{member_id}>! 🎂"

      em = discord.Embed(title="", description=description_, color=MAIN_COLOR)

      guild = await bot.fetch_guild(GUILD_ID)
      channel = await guild.fetch_channel(NEWS_CHANNEL_ID)

      await channel.send(embed=em)
   