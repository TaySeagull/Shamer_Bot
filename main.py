from utils import load_config
import discord
from discord.ext import commands


SETTINGS = load_config('config.ini')
TOKEN = SETTINGS['TOKEN']
DB_PATH = SETTINGS['DB_PATH']


intents = discord.Intents.default()
bot = commands.Bot(command_prefix='$', intents=intents, help_command=None)



