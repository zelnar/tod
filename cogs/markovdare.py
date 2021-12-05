import json
import random as rm

import numpy as np
from discord.ext import commands
from numpy.random import choice
from scipy.sparse import dok_matrix

from utils.send_embed import send_embed


class MarkovDare(commands.Cog):
    '''
    Tests
    Usage:
    `<prefix> markovdare [pg | pg13 | r]` (If category not specified, I choose a pg or pg13 question.)
    '''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['md', 'markovdare'])
    @commands.guild_only()
    async def markov_dare(self, ctx, *, category=None):
        k = 2
        data = json.load(open('data\\questions\\dares.json', 'r'))
        if not category:
            default_category = json.load(open('data\\default_category.json', 'r'))
            if str(ctx.guild.id) in default_category:
                category = default_category[str(ctx.guild.id)]
            else:
                category = 'pg'
        category = category.lower()

        questions = data[category]
        distinct_words = set()
        sets_of_k_words = []

        for i, question in enumerate(questions):
            for spaced in ['.', '?', '(', ')', ',']:
                question = question.replace(spaced, ' {0} '.format(spaced))
            questions[i] = [x for x in question.strip().split() if x != '']
            for word in questions[i]:
                distinct_words.add(word)

            wordset = questions[i]
            if len(wordset) >= k:
                for i in range(len(wordset[:-k]) + 1):
                    sets_of_k_words.append(' '.join(wordset[i:i + k]))

        distinct_words = list(distinct_words)
        word_idx_dict = {word: i for i, word in enumerate(distinct_words)}

        k_minus_one_keys = list(set([' '.join(word.split()[:-1]) for word in list(set(sets_of_k_words))]))
        sets_count = len(k_minus_one_keys)
        next_after_k_words_matrix = dok_matrix((sets_count, len(distinct_words)))

        distinct_sets_of_k_words = list(set(sets_of_k_words))
        k_words_idx_dict = {word: i for i, word in enumerate(k_minus_one_keys)}

        for phrase in distinct_sets_of_k_words:
            word_sequence_idx = k_words_idx_dict[' '.join(phrase.split()[:-1])]
            next_word_idx = word_idx_dict[phrase.split()[-1]]
            next_after_k_words_matrix[word_sequence_idx, next_word_idx] += 1

        async def weighted_choice(objects, weights):
            weights = np.array(weights, dtype=np.float64)
            sum_of_weights = weights.sum()
            np.multiply(weights, 1 / sum_of_weights, weights)
            weights = weights.cumsum()
            x = rm.random()
            for i in range(len(weights)):
                if x < weights[i]:
                    return objects[i]

        async def sample_next_word_after_sequence(word_sequence, alpha=0):
            next_word_vector = next_after_k_words_matrix[k_words_idx_dict[word_sequence]] + alpha
            likelihoods = next_word_vector / next_word_vector.sum()
            return await weighted_choice(distinct_words, likelihoods.toarray())

        async def stochastic_chain(seed, seed_length=k - 1):
            current_words = seed.split(' ')
            if len(current_words) != seed_length:
                raise ValueError(f'wrong number of words, expected {seed_length}')
            sentence = seed
            while True:
                if sentence.endswith('?') or sentence.endswith('.'):
                    return sentence.replace(' ?', '?').replace(' .', '.').replace(' ,', ',').replace('( ', '(').replace(
                        ' )', ')')
                sentence += ' '
                next_word = await sample_next_word_after_sequence(' '.join(current_words))
                sentence += next_word
                current_words = current_words[1:] + [next_word]

        starters = []
        for q in questions:
            if len(q) >= k - 1:
                starters.append(' '.join(q[:k - 1]))
        await send_embed(ctx, 'Generated dare question', await stochastic_chain(choice(starters)))


#

def setup(bot):
    bot.add_cog(MarkovDare(bot))
