import argparse
import json
import pickle
from tqdm import tqdm

from . import extract_and_add_features

def main():
    # Read data
    lyrics = pickle.load(open(args.lyrics_pickle, "rb"))[:1000]

    # Extract features for all songs
    for current_song in tqdm(lyrics, desc="Feature extraction"):
        extract_and_add_features(current_song)

    # Write data.
    pickle.dump(lyrics, open(args.output_path, "wb"))


if __name__ == "__main__":
    # Parse command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--lyrics-pickle", dest="lyrics_pickle", required=True, help="Pickle file containing lyrics.")
    parser.add_argument("--output-path", dest="output_path", required=True, help="The file to which the computed features should be written.")
    args = parser.parse_args()

    # Run main.
    main()
