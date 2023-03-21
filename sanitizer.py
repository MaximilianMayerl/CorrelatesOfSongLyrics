import re


# https://dbis-owncloud.uibk.ac.at/index.php/apps/files/?dir=/dbis-theses-msc/171002_Stefan_Wurzinger/source/musicanalysis/src/main/java/musicanalysis/model/music/lyric&openfile=1577008

def remove_superfluous_whitespace(text):
    sanitized_text = text.strip()  # Remove leading and trailing whitespace
    sanitized_text = re.sub(r"\r?\n", "\n", sanitized_text)  # Fix line breaks
    sanitized_text = re.sub(r"(?m)^[^\S\n]+", "", sanitized_text)  # delete leading spaces in every line
    sanitized_text = re.sub(r"(?m)[^\S\n]+$", "", sanitized_text)  # delete trailing spaces in every line
    sanitized_text = re.sub(r"[^\S\n]+", " ", sanitized_text)  # delete consecutive spaces (excluding new lines)

    return sanitized_text


def reduplicate_segment(text):
    # This function deals with annotations of the form [x2] or [2x].
    # There are different forms of these multipliers in our data.
    # On form is the multiplier directly following a line, like
    #    lorem ipsum dolor [2x]
    # In this case, we interpret the multiplier to apply to the line it
    # follows, turnin this into
    #    lorem ipsum dolor
    #    lorem ipsum dolor
    #
    # The second form has the multiplier predecing a paragraph,
    # like in
    #    Lorem ipsum dolor sit amet
    #    consectetur adipiscing elit
    #    Pellentesque in aliquam tellus
    #
    #    [x2]
    #    Vivamus congue eros et sapien sollicitudin
    #    ut pretium erat condimentum
    #    Interdum et malesuada fames ac ante ipsum
    # In this case, we apply the multiplier to the whole paragraph,
    # turning this into
    #    Lorem ipsum dolor sit amet
    #    consectetur adipiscing elit
    #    Pellentesque in aliquam tellus
    #
    #    Vivamus congue eros et sapien sollicitudin
    #    ut pretium erat condimentum
    #    Interdum et malesuada fames ac ante ipsum
    #
    #    Vivamus congue eros et sapien sollicitudin
    #    ut pretium erat condimentum
    #    Interdum et malesuada fames ac ante ipsum
    #
    # The third form has the mulitplier following a paragraph
    # on an empty line, like
    #    Lorem ipsum dolor sit amet
    #    consectetur adipiscing elit
    #    Pellentesque in aliquam tellus
    #
    #    Vivamus congue eros et sapien sollicitudin
    #    ut pretium erat condimentum
    #    Interdum et malesuada fames ac ante ipsum
    #    [x2]
    # We handle this in the same way as the second form.
    #
    # There are some instances were multipliers are unspecified,
    # i.e., they are given as [?x] or [x?]. We don't handle those
    # for now.
    # ToDo: Are there any other cases?

    # Step 1: Handle lines that have to be duplicated.
    sanitized_text = ""
    lines = text.split("\n")
    for line in lines:
        if match := re.match(r"(?P<text>[^\[\n]+)\[x(?P<number>[0-9]+)\]", line):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n") * number
        elif match := re.match(r"(?P<text>[^\[\n]+)\[(?P<number>[0-9]+)x\]", line):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n") * number
        else:
            sanitized_text += line + "\n"

    # Step 2: Handle paragraphs that have to be duplicated.
    paragraphs = sanitized_text.split("\n\n")
    sanitized_text = ""
    for paragraph in paragraphs:
        if match := re.match(r"(?s)^\[(?P<number>[0-9]+)x\]\n(?P<text>.*)", paragraph):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n\n") * number
        elif match := re.match(r"(?s)^\[x(?P<number>[0-9]+)\]\n(?P<text>.*)", paragraph):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n\n") * number
        elif match := re.match(r"(?s)(?P<text>.*)\[(?P<number>[0-9]+)x\]$", paragraph):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n\n") * number
        elif match := re.match(r"(?s)(?P<text>.*)\[x(?P<number>[0-9]+)\]$", paragraph):
            text = match.group("text")
            number = int(match.group("number"))
            sanitized_text += (text + "\n\n") * number
        else:
            sanitized_text += paragraph + "\n\n"

    return sanitized_text


def remove_song_structure_annotations(text):
    sanitized_text = re.sub(r"(?i)\[.*Verse.*\]", "", text)
    sanitized_text = re.sub(r"(?i)\[.*Chorus.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Intro.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Outro.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Bridge.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Hook.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Refrain.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Interlude.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Drop.*\]", "", sanitized_text)

    return sanitized_text


def remove_instrument_annotations(text):
    sanitized_text = re.sub(r"(?i)\[.*Guitar Solo.*\]", "", text)
    sanitized_text = re.sub(r"(?i)\[.*Instrumental.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Solo.*\]", "", sanitized_text)
    sanitized_text = re.sub(r"(?i)\[.*Spoken.*\]", "", sanitized_text)

    return sanitized_text


def remove_consecutive_newlines(text):
    sanitized_text = re.sub(r"\n{2,}", "\n\n", text)
    return sanitized_text


def remove_remaining_annotations(text):
    sanitized_text = re.sub(r"\[[^\]]*\]", "", text)
    return sanitized_text


def sanitize_lyric(text, remove_all=False):
    sanitized_text = remove_superfluous_whitespace(text)
    sanitized_text = reduplicate_segment(sanitized_text)
    sanitized_text = remove_instrument_annotations(sanitized_text)
    sanitized_text = remove_song_structure_annotations(sanitized_text)

    if remove_all:
        sanitized_text = remove_remaining_annotations(sanitized_text)

    sanitized_text = remove_superfluous_whitespace(sanitized_text)  # Yes, again.
    sanitized_text = remove_consecutive_newlines(sanitized_text)

    return sanitized_text
