# Hola Roosters!

Este repo contine el source para nuestro **bot de discord**. Si gustas colaborar por favor leer la sección [Para Desarrolladores](#para-desarrolladores), o si tienes algun bug que reportar puedes revisar [Reportar Bugs](#reportar-bugs)

## Para Desarrolladores
Poio esta escrito en **python** utilizando [discord.py](https://discordpy.readthedocs.io/en/stable/). Cualquier duda puedes contactarnos en el [server de discord](https://discord.com/invite/6A5wwHVGGC)

### Setup
1. Obten una copia local del repositorio
```
git clone https://github.com/RoosterGamesClub/poio-bot.git
```
2. Instala los módulos necesarios
```
pip install -r requirements.txt
```
3. Crea un nuevo archivo `.env` con los siguientes parámetros en el directorio del proyecto
```env
DISCORD_TOKEN = "YOUR DISCORD TOKEN"

COMMAND_PREFIX = "!"
MAIN_COLOR = "#4E5058"

GUILD_ID = 0000000000000000000

WELCOME_CHANNEL_ID = 0000000000000000000

REROL_CHANNEL_ID = 0000000000000000000
REROL_MESSAGE_ID = 0000000000000000000

NEWS_CHANNEL_ID = 0000000000000000000

LOG_LEVEL = "DEBUG"
```

## Reportar Bugs
Ve a la página de [issues](https://github.com/RoosterGamesClub/poio-bot/issues) y crea un nuevo ticket. 
Recomendamos ser descriptivo y de ser posible proporcionar los pasos para reproducir el problema
