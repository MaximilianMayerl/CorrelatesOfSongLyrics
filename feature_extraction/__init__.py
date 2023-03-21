"""
Extracts lyrics features (readability, lexical, linguistic, complexity, song structure, etc.).
"""

from . import features_compression as fcomp
from . import features_lexical as flex
from . import features_readability as fread
from . import features_linguistic as fling
from . import features_structure as fstruct
from . import features_rhyme as frhyme


def extract_and_add_features(song):
    """
    Extracts features for the given song and adds the feature values to the song object.

    Returns True if feature extract for the given song was successfull, and False otherwise.

    Parameters
    ----------
    song : dict
        The song objects, as a dictionary.

    Returns
    -------
    bool
        True is the feature extraction was successfull, False otherwise.
    """
    lyrics = song['sanitized_lyrics']
    features = {}

    # Skip songs that do not have sufficient lyrics for computing our features.
    if lyrics.count(" ") < 2:
        return False

    try:
        # Compute compression features
        features['compression_ratio'] = fcomp.get_compression_ratio(lyrics)

        # Compute readability features
        features['readability_flesch_kincaid_grade'] = fread.get_flesch_kincaid_grade(lyrics)
        features['readability_flesch_reading_ease'] = fread.get_flesch_reading_ease(lyrics)
        features['readability_smog'] = fread.get_smog(lyrics)
        features['readability_automated_readability_index'] = fread.get_automated_readability_index(lyrics)
        features['readability_coleman_liau_index'] = fread.get_coleman_liau_index(lyrics)
        features['readability_dale_chall_readability_score'] = fread.get_dale_chall_readability_score(lyrics)
        features['readability_difficult_words'] = fread.get_difficult_words(lyrics)
        features['readability_linsear_write_formula'] = fread.get_linsear_write_formula(lyrics)
        features['readability_gunning_fog'] = fread.get_gunning_fog(lyrics)
        features['readability_fernandez_huerta'] = fread.get_fernandez_huerta(lyrics)
        features['readability_szigriszt_pazos'] = fread.get_szigriszt_pazos(lyrics)
        features['readability_gutierrez_polini'] = fread.get_gutierrez_polini(lyrics)
        features['readability_crawford'] = fread.get_crawford(lyrics)

        # Compute lexical features
        features['token_count'] = flex.get_token_count(lyrics)
        features['character_count'] = flex.get_character_count(lyrics)
        features['repeated_token_ratio'] = flex.get_repeated_token_ratio(lyrics)
        features['unique_tokens_per_line'] = flex.get_unique_tokens_per_line(lyrics)
        features['average_token_length'] = flex.get_average_token_length(lyrics)
        features['average_tokens_per_line'] = flex.get_average_tokens_per_line(lyrics)
        features['line_count'] = flex.get_line_count(lyrics)
        features['unique_line_count'] = flex.get_unique_line_count(lyrics)
        features['blank_line_count'] = flex.get_blank_line_count(lyrics)
        features['blank_line_ratio'] = flex.get_blank_line_ratio(lyrics)
        features['repeated_line_ratio'] = flex.get_repeated_line_ratio(lyrics)
        features['exclamation_mark_count'] = flex.get_exclamation_mark_count(lyrics)
        features['question_mark_count'] = flex.get_question_mark_count(lyrics)
        features['digit_count'] = flex.get_digit_count(lyrics)
        features['colon_count'] = flex.get_colon_count(lyrics)
        features['semicolon_count'] = flex.get_semicolon_count(lyrics)
        features['quote_count'] = flex.get_quote_count(lyrics)
        features['comma_count'] = flex.get_comma_count(lyrics)
        features['dot_count'] = flex.get_dot_count(lyrics)
        features['hyphen_count'] = flex.get_hyphen_count(lyrics)
        features['parens_count'] = flex.get_parens_count(lyrics)
        features['punctuation_count'] = flex.get_punctuation_count(lyrics)
        features['digit_ratio'] = flex.get_digit_ratio(lyrics)
        features['punctuation_ratio'] = flex.get_punctuation_ratio(lyrics)
        features['stop_word_count'] = flex.get_stop_word_count(lyrics)
        features['stop_word_ratio'] = flex.get_stop_word_ratio(lyrics)
        features['stop_words_per_line'] = flex.get_stop_words_per_line(lyrics)
        features['unique_bigram_ratio'] = flex.get_unique_bigram_ratio(lyrics)
        features['unique_trigram_ratio'] = flex.get_unique_trigram_ratio(lyrics)
        features['hapax_legomenon_ratio'] = flex.get_legomenon_ratio(lyrics, n=1)
        features['dis_legomenon_ratio'] = flex.get_legomenon_ratio(lyrics, n=2)
        features['tris_legomenon_ratio'] = flex.get_legomenon_ratio(lyrics, n=3)
        features['mtld'] = flex.get_mtld(lyrics)
        features['herdan'] = flex.get_herdan(lyrics)
        features['summer'] = flex.get_summer(lyrics)
        features['dugast'] = flex.get_dugast(lyrics)
        features['maas'] = flex.get_maas(lyrics)
        features['pronoun_frequency'] = flex.get_pronoun_frequency(lyrics)
        features['past_tense_ratio'] = flex.get_past_tense_ratio(lyrics)
        features['adjective_frequency'] = flex.get_adjective_frequency(lyrics)
        features['adverb_frequency'] = flex.get_adverb_frequency(lyrics)
        features['noun_frequency'] = flex.get_noun_frequency(lyrics)
        features['verb_frequency'] = flex.get_verb_frequency(lyrics)

        # Compute linguistic features.
        features['uncommon_words_ratio'] = fling.get_uncommon_words_ratio(lyrics)

        # Compute structural features.
        features['title_occurences'] = fstruct.get_title_occurrences(song['lyrics'], song['_id']['track'])
        features['number_of_sections'] = fstruct.get_number_of_total_sections(song['lyrics'])
        features['number_of_verses'] = fstruct.get_number_of_verses(song['lyrics'])
        features['starts_with_chorus'] = fstruct.get_starts_with_chorus(song['lyrics'])
        features['relation_verses_sections'] = fstruct.get_relation_verses_sections(song['lyrics'])
        features['relation_chorus_sections'] = fstruct.get_relation_chorus_sections(song['lyrics'])
        features['ends_with_two_chorus_repetitions'] = fstruct.get_ends_with_two_chorus_repetitions(song['lyrics'])
        features['pattern_verse_chorus_alternating'] = fstruct.get_verse_chorus_alternating(song['lyrics'])
        features['pattern_two_verses_at_least_one_chorus'] = fstruct.get_two_verses_at_least_one_chorus(song['lyrics'])
        features['pattern_two_choruses_at_least_one_verse'] = fstruct.get_two_choruses_at_least_one_verse(
            song['lyrics'])

        # Compute rhyme features.
        features |= frhyme.get_rhyme_features(lyrics)
    except Exception as e:
        # print(f'{type(e)=} --- {e}')
        return False

    song['features'] = features
    return True
