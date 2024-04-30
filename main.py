import discord
from discord.ext import commands
from discord.ext.commands import has_role, MissingRole
from discord.utils import get
from discord import Member
from discord import FFmpegPCMAudio
from utils import load_config
import logging
import requests


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# settings = load_config('config.ini')
# TOKEN = settings['TOKEN']
# DB_PATH = settings['DB_PATH']

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
BAN_WORDS = list(line.strip() for line in open('ban_words.txt', encoding="utf-8"))  # мы не причастны к созданию, честно


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Яндекс"))
    print("Бот готов к использованию!")
    print("__________________________")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    elif not message.content.startswith("!"):
        words = [simple_form(i) for i in message.content.split()]
        for word in words:
            if word in BAN_WORDS:
                try:
                    await message.delete()
                except:
                    print('Ошибка при удалении сообщения')
                await message.channel.send(f'{message.author.mention} написал(а) запрещенное слово! ПОЗОР! Повторишь-бан')
    else:
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
async def rules(ctx):
    rules = """Правила просты:
               1. Ненормативная лексика запрещена
               2. Все мы позорища
               3. Все мы обожаем Яхве
               4. По возможности делаем дз
               5. Сдаем проекты и решаем кр и ср"""
    await ctx.send(rules)


@bot.command(pass_context=True)
async def classes(ctx):
    schedule = "Вторник: с 17:00 до 18:30; с 18:30 до 20:00" \
               "Пятница: с 17:15 до 18:45; с 18:45 до 20:15"
    await ctx.send(schedule)


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


@bot.command(pass_context=True)
@has_role("Яхве")
async def add_Role(ctx, member: discord.Member, *, role: discord.Role):
    if role in member.roles:
        await ctx.send(f"{member.mention} уже с ролью позорища")
    else:
        await member.add_roles(role)
        await ctx.send(f"Добавили роль {role} для {member.mention}")


@add_Role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("А кто дал вам право?")


@bot.command(pass_context=True)
@has_role("Яхве")
async def remove_Role(ctx, member: discord.Member, *, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"У {member.mention} украли роль {role}")
    else:
        await ctx.send(f"Роли у него/нее нет")


@remove_Role.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Без прав")


@bot.command()
@has_role("Яхве")
async def kick(ctx, member: discord.Member, *, reason="Вы не понравились Яхве"):
    if member == None or member == ctx.message.author:
        await ctx.channel.send("Не уходите, Яхве!")
        return
    message = f"Вас выкинули из {ctx.guild.name}, так как {reason}"
    await member.send(message)
    await ctx.send(f"{member} ПОЗОРИЩЕ")
    await member.kick(reason=reason)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("А у вас нет прав!")


def simple_form(word):
    letter, res = '', ''
    for i in word:
        if i != letter:
            letter = i
            res += i
    return res


bot.run(token)