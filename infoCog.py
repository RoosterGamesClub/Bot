import logging

import discord
from discord.ext import commands

from settings import MAIN_COLOR

import loggingUtils

class InfoCog(commands.Cog, name="Info"):

  """ Get relevant news, links and resources from Rooster Games """

  def __init__(self, bot):
    self.bot = bot

    self.logger = logging.getLogger("bot.info_cog")

  async def cog_before_invoke(self, ctx):
    loggingUtils.log_command_call(self.logger, ctx)

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
