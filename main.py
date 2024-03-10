import discord
from discord.ext import commands

import utils_other 
import random

import os
from dotenv import load_dotenv

load_dotenv(override=True)

######## CONFIGS ########
DISCORD_TOKEN   = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX  = os.getenv("COMMAND_PREFIX")
MAIN_COLOR = utils_other.getDiscordColorFromString(os.getenv("MAIN_COLOR"))
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

REROL_MESSAGE_ID = os.getenv("REROL_MESSAGE_ID")
REROL_CHANNEL_ID = os.getenv("REROL_CHANNEL_ID")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
  print("bot ready")

  print("-------------- loading commands --------------")
  print("loading developer commands...")
  bot.add_command(ping)

  print("loading admin commands...")
  bot.add_command(genrerol)

  print("loading user commands...")
  bot.add_command(about)
  bot.add_command(website)
  bot.add_command(github)
  bot.add_command(linkedin)
  bot.add_command(x)
  bot.add_command(instagram)
  bot.add_command(socials)

  bot.add_command(poll)
  bot.add_command(boolean)
  bot.add_command(integer)

  print("---------------------------------------------")

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
@commands.command(brief="about poio", description="")
async def about(ctx):

  title_ = "**Líder Supremo**"

  url_ = "https://roostergamesclub.github.io/Site/pollo.html"

  description_ = ""
  description_ += "Aunque solo me vean en la pantalla, soy un miembro activo del equipo y el **líder supremo**. Confío plenamente en cada uno de los miembros del Club para crear juegos increíbles, ya que son talentosos y comprometidos"
  description_ += "\n\nContribuye a mi desarrollo [aquí](https://github.com/RoosterGamesClub/Bot)"

  em = discord.Embed(title=title_, url=url_, description=description_, color=MAIN_COLOR)

  await ctx.send(embed=em)

#socials
@commands.command(brief="official website link", description="get a link to Rooster Games official website")
async def website(ctx):
  await ctx.send("<https://roostergamesclub.github.io/Site/index.html>")

@commands.command(brief="github link", description="get a link to Rooster Games official github organization")
async def github(ctx):
  await ctx.send("<https://github.com/RoosterGamesClub>")

@commands.command(brief="linkedin link", description="get a link to Rooster Games official linkedin company profile")
async def linkedin(ctx):
  await ctx.send("<https://www.linkedin.com/company/rooster-games-devclub/about/>")

@commands.command(brief="x (twitter) link", description="get a link to Rooster Games official x account")
async def x(ctx):
  await ctx.send("<https://twitter.com/RoosterGamesUaa>")

@commands.command(brief="youtube link", description="get a link to Rooster Games official youtube channel")
async def youtube(ctx):
  await ctx.send("<https://www.youtube.com/channel/UCEti3QAC17BPa1MzS4moV5w>")

@commands.command(brief="instagram link", description="get a link to Rooster Games official instagram profile")
async def instagram(ctx):
  await ctx.send("<https://www.instagram.com/rooster.games/>")

@commands.command(brief="social accounts links", description="get a list of all Rooster Games social accounts")
async def socials(ctx):
  title_ = "Rooster Games Socials"

  url_ = "https://roostergamesclub.github.io/Site/index.html"

  description_ = ""
  description_ += "\n**GitHub: **[RoosterGamesClub](https://github.com/RoosterGamesClub)"
  description_ += "\n**LinkedIn: **[Rooster Games](https://www.linkedin.com/company/rooster-games-devclub/about/)"
  description_ += "\n**X (twitter): **[@RoosterGamesUaa](https://twitter.com/RoosterGamesUaa)"
  description_ += "\n**YouTube: **[@RoosterGamesClub](https://www.youtube.com/channel/UCEti3QAC17BPa1MzS4moV5w)"
  description_ += "\n**Instagram: **[rooster.games](https://www.instagram.com/rooster.games/)"

  em = discord.Embed(title=title_, url=url_, description=description_, color=MAIN_COLOR)

  await ctx.send(embed=em)

#desitions
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



bot.run(DISCORD_TOKEN)