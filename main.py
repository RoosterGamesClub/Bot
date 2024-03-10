import logging
import os
import random
import time
import datetime

import discord
from discord.ext import commands

import git

import utils_other 

####### Settings ########
from settings import COMMAND_PREFIX, WELCOME_CHANNEL_ID, MAIN_COLOR, REROL_MESSAGE_ID, REROL_CHANNEL_ID, DISCORD_TOKEN

####### Commands ########
import helpCommand

########## Cogs #########
import infoCog

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
  main_logger = logging.getLogger("bot")

  main_logger.log(logging.INFO, "-------------- loading commands --------------")

  main_logger.log(logging.INFO, "loading developer commands...")
  bot.add_command(ping)
  bot.add_command(changelog)
  bot.add_command(log)

  main_logger.log(logging.INFO, "loading admin commands...")
  bot.add_command(genrerol)

  main_logger.log(logging.INFO, "loading user commands...")
  bot.add_command(poll)
  bot.add_command(boolean)
  bot.add_command(integer)

  bot.help_command = helpCommand.CustomHelpCommand()

  main_logger.log(logging.INFO, "--------------   loading cogs   --------------")

  main_logger.log(logging.INFO, "loading info cog...")
  await bot.add_cog(infoCog.InfoCog(bot))

  main_logger.log(logging.INFO, "----------------------------------------------")

# WELCOME MESSAGE
@bot.event
async def on_member_join(member):
  channel = await member.guild.fetch_channel(WELCOME_CHANNEL_ID)

  if channel == None:
    print(member.guild)
    print(f"welcome channel {WELCOME_CHANNEL_ID} not found...")
    return
  
  description_= ""
  description_ += f"**¡Bienvenido {member.mention} a Rooster Games!**"
  #description_ += f"\n\n¡Estamos emocionados de darte la bienvenida a nuestra comunidad dedicada al desarrollo de videojuegos! En Rooster Games, nos apasiona la creación de experiencias únicas y emocionantes para todo el mundo. 🌍🎮"
  description_ += f"\n\nEste Discord es tu espacio para conectarte con otros miembros del club, compartir tus proyectos, recibir retroalimentación valiosa y colaborar en nuevas ideas. Ya seas un desarrollador novato o un veterano en la industria, aquí encontrarás un ambiente acogedor donde tu creatividad puede prosperar. 🚀💡"
  #description_ += f"\n\nÚnete a nuestras discusiones, participa en eventos especiales y sé parte de una comunidad apasionada que comparte tu amor por los videojuegos. En Rooster Games, cada miembro es una pieza vital de nuestro equipo, ¡y esperamos ver tus ideas brillar! 💬✨"
  description_ += f"\n\n¡Bienvenido a Rooster Games, donde los sueños de los videojuegos toman vuelo! 🐓🎮"

  em = discord.Embed(title="", description=description_, color=MAIN_COLOR)

  em.set_image(url="https://i.pinimg.com/originals/ca/04/53/ca04538e846d9d7f11e56c9bc6e57acb.gif")

  await channel.send(embed=em)

# RE-ROL MESSAGE
@bot.event
async def on_raw_reaction_add(payload : discord.RawReactionActionEvent):
  await on_raw_reaction_event(payload, True)

@bot.event
async def on_raw_reaction_remove(payload : discord.RawReactionActionEvent):
  await on_raw_reaction_event(payload, False)

async def on_raw_reaction_event(payload : discord.RawReactionActionEvent, is_addition : bool):
  print(f"raw reaction event, is_addition : {is_addition}")

  if payload.message_id != int(REROL_MESSAGE_ID):
    print(f"reacted on untracked message {payload.message_id}")
    return
  
  guild = await bot.fetch_guild(payload.guild_id)
  member = await guild.fetch_member(payload.user_id)
  #channel = await guild.fetch_channel(payload.channel_id)
  #message = await channel.fetch_message(payload.message_id)
  emoji = payload.emoji

  print(f"reacted on re-rol message. reaction name : {emoji.name}")

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
@commands.command(brief="create a poll", description="create a poll specifying <title> <option n> <option n + 1>...")
async def poll(ctx, title, *options):

  reactions = ["🍎", "🍊","🍇", "🥑", "🍞", "🧅", "🥚", "🌶️", "🥦", "🧀"]

  if len(options) == 0:
    await ctx.send(f"define at least 1 option")
    return
  elif len(options) > 10:
    await ctx.send(f"define at most {len(reactions)} options")
    return

  description_ = ""

  emojis = []

  for i, option in enumerate(options):
    emoji = reactions.pop(random.randint(0, len(reactions) - 1))
    
    emojis.append(emoji)

    description_ += f"\n{emoji} - {option}"

  em = discord.Embed(title=title, description=description_, color=MAIN_COLOR)

  message = await ctx.send(embed=em)

  for i in range(len(options)):
    await message.add_reaction(emojis[i])

@commands.command(brief="random boolean", description="get a random boolean")
async def boolean(ctx):
  value = random.randint(0, 99) > 50

  await ctx.send(f"{value}")

@commands.command(brief="random integer", description="get a random integer")
async def integer(ctx, lower_limit = 10, upper_limit = 0):
  
  if lower_limit > upper_limit:
    temp = upper_limit
    upper_limit = lower_limit
    lower_limit = temp

  await ctx.send(f"{random.randint(lower_limit, upper_limit)}")

# ADMIN COMMANDS
def is_admin(guild : discord.guild, member : discord.Member) -> bool:
  admin_role = discord.utils.get(guild.roles, name="silkie chicken")

  if admin_role in member.roles:
    return True

@commands.command(hidden=True)
async def genrerol(ctx : commands.Context):

  if not is_admin(ctx.guild, ctx.message.author):
    return

  description_ = "Reacciona con el emoji adecuado para obtener tu rol"
  description_ += "\n\n**---------- Intereses ----------**\n"
  description_ += "\n> 🎲 para **Game Design**"
  description_ += "\n> ⚙️ para **Programming**"
  description_ += "\n> 🎨 para **Graphics** o **Animation**"
  description_ += "\n> 🎵 para **Music**"
  description_ += "\n> 🔊 para **Sound Design** o **Voice Acting**"
  description_ += "\n> 📚 para **Writing** o **Narrative Design**"
  description_ += "\n\n**----------  Hobbies ----------**\n"
  description_ += "\n> 🕹️ para **Gaming**"

  em = discord.Embed(title="Obten tus roles", description=description_, color=MAIN_COLOR)
  
  channel = await bot.fetch_channel(REROL_CHANNEL_ID)

  message = await channel.send(embed=em)

  await message.add_reaction("🎲")
  await message.add_reaction("⚙️")
  await message.add_reaction("🎨")
  await message.add_reaction("🎵")
  await message.add_reaction("🔊")
  await message.add_reaction("📚")
  await message.add_reaction("🕹️")

# DEVELOPER COMMANDS
@commands.command(hidden=True, brief="pong", description="test for correct bot connection")
async def ping(ctx):
  await ctx.send("pong")

@commands.command(hidden=True, brief="latest changes", description="get a list of all the recent improvements, new features and bug fixes done to naota")
async def changelog(ctx):
  # obtain the log from local repo
  repo = git.Repo(os.getcwd())

  commit_list = list(repo.iter_commits(all=True))

  # number of commits = version number
  version = f"0.0.{len(commit_list)}"

  # show the last 5 commits messages
  logs = ""

  for i in range(len(commit_list)):
    
    if i > 5: break

    commit = commit_list[i]

    date = time.gmtime(commit.committed_date)
    author = commit.author
    message = commit.message

    logs += f"[{date.tm_year}/{date.tm_mon}/{date.tm_mday}] - {message}\n"

  em = discord.Embed(title=f"Poio v_{version}", description=logs, color=MAIN_COLOR)
  await ctx.send(embed=em)

@commands.command(hidden=True, brief="latest logs", description="get a list of the lastest log entries, output will depend on LOG_LEVEL configuration, by default INFO")
async def log(ctx, lines = 50):
  title_ = f"Poio.log at {datetime.datetime.now()} last {lines} lines"
  
  description_ = "```" 
  
  with open("Poio.log", "r") as log_file:
    for line in (log_file.readlines() [-lines:]):
      description_ += line

  description_ += "```"

  em = discord.Embed(title=title_, description=description_, color=MAIN_COLOR)
      
  await ctx.send(embed=em)

bot.run(DISCORD_TOKEN)