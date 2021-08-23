import json
import random


def get_embed_color(user_id, hex_code=False):
    data = json.load(open('data\\colors.json', 'r'))
    if str(user_id) in data:
        if not hex_code:
            if data[str(user_id)] == 'random':
                r = lambda: random.randint(0, 255)
                sixteenIntegerHex = int('%02X%02X%02X' % (r(), r(), r()), 16)
            else:
                sixteenIntegerHex = int(data[str(user_id)].replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)
            return readableHex
        else:
            return data[str(user_id)]
    else:
        if not hex_code:
            return 0xffffff  # white color
        else:
            return '#FFFFFF'
