from discord.ext import commands

from utils.send_embed import send_embed


class Info(commands.Cog):
    '''
    Get various useful information about the bot including ping and links
    Usage:
    `<prefix> info`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ping', 'invite', 'links'])
    @commands.guild_only()
    async def info(self, ctx, *, content=None):
        await send_embed(ctx, 'Info', f'**Ping:** {round(self.bot.latency * 1000, 2)}ms\n'
                                      f'**Invite Link (admin):** [here]('
                                      f'https://discord.com/api/oauth2/authorize?client_id=869046610708013089'
                                      f'&permissions=8&scope=bot%20applications.commands)\n '
                         )

def setup(bot):
    bot.add_cog(Info(bot))
