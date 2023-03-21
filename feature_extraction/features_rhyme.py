"""
Computes rhyme features for given lyrics, based on
"Rhyme and Style Features for Musical Genre Classification 
by Song Lyrics" by Mayer et al.
"""

import string
from collections import defaultdict

from nltk import word_tokenize
from pronouncing import rhymes, phones_for_word


def _do_rhyme(a, b):
        return a in rhymes(b) or a == b


def get_rhyme_features(text):
    res = {}

    # The features we consider are line-wise, so to check for rhymes, 
    # we need to look at the last word of every line.
    lines = text.split("\n") #ToDo: How do we handle paragraph breaks?
    
    line_tokens = [word_tokenize(l) for l in lines if l.strip() != ""]
    line_tokens = [list(filter(lambda t: t not in string.punctuation, l)) for l in line_tokens]

    # We will compute some general ryhme statistict that span several different types of rhymes.
    rhyming_line_indices = set()
    unique_rhyme_words = set()

    # Check if subsequent lines rhyme (i.e., couplets). 
    # For now, we ignore the meter requirement.
    num_couplets = 0
    for i, (first, second) in enumerate(zip(line_tokens[:-1], line_tokens[1:])):
        if _do_rhyme(second[-1], first[-1]):
            num_couplets += 1

            rhyming_line_indices.add(i)
            rhyming_line_indices.add(i + 1)

            unique_rhyme_words.add(first[-1])
            unique_rhyme_words.add(second[-1])

    res["num_couplets"] = num_couplets

    # Check for patterns involving sequences of four lines. These are:
    #   * subsequent pairs of rhyming lines (i.e., clerihews),
    #   * alternating rhymes, and
    #   * nested rhymes.
    num_clerihews = 0
    num_alternating = 0
    num_nested = 0
    for i, (first, second, third, fourth) in enumerate(zip(line_tokens[:-3], line_tokens[1:-2], line_tokens[2:-1], line_tokens[3:])):
        if _do_rhyme(second[-1], first[-1]) and _do_rhyme(fourth[-1], third[-1]):
            num_clerihews += 1

            rhyming_line_indices.add(i)
            rhyming_line_indices.add(i + 1)
            rhyming_line_indices.add(i + 2)
            rhyming_line_indices.add(i + 3)

            unique_rhyme_words.add(first[-1])
            unique_rhyme_words.add(second[-1])
            unique_rhyme_words.add(third[-1])
            unique_rhyme_words.add(fourth[-1])

        if _do_rhyme(third[-1], first[-1]) and _do_rhyme(fourth[-1], second[-1]):
            num_alternating += 1

            rhyming_line_indices.add(i)
            rhyming_line_indices.add(i + 1)
            rhyming_line_indices.add(i + 2)
            rhyming_line_indices.add(i + 3)

            unique_rhyme_words.add(first[-1])
            unique_rhyme_words.add(second[-1])
            unique_rhyme_words.add(third[-1])
            unique_rhyme_words.add(fourth[-1])

        if _do_rhyme(fourth[-1], first[-1]) and _do_rhyme(third[-1], second[-1]):
            num_nested += 1

            rhyming_line_indices.add(i)
            rhyming_line_indices.add(i + 1)
            rhyming_line_indices.add(i + 2)
            rhyming_line_indices.add(i + 3)

            unique_rhyme_words.add(first[-1])
            unique_rhyme_words.add(second[-1])
            unique_rhyme_words.add(third[-1])
            unique_rhyme_words.add(fourth[-1])

    res["num_clerihews"] = num_clerihews
    res["num_alternating"] = num_alternating
    res["num_nested"] = num_nested

    # Check for alliterations.
    num_alliterations = defaultdict(int)
    for tokens in line_tokens:
        i = 0
        while i < len(tokens):
            token = tokens[i]
            token_initial_phones = set([p.split(" ")[0] for p in phones_for_word(token)])

            # Check if there is an alliteration starting 
            # from the current token.
            seq_length = 1
            for j in range(i + 1, len(tokens)):
                next_token = tokens[j]
                next_token_initial_phones = set([p.split(" ")[0] for p in phones_for_word(next_token)])

                if len(token_initial_phones.intersection(next_token_initial_phones)) == 0:
                    break

                seq_length += 1

            if seq_length > 1:
                num_alliterations[seq_length] += 1

            i += seq_length

    res["alliterations_len_2"] = num_alliterations[2]
    res["alliterations_len_3"] = num_alliterations[3]
    res["alliterations_len_4_plus"] = sum(num_alliterations.values()) - num_alliterations[2] - num_alliterations[3]

    # Compute general features.
    res["rhyme_percent"] = len(rhyming_line_indices) / len(line_tokens) # Percentage of rhyming lines.
    res["unique_rhyme_words"] = len(unique_rhyme_words) # Number of unique rhyme words.

    return res