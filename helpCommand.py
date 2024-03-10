from typing import Any
import discord
from discord.ext import commands

from settings import MAIN_COLOR, COMMAND_PREFIX

class CustomHelpCommand(commands.HelpCommand):
  def __init__(self):
    super().__init__()

    self.help_usage_str = f"\n\nType `{COMMAND_PREFIX}help command_name` for more info on a command. You can also type `{COMMAND_PREFIX}help category_name` for more info on a category"

    self.command_attrs["brief"] = "show this message"

    self.command_attrs["description"] = f"Show al list of commands and its description"
    self.command_attrs["description"] += self.help_usage_str

  async def send_bot_help(self, mapping):
    desciption_ = ""
    for cog, cmds in mapping.items():
      
      if cog:
        desciption_ += f"\n\n__**{cog.qualified_name}**__"
      else:
        desciption_ += "\n\n__**No Category**__"

      for command in cmds:
        if command.hidden: 
          continue

        desciption_ += f"\n**{COMMAND_PREFIX}{command.qualified_name}: ** {command.brief}"

    desciption_ += self.help_usage_str

    em = discord.Embed(title="All commands", description=desciption_, color=MAIN_COLOR)

    channel = self.get_destination()
    await channel.send(embed=em)

  async def send_command_help(self, command):
    if command.hidden: 
      return
    
    description_ = f"{command.description}"

    # [TODO] aqui mas bien hay que usar el otro metodo send_group_help... 
    # if isinstance(command, commands.Group):
    #   description_ += "\n\nsub commands:"
    #   for subcommand in command.walk_commands():
    #     description_ += f"\n> {subcommand.name}"

    signature = self.get_command_signature(command).strip().split(" ")

    if len(signature) > 1:
      description_ += "\n\n**Arguments:**"

      signature.pop(0)

      for parameter in signature:
        description_ += f"\n{parameter}"

    em = discord.Embed(title="", description=description_, color=MAIN_COLOR)

    channel = self.get_destination()
    await channel.send(embed=em)

  async def send_cog_help(self, cog: commands.Cog):
    
    description_ = f"{cog.description}"

    description_ += "\n\n __**Commands**__"

    for command in cog.get_commands():
      description_ += f"\n **{COMMAND_PREFIX}{command.qualified_name}: ** {command.brief}"

    description_ += self.help_usage_str

    em = discord.Embed(title=f"", description=description_, color=MAIN_COLOR)

    channel = self.get_destination()
    await channel.send(embed=em)
 