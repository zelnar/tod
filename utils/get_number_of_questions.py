import json


async def get_category_questions(guild_id, category):
    count = 0
    data = json.load(open(f'data\\questions\\{category}s.json', 'r'))
    for c in data:
        count += len(data[c])
    data = json.load(open(f'data\\questions\\server{category}s.json', 'r'))
    if guild_id in data:
        for c in data[guild_id]:
            count += len(data[guild_id][c])
    return count


async def get_number_of_questions(guild_id=None, category=None):
    if category == 'truth' or category == 't':
        count = await get_category_questions(guild_id, 'truth')
    elif category == 'dare' or category == 'd':
        count = await get_category_questions(guild_id, 'dare')
    elif category == 'wyr':
        count = await get_category_questions(guild_id, 'wyr')
    elif category == 'paranoia' or category == 'p':
        count = await get_category_questions(guild_id, 'paranoia')
    else:
        count = 0
        count += await get_category_questions(guild_id, 'truth')
        count += await get_category_questions(guild_id, 'dare')
        count += await get_category_questions(guild_id, 'wyr')
        count += await get_category_questions(guild_id, 'paranoia')
    return count
