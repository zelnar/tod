import json
import random
from random import choice

from discord.ext import commands

from utils.choose_random_member import choose_random_member
from utils.get_millis_time import get_millis_time
from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Truth(commands.Cog):
    '''
    Ask a truth question in chat!
    Usage:
    `<prefix> truth [pg | pg13 | r]` (If category not specified, I choose a pg or pg13 question.)
    '''

    def __init__(self, bot):
        self.bot = bot

    async def list_extend(self, list1, list2):
        list1.extend(list2)
        return list1

    @commands.command(aliases=['t'])
    @commands.guild_only()
    async def truth(self, ctx, *, category=None):
        async with ctx.typing():
            data = json.load(open('data\\questions\\truths.json', 'r'))
            if not category:
                default_category = json.load(open('data\\default_category.json', 'r'))
                if str(ctx.guild.id) in default_category:
                    category = default_category[str(ctx.guild.id)]
                else:
                    category = random.choice(['pg'])
            category = category.lower()

            data2 = json.load(open('data\\questions\\servertruths.json', 'r'))
            if str(ctx.guild.id) in data2:
                questions = data2[str(ctx.guild.id)][category]
            else:
                questions = []

        if category == 'add':
            await send_embed(ctx, f'Wrong command?', f'Did you mean to use the add command?'
                                                     f'\n(`{await get_server_prefix(self.bot, ctx)}add '
                                                     f'<truth | dare | wyr> <pg | pg13 | r> <question>`)')
            return

        random.seed(get_millis_time())

        question_chosen = choice(await self.list_extend(questions, data[category]))
        question_chosen = question_chosen.replace('[random user]', f'{choose_random_member(ctx)}')
        if category in ['pg', 'pg13', 'r']:
            await send_embed(ctx, f'Truth ({category})', question_chosen)

    @truth.error
    async def truth_error(self, ctx, error):
        await send_embed(ctx, 'Invalid category', f'Use {await get_server_prefix(self.bot, ctx)}truth '
                                                  f'[pg | pg13 | r]')


def setup(bot):
    bot.add_cog(Truth(bot))
