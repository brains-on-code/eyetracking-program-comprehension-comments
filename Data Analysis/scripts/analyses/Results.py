import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config


def analyse_results():
    # Load correct solutions
    correct_solutions = pd.read_csv(config.PATH_SNIPPET_SOLUTIONS_CSV, delimiter=';')
    # Create a directory for saving results stats and plots
    if not os.path.exists(config.PATH_RESULTS):
        os.makedirs(config.PATH_RESULTS)

    combined_results = pd.DataFrame()
    # Iterate through participant folders
    for directory in os.listdir(config.PATH_DATA_RAW):
        # ignore hidden files
        if str(directory).startswith('.'):
            continue
        # Get participant id from folder name
        participant_id = str(directory).split("_")[1]
        results_file_path = os.path.join(str(config.PATH_DATA_RAW), str(directory),
                                         "Results_" + str(participant_id) + ".csv")
        # Check if Results file exists in participant folder
        if not os.path.isfile(results_file_path):
            print("Results file not found for participant: " + participant_id)
            continue
        # Create a directory for saving individual participant results stats and plots
        individual_stats_dir = os.path.join(config.PATH_RESULTS, 'Individual', participant_id)
        if not os.path.exists(individual_stats_dir):
            os.makedirs(individual_stats_dir)

        # Perform individual participant analysis
        participant_results, participant_results_by_task_type = evaluate_participant_results(correct_solutions,
                                                                                             results_file_path)
        # Save df for individual participant's results
        participant_results.to_csv(os.path.join(individual_stats_dir, 'ParticipantResults.csv'), index=False)
        participant_results_by_task_type = participant_results_by_task_type.round(1)
        participant_results_by_task_type.to_csv(
            os.path.join(individual_stats_dir, 'ParticipantResultsByTaskType.csv'), index=True)

        # Append individual participant's results to combined results
        combined_results = pd.concat([combined_results, participant_results], ignore_index=True)

    # Perform analysis on the combined_results DataFrame for all participants
    (combined_results,
     combined_results_by_task,
     combined_results_by_task_number,
     combined_results_by_task_type) = evaluate_combined_results(combined_results)

    # Save combined results to csv
    combined_results.to_csv(os.path.join(config.PATH_RESULTS, 'CombinedResults.csv'), index=False)
    combined_results_by_task.to_csv(os.path.join(config.PATH_RESULTS, 'CombinedResultsByTask.csv'), index=True)
    combined_results_by_task_number.to_csv(os.path.join(config.PATH_RESULTS, 'CombinedResultsByTaskNumber.csv'),
                                           index=True)
    combined_results_by_task_type.to_csv(os.path.join(config.PATH_RESULTS, 'CombinedResultsByTaskType.csv'), index=True)

    print("Results analysis and visualization completed.")


def evaluate_participant_results(correct_solutions, results_file_path):
    participant_results = pd.read_csv(results_file_path, delimiter=";")
    participant_results = pd.merge(participant_results, correct_solutions, how='inner', on='Task')
    participant_results = participant_results.drop(columns=['Number'])
    participant_results = participant_results[~participant_results['Task'].str.contains('WarmUp')]
    participant_results['Correct'] = participant_results['Answer_Out'] == participant_results['Solution']
    participant_results['Time'] = participant_results['Time'] / 1000
    participant_results['Correct_Only_Time'] = participant_results['Correct'] * participant_results['Time']
    participant_results['Task_Type'] = participant_results['Task'].str[-2:]
    participant_results['Task_Number'] = participant_results['Task'].str[4:-2]
    participant_results['Task_Number'] = participant_results['Task_Number'].astype(int)
    participant_results = participant_results.sort_values(by=['Task_Number', 'Task_Type'])
    participant_results = participant_results[
        ['Task', 'Task_Number', 'Task_Type', 'Answer_Out', 'Solution', 'Correct', 'Time',
         'TimeOut', 'Correct_Only_Time', 'SubjectID']]

    # Group participant results by task type
    participant_results_by_task_type = participant_results.groupby('Task_Type').agg(
        {'Correct': ['mean'], 'TimeOut': ['sum'], 'Time': ['mean'], 'Correct_Only_Time': ['mean']})
    # rename columns
    participant_results_by_task_type.columns = ['Accuracy', 'TimeOut_Count', 'Time', 'Correct_Only_Time']
    participant_results_by_task_type['Accuracy'] = participant_results_by_task_type['Accuracy'] * 100
    # reorder columns such that correct count is before correct only time
    participant_results_by_task_type = participant_results_by_task_type[
        ['Accuracy', 'Time', 'TimeOut_Count', 'Correct_Only_Time']]

    return participant_results, participant_results_by_task_type


def evaluate_combined_results(combined_results):
    # Sort the tasks by task type and then by task number
    combined_results = combined_results.sort_values(by=['Task_Number', 'Task_Type'])

    # Extract the base task identifier from the Task column
    combined_results['TaskBase'] = combined_results['Task'].str.extract(r'(Task\d+)')

    # Calculate common min and max times for each base task
    common_min_max_times = combined_results.groupby('TaskBase')['Time'].agg(['min', 'max']).reset_index()

    # Merge the common min and max times back to the original dataset
    combined_results = combined_results.merge(common_min_max_times, on='TaskBase', how='left')

    # Apply min-max normalization
    combined_results['Normalized_Time'] = (combined_results['Time'] - combined_results['min']) / (
                combined_results['max'] - combined_results['min'])
    combined_results['Time_Score'] = 1 - combined_results['Normalized_Time']

    # Recalculate the mean values for each task
    combined_results_by_task = combined_results.groupby('Task').agg(
        Accuracy=('Correct', 'mean'),
        Time=('Time', 'mean'),
        Time_SD=('Time', 'std'),
        Correct_Only_Time=('Correct_Only_Time', 'mean'),
        Correct_Only_Time_SD=('Correct_Only_Time', 'std'),
        Time_Score=('Time_Score', 'mean')
    )

    # Calculate the final score
    combined_results_by_task['Score'] = 0.5 * combined_results_by_task['Accuracy'] + 0.5 * combined_results_by_task['Time_Score']


    # Reorder columns
    combined_results_by_task = combined_results_by_task[
        ['Accuracy', 'Time', 'Time_SD', 'Correct_Only_Time', 'Correct_Only_Time_SD', 'Time_Score', 'Score']]
    combined_results_by_task['Accuracy'] = combined_results_by_task['Accuracy'] * 100
    combined_results_by_task['Score'] = combined_results_by_task['Score'] * 100
    combined_results_by_task = combined_results_by_task.round(1)
    combined_results_by_task = combined_results_by_task.reindex(config.SNIPPETS)

    # Group combined results by task number
    combined_results_by_task_number = combined_results.groupby('Task_Number').agg(
        {'Correct': ['mean'], 'Time': ['mean', 'std'], 'Correct_Only_Time': ['mean', 'std']})
    combined_results_by_task_number.index = ['Task' + str(i) for i in combined_results_by_task_number.index]
    combined_results_by_task_number.index.name = 'Task'
    combined_results_by_task_number.columns = ['Accuracy', 'Time', 'Time_SD', 'Correct_Only_Time',
                                               'Correct_Only_Time_SD']
    combined_results_by_task_number['Accuracy'] = combined_results_by_task_number['Accuracy'] * 100
    # reorder columns
    combined_results_by_task_number = combined_results_by_task_number[
        ['Accuracy', 'Time', 'Time_SD', 'Correct_Only_Time', 'Correct_Only_Time_SD']]
    combined_results_by_task_number = combined_results_by_task_number.round(1)

    # Group combined results by task type
    combined_results_by_task_type = combined_results.groupby('Task_Type').agg(
        {'Correct': ['mean'], 'Time': ['mean', 'std'], 'Correct_Only_Time': ['mean', 'std']})
    combined_results_by_task_type.columns = ['Accuracy', 'Time', 'Time_SD', 'Correct_Only_Time', 'Correct_Only_Time_SD']
    combined_results_by_task_type['Accuracy'] = combined_results_by_task_type['Accuracy'] * 100
    # reorder columns
    combined_results_by_task_type = combined_results_by_task_type[
        ['Accuracy', 'Time', 'Time_SD', 'Correct_Only_Time', 'Correct_Only_Time_SD']]
    combined_results_by_task_type = combined_results_by_task_type.round(1)
    combined_results_by_task_type = combined_results_by_task_type.transpose()

    return combined_results, combined_results_by_task, combined_results_by_task_number, combined_results_by_task_type
