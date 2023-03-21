""" 
Computes linguistic features for given lyrics.
"""

import json
from functools import cache

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Initialize.
lemmatizer = WordNetLemmatizer()

# Initialize.
lemmatizer = WordNetLemmatizer()

wordnet_words = set([".", ",", "(", ")", "-"])
with open("./data/wiktionary_english.json", encoding="utf-8") as f:
    for line in f:
        word = json.loads(line)
        wordnet_words.add(word["word"])


@cache
def is_uncommon(token):
    return lemmatizer.lemmatize(token) not in wordnet_words


def get_uncommon_words_ratio(text):
    tokens = word_tokenize(text)
    uncommon_count = 0
    for token in tokens:
        if is_uncommon(token):
            uncommon_count += 1

    return uncommon_count / len(tokens)
