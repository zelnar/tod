import asyncio

from discord.ext import commands

bot = commands.Bot(description="test", command_prefix="td ", self_bot=True)
bot.remove_command("help")

TOKEN = "NDYxMzQ1MTczMzE0NzMyMDUy.YI8Vpw.48mTLuhksdZbUlH8W4Q_6jEeGPw"  # me


@bot.event
async def on_ready():
    print("Ready!")


@bot.command()
async def t(ctx):
    while True:
        await ctx.send('-truth')
        await asyncio.sleep(0.5)


bot.run(TOKEN, bot=False)
