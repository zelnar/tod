import json

import discord

from data.default_prefix import PREFIX


async def mixed_case(*args):
    total = []
    import itertools
    for string in args:
        a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in string)))
        for x in list(a): total.append(x)
    return list(total)

async def get_server_prefix(bot, message) -> str:
    data = json.load(open('data\\prefixes.json', 'r'))
    if str(message.guild.id) in data:
        return data[str(message.guild.id)]
    else:
        return PREFIX


async def get_server_prefix_list(bot, message) -> list[str]:
    if isinstance(message.channel, discord.DMChannel):
        return await mixed_case(PREFIX)
    data = json.load(open('data\\prefixes.json', 'r'))
    if str(message.guild.id) in data:
        return await mixed_case(data[str(message.guild.id)])
    else:
        return await mixed_case(PREFIX)
