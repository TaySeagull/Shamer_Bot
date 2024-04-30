import asyncio

from utils import load_config
import discord
from discord.ext import commands
import logging

import commands as bot_commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

settings = load_config('config.ini')
DB_PATH = settings.BOT.DB_PATH

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.command(name='sync')
async def sync(ctx):
    print('Syncing...')
    if ctx.author.id == 503272813570818070:
        await bot.tree.sync()
        print('Synced')


async def main():
    await bot.add_cog(bot_commands.Authentication(bot))
    await bot.start(settings.BOT.TOKEN)


asyncio.run(main())
