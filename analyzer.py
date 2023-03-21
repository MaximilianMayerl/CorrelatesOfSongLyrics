import re
from collections import Counter


def check_patterns(lyrics, field="lyrics"):
    count_decorations = 0
    count_annotations = 0
    for current_song in lyrics:
        current_lyrics = current_song[field]
        decoration_pattern = re.compile(r"\[.*\]")
        if decoration_pattern.search(current_lyrics):
            count_decorations += 1
        if any(annotation in current_lyrics.lower() for annotation in
               ['solo', 'verse', 'intro', 'chorus', 'refrain', 'outro', 'bridge', 'interlude', 'pre-chorus',
                'end chorus', 'end refrain']):
            count_annotations += 1

    print(f'Lyrics w/ decoration: {count_decorations}')
    print(f'Lyrics w/ annotations: {count_annotations}')


def extract_annotations(lyrics, field="lyrics"):
    # Get all lyrics that contain annotations.
    lyrics_with_annotations = [l for l in lyrics if re.match(r"\[[^\]]*\]", l[field])]

    # Extract the specific annotations used.
    annotations = []
    for lyric in lyrics:
        annotations.extend(re.findall(r"\[[^\]]*\]", lyric[field]))

    annotations_counts = Counter(annotations)

    # Output statistics.
    print(
        f"Lyrics with annotations: {len(lyrics_with_annotations)} ({100 * len(lyrics_with_annotations) / len(lyrics)}%)")
    print("100 most common annotations:")
    for k, v in annotations_counts.most_common(100):
        print(f"{k}: {v}")
