""""
segments lyrics into parts like Verse, Chorus, etc. based on annotations provided.
Requires lyrics to contain annotations, otherwise, None will be returned for features.
"""
import re
import sanitizer


def get_part_type(text):
    t = text.lower()
    if "verse" in t:
        return "Verse"
    elif "chorus" in t:
        return "Chorus"
    elif "intro" in t:
        return "Intro"
    elif "outro" in t:
        return "Outro"
    elif "bridge" in t:
        return "Bridge"
    elif "hook" in t:
        return "Hook"
    elif "refrain" in t:
        return "Chorus"
    elif "interlude" in t:
        return "Interlude"
    elif "drop" in t:
        return "Drop"

    return "Unknown"


def is_structure_annotation(text):
    return bool(re.search(r"(?i)\[.*Verse.*]", text)) or \
        bool(re.search(r"(?i)\[.*Chorus.*]", text)) or \
        bool(re.search(r"(?i)\[.*Intro.*]", text)) or \
        bool(re.search(r"(?i)\[.*Outro.*]", text)) or \
        bool(re.search(r"(?i)\[.*Bridge.*]", text)) or \
        bool(re.search(r"(?i)\[.*Hook.*]", text)) or \
        bool(re.search(r"(?i)\[.*Refrain.*]", text)) or \
        bool(re.search(r"(?i)\[.*Interlude.*]", text)) or \
        bool(re.search(r"(?i)\[.*Drop.*]", text))


def split_into_parts(text):
    # This function splits the given sanitized song lyrics into parts
    # representing the song structure. This information is coded in the lyrics
    # in the form of [Annotations].
    lines = text.split("\n")
    current_part = "Unknown"
    parts = []

    # Assign lines to parts.
    for line in lines:
        # Check if the current line is the beginning of a new block.
        if is_structure_annotation(line):
            # If it is a new part, add it with the current type annotation.
            part_type = get_part_type(line)
            parts.append((part_type, ""))
        # Handle the special case where the first line is not a structure annotation.
        elif len(parts) == 0:
            parts.append(("Unknown", line))
        else:
            # If not, we add the current line to the current part.
            parts[-1] = (parts[-1][0], parts[-1][1] + "\n" + line)

    # Clean parts.
    for i in range(0, len(parts)):
        parts[i] = (parts[i][0], parts[i][1].strip())

    return parts


def prepare_segmentation(text):
    sanitized_text = sanitizer.remove_superfluous_whitespace(text)
    sanitized_text = sanitizer.reduplicate_segment(sanitized_text)
    sanitized_text = sanitizer.remove_instrument_annotations(sanitized_text)
    sanitized_text = sanitizer.remove_superfluous_whitespace(sanitized_text)  # Yes, again.
    sanitized_text = sanitizer.remove_consecutive_newlines(sanitized_text)

    return sanitized_text

def get_parts(text):
    sanitized_text = prepare_segmentation(text)
    return split_into_parts(sanitized_text)