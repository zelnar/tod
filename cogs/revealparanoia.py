import json

import discord
from discord.ext import commands

from utils.get_embed_color import get_embed_color
from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class RevealParanoia(commands.Cog):
    '''
    Reveal all the hidden paranoia questions in a channel.
    Play with `<prefix> paranoia <member> [pg | pg13 | r]`.
    Usage:
    `<prefix> revealparanoia`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['showparanoia', 'showp', 'revealp', 'pshow', 'preveal'])
    @commands.guild_only()
    async def revealparanoia(self, ctx, *, content=None):
        data = json.load(open('data\\active_paranoia_questions.json', 'r'))
        if str(ctx.channel.id) not in data:
            await send_embed(ctx, 'No more unseen questions',
                             'This channel doesn\'t have any more paranoia questions.')
            return
        embed = discord.Embed(
            color=get_embed_color(ctx.author.id),
            description='Shows only the questions with hidden answers sent in this channel previously.'
        )
        count = 0
        for question_data in data[str(ctx.channel.id)]:
            try:
                user = (await self.bot.fetch_user(question_data[0]))
                user = f'{user.name}#{user.discriminator}'
            except:
                user = '(invalid user)'
            embed.add_field(name=question_data[1],
                            value=f'{user} responded: **{question_data[2]}** ([Link]({question_data[3]}))',
                            inline=False)
            count += 1
        embed.set_author(name=f'#{ctx.channel.name} hidden paranoia questions ({count})',
                         icon_url=ctx.author.avatar_url)

        data.pop(str(ctx.channel.id))
        f = open('data\\active_paranoia_questions.json', 'w')
        f.write(json.dumps(data))
        f.close()
        await ctx.send(embed=embed)

    @revealparanoia.error
    async def revealparanoia_error(self, ctx, error):
        await send_embed(ctx, 'Invalid usage',
                         f'Invalid usage. Use `{await get_server_prefix(self.bot, ctx)}revealparanoia`')


def setup(bot):
    bot.add_cog(RevealParanoia(bot))
