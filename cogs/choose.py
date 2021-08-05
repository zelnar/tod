from random import choice

import discord
from discord.ext import commands

from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Choose(commands.Cog):
    '''
    The bot will choose something for you
    Usage:
    `<prefix> choose <choices>` (2 or more choices separated by commas or spaces)
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['select'])
    async def choose(self, ctx, *, message):
        choices = [x.strip() for x in message.strip().split(',') if x]
        if len(choices) == 1:
            choices = message.strip().split()
        embed = await send_embed(ctx, ctx.author.display_name, f'I choose **{choice(choices)}**.', send=False)
        if len(choices) == 1:
            embed.set_footer(text='What a huge decision for me!')
        await ctx.send(embed=embed)

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await send_embed(ctx, 'Invalid usage', 'You need to specify some choices.\n'
                                                   f'Usage: `{await get_server_prefix(self.bot, ctx)}choose <choices>` '
                                                   '(2 or more choices separated by spaces)')


def setup(bot):
    bot.add_cog(Choose(bot))
