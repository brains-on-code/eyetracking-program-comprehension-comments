import os

import config


def export_data(preprocessed_data):
    print('\n## EXPORT TO OGAMA')
    for i, participant in enumerate(preprocessed_data):
        id = 'P' + participant['id_short']

        df = participant['gaze_data'].copy(deep=True)

        df.insert(0, 'SubjectName', id)
        df.insert(1, 'TrialID', i)

        unused_columns = ['index', 'GazePosXSmooth', 'GazePosYSmooth', 'Gaze_Event', 'Gaze_EventSmooth',
                          'ExperimentTime', 'Velocity', 'VelocitySmooth']
        unused_columns = [c for c in unused_columns if c in df.index]
        df.drop(unused_columns, axis=1, inplace=True)

        # Ogama does not allow multiple measurements for the same time
        df.drop_duplicates(subset='Time', keep=False, inplace=True)

        df['TrialNumber'] = df['TrialNumber'].apply(lambda x: x + (i * 8))
        df['Task'] = df['Task'].apply(lambda x: x + '.png')

        df.rename(index=str, inplace=True, columns={"TrialNumber": "TrialSequence", "Task": "TrialImage"})

        file_name = 'OgamaExport_' + str(id)

        if not os.path.exists(config.PATH_OGAMA):
            os.makedirs(config.PATH_OGAMA)

        df.to_csv(config.PATH_OGAMA + '/' + file_name + '.csv', index=False)

    print('-> export done')


def export_trial_aois(preprocessed_data, group=None):
    print('\n## EXPORT AOIS FOR OGAMA')
    for i, participant in enumerate(preprocessed_data):
        # get trial sequence of participant
        trial_sequence = participant['gaze_data']['TrialNumber'].unique().tolist()
        trial_image = participant['gaze_data']['Task'].unique().tolist()

        # assign trial sequence to trial image
        trials = dict(zip(trial_sequence, trial_image))

        # create new text file including all aoi data for all trials of participant
        # for each trial get the corresponding aoi text file from directory, add column with TrialId before each line and append to new file
        # the files are named after the task they belong to e.g. Task1CM aois.txt or Task1CP aois.txt
        # and are stored in the AOIs directory
        file_name = 'OgamaExport_AOIS'
        pid = 'P' + participant['id_short']
        if group:
            file_name += group
        file_name += '_' + str(pid)

        with open(config.PATH_OGAMA + '/' + file_name + '.txt', 'w') as outfile:
            outfile.write('TrialId\tSnippetName\tShapeName\tShapeType\tShapeNumPts\tShapePts\n')
            for id, snippet in trials.items():
                with open(config.PATH_AOI_DIR + '/' + snippet + ' aois.txt') as infile:
                    # skip header
                    next(infile)
                    for line in infile:
                        outfile.write(str(id) + line)
