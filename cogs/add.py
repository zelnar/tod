import json

import discord
from discord.ext import commands

from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Add(commands.Cog):
    '''
    Add a custom question in your server.
    Usage:
    `<prefix> add <truth | dare | wyr | paranoia> <pg | pg13 | r> <question>`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['addquestion'])
    @commands.guild_only()
    async def add(self, ctx, question_type, category, *, question):
        if ctx.author.id != 461345173314732052:
            return
        if '\n' in question.strip():
            await send_embed(ctx, f'Wrong command?', f'Did you mean to use the bulkadd command?'
                                                     f'\n(`{await get_server_prefix(self.bot, ctx)}bulkadd '
                                                     f'<truth | dare | wyr> <pg | pg13 | r> <questions>` (separated by new lines))')
            return
        question_type = question_type.lower()
        category = category.lower()
        async with ctx.typing():
            if question_type in ['truth', 't', 'truths']:
                location = 'data\\questions\\truths.json'
                data = json.load(open(location, 'r'))
                question_type = 'truth'
                question = question.capitalize().replace(' u ', ' you ')
            elif question_type in ['dare', 'd', 'dares']:
                location = 'data\\questions\\dares.json'
                data = json.load(open(location, 'r'))
                question_type = 'dare'
                question = question.capitalize().replace(' u ', ' you ')
            elif question_type in ['wyr', 'wouldyourather']:
                location = 'data\\questions\\wyrs.json'
                data = json.load(open(location, 'r'))
                question_type = 'wyr'
                question = question.capitalize().replace(' u ', ' you ')
            elif question_type in ['p', 'paranoia']:
                location = 'data\\questions\\paranoias.json'
                data = json.load(open(location, 'r'))
                question_type = 'paranoia'
                question = question.capitalize().replace(' u ', ' you ')

            if category in ['pg', 'pg13', 'r']:
                # if str(ctx.guild.id) in data:
                if question in data[category]:
                    await send_embed(ctx, 'Duplicate question',
                                     'This question is already inside the list of questions.')
                    return
                data[category].append(question.strip())
                data[category] = list(set(data[category]))
                # data[str(ctx.guild.id)][category].append(question)
                # else:
                # data[str(ctx.guild.id)] = {'pg': [], 'pg13': [], 'r': []}
                # data[str(ctx.guild.id)][category].append(question)
            else:
                await send_embed(ctx, 'Invalid category', f'Use {await get_server_prefix(self.bot, ctx)}add '
                                                          f'<truth | dare | wyr | paranoia> <pg | pg13 | r> <question>')
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
                                                   f'<truth | dare | wyr | paranoia> <pg | pg13 | r> <question>')
        else:
            raise error


def setup(bot):
    bot.add_cog(Add(bot))
