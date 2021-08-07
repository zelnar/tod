import json
import time

import discord
from discord.ext import commands

from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Suggestion(commands.Cog):
    '''
    Suggest a command or feature to the owner of the bot!
    Usage:
    `<prefix> suggestion <suggestion>`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['suggest'])
    async def suggestion(self, ctx, *, suggestion):
        async with ctx.typing():
            data = json.load(open('data\\suggestions.json', 'r'))
            if str(ctx.author.id) in data:
                data[str(ctx.author.id)][time.time()] = suggestion
            else:
                data[str(ctx.author.id)] = {time.time(): suggestion}
            json_data = json.dumps(data)
            f = open('data\\suggestions.json', 'w')
            f.write(json_data)
            f.close()
            await send_embed(ctx, 'Suggestion sent', f'I sent your suggestion to the owner! ({suggestion})')

    @suggestion.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await send_embed(ctx, 'Provide a suggestion', 'You need to suggest *something*.\n'
                                                          f'Use `{await get_server_prefix(self.bot, ctx)}suggest <suggestion>`'
                                                          f' to suggest a command or feature.')
        else:
            raise error


def setup(bot):
    bot.add_cog(Suggestion(bot))
