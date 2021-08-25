import json
import random

import discord
from discord.ext import commands
from numpy.random import choice

from utils.choose_random_member import choose_random_member
from utils.get_server_prefix import get_server_prefix
from utils.send_embed import send_embed


class Paranoia(commands.Cog):
    '''
    Play paranoia!
    To play, I dm a person of your choice a question (most likely to...) and the person responds who they think represents the statement the most.
    Then, a coinflip decides whether the question is revealed or not.
    Usage:
    `<prefix> paranoia <member> <pg | pg13 | r>` (If category not specified, I choose a pg or pg13 question.)
    '''

    def __init__(self, bot):
        self.bot = bot

    async def list_extend(self, list1, list2):
        list1.extend(list2)
        return list1

    @commands.command(aliases=['p'])
    @commands.guild_only()
    async def paranoia(self, ctx, member: discord.Member, *, category=None):
        async with ctx.typing():
            data = json.load(open('data\\questions\\paranoias.json', 'r'))
            if not category:
                default_category = json.load(open('data\\default_category.json', 'r'))
                if str(ctx.guild.id) in default_category:
                    category = default_category[str(ctx.guild.id)]
                else:
                    category = random.choice(['pg', 'pg13'])
            category = category.lower()

            data2 = json.load(open('data\\questions\\serverparanoias.json', 'r'))
            if str(ctx.guild.id) in data2:
                questions = data2[str(ctx.guild.id)][category]
            else:
                questions = []

        if category == 'add':
            await send_embed(ctx, f'Wrong command?', f'Did you mean to use the add command?'
                                                     f'\n({await get_server_prefix(self.bot, ctx)}add '
                                                     f'<truth | dare | wyr> <pg | pg13 | r> <question>)')
            return

        question_chosen = choice(await self.list_extend(questions, data[category]))
        question_chosen = question_chosen.replace('[random user]', f'{choose_random_member(ctx)}')
        if category in ['pg', 'pg13', 'r']:
            await ctx.message.add_reaction('<:check:867760636980756500>')

            embed = await send_embed(ctx, f'Paranoia ({category})', question_chosen, send=False)
            embed.set_footer(text=f'Reply to this message with your answer in this dm')
            dm_msg = await member.send(embed=embed)

            response = await self.bot.wait_for('message',
                                               check=lambda msg: msg.author == member and isinstance(msg.channel,
                                                                                                     discord.DMChannel))
            while not (response.reference and response.reference.message_id == dm_msg.id):
                response = await self.bot.wait_for('message',
                                                   check=lambda msg: msg.author == member and isinstance(msg.channel,
                                                                                                         discord.DMChannel))

            if response.reference.message_id == dm_msg.id:
                await response.add_reaction('<:check:867760636980756500>')
                reveal_embed = await send_embed(ctx, f'{member.display_name} responded',
                                                f'{response.content}', send=False, avatar_url=member.avatar_url)
                if random.randint(1, 100) >= 49:
                    reveal_embed.add_field(name='Coin landed on heads', value=question_chosen)
                    await dm_msg.edit(embed=embed.set_footer(text='Question revealed :)'))
                    await ctx.message.reply(embed=reveal_embed)
                else:
                    reveal_embed.add_field(name='Coin landed on tails', value=':(')
                    await dm_msg.edit(embed=embed.set_footer(text='Question kept secret :('))
                    msg = await ctx.message.reply(embed=reveal_embed)

                    data = json.load(open('data\\active_paranoia_questions.json', 'r'))
                    if str(ctx.channel.id) not in data:
                        data[str(ctx.channel.id)] = []
                    data[str(ctx.channel.id)].append([str(member.id), question_chosen, response.content, msg.jump_url])
                    json_data = json.dumps(data)
                    f = open('data\\active_paranoia_questions.json', 'w')
                    f.write(json_data)
                    f.close()

    @paranoia.error
    async def paranoia_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            await send_embed(ctx, 'Invalid usage', f'Use {await get_server_prefix(self.bot, ctx)}paranoia '
                                                   f'<member> <pg | pg13 | r>')
        else:
            await send_embed(ctx, 'Invalid usage', f'Use {await get_server_prefix(self.bot, ctx)}paranoia '
                                                   f'<member> <pg | pg13 | r>')


def setup(bot):
    bot.add_cog(Paranoia(bot))
