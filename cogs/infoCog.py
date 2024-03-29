import logging
import typing

import discord
from discord.ext import commands

from settings import MAIN_COLOR

import utils.loggingUtils

class InfoCog(commands.Cog, name="Info"):

  """ Get relevant news, links and resources from Rooster Games """

  def __init__(self, bot):
    self.bot = bot

    self.logger = logging.getLogger("bot.info_cog")

  async def cog_before_invoke(self, ctx):
    utils.loggingUtils.log_command_call(self.logger, ctx)

  @commands.hybrid_command(brief="get stats for this server", description="get stats for the server or for individual members or commands")
  async def stats(self, ctx : commands.Context, mention : typing.Union[discord.Member, discord.Role] = None):

    em = discord.Embed(title="", description="", color=MAIN_COLOR)

    if isinstance(mention, discord.Member):
      em.set_author(name=f"\"{mention.display_name}\" stats", url="", icon_url=mention.display_avatar.url)
    
      em.description += f"\n**__Rooster desde__** \n{mention.joined_at.strftime('%Y-%m-%d')}"
      
      em.description += "\n\n**__Intereses__**"
      for role in mention.roles:
        #print(role.name)

        if role.name == "@everyone": continue
        if role.name == "silkie chicken": continue

        em.description += f"\n{role.name}" 

    elif isinstance(mention, discord.Role):
      role = ctx.guild.get_role(mention.id)

      em.description += f"> **miembros**: {len(role.members)}"
    
      em.description += "\n"
      for i, member in enumerate(role.members):
        if i > 5:
          break

        em.description += f"\n> {1+i}. {member.display_name}"

    else:
      em.title = "Rooster Games Stats"

      em.description += f"\n**{len(ctx.guild.members)}** - Miembros"

      programming_role = discord.utils.get(ctx.guild.roles,name="Programming")
      gamedesing_role = discord.utils.get(ctx.guild.roles,name="GameDesign")
      graphics_role = discord.utils.get(ctx.guild.roles,name="Graphics/Animation")
      music_role = discord.utils.get(ctx.guild.roles,name="Music")
      sound_role = discord.utils.get(ctx.guild.roles,name="SoundDesign/VoiceActing")
      writting_role = discord.utils.get(ctx.guild.roles,name="Writing/NarrativeDesign")

      em.description += "\n"

      if programming_role:
        em.description += f"\n**{len(programming_role.members)}** - Programadores"

      if gamedesing_role:
        em.description += f"\n**{len(gamedesing_role.members)}** - Game Designers"

      if graphics_role:
        em.description += f"\n**{len(graphics_role.members)}** - Artistas/Animadores"

      if music_role:
        em.description += f"\n**{len(music_role.members)}** - Músicos/Compositores "

      if sound_role:
        em.description += f"\n**{len(sound_role.members)}** - Actores de voz/Sound designers"

      if writting_role:
        em.description += f"\n**{len(writting_role.members)}** - Escritores"

    await ctx.send(embed=em)

  @commands.hybrid_command(brief="about poio", description="get to know a little bit about Poio and how to contribute")
  async def about(self, ctx):

    title_ = "**Líder Supremo**"

    url_ = "https://roostergamesclub.github.io/Site/pollo.html"

    description_ = ""
    description_ += "Aunque solo me vean en la pantalla, soy un miembro activo del equipo y el **líder supremo**. Confío plenamente en cada uno de los miembros del Club para crear juegos increíbles, ya que son talentosos y comprometidos"
    description_ += "\n\nContribuye a mi desarrollo [aquí](https://github.com/RoosterGamesClub/poio-bot.git)"

    em = discord.Embed(title=title_, url=url_, description=description_, color=MAIN_COLOR)

    await ctx.send(embed=em)

  @commands.hybrid_command(brief="official website link", description="get a link to Rooster Games official website")
  async def website(self, ctx):
    await ctx.send("> <https://roostergamesclub.github.io/Site/index.html>")

  @commands.hybrid_command(brief="github link", description="get a link to Rooster Games official github organization")
  async def github(self, ctx):
    await ctx.send("> <https://github.com/RoosterGamesClub>")

  @commands.hybrid_command(brief="linkedin link", description="get a link to Rooster Games official linkedin company profile")
  async def linkedin(self, ctx):
    await ctx.send("> <https://www.linkedin.com/company/rooster-games-devclub/about/>")

  @commands.hybrid_command(brief="x (twitter) link", description="get a link to Rooster Games official x account")
  async def x(self, ctx):
    await ctx.send("> <https://twitter.com/RoosterGamesUaa>")

  @commands.hybrid_command(brief="youtube link", description="get a link to Rooster Games official youtube channel")
  async def youtube(self, ctx):
    await ctx.send("> <https://www.youtube.com/channel/UCEti3QAC17BPa1MzS4moV5w>")

  @commands.hybrid_command(brief="instagram link", description="get a link to Rooster Games official instagram profile")
  async def instagram(self, ctx):
    await ctx.send("> <https://www.instagram.com/rooster.games/>")

  @commands.hybrid_command(brief="social accounts links", description="get a list of all Rooster Games social accounts")
  async def socials(self, ctx):
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

  @commands.hybrid_command(brief="know our work", description="get a list of the projects we've build and/or are currently working on")
  async def projects(self, ctx):
    em = discord.Embed(title="", description="", color=MAIN_COLOR)

    em.title = "Proyectos"

    # em.description += "\n__Upcoming__"
    # em.description += "\n"
    em.description += "\nRed Hood"
    em.description += "\nUaa Ascension"
    em.description += "\nNatu"

    await ctx.send(embed=em)