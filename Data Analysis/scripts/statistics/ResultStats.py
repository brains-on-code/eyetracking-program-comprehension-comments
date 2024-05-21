import os

import pandas as pd
from scipy.stats import wilcoxon

import config


def calculate_result_stats():
    combined_results_by_task = pd.read_csv(os.path.join(config.PATH_RESULTS, 'CombinedResultsByTask.csv'))

    metrics = {'Accuracy': 'greater',
               'Time': 'less',
               'Correct_Only_Time': 'less',
               }
    results = pd.DataFrame(columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])
    for metric_to_be_tested, alternative in metrics.items():
        print('Metric: ' + metric_to_be_tested)

        cp_data = combined_results_by_task.loc[combined_results_by_task['Task'].str.contains('CP'), metric_to_be_tested]
        cm_data = combined_results_by_task.loc[combined_results_by_task['Task'].str.contains('CM'), metric_to_be_tested]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(cp_data, cm_data, alternative=alternative)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_to_be_tested}:')
        print(f't = {stat}, p = {p_value}')
        print(f'CP: {cp_data.mean()}')
        print(f'CM: {cm_data.mean()} \n')

        alpha = 0.05
        if alternative == 'greater':
            if p_value < alpha:
                print(f'CP has a significantly positive effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly positive effect on {metric_to_be_tested}.')
        elif alternative == 'less':
            if p_value < alpha:
                print(f'CP has a significantly negative effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly negative effect on {metric_to_be_tested}.')
        else:
            print('Error: alternative not specified.')

        # Save the results
        results = pd.concat([results, pd.DataFrame(
            [[metric_to_be_tested, alternative, cm_data.mean(), cp_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])])

    # Save the results to a csv file
    if not os.path.exists(config.PATH_RESULTS_STATISTICS):
        os.makedirs(config.PATH_RESULTS_STATISTICS)

    results = results.round(3)
    results.to_csv(config.PATH_RESULTS_STATISTICS + '/Results_By_Task.csv', index=False)
