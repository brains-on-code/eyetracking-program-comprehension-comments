import _pickle as pickle
import os

from scripts.preprocessing.DataFramesCollector import DataFramesCollector
from scripts.preprocessing.GazeDataCleaner import GazeDataCleaner
from scripts.preprocessing.GazeDataClassifier import GazeDataClassifier
from scripts.preprocessing.GazeDataPreprocessing import GazeDataPreprocessing
import config


def preprocess_raw_data():
    print('\n--> Reading data...')
    gaze_frames = DataFramesCollector.load_gazeframes(config.PATH_DATA_RAW)

    print('\n-> Cleaning data...')
    gaze_frames_cleaned = GazeDataCleaner.clean_gaze_data_frames(gaze_frames)

    print('\n-> Preprocessing data...')
    gaze_frames_preprocessed = GazeDataPreprocessing.preprocess_data_frames(gaze_frames_cleaned, config.VELOCITY_THRESHOLD)

    print('\n-> Classifying data...')
    participant_dicts = GazeDataClassifier.prepare_participant_dfs(gaze_frames_preprocessed)
    participant_dicts = GazeDataClassifier.classify_data_frames(participant_dicts, config.TEMPORAL_RESOLUTION)

    participant_dicts = GazeDataClassifier.reduce_gaze_dataframes(participant_dicts)

    with open(os.path.join(config.PATH_DATA_PREPROCESSED, "PreprocessedData.pkl"), 'wb') as output:
        pickle.dump(participant_dicts, output)

    return participant_dicts


def load_preprocessed():
    preprocessed_file_path = os.path.join(config.PATH_DATA_PREPROCESSED, 'PreprocessedData.pkl')
    print("Using existing preprocessed data!")
    print('Looking for preprocessed data in:', preprocessed_file_path)
    print('Loading preprocessed data:')
    print('-> Unpickling preprocessed data:')
    with open(preprocessed_file_path, 'rb') as preprocessed_data_file:
        return pickle.load(preprocessed_data_file)
