""" 
Extracts readability features for given text based on textstat package.
"""

import textstat


def get_flesch_reading_ease(text):
    return textstat.flesch_reading_ease(text)


def get_smog(text):
    return textstat.smog_index(text)


def get_flesch_kincaid_grade(text):
    return textstat.flesch_kincaid_grade(text)


def get_automated_readability_index(text):
    return textstat.automated_readability_index(text)


def get_coleman_liau_index(text):
    return textstat.coleman_liau_index(text)


def get_dale_chall_readability_score(text):
    return textstat.dale_chall_readability_score(text)


def get_difficult_words(text):
    return textstat.difficult_words(text)


def get_linsear_write_formula(text):
    return textstat.linsear_write_formula(text)


def get_gunning_fog(text):
    return textstat.gunning_fog(text)


def get_text_standard(text):
    return textstat.text_standard(text)


def get_fernandez_huerta(text):
    return textstat.fernandez_huerta(text)


def get_szigriszt_pazos(text):
    return textstat.szigriszt_pazos(text)


def get_gutierrez_polini(text):
    return textstat.gutierrez_polini(text)


def get_crawford(text):
    return textstat.crawford(text)
