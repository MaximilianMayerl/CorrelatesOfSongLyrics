""" 
Computes lexical features for given lyrics.
"""

from collections import Counter
from functools import lru_cache

from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.util import ngrams
from lexical_diversity import lex_div as ld
from lexicalrichness import LexicalRichness


@lru_cache
def get_tokens(text):
    return word_tokenize(text)


@lru_cache
def get_lexical_richness_object(text):
    return LexicalRichness(text)


@lru_cache
def get_pos_tags(text):
    return pos_tag(get_tokens(text))


def get_token_count(text):
    return len(get_tokens(text))


def get_character_count(text):
    return len(text)


def get_repeated_token_ratio(text):
    return 1 - get_legomenon_ratio(text, 1)


def get_unique_tokens_per_line(text):
    tokens = get_tokens(text)
    unique_tokens = len(list(set(tokens)))
    
    return unique_tokens / get_line_count(text)


def get_average_token_length(text):
    tokens = get_tokens(text)
    return sum(len(word) for word in tokens) / len(tokens)


def get_average_tokens_per_line(text):
    return get_token_count(text) / get_line_count(text)


def get_line_count(text):
    return text.count('\n') + 1


def get_unique_line_count(text):
    lines = text.split('\n')
    return len(list(set(lines)))


def get_blank_line_count(text):
    return text.count('\n\n')


def get_blank_line_ratio(text):
    return get_blank_line_count(text) / get_line_count(text)


def get_repeated_line_ratio(text):
    lines = text.split('\n')
    repeated_lines = filter(lambda elem: elem[1] > 1, Counter(lines).items())

    return len(dict(repeated_lines))/len(lines)


def get_exclamation_mark_count(text):
    return text.count('!')


def get_question_mark_count(text):
    return text.count('?')


def get_digit_count(text):
    return len([character for character in text if character.isdigit()])


def get_colon_count(text):
    return text.count(':')


def get_semicolon_count(text):
    return text.count(';')


def get_quote_count(text):
    return text.count('"')


def get_comma_count(text):
    return text.count(',')


def get_dot_count(text):
    return text.count('.')


def get_hyphen_count(text):
    return text.count('-')


def get_parens_count(text):
    return text.count('(') + text.count(')')


def get_punctuation_count(text):
    return get_exclamation_mark_count(text) + \
        get_question_mark_count(text) + \
        get_colon_count(text) + \
        get_semicolon_count(text) + \
        get_quote_count(text) + \
        get_comma_count(text) + \
        get_dot_count(text) + \
        get_hyphen_count(text) + \
        get_parens_count(text)


def get_digit_ratio(text):
    return get_digit_count(text) / get_character_count(text)


def get_punctuation_ratio(text):
    return get_punctuation_count(text) / get_character_count(text)


def get_stop_word_count(text):
    tokens = get_tokens(text)
    stop_words = set(stopwords.words('english'))

    return len([token for token in tokens if token.lower() in stop_words])


def get_stop_word_ratio(text):
    return get_stop_word_count(text) / get_token_count(text)


def get_stop_words_per_line(text):
    return get_stop_word_count(text) / get_line_count(text)


def get_unique_bigram_ratio(text):
    bigrams = list(ngrams(text.split(), 2))
    unique_bigrams = set(bigrams)

    return len(unique_bigrams) / len(bigrams)
    

def get_unique_trigram_ratio(text):
    trigrams = list(ngrams(text.split(), 3))
    unique_trigrams = set(trigrams)

    return len(unique_trigrams) / len(trigrams)


def get_legomenon_ratio(text, n):
    tokens = get_tokens(text)
    counter = Counter(tokens)

    return len([i for i in counter.items() if i[1] == n]) / len(counter)


def get_mtld(text):
    tokens = get_tokens(text)
    return ld.mtld(tokens)


def get_herdan(text):
    richness = get_lexical_richness_object(text)
    return richness.Herdan


def get_summer(text):
    richness = get_lexical_richness_object(text)
    return richness.Summer


def get_dugast(text):
    richness = get_lexical_richness_object(text)
    return richness.Dugast


def get_maas(text):
    richness = get_lexical_richness_object(text)
    return richness.Maas


def get_pronoun_frequency(text):
    tags = get_pos_tags(text)

    # We define pronoun frequency as the ratio
    # of personal/possessive pronouns among all tokens.
    return len([t for t in tags if t[1] in ("PRP", "PRP$")]) / len(tags)


def get_past_tense_ratio(text):
    tags = get_pos_tags(text)

    # We define the past tense ratio as the ratio
    # of verbs in past tense among all verbs.
    all_verbs = [t for t in tags if t[1].startswith("V")]
    past_verbs = [t for t in tags if t[1] in ("VBD", "VBN")]

    if len(all_verbs) == 0:
        return 0.0
        
    return len(past_verbs) / len(all_verbs)

def get_adjective_frequency(text):
    tags = get_pos_tags(text)
    return len([t for t in tags if t[1].startswith("JJ")]) / len(tags)

def get_adverb_frequency(text):
    tags = get_pos_tags(text)
    return len([t for t in tags if t[1].startswith("RB")]) / len(tags)

def get_noun_frequency(text):
    tags = get_pos_tags(text)
    return len([t for t in tags if t[1].startswith("N")]) / len(tags)

def get_verb_frequency(text):
    tags = get_pos_tags(text)
    return len([t for t in tags if t[1].startswith("V")]) / len(tags)
