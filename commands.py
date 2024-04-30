import asyncio
import aiosqlite
from discord.ext import commands
import requests

from utils import load_config
from api.user import User

settings = load_config('config.ini')

DB_PATH = settings['BOT']['DB_PATH']


async def estimate_posorishe_level(user, course, group):
    lessons = user.get_lesson_ids(group_id=group, course_id=course)
    tasks = user.get_all_tasks(group_id=group, course_id=course)


class Authentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='init')
    async def init(self, ctx):
        conn = await aiosqlite.connect(DB_PATH)
        query = f'''INSERT INTO users (id, posorishe_level) VALUES ({ctx.author.id}, 0)'''
        await conn.execute(query)
        await conn.commit()
        await conn.close()
        await ctx.send('**Первичное опознание ~~позорища~~ учащегося - готово!**')

    @commands.command(name='my_level')
    async def update_posorishe_level(self, ctx, login, password, course, group):
        user = User(login, password)
        try:
            user.auth(user.login, user.password)
        except ValueError:
            await ctx.send('Введены неверные данные!')

        new_level = estimate_posorishe_level(user, course, group)

