import math

import pandas as pd
from tqdm import tqdm


class GazeDataClassifier:

    @staticmethod
    def prepare_participant_dfs(gaze_data_frames):
        participant_dicts = []

        for gaze_frame in gaze_data_frames:
            subject_id = gaze_frame['SubjectID'].iloc[0]
            gaze_data = gaze_frame.drop(columns='SubjectID')

            participant_dict = {
                'id': subject_id,
                'id_short': subject_id[:8],
                'gaze_frames': gaze_data.shape[0],
                'experiment_runtime': gaze_data['ExperimentTime'].iloc[-1] - gaze_data['ExperimentTime'].iloc[0],
                'gaze_data': gaze_data,
                'fixations': [],
                'saccades': [],
                'results': {
                    'ByTask': {},
                },
            }

            participant_dicts.append(participant_dict)

        return participant_dicts

    @staticmethod
    def classify_data_frames(participant_dfs, temporal_resolution):
        print('Total Participants: ', len(participant_dfs))
        return [GazeDataClassifier.classify_data_frame(i, len(participant_dfs), participant_df, temporal_resolution) for i, participant_df in
                enumerate(participant_dfs)]

    @staticmethod
    def classify_data_frame(i, total, participant_df, temporal_resolution):
        participant_df = GazeDataClassifier.compute_fixations_saccades(i, total, participant_df, temporal_resolution)
        return participant_df

    @staticmethod
    def compute_fixations_saccades(i, total, participant_df, temporal_resolution):
        # print out some statistics
        frames = participant_df['gaze_data'].shape[0]
        print('\n## Participant: ' + participant_df['id_short'] + ' (' + str(i+1) + '/' + str(total) + ')')
        print('Amount of frames: ' + str(frames))
        print('-> This dataframe contains roughly ' + str(
            round(participant_df['gaze_data'].shape[0] / temporal_resolution / 60)) + ' minutes of eye gaze.')

        gaze_data = participant_df['gaze_data']
        events = gaze_data['Gaze_EventSmooth'].values
        fixations = []
        saccades = []
        current_event = None

        with tqdm(total=len(events), unit='events') as pbar:
            # set colour of progress bar to white
            pbar.set_description('Classifying Fixation/Saccades')
            for i, event in enumerate(events):
                pbar.update(1)
                if current_event is None:
                    current_event = {
                        'Type': event,
                        'Task': gaze_data['Task'].iloc[i],
                        'Data': gaze_data.iloc[[i]],
                    }
                    continue

                if current_event['Type'] == event and current_event['Task'] == gaze_data['Task'].iloc[i]:
                    current_event['Data'] = pd.concat([current_event['Data'], gaze_data.iloc[[i]]], ignore_index=True)
                else:
                    if current_event['Type'] == 'Fixation':
                        current_event['AveragePositionX'] = current_event['Data']['GazePosX'].mean()
                        current_event['AveragePositionY'] = current_event['Data']['GazePosY'].mean()
                        current_event['Frames'] = current_event['Data'].shape[0]
                        time_diff = current_event['Data']['ExperimentTime'].iloc[-1] - \
                                    current_event['Data']['ExperimentTime'].iloc[0]
                        current_event['TimeLength'] = time_diff
                        fixations.append(current_event)
                    else:  # Saccade
                        gaze_pos_diff = current_event['Data'][['GazePosX', 'GazePosY', 'ExperimentTime']].diff().iloc[
                            -1]
                        current_event['DistanceX'] = abs(gaze_pos_diff['GazePosX'])
                        current_event['DistanceY'] = abs(gaze_pos_diff['GazePosY'])
                        current_event['Distance'] = math.sqrt(
                            gaze_pos_diff['GazePosX'] ** 2 + gaze_pos_diff['GazePosY'] ** 2)
                        current_event['AverageVelocity'] = current_event['Data']['VelocitySmooth'].mean()
                        current_event['Frames'] = current_event['Data'].shape[0]
                        time_diff = current_event['Data']['ExperimentTime'].iloc[-1] - \
                                    current_event['Data']['ExperimentTime'].iloc[0]
                        current_event['TimeLength'] = time_diff
                        saccades.append(current_event)

                    current_event = {
                        'Type': event,
                        'Task': gaze_data['Task'].iloc[i],
                        'Data': gaze_data.iloc[[i]],
                    }

        participant_df['fixations'] = fixations
        participant_df['saccades'] = saccades
        print('-> classifying fixation/saccades done')

        return participant_df

    @staticmethod
    def reduce_gaze_dataframes(participant_dicts):
        return [GazeDataClassifier.reduce_gaze_dataframe(participant_dict) for participant_dict in participant_dicts]

    @staticmethod
    def reduce_gaze_dataframe(participant_dict):
        gaze_data = participant_dict['gaze_data'][
            ['Time', 'GazePosX', 'GazePosY', 'VelocitySmooth', 'Task', 'ExperimentTime', 'Gaze_Event', 'TrialNumber']]
        gaze_data = gaze_data.round({'GazePosX': 2, 'GazePosY': 2, 'VelocitySmooth': 2})

        print('Reduced gaze_data dataframe:')
        print(gaze_data.head(5))

        return participant_dict
