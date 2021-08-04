from random import choice

def choose_random_member(ctx, bots=False):
    guild_members = ctx.channel.guild.members
    member = choice(guild_members)
    if not bots:
        while member.bot:
            member = choice(guild_members)
    return member