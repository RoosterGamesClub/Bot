import os
from dotenv import load_dotenv

import utils_other

load_dotenv(override=True)

DISCORD_TOKEN   = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX  = os.getenv("COMMAND_PREFIX")
MAIN_COLOR = utils_other.getDiscordColorFromString(os.getenv("MAIN_COLOR"))
WELCOME_CHANNEL_ID = os.getenv("WELCOME_CHANNEL_ID")

REROL_MESSAGE_ID = os.getenv("REROL_MESSAGE_ID")
REROL_CHANNEL_ID = os.getenv("REROL_CHANNEL_ID")