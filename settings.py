import logging
import logging.handlers

import os
from dotenv import load_dotenv

import utils.otherUtils

load_dotenv(override=True)

""" Configuration for the logger """

LOG_LEVEL = os.getenv('LOG_LEVEL')

# logging handler
handler = logging.handlers.RotatingFileHandler(
  filename='Poio.log',
  encoding='utf-8',
  maxBytes=32*1024*1024, #32 MiB
  backupCount=10
)

# formatter
datetime_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', datefmt=datetime_format, style='{')
handler.setFormatter(formatter)

# loggers
discordLogger = logging.getLogger('discord')
discordLogger.setLevel(LOG_LEVEL)
discordLogger.addHandler(handler)

botLogger = logging.getLogger('bot')
botLogger.setLevel(LOG_LEVEL) 
botLogger.addHandler(handler)

""" Other configurations """

DISCORD_TOKEN   = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX  = os.getenv("COMMAND_PREFIX")
MAIN_COLOR = utils.otherUtils.getDiscordColorFromString(os.getenv("MAIN_COLOR"))

GUILD_ID = os.getenv("GUILD_ID")

WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

REROL_MESSAGE_ID = os.getenv("REROL_MESSAGE_ID")
REROL_CHANNEL_ID = os.getenv("REROL_CHANNEL_ID")

NEWS_CHANNEL_ID = os.getenv("NEWS_CHANNEL_ID")

RULES_CHANNEL_ID = os.getenv("RULES_CHANNEL_ID")
RULES_MESSAGE_ID = os.getenv("RULES_MESSAGE_ID")