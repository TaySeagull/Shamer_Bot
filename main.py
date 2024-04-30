import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from utils import load_config
import logging
import requests

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#settings = load_config('config.ini')
#TOKEN = settings['TOKEN']
#DB_PATH = settings['DB_PATH']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready(self):
    logger.info(f'{self.user} has connected to Discord!')
    for guild in self.guilds:
        logger.info(
            f'{self.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1232029791876677733)
    await channel.send(f"Добро пожаловать, новое позорище {member.name}!")
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    await channel.send(data['message'])


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1232029791876677733)
    await channel.send(f'Хм, теперь мы все знаем, что {member.name} главное позорище')


@bot.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio("music.mp3")
        player = voice.play(source)
    else:
        await ctx.send("Вы не находитесь в голосовом канале. Чтобы использовать функцию, войдите в голосовой канал.")


@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Пока-пока, позорища")
    else:
        await ctx.send("Я не в голосовом канале")


@bot.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Аудио не играет")


@bot.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Аудио не стоит на паузе")


@bot.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@bot.command(pass_context=True)
async def play(ctx):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio("music.mp3")
    player = voice.play(source)


bot.run('token')