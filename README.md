# Correlates of Song Lyrics

This repository holds the code used for _Correlates of Song Lyrics_, our project for analyzing lyrical evolution with respect to sentiment, topic, and complexity of lyrics. The data used for this is based on the LFM-2b dataset, with lyrics crawled from genius.com.

## Feature Extraction

The directory `feature_extraction` holds the code we used to extract features from the lyrics crawled from genius.com. It can be used as a Python module and exposes a function `extract_and_add_features(song)` to extract the features for a given song.

For full feature extraction, put `wiktionary_english.json` into `./data`.

## Analysis

The analysis described in our paper can be found in the files `lyrics_analyse_full_feature_importance.ipynb` and `STATS_5_Genres.Rmd`. `lyrics_analyse_full_feature_importance.ipynb` contains the code for _Experiment 1_ described in the paper, while `STATS_5_Genres.Rmd` contains the code for _Experiment 2_.