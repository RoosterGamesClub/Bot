import logging
from discord.ext import commands

from settings import COMMAND_PREFIX

def log_command_call(logger : logging.Logger, ctx : commands.context):
  
  message = f"{COMMAND_PREFIX}{ctx.command.qualified_name} called (member ID: {ctx.message.author.id}) (member NAME: {ctx.message.author.display_name})"
  
  logger.log(logging.INFO, message)