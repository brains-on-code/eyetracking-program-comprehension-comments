import itertools
import math
import os

import numpy
import pandas as pd
from tqdm import tqdm

import config
from scripts.utils import NWAlgorithm
from scripts.utils.SnippetAoiUtils import generate_snippet_aoi_reading_order_map

HORIZONTAL_AOI_DEVIATION_THRESHOLD = 100
VERTICAL_AOI_DEVIATION_THRESHOLD = 5


def run_calculations(preprocessed_data):
    rtgct_df = pd.DataFrame()
    visual_attention_df = pd.DataFrame()
    linearity_df = pd.DataFrame()
    nw_df = pd.DataFrame()
    gaze_strategy_df = pd.DataFrame()

    if not os.path.exists(config.PATH_LINEARITY_METRICS):
        os.makedirs(config.PATH_LINEARITY_METRICS)
    if not os.path.exists(config.PATH_VISUAL_ATTENTION_METRICS):
        os.makedirs(config.PATH_VISUAL_ATTENTION_METRICS)
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS)

    snippets_info = generate_snippet_aoi_reading_order_map()
    for i, task_name in enumerate(config.SNIPPETS):
        cp = True if 'CP' in task_name else False
        snippet_type = 'CP' if cp else 'CM'
        print('\nComputing task: ', task_name)

        fixations = []

        saccades_by_participant = {}
        matched_fixations_by_participant = {}

        # get all fixations from task
        for participant in preprocessed_data:
            for fixation in participant['fixations']:
                if fixation['Task'] == task_name:
                    matched_fixations_by_participant[participant['id_short']] = []
                    fixation['Participant'] = participant['id_short']
                    fixations.append(fixation)

            for saccade in participant['saccades']:
                if saccade['Task'] == task_name:
                    if participant['id_short'] not in saccades_by_participant:
                        saccades_by_participant[participant['id_short']] = []
                    saccade['Participant'] = participant['id_short']
                    saccades_by_participant[participant['id_short']].append(saccade)

        overall_fixations = len(fixations)
        participants_with_fixations = len(matched_fixations_by_participant)
        print('-> Number of fixations ', overall_fixations)
        print('-> Number of participants with fixations ', participants_with_fixations)

        # match AOIs for each fixation

        # get AOI information
        aoi_map, story_order, execution_order = snippets_info[task_name]
        story_order_code_first = story_order[0]
        story_order_comment_first = story_order[1]
        story_order_code_only = story_order[2]
        story_order_global = story_order[3]
        execution_order_code_first = execution_order[0]
        execution_order_comment_first = execution_order[1]
        execution_order_code_only = execution_order[2]
        execution_order_global = execution_order[3]

        for fixation in fixations:
            # check whether fixation is in an AOI
            # get coordinates
            x = fixation['AveragePositionX']
            y = fixation['AveragePositionY']

            line_hit = None
            aoi_hit = None

            # go through each AOI and check whether there is a hit
            for aoi_name, aoi_points in aoi_map.items():
                if (aoi_points[1] - VERTICAL_AOI_DEVIATION_THRESHOLD) <= y <= (
                        aoi_points[3] + VERTICAL_AOI_DEVIATION_THRESHOLD) and (
                        aoi_points[0] - HORIZONTAL_AOI_DEVIATION_THRESHOLD) <= x <= (
                        aoi_points[2] + HORIZONTAL_AOI_DEVIATION_THRESHOLD):
                    # the aoi name consists of the task name and the line number
                    # extract the line number
                    if 'CPC' in aoi_name:
                        line_hit = int(aoi_points[4])
                        aoi_hit = aoi_name.split('CP')[1]
                        break
                    elif 'CPL' in aoi_name or 'CM' in aoi_name:
                        line_hit = int(aoi_points[4])
                        aoi_hit = 'L' + aoi_name.split('L')[1]
                        break

            matched_fixations_by_participant[fixation['Participant']].append({
                'aoi': aoi_hit,
                'line': line_hit,
                'fixation': fixation,
                'duration': fixation['TimeLength'],
            })

        if overall_fixations == 0:
            print('No fixations for task ' + task_name)
            continue

        # calculate metrics
        with (tqdm(total=len(matched_fixations_by_participant), unit='participant') as pbar):
            pbar.set_description('Calculating AOI metrics')
            for participant in matched_fixations_by_participant:
                pbar.update(1)
                vertical_next = []
                vertical_later = []
                regression = []
                horizontal_later = []
                line_regression = []
                code_to_comment = []
                comment_to_code = []

                fixations_part = matched_fixations_by_participant[participant]
                # remove fixations that are None but keep fixations that are 0
                fixations_aoi_cleaned_line = list(filter(lambda elem: elem['line'] is not None, fixations_part))
                if not fixations_aoi_cleaned_line:
                    # print('seems like there are no fixations for ' + participant + ' for task ' + task)
                    continue

                for current_fixation, next_fixation in zip(fixations_aoi_cleaned_line, fixations_aoi_cleaned_line[1:]):
                    if not next_fixation['line'] or not current_fixation['line']:
                        continue

                    # only compute when both fixations have matched lines
                    # Horizontal Later Text: check whether a saccade (between two fixations) is forward on a line
                    if current_fixation['line'] == next_fixation['line']:
                        # check whether it moved to the right
                        if (next_fixation['fixation']['AveragePositionX']
                                >= current_fixation['fixation']['AveragePositionX']):
                            horizontal_later.append(next_fixation)
                        else:
                            line_regression.append(next_fixation)

                        # Code to Comment: check whether a saccade (between two fixations) is from code to comment
                        if 'L' in current_fixation['aoi'] and 'C' in next_fixation['aoi']:
                            code_to_comment.append(next_fixation)
                        elif 'C' in current_fixation['aoi'] and 'L' in next_fixation['aoi']:
                            comment_to_code.append(next_fixation)
                    else:
                        # check whether it's an up or down movement
                        if current_fixation['line'] + 1 == next_fixation['line']:
                            vertical_next.append(next_fixation)
                        elif next_fixation['line'] > current_fixation['line'] + 1:
                            vertical_later.append(next_fixation)
                        else:
                            regression.append(next_fixation)

                # clean C and L prefix from AOI names and cast to int
                for fixation in fixations_aoi_cleaned_line:
                    fixation['type'] = fixation['aoi']
                    fixation['aoi'] = int(fixation['aoi'][1:])
                reading_order_aoi = [fixation['aoi'] for fixation in fixations_aoi_cleaned_line]
                reading_order_line = [fixation['line'] for fixation in fixations_aoi_cleaned_line]
                reading_order_fixations = [(fixation['aoi'], fixation['duration']) for fixation in
                                           fixations_aoi_cleaned_line]
                reading_order_aoi_time = [(fixation['type'], fixation['duration']) for fixation in
                                          fixations_aoi_cleaned_line]

                reading_order_aoi_no_duplicates = [x[0] for x in itertools.groupby(reading_order_aoi)]
                reading_order_line_no_duplicates = [x[0] for x in itertools.groupby(reading_order_line)]
                reading_order_fixations_no_duplicates = [(key, sum([x[1] for x in group])) for key, group in
                                                         itertools.groupby(reading_order_fixations, lambda x: x[0])]
                reading_order_aoi_time_no_duplicates = [(key, sum([x[1] for x in group])) for key, group in
                                                        itertools.groupby(reading_order_aoi_time, lambda x: x[0])]

                # Code Line and Comment Fixations
                code_line_fixations = [fixation for fixation in fixations_aoi_cleaned_line if 'L' in fixation['type']]
                comment_line_fixations = [fixation for fixation in fixations_aoi_cleaned_line if
                                          'C' in fixation['type']]

                # Total Code Line and Comment Fixation Durations
                total_fixations_duration = sum([fixation['duration'] for fixation in fixations_part]) / 1000
                total_aoi_fixations_duration = sum(
                    [fixation['duration'] for fixation in fixations_aoi_cleaned_line]) / 1000
                code_line_fixations_duration = sum([fixation['duration'] for fixation in code_line_fixations]) / 1000
                comment_line_fixations_duration = sum(
                    [fixation['duration'] for fixation in comment_line_fixations]) / 1000

                # Calculate RTGCT
                rtgct_results = pd.DataFrame(reading_order_fixations_no_duplicates,
                                             columns=['AOIName', 'FixationDuration'])
                rtgct_results['Stimulus'] = task_name
                rtgct_results['Participant'] = participant

                rtgct_participant_dir = os.path.join(config.PATH_RTGCT, 'IndividualExport', participant)
                if not os.path.exists(rtgct_participant_dir):
                    os.makedirs(rtgct_participant_dir)

                rtgct_results.to_csv(rtgct_participant_dir + '/' + task_name + '.csv', mode='w', index=False)
                # append to overall rtgct df
                rtgct_df = pd.concat([rtgct_df, rtgct_results])

                # NW Scores for STORY ORDER NAIVE
                nw_score_story_code_first_naive = NWAlgorithm.nw_score_naive(story_order_code_first,
                                                                             reading_order_aoi_no_duplicates)
                nw_score_story_comment_first_naive = NWAlgorithm.nw_score_naive(story_order_comment_first,
                                                                                reading_order_aoi_no_duplicates)
                nw_score_story_code_only_naive = NWAlgorithm.nw_score_naive(story_order_code_only,
                                                                            reading_order_aoi_no_duplicates)
                nw_score_story_global_naive = NWAlgorithm.nw_score_naive(story_order_global,
                                                                         reading_order_line_no_duplicates)

                # NW Scores for STORY ORDER DYNAMIC
                [nw_score_story_code_first_dynamic_repetitions,
                 nw_score_story_code_first_dynamic_score] = NWAlgorithm.nw_score_dynamic(story_order_code_first,
                                                                                         reading_order_aoi_no_duplicates)
                [nw_score_story_comment_first_dynamic_repetitions,
                 nw_score_story_comment_first_dynamic_score] = NWAlgorithm.nw_score_dynamic(story_order_comment_first,
                                                                                            reading_order_aoi_no_duplicates)
                [nw_score_story_code_only_dynamic_repetitions,
                 nw_score_story_code_only_dynamic_score] = NWAlgorithm.nw_score_dynamic(story_order_code_only,
                                                                                        reading_order_aoi_no_duplicates)
                [nw_score_story_global_dynamic_repetitions,
                 nw_score_story_global_dynamic_score] = NWAlgorithm.nw_score_dynamic(story_order_global,
                                                                                     reading_order_line_no_duplicates)

                # NW Scores for EXECUTION ORDER NAIVE
                nw_score_exec_code_first_naive = NWAlgorithm.nw_score_naive(execution_order_code_first,
                                                                            reading_order_aoi_no_duplicates)
                nw_score_exec_comment_first_naive = NWAlgorithm.nw_score_naive(execution_order_comment_first,
                                                                               reading_order_aoi_no_duplicates)
                nw_score_exec_code_only_naive = NWAlgorithm.nw_score_naive(execution_order_code_only,
                                                                           reading_order_aoi_no_duplicates)
                nw_score_exec_global_naive = NWAlgorithm.nw_score_naive(execution_order_global,
                                                                        reading_order_line_no_duplicates)

                # NW Scores for EXECUTION ORDER DYNAMIC
                [nw_score_exec_code_first_dynamic_repetitions,
                 nw_score_exec_code_first_dynamic_score] = NWAlgorithm.nw_score_dynamic(
                    execution_order_code_first, reading_order_aoi_no_duplicates)
                [nw_score_exec_comment_first_dynamic_repetitions,
                 nw_score_exec_comment_first_dynamic_score] = NWAlgorithm.nw_score_dynamic(
                    execution_order_comment_first, reading_order_aoi_no_duplicates)
                [nw_score_exec_code_only_dynamic_repetitions,
                 nw_score_exec_code_only_dynamic_score] = NWAlgorithm.nw_score_dynamic(
                    execution_order_code_only, reading_order_aoi_no_duplicates)
                [nw_score_exec_global_dynamic_repetitions,
                 nw_score_exec_global_dynamic_score] = NWAlgorithm.nw_score_dynamic(
                    execution_order_global, reading_order_line_no_duplicates)

                linearity_results_for_participant = {
                    'Participant': participant.split('-')[0],
                    'Task': task_name,
                    'Type': snippet_type,
                    'VerticalNext': len(vertical_next) / len(fixations_aoi_cleaned_line),
                    'VerticalLater': len(vertical_later) / len(fixations_aoi_cleaned_line),
                    'Regression': len(regression) / len(fixations_aoi_cleaned_line),
                    'HorizontalLater': len(horizontal_later) / len(fixations_aoi_cleaned_line),
                    'LineRegression': len(line_regression) / len(fixations_aoi_cleaned_line),
                    'SaccadeLength': numpy.mean(
                        [saccade['Distance'] for saccade in saccades_by_participant[participant] if
                         saccade['Task'] == task_name and not math.isnan(saccade['Distance'])]),
                }

                nw_results_for_participant = {
                    'Participant': participant.split('-')[0],
                    'Task': task_name,
                    'Type': snippet_type,

                    'Story_CodeFirst_Naive': nw_score_story_code_first_naive if cp else 0,
                    'Exec_CodeFirst_Naive': nw_score_exec_code_first_naive if cp else 0,
                    'Story_CodeFirst_Dynamic': nw_score_story_code_first_dynamic_score if cp else 0,
                    'Story_CodeFirst_Dynamic_Reps': nw_score_story_code_first_dynamic_repetitions if cp else 0,
                    'Exec_CodeFirst_Dynamic': nw_score_exec_code_first_dynamic_score if cp else 0,
                    'Exec_CodeFirst_Dynamic_Reps': nw_score_exec_code_first_dynamic_repetitions if cp else 0,

                    'Story_CommentFirst_Naive': nw_score_story_comment_first_naive if cp else 0,
                    'Exec_CommentFirst_Naive': nw_score_exec_comment_first_naive if cp else 0,
                    'Story_CommentFirst_Dynamic': nw_score_story_comment_first_dynamic_score if cp else 0,
                    'Story_CommentFirst_Dynamic_Reps': nw_score_story_comment_first_dynamic_repetitions if cp else 0,
                    'Exec_CommentFirst_Dynamic': nw_score_exec_comment_first_dynamic_score if cp else 0,
                    'Exec_CommentFirst_Dynamic_Reps': nw_score_exec_comment_first_dynamic_repetitions if cp else 0,

                    'Story_CodeOnly_Naive': nw_score_story_code_only_naive,
                    'Exec_CodeOnly_Naive': nw_score_exec_code_only_naive,
                    'Story_CodeOnly_Dynamic': nw_score_story_code_only_dynamic_score,
                    'Story_CodeOnly_Dynamic_Reps': nw_score_story_code_only_dynamic_repetitions,
                    'Exec_CodeOnly_Dynamic': nw_score_exec_code_only_dynamic_score,
                    'Exec_CodeOnly_Dynamic_Reps': nw_score_exec_code_only_dynamic_repetitions,

                    'Story_Global_Naive': nw_score_story_global_naive,
                    'Exec_Global_Naive': nw_score_exec_global_naive,
                    'Story_Global_Dynamic': nw_score_story_global_dynamic_score,
                    'Story_Global_Dynamic_Reps': nw_score_story_global_dynamic_repetitions,
                    'Exec_Global_Dynamic': nw_score_exec_global_dynamic_score,
                    'Exec_Global_Dynamic_Reps': nw_score_exec_global_dynamic_repetitions,

                    'ReadingOrder_AOI': reading_order_aoi_no_duplicates,
                    'ReadingOrder_Line': reading_order_line_no_duplicates,
                }

                visual_attention_results_for_participant = {
                    'Participant': participant.split('-')[0],
                    'Task': task_name,
                    'Type': snippet_type,

                    'AllFixations_Count': len(fixations_part),
                    'AllFixations_Duration': total_fixations_duration,

                    'AoiFixations_Count': len(fixations_aoi_cleaned_line),
                    'AoiFixations_Duration': total_aoi_fixations_duration,
                    'AoiHits_CountRatio': len(fixations_aoi_cleaned_line) / len(fixations_part),
                    'AoiHits_DurationRatio': total_aoi_fixations_duration / total_fixations_duration,

                    'CodeFixations_Count': len(code_line_fixations),
                    'CodeFixations_Duration': code_line_fixations_duration,
                    'CodeHits_CountRatio': len(code_line_fixations) / len(fixations_aoi_cleaned_line),
                    'CodeHits_DurationRatio': code_line_fixations_duration / total_aoi_fixations_duration,

                    'CommentFixations_Count': len(comment_line_fixations),
                    'CommentFixations_Duration': comment_line_fixations_duration,
                    'CommentHits_CountRatio': len(comment_line_fixations) / len(fixations_aoi_cleaned_line),
                    'CommentHits_DurationRatio': comment_line_fixations_duration / total_aoi_fixations_duration,
                }

                gaze_strategy_results_for_participant = {
                    'Participant': participant.split('-')[0],
                    'Task': task_name,
                    'Type': snippet_type,

                    'CodeToComment_Count': len(code_to_comment) if snippet_type == 'CP' else 0,
                    'CommentToCode_Count': len(comment_to_code) if snippet_type == 'CP' else 0,

                    'CodeToComment_Ratio': (len(code_to_comment) / len(
                        matched_fixations_by_participant[participant])) if snippet_type == 'CP' else 0,
                    'CommentToCode_Ratio': (len(comment_to_code) / len(
                        matched_fixations_by_participant[participant])) if snippet_type == 'CP' else 0,
                }

                linearity_results_for_participant = pd.DataFrame([linearity_results_for_participant])
                nw_results_for_participant = pd.DataFrame([nw_results_for_participant])
                visual_attention_results_for_participant = pd.DataFrame([visual_attention_results_for_participant])
                gaze_strategy_results_for_participant = pd.DataFrame([gaze_strategy_results_for_participant])

                linearity_individual_export_dir = config.PATH_LINEARITY_METRICS + '/IndividualExport/' + participant
                visual_attention_individual_export_dir = config.PATH_VISUAL_ATTENTION_METRICS + '/IndividualExport/' + participant
                gaze_strategy_individual_export_dir = config.PATH_GAZE_STRATEGY_METRICS + '/IndividualExport/' + participant

                if not os.path.exists(linearity_individual_export_dir):
                    os.makedirs(linearity_individual_export_dir)
                if not os.path.exists(visual_attention_individual_export_dir):
                    os.makedirs(visual_attention_individual_export_dir)
                if not os.path.exists(gaze_strategy_individual_export_dir):
                    os.makedirs(gaze_strategy_individual_export_dir)

                linearity_results_for_participant = linearity_results_for_participant.round(2)
                linearity_results_for_participant.to_csv(
                    os.path.join(linearity_individual_export_dir, task_name + '.csv'), index=False)
                nw_results_for_participant = nw_results_for_participant.round(2)
                nw_results_for_participant.to_csv(
                    os.path.join(linearity_individual_export_dir, task_name + '_nw.csv'), index=False)
                visual_attention_results_for_participant = visual_attention_results_for_participant.round(2)
                visual_attention_results_for_participant.to_csv(
                    os.path.join(visual_attention_individual_export_dir, task_name + '.csv'), index=False)
                gaze_strategy_results_for_participant = gaze_strategy_results_for_participant.round(2)
                gaze_strategy_results_for_participant.to_csv(
                    os.path.join(gaze_strategy_individual_export_dir, task_name + '.csv'), index=False)

                linearity_df = pd.concat([linearity_df, linearity_results_for_participant], ignore_index=True)
                nw_df = pd.concat([nw_df, nw_results_for_participant], ignore_index=True)
                visual_attention_df = pd.concat([visual_attention_df, visual_attention_results_for_participant],
                                                ignore_index=True)
                gaze_strategy_df = pd.concat([gaze_strategy_df, gaze_strategy_results_for_participant],
                                             ignore_index=True)

    # save results
    rtgct_df.to_csv(config.PATH_RTGCT + '/RTGCT_METRICS_ALL.csv', index=False)
    process_linearity_df(linearity_df)
    process_nw_df(nw_df)
    process_visual_attention_df(visual_attention_df)
    process_gaze_strategy_df(gaze_strategy_df)


def process_linearity_df(linearity_df):
    linearity_df.to_csv(config.PATH_LINEARITY_METRICS + '/Linearity_Metrics_All.csv', index=False)

    # group by Type
    linearity_df_by_type = linearity_df.groupby(['Type']).mean(numeric_only=True)
    linearity_df_by_type = linearity_df_by_type.round(2)
    linearity_df_by_type.to_csv(config.PATH_LINEARITY_METRICS + '/Linearity_Metrics_By_Type.csv')

    # group by Task
    linearity_df_by_task = linearity_df.groupby(['Task']).mean(numeric_only=True)
    linearity_df_by_task = linearity_df_by_task.round(2)
    linearity_df_by_task = linearity_df_by_task.reindex(config.SNIPPETS)
    linearity_df_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/Linearity_Metrics_By_Task.csv')

    # group by Participant and Type
    linearity_df_by_participant_cp = linearity_df.groupby(['Participant', 'Type']).mean(numeric_only=True)
    linearity_df_by_participant_cp = linearity_df_by_participant_cp.round(2)
    linearity_df_by_participant_cp.to_csv(config.PATH_LINEARITY_METRICS + '/Linearity_Metrics_By_Participant_Type.csv')


def process_nw_df(nw_df):
    nw_df.to_csv(config.PATH_LINEARITY_METRICS + '/NW_Metrics_All.csv', index=False)

    # group by Type
    nw_df_by_type = nw_df.groupby(['Type']).mean(numeric_only=True)
    nw_df_by_type = nw_df_by_type.round(2)
    nw_df_by_type = nw_df_by_type.transpose()
    nw_df_by_type.to_csv(config.PATH_LINEARITY_METRICS + '/NW_Metrics_By_Type.csv')

    # group by Task
    nw_df_by_task = nw_df.groupby(['Task']).mean(numeric_only=True)
    nw_df_by_task = nw_df_by_task.round(2)
    nw_df_by_task = nw_df_by_task.reindex(config.SNIPPETS)
    nw_df_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/NW_Metrics_By_Task.csv')

    # group by Participant and Type
    nw_df_by_participant_cp = nw_df.groupby(['Participant', 'Type']).mean(numeric_only=True)
    nw_df_by_participant_cp = nw_df_by_participant_cp.round(2)
    nw_df_by_participant_cp.to_csv(config.PATH_LINEARITY_METRICS + '/NW_Metrics_By_Participant_Type.csv')


def process_visual_attention_df(visual_attention_df):
    visual_attention_df.to_csv(config.PATH_VISUAL_ATTENTION_METRICS + '/VisualAttention_Metrics_All.csv', index=False)

    # group by Type
    visual_attention_df_by_type = visual_attention_df.groupby(['Type']).mean(numeric_only=True)
    visual_attention_df_by_type = visual_attention_df_by_type.round(2)
    visual_attention_df_by_type = visual_attention_df_by_type.transpose()
    visual_attention_df_by_type.to_csv(config.PATH_VISUAL_ATTENTION_METRICS + '/VisualAttention_Metrics_By_Type.csv')

    # group by Task
    visual_attention_df_by_task = visual_attention_df.groupby(['Task']).mean(numeric_only=True)
    visual_attention_df_by_task = visual_attention_df_by_task.round(2)
    visual_attention_df_by_task = visual_attention_df_by_task.reindex(config.SNIPPETS)
    visual_attention_df_by_task.to_csv(config.PATH_VISUAL_ATTENTION_METRICS + '/VisualAttention_Metrics_By_Task.csv')

    # group by Participant and Type
    visual_attention_df_by_participant_cp = visual_attention_df.groupby(['Participant', 'Type']).mean(numeric_only=True)
    visual_attention_df_by_participant_cp = visual_attention_df_by_participant_cp.round(2)
    visual_attention_df_by_participant_cp.to_csv(
        config.PATH_VISUAL_ATTENTION_METRICS + '/VisualAttention_Metrics_By_Participant_Type.csv')


def process_gaze_strategy_df(gaze_strategy_df):
    gaze_strategy_df.to_csv(config.PATH_GAZE_STRATEGY_METRICS + '/GazeStrategy_Metrics_All.csv', index=False)

    # group by Type
    gaze_strategy_df_by_type = gaze_strategy_df.groupby(['Type']).mean(numeric_only=True)
    gaze_strategy_df_by_type = gaze_strategy_df_by_type.round(2)
    gaze_strategy_df_by_type.to_csv(config.PATH_GAZE_STRATEGY_METRICS + '/GazeStrategy_Metrics_By_Type.csv')

    # group by Task
    gaze_strategy_df_by_task = gaze_strategy_df[gaze_strategy_df['Type'] == 'CP'].drop(columns=['Type'])
    gaze_strategy_df_by_task = gaze_strategy_df_by_task.groupby(['Task']).mean(numeric_only=True)
    gaze_strategy_df_by_task = gaze_strategy_df_by_task.round(2)
    gaze_strategy_df_by_task.index = gaze_strategy_df_by_task.index.str[:-2]
    gaze_strategy_df_by_task = gaze_strategy_df_by_task.reindex(config.SNIPPETS_UNIQUE)
    gaze_strategy_df_by_task.to_csv(config.PATH_GAZE_STRATEGY_METRICS + '/GazeStrategy_Metrics_By_Task.csv')

    # group by Participant and Type
    gaze_strategy_df_by_participant_cp = gaze_strategy_df[gaze_strategy_df['Type'] == 'CP'].drop(columns=['Type'])
    gaze_strategy_df_by_participant_cp = gaze_strategy_df_by_participant_cp.groupby(['Participant']).mean(
        numeric_only=True)
    gaze_strategy_df_by_participant_cp = gaze_strategy_df_by_participant_cp.round(2)
    gaze_strategy_df_by_participant_cp.to_csv(
        config.PATH_GAZE_STRATEGY_METRICS + '/GazeStrategy_Metrics_By_Participant.csv')


if __name__ == "__main__":
    print('should not call this python file directly anymore.')
