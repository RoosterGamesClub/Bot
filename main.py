import os

import logging

import random

import discord
from discord.ext import commands

####### Settings ########
from settings import COMMAND_PREFIX, WELCOME_CHANNEL_ID, MAIN_COLOR, REROL_MESSAGE_ID, REROL_CHANNEL_ID, DISCORD_TOKEN, GUILD_ID

import loggingUtils
import otherUtils

#######   Tasks  ########
from birthdayTask import birthdayNotification

####### Commands ########
import helpCommand

########## Cogs #########
import infoCog
import devCog
import adminCog

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

main_logger = logging.getLogger("bot.main")

@bot.event
async def on_ready():

  main_logger.log(logging.INFO, "--------------   loading tasks  --------------")

  main_logger.log(logging.INFO, "starting birthday notification tasks...")
  birthdayNotification.start(bot)

  main_logger.log(logging.INFO, "-------------- loading commands --------------")

  #main_logger.log(logging.INFO, "loading admin commands...")
  #bot.add_command(genrerol)

  main_logger.log(logging.INFO, "loading user commands...")
  # bot.add_command(poll)
  # bot.add_command(boolean)
  # bot.add_command(integer)

  # main_logger.log(logging.INFO, "loading dev commands...")
  # bot.add_command(sync)

  main_logger.log(logging.INFO, "loading custom help commnd...")
  bot.help_command = helpCommand.CustomHelpCommand()

  main_logger.log(logging.INFO, "--------------   loading cogs   --------------")

  main_logger.log(logging.INFO, "loading info cog...")
  await bot.add_cog(infoCog.InfoCog(bot))

  main_logger.log(logging.INFO, "loading dev cog...")
  await bot.add_cog(devCog.DevCog(bot))

  main_logger.log(logging.INFO, "loading admin cog...")
  await bot.add_cog(adminCog.AdminCog(bot))

  main_logger.log(logging.INFO, "----------------------------------------------")

# WELCOME MESSAGE
@bot.event
async def on_member_join(member):
  main_logger.log(logging.INFO, f"on_member_join event (member ID: {member.id}) (member NAME: {member.display_name})")

  channel = await member.guild.fetch_channel(WELCOME_CHANNEL_ID)

  if channel == None:
    main_logger.log(logging.DEBUG, f"WELCOME_CHANNEL {WELCOME_CHANNEL_ID} not found... check .env file configuration")
    return
  
  description_ = ""
  description_ += f"**¡Bienvenid@ {member.mention} a Rooster Games!**"
  description_ += f"\n\n¡Estamos emocionados de darte la bienvenida a nuestra comunidad dedicada al desarrollo de videojuegos! En Rooster Games, nos apasiona la creación de experiencias únicas y emocionantes para todo el mundo. 🌍🎮"
  description_ += f"\n\nEste Discord es tu espacio para conectarte con otros miembros del club, compartir tus proyectos, recibir retroalimentación valiosa y colaborar en nuevas ideas. Ya seas un desarrollador novato o un veterano en la industria, aquí encontrarás un ambiente acogedor donde tu creatividad puede prosperar. 🚀💡"
  description_ += f"\n\nÚnete a nuestras discusiones, participa en eventos especiales y sé parte de una comunidad apasionada que comparte tu amor por los videojuegos. En Rooster Games, cada miembro es una pieza vital de nuestro equipo, ¡y esperamos ver tus ideas brillar! 💬✨"
  description_ += f"\n\n¡Bienvenido a Rooster Games, donde los sueños de los videojuegos toman vuelo! 🐓🎮"

  #get a random file from img/welcome/ folder
  file_list = os.listdir("./img/welcome")
  
  file_name = file_list[random.randint(0, len(file_list) -1)]

  file_path = f"./img/welcome/{file_name}"

  file = discord.File(file_path)

  em = discord.Embed(title="", description=description_, color=MAIN_COLOR)

  em.set_image(url=f"attachment://{file_name}")

  await channel.send(file=file, embed=em)

# RE-ROL MESSAGE
@bot.event
async def on_raw_reaction_add(payload : discord.RawReactionActionEvent):
  await on_raw_reaction_event(payload, True)

@bot.event
async def on_raw_reaction_remove(payload : discord.RawReactionActionEvent):
  await on_raw_reaction_event(payload, False)

async def on_raw_reaction_event(payload : discord.RawReactionActionEvent, is_addition : bool):
  #print(f"raw reaction event, is_addition : {is_addition}")

  if payload.message_id != int(REROL_MESSAGE_ID):
    #print(f"reacted on untracked message {payload.message_id}")
    return

  guild = await bot.fetch_guild(payload.guild_id)
  member = await guild.fetch_member(payload.user_id)
  #channel = await guild.fetch_channel(payload.channel_id)
  #message = await channel.fetch_message(payload.message_id)
  emoji = payload.emoji

  main_logger.log(logging.INFO, f"on_raw_reaction event (member ID: {member.id}) (member NAME: {member.display_name}) (reaction: {emoji})")

  if emoji.name == "🎲": await set_role(guild, member, "GameDesign", is_addition)
  if emoji.name == "⚙️": await set_role(guild, member, "Programming", is_addition)
  if emoji.name == "🎨": await set_role(guild, member, "Graphics/Animation", is_addition)
  if emoji.name == "🎵": await set_role(guild, member, "Music", is_addition)
  if emoji.name == "🔊": await set_role(guild, member, "SoundDesign/VoiceActing", is_addition)
  if emoji.name == "📚": await set_role(guild, member, "Writing/NarrativeDesign", is_addition)

  if emoji.name == "🕹️": await set_role(guild, member, "Gaming", is_addition)

async def set_role(guild : discord.guild, member : discord.Member, role_name : str, is_addition : bool):
  role = discord.utils.get(guild.roles, name=role_name)
  
  if role in member.roles:
    if not is_addition:
      await member.remove_roles(role)
  else:  
    if is_addition:
      await member.add_roles(role)

""" COMMANDS """
# UTILITY COMMANDS
@bot.hybrid_command(brief="create a poll", description="create a poll specifying <title> <option n> <option n + 1>")
async def poll(ctx : commands.context, title : str, option_1 = "", option_2 = "", option_3 = "", option_4 = "", option_5 = "", option_6 = "", option_7 = "", option_8 = "", option_9 = "", option_10 = "", is_official_poll = False):

  # fugly hack because slash commands don't support *args parameters
  # ----------------------------------------------------------------
  options = []

  if option_1 : options.append(option_1)
  if option_2 : options.append(option_2)
  if option_3 : options.append(option_3)
  if option_4 : options.append(option_3)
  if option_5 : options.append(option_3)
  if option_6 : options.append(option_3)
  if option_7 : options.append(option_3)
  if option_8 : options.append(option_3)
  if option_9 : options.append(option_3)
  if option_10 : options.append(option_3)
  # ----------------------------------------------------------------

  reactions = ["🍎", "🍊","🍇", "🥑", "🍞", "🧅", "🥚", "🌶️", "🥦", "🧀", "🥓", "🍓", "🫐", "🍿", "🍪", "🍭", "🍬"]

  em = discord.Embed(title=title, color=MAIN_COLOR)

  if otherUtils.isAdmin(ctx.guild, ctx.author) and is_official_poll:
    em.set_author(name="by Rooster Games")

  if len(options) == 0:
    message = await ctx.send(embed=em)
    
    await message.add_reaction("👍")
    await message.add_reaction("👎")

    return
  elif len(options) > 10:
    await ctx.send(f"define at most 10 options")
    return

  description_ = ""

  emojis = []

  for i, option in enumerate(options):
    emoji = reactions.pop(random.randint(0, len(reactions) - 1))
    
    emojis.append(emoji)

    description_ += f"\n{emoji} - {option}"

  em.description = description_

  message = await ctx.send(embed=em)

  for i in range(len(options)):
    await message.add_reaction(emojis[i])

@bot.hybrid_command(name="boolean", brief="random boolean", description="get a random boolean")
async def boolean(ctx):
  value = random.randint(0, 99) > 50

  await ctx.send(f"{value}")

@bot.hybrid_command(brief="random integer", description="get a random integer")
async def integer(ctx, lower_limit = 10, upper_limit = 0):
  
  if lower_limit > upper_limit:
    temp = upper_limit
    upper_limit = lower_limit
    lower_limit = temp

  await ctx.send(f"{random.randint(lower_limit, upper_limit)}")

bot.run(DISCORD_TOKEN)