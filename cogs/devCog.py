import logging
import os
import time
import datetime

import discord
from discord.ext import commands

import git

import utils.loggingUtils
import utils.otherUtils

from settings import MAIN_COLOR

class DevCog(commands.Cog, name="Dev"):

  """ Get debug and performace info for poio """

  def __init__(self, bot):
    self.bot = bot

    self.logger = logging.getLogger("bot.dev_cog")

  async def cog_before_invoke(self, ctx):
    utils.loggingUtils.log_command_call(self.logger, ctx) 

  @commands.hybrid_command(hidden=True, brief="pong", description="test for correct bot connection")
  async def ping(self, ctx):
    await ctx.send(f"pong! {int(round(self.bot.latency, 3) * 1000)}ms")

  @commands.hybrid_command(brief="latest commits", description="get a list of all the recent improvements, new features and bug fixes done to poio")
  async def changelog(self, ctx):
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

  @commands.hybrid_command(hidden=True, brief="show the log", description="get a list of the lastest log entries, output will depend on LOG_LEVEL, by default INFO")
  async def log(self, ctx, lines = 50):
    title_ = f"Poio.log at {datetime.datetime.now()} last {lines} lines"
    
    description_ = "```" 
    
    with open("Poio.log", "r") as log_file:
      for line in (log_file.readlines()[-lines:]):
        description_ += line

    description_ += "```"

    em = discord.Embed(title=title_, description=description_, color=MAIN_COLOR)
        
    await ctx.send(embed=em)

  @commands.hybrid_command(brief="report a bug", description="log a bug for fixing, the description should be enclose in \" \" for example: `!bug \"not working!\"`")
  async def bug(self, ctx, description : str):
    with open("bugs.txt", "r") as file:
      bug_number = len(file.readlines()) + 1

    with open("bugs.txt", "a") as file:
      file.write(f"\n{bug_number}.\t [{ctx.message.created_at}] by {ctx.message.author.display_name} (user ID: {ctx.message.author.id}) \treport: {description}")

    await ctx.send(f"> _**\"{description}\"**_ logged as `#{bug_number}`")

  # GOD COMMANDS (only for devs)
  @commands.command(hidden=True, brief="sync commands", description="sync the current app command tree")
  async def sync(self, ctx):

    if not utils.otherUtils.isDev(ctx.author):
      self.logger.log(logging.INFO, f"access denied for user {ctx.author.display_name} (member ID: {ctx.author.id}) when running sync command")
      await ctx.send("sorry, you have no permision to run !sync command")
      return

    await self.bot.tree.sync() #guild = discord.Object(id = GUILD_ID)  
    await ctx.send("syncing commands...")

    self.logger.log(logging.INFO, f"synced slash commands for {self.bot.user}")