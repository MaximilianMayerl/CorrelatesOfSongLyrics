"""
Computes structural features for given lyrics, based on
"Emotionally-Relevant Features for Classification
and Regression of Music Lyrics" by Malheiro et al.
"""
from functools import lru_cache
import re
from . import segment_lyrics

@lru_cache
def contains_annotations(text: str):
    """checks whether lyrics contain annotations (boolean)"""
    decoration_pattern = re.compile(r"\[.*]")
    return decoration_pattern.search(text)

@lru_cache
def get_song_structure(text: str):
    """ returns the structure of a song (verses, chorus, etc.) as list of pairs """
    # only return structure, no need to return the actual contents
    return [segment[0] for segment in segment_lyrics.get_parts(text)]


def get_number_of_choruses(text):
    """ #CH, which stands for the number of times the chorus is repeated in the lyric """
    if contains_annotations(text):
        return get_song_structure(text).count('Chorus')
    else:
        return -1

def get_title_occurrences(text, title):
    """#Title, which is the number of times the title appears in the lyric"""
    return text.lower().count(title.lower())

def get_number_of_verses(text):
    """ #V (number of verses) """
    if contains_annotations(text):
        return get_song_structure(text).count('Verse')
    else:
        return -1

def get_number_of_total_sections(text):
    """ #VorC (total of sections – verses and chorus – in the lyrics)
        note that our segmentation provides more than verse and chorus segments"""
    if contains_annotations(text):
        structure = get_song_structure(text)
        return structure.count('Verse') + structure.count('Chorus')
    else:
        return -1

def get_starts_with_chorus(text):
    """C... (the lyric starts with chorus – boolean)"""
    if contains_annotations(text):
        return int(get_song_structure(text)[0] == 'Chorus')
    else:
        return -1

def get_relation_verses_sections(text):
   """# V/Total (relation between Vs and the total of sections) """
   if contains_annotations(text):
       return get_number_of_verses(text) / get_number_of_total_sections(text)
   else:
       return -1

def get_relation_chorus_sections(text):
    """# C/Total (relation between C and the total of sections) """
    if contains_annotations(text):
        return get_number_of_choruses(text) / get_number_of_total_sections(text)
    else:
        return -1

def get_ends_with_two_chorus_repetitions(text):
    """more than two chorus repetitions at the end? (boolean)"""
    if contains_annotations(text):
        return int(get_song_structure(text)[:-1] == 'Chorus' and get_song_structure(text)[:-2] == 'Chorus')
    else:
        return -1

def get_verse_chorus_alternating(text):
    """alternation between verses and chorus; e.g., VCVC. """
    if contains_annotations(text):
        structure = get_song_structure(text)
        for i in range(0,len(structure)):
            if i % 2 == 0 and structure[i] != 'Verse':
                return 0
            if i % 2 == 1 and structure[i] != 'Chorus':
                return 0
        return 1
    else:
        return -1

def get_two_verses_at_least_one_chorus(text):
    """alternation between verse and chorus;  e.g., VCCVCC (between 2 verses we
    have at least 1 chorus) """
    if contains_annotations(text):
        structure = get_song_structure(text)
        # get indices of verses
        verse_indices = [i for i, value in enumerate(structure) if value == "Verse"]

        # for each pair of verses
        for i in range(0, len(verse_indices)-1):
            # if we only have one verse, pattern is fulfilled
            if len(verse_indices) == 1:
                break
            # for pairs of verses, search for chorus in between
            # if it is not contained, the pattern is not fulfilled
            if not 'Chorus' in structure[verse_indices[i]: verse_indices[i+1]]:
                return 0
        # we cannot find any violation of the pattern, return True
        return 1

    else:
        return -1

def get_two_choruses_at_least_one_verse(text):
    """alternation between verse and chorus; e.g., VVCVC (between 2 chorus we have at least 1 verse)."""
    if contains_annotations(text):
        structure = get_song_structure(text)
        # get indices of choruses
        chorus_indices = [i for i, value in enumerate(structure) if value == "Chorus"]
        # for each pair of verses
        for i in range(0, len(chorus_indices) - 1):
            # if we only have one chorus, pattern is fulfilled
            if len(chorus_indices) == 1:
                break
            # for pairs of choruses, search for verse in between
            # if it is not contained, the pattern is not fulfilled
            if not 'Chorus' in structure[chorus_indices[i]: chorus_indices[i + 1]]:
                return 0
        # we cannot find any violation of the pattern, return True
        return 1

    else:
        return -1

