import logging
import typing

import discord
from discord.ext import commands

from settings import MAIN_COLOR

import utils.loggingUtils
import utils.otherUtils

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
    
      em.description += f"\n**__Rooster since__** \n{mention.joined_at.strftime('%Y-%m-%d')}"
      
      em.description += "\n\n**__Roles__**"
      for role in mention.roles:

        if role.name == "@everyone": continue
        if role.name.lower() == "Silkie Chicken".lower(): continue

        em.description += f"\n{role.name}" 

    elif isinstance(mention, discord.Role):
      em.title = f"{mention.name} Rol Stats"

      role = ctx.guild.get_role(mention.id)

      em.description += f"> **members**: {len(role.members)}"
    
      em.description += "\n"
      for i, member in enumerate(role.members):
        if i > 5:
          break

        em.description += f"\n> {1+i}. {member.display_name}"

    else:
      em.title = "Rooster Games Stats"

      em.description += f"\n**{len(ctx.guild.members)}** - Members"

      programming_role = discord.utils.get(ctx.guild.roles,name="Programming")
      gamedesing_role = discord.utils.get(ctx.guild.roles,name="GameDesign")
      graphics_role = discord.utils.get(ctx.guild.roles,name="Graphics/Animation")
      music_role = discord.utils.get(ctx.guild.roles,name="Music")
      sound_role = discord.utils.get(ctx.guild.roles,name="SoundDesign/VoiceActing")
      writting_role = discord.utils.get(ctx.guild.roles,name="Writing/NarrativeDesign")

      em.description += "\n"

      if programming_role:
        em.description += f"\n**{len(programming_role.members)}** - Programming"

      if gamedesing_role:
        em.description += f"\n**{len(gamedesing_role.members)}** - GameDesing"

      if graphics_role:
        em.description += f"\n**{len(graphics_role.members)}** - Graphics/Animation"

      if music_role:
        em.description += f"\n**{len(music_role.members)}** - Music"

      if sound_role:
        em.description += f"\n**{len(sound_role.members)}** - SoundDesign/VoiceActing"

      if writting_role:
        em.description += f"\n**{len(writting_role.members)}** - Writing/NarrativeDesign"

    await ctx.send(embed=em)

  @commands.hybrid_command(brief="about poio", description="get to know a little bit about Poio and how to contribute")
  async def about(self, ctx):

    title_ = "**Líder Supremo**"

    url_ = "https://roostergamesclub.github.io/Site/pollo.html"

    description_ = ""
    description_ += "Aunque solo me vean en la pantalla, soy un miembro activo del equipo y el **líder supremo**. Confío plenamente en cada uno de los miembros del Club para crear juegos increíbles, ya que son talentosos y comprometidos"
    description_ += "\n\nContribuye a mi desarrollo [aquí](https://github.com/RoosterGamesClub/Poio-Bot)"

    em = discord.Embed(title=title_, url=url_, description=description_, color=MAIN_COLOR)

    await ctx.send(embed=em)

  @commands.hybrid_command(brief="social accounts links", description="get a list of all Rooster Games social accounts")
  async def socials(self, ctx):
    title_ = "Rooster Games Socials"

    url_ = "https://roostergamesclub.github.io/Site/index.html"

    description_ = ""
    description_ += "\n**Website: **[roostergamesclub](https://roostergamesclub.github.io/Site/index.html)"
    description_ += "\n**GitHub: **[RoosterGamesClub](https://github.com/RoosterGamesClub)"
    description_ += "\n**LinkedIn: **[Rooster Games](https://www.linkedin.com/company/rooster-games-devclub/about/)"
    description_ += "\n**X (twitter): **[@RoosterGamesUaa](https://twitter.com/RoosterGamesUaa)"
    description_ += "\n**YouTube: **[@RoosterGamesClub](https://www.youtube.com/channel/UCEti3QAC17BPa1MzS4moV5w)"
    description_ += "\n**Instagram: **[rooster.games](https://www.instagram.com/rooster.games/)"

    em = discord.Embed(title=title_, url=url_, description=description_, color=MAIN_COLOR)

    await ctx.send(embed=em)

  async def __proyects_show(self, ctx):
    em = discord.Embed(title="", description="", color=MAIN_COLOR)

    em.title = "Projects"

    #em.description += "\nRed Hood"
    #em.description += "\nNatu"

    em.description += "We'll start a new project soon. Make sure to [leave a propousal here](https://docs.google.com/forms/d/e/1FAIpQLSdomvlxpXMuAKcRC0UkWgI4tfx-sdha4MjS474sqbT0HzE_rQ/viewform)"

    await ctx.send(embed=em)

  @commands.hybrid_group(brief="know the work", description="get a list of the projects we've build and/or are currently working on")
  async def projects(self, ctx):
    await self.__proyects_show(ctx)

  @projects.command(name="show", brief="know the work", description="get a list of the projects we've build and/or are currently working on")
  async def projects_show(self, ctx):
    await self.__proyects_show(ctx)

  @projects.command(name="natu", brief="resources for Natu", description="get a list of resources for Natu")
  async def proyectos_main(self, ctx):
    if not utils.otherUtils.isRole(ctx, "Natu"):
      return await ctx.send("Not a member of Natu")

    em = discord.Embed(title = "", description="", color=MAIN_COLOR)

    em.title="Natu's resources"

    em.description += "\n[The Milanote](https://app.milanote.com/1S7tUv15aVQk2b/natu?p=pWUsBgCem2B) for ideas and more"
    em.description += "\n[The Github](https://github.com/RoosterGamesClub/Natu) to save the work"
    em.description += "\n[The Art Reference](https://drive.google.com/drive/folders/1rd0niaU6imMJzC9nerQq8uP3nRCDUABU) to get an idea of how it may look"

    await ctx.send(embed=em)

  @projects.command(name="reed", brief="resources for Reed Hood", description="get a list of resources for Red Hood")
  async def projects_reed_hood(self, ctx):
    if not utils.otherUtils.isRole(ctx, "Reed Hood"):
      return await ctx.send("Not a member of Reed Hood")

    em = discord.Embed(description="", color=MAIN_COLOR)

    em.title = "Red Hood's resources"

    em.description += "\n[The Github](https://github.com/RoosterGamesClub/Red-Hood) to save the work"

    await ctx.send(embed=em)
