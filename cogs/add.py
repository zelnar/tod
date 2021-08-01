import json

import discord
from random import choice
from discord.ext import commands

from util.get_server_prefix import get_server_prefix
from util.send_embed import send_embed


class Add(commands.Cog):
    '''
    Add a custom question in your server.
    Usage:
    `<prefix> add <truth | dare | wyr> <pg | pg13 | r> <question>`
    `<prefix> add wyr <pg | pg13 | r> <choice1>, <choice2>, ...` (2-5 choices)
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addquestion'])
    @commands.guild_only()
    async def add(self, ctx, question_type, category, *, question):
        if ctx.author.id != 461345173314732052:
            return
        question_type = question_type.lower()
        category = category.lower()
        async with ctx.typing():
            if not category:
                default_category = json.load(open('data\\default_category.json', 'r'))
                if str(ctx.guild.id) in default_category:
                    category = default_category[str(ctx.guild.id)]
                else:
                    category = 'pg'

            if question_type in ['truth', 't', 'truths']:
                location = 'data\\questions\\truths.json'
                data = json.load(open(location, 'r'))
                question_type = 'truth'
                question = question.lower().capitalize().replace(' u ', ' you ')
            elif question_type in ['dare', 'd', 'dares']:
                location = 'data\\questions\\dares.json'
                data = json.load(open(location, 'r'))
                question_type = 'dare'
                question = question.lower().capitalize().replace(' u ', ' you ')
            elif question_type in ['wyr', 'wouldyourather']:
                location = 'data\\questions\\wyrs.json'
                data = json.load(open(location, 'r'))
                question_type = 'wyr'
                question = question.lower().capitalize().replace(' u ', ' you ')

            if category in ['pg', 'pg13', 'r']:
                #if str(ctx.guild.id) in data:
                if question in data[category]:
                    await send_embed(ctx, 'dupe', 'dupe')
                    return
                data[category].append(question)
                data[category] = list(set(data[category]))
                    #data[str(ctx.guild.id)][category].append(question)
                #else:
                    #data[str(ctx.guild.id)] = {'pg': [], 'pg13': [], 'r': []}
                    #data[str(ctx.guild.id)][category].append(question)
            else:
                await send_embed(ctx, 'Invalid category', f'Use {await get_server_prefix(self.bot, ctx)}add '
                                                          f'<truth | dare | wyr> <pg | pg13 | r> <question>')
                return

        json_data = json.dumps(data)
        f = open(location, 'w')
        f.write(json_data)
        f.close()
        await send_embed(ctx, f'Added a {question_type} question (Category: {category})', question)


    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await send_embed(ctx, 'Invalid usage', f'Use {await get_server_prefix(self.bot, ctx)}add '
                                                   f'<truth | dare | wyr> <pg | pg13 | r> <question>')
        else:
            raise error

def setup(bot):
    bot.add_cog(Add(bot))