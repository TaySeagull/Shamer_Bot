import asyncio
import aiosqlite
from discord.ext import commands
import requests

from utils import load_config
from api.user import User

settings = load_config('config.ini')

DB_PATH = settings.BOT.DB_PATH


async def estimate_posorishe_level(user, course, group):
    lessons = user.get_lesson_ids(course, group)
    max_score, user_score = 0, 0
    for lesson_id in lessons:
        tasks = user.get_all_tasks(lesson_id=lesson_id, course_id=course, group_id=group)
        for i in tasks['0']['tasks']:
            max_score += i['scoreMax']
            if i['solution']:
                solution = sorted(i['solution'], key=lambda x: x['score'])
                user_score += solution[-1]
        for i in tasks['1']['tasks']:
            max_score += i['scoreMax']
            if i['solution']:
                solution = sorted(i['solution'], key=lambda x: x['score'])
                user_score += solution[-1]
        for i in tasks['2']['tasks']:
            max_score += i['scoreMax']
            if i['solution']:
                solution = sorted(i['solution'], key=lambda x: x['score'])
                user_score += solution[-1]


class Authentication(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='init')
    async def init(self, ctx, group: int):
        conn = await aiosqlite.connect(DB_PATH)
        res = await conn.execute('SELECT * FROM users WHERE id = ?', (ctx.author.id, ))
        if not res.fetchall():
            query = str(f'''INSERT INTO users (id, student_group, posorishe_level) VALUES (?, ?, ?)''')
            await conn.execute(query, (ctx.author.id, group, 0, ))
            await conn.commit()
            await ctx.reply('**Первичное опознание ~~позорища~~ учащегося - готово!**')
        else:
            await ctx.reply('Такое позорище уже есть в таблице!')
        await conn.close()

    @commands.hybrid_command(name='my_level')
    async def update_posorishe_level(self, ctx, login, password, course):
        await ctx.message.delete()
        user = User(login, password)
        try:
            user.auth(user.login, user.password)
        except ValueError:
            await ctx.send('Введены неверные данные!')

        conn = await aiosqlite.connect(DB_PATH)
        query = f'''SELECT student_group FROM users WHERE id = {ctx.author.id}'''
        group = await conn.execute(query)
        await conn.close()
        new_level = estimate_posorishe_level(user, course, group)
