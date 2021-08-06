import os

import discord
from discord.ext import commands

from data.default_prefix import PREFIX
from utils.get_server_prefix import get_server_prefix, get_server_prefix_list
from utils.send_embed import send_embed

intents = discord.Intents.all()
TOKEN = "ODY5MDQ2NjEwNzA4MDEzMDg5.YP4gug.NOi7IJD7aDYZXXJt6K-CFwKSKfg"
bot = commands.Bot(command_prefix=get_server_prefix_list, case_insensitive=True, intents=intents)
bot.remove_command('help')

for extension in os.listdir('cogs'):
    if extension.endswith('.py'):
        bot.load_extension('cogs.' + extension[:-3])

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            prefix = PREFIX
            embed = discord.Embed(
                description=f'Hey! I\'m **TruthOrDare**.\n\n'
                            f'To see what I can do, send `{prefix}help`. All my commands are run like this,'
                            f'with a `{prefix}` before the command (for example `{prefix}truth pg13`).\n\n',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='**My Links**',
                            value='[Invite]('
                                  'https://discord.com/api/oauth2/authorize?'
                                  'client_id=869046610708013089&permissions=8&scope=bot%20applications.commands'
                                  ') - Add this bot to one of your servers and have some fun!',inline=False)
            await channel.send(embed=embed)
        break

@bot.event
async def on_ready():
    count = 0
    for guild in bot.guilds:
        count += guild.member_count
    print(f'Connected to {len(bot.guilds)} guild(s) and serving {count} members')

@bot.event
async def on_message(message):
    if f'<@!{bot.user.id}>' in message.content:
        await send_embed(message, 'Hey! I\'m TruthOrDare.', f'Run `{await get_server_prefix(message, message.guild.id)}'
                                                         f'help` to see my commands.', bot.user.avatar_url)
    await bot.process_commands(message)

bot.run(TOKEN)