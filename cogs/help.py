import discord
from discord.ext import commands

from utils.get_embed_color import get_embed_color
from utils.get_number_of_questions import get_number_of_questions
from utils.get_server_prefix import get_server_prefix


class Help(commands.Cog):
    '''
    The bot's help command.
    Usage:
    `<prefix> help`
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *, command=None):
        prefix = await get_server_prefix(self.bot, ctx)
        version = '1.0'
        owner = 'blabla#9999'
        if not command:
            questions = await get_number_of_questions(ctx.guild.id)
            custom_questions = questions - await get_number_of_questions()
            emb = discord.Embed(
                title='TruthOrDare Command List', color=discord.Color.blue(),
                description=f'**Prefix: {await get_server_prefix(self.bot, ctx)}**\n'
                            f'Total questions (including {custom_questions} guild-specific custom questions): {questions}\n'
                            f'Use `{prefix}help <command>` to see specific information about a command.',
                colour=get_embed_color(ctx.author.id)
            )
            for cog in self.bot.cogs:
                emb.add_field(name=cog, value=self.bot.cogs[cog].__doc__.split('\n')[1].strip())

            emb.set_footer(text=f'Bot is running version {version}')
        else:
            for cog in self.bot.cogs:
                if command.lower() == cog.lower():
                    full_desc = '\n'.join([x.strip() for x in (self.bot.cogs[cog].__doc__.split('Usage:')[0].strip().split('\n'))])
                    usage = '\n'.join([x.strip() for x in (self.bot.cogs[cog].__doc__.strip().split('Usage:')[1].strip().split('\n'))])
                    aliases = ', '.join([f'`{x}`' for x in self.bot.get_command(cog.lower()).aliases])
                    emb = discord.Embed(
                        title=f'{cog} - Command',
                        description=full_desc,
                        colour=get_embed_color(ctx.author.id)
                    )
                    emb.add_field(name='Usage', value=usage, inline=False)
                    emb.add_field(name='Aliases', value=aliases if aliases else 'None', inline=False)
                    break
            else:
                emb = discord.Embed(
                    title='Command not found',
                    description=f'No command named `{command}`.',
                    colour=get_embed_color(ctx.author.id)
                )
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Help(bot))