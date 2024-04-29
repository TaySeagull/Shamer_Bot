from utils import load_config
import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

settings = load_config('config.ini')
TOKEN = settings['TOKEN']
DB_PATH = settings['DB_PATH']


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Добро пожаловать, новое позорище, {member.name}!')
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json()
        await message.channel.send(data['message'])

    async def on_member_remove(self, member):
        await member.dm_channel.send(
            f'Хм, теперь мы все знаем, что {member.name} главное позорище')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "я позорище" in message.content.lower():
            await message.channel.send("Ну-ну, все мы не без греха")

    @bot.slash_command(name='test_slash_command', description='Отвечает "Успешный тест!"')
    async def __test(ctx):
        await ctx.respond('Успешный тест!')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(settings["TOKEN"])
