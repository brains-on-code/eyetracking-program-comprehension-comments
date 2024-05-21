import os

import pandas as pd
from scipy.stats import wilcoxon

import config


def calculate_rating_stats():
    combined_difficulties = pd.read_csv(config.PATH_RATINGS + '/CombinedDifficultiesByTask.csv')

    metrics = ['Difficulty Mean']

    results = pd.DataFrame(columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])
    for metric_to_be_tested in metrics:
        print('Metric: ' + metric_to_be_tested)

        cp_data = combined_difficulties.loc[combined_difficulties['Task'].str.contains('CP'), metric_to_be_tested]
        cm_data = combined_difficulties.loc[combined_difficulties['Task'].str.contains('CM'), metric_to_be_tested]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(cp_data, cm_data, alternative='less')

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_to_be_tested}:')
        print(f't = {stat}, p = {p_value}')
        print(f'CP: {cp_data.mean()}')
        print(f'CM: {cm_data.mean()} \n')

        alpha = 0.05
        if p_value < alpha:
            print(f'CP has a significantly negative effect on {metric_to_be_tested}.')
        else:
            print(f'CP does not have a significantly negative effect on {metric_to_be_tested}.')

        # Save the results
        results = pd.concat([results, pd.DataFrame(
            [[metric_to_be_tested, 'less', cm_data.mean(), cp_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])])

    # Save the results to a csv file
    if not os.path.exists(config.PATH_RATINGS_STATISTICS):
        os.makedirs(config.PATH_RATINGS_STATISTICS)

    results = results.round(3)
    results.to_csv(config.PATH_RATINGS_STATISTICS + '/Difficulty_By_Task.csv', index=False)


# calculate statistics for ratings and comment contributions
def calculate_aggregated_ratings():
    combined_difficulties = pd.read_csv(config.PATH_RATINGS + '/CombinedDifficulties.csv')
    combined_comment_contributions = pd.read_csv(config.PATH_RATINGS + '/CombinedCommentContributions.csv')

    # calculate the difference between the mean of the CP and CM tasks for difficulty and calculate if there is a correlation between the difference and the comment contribution
    # calculate difficulty difference of cp and cm for each task

    combined_data = pd.DataFrame(
        columns=['Task', 'CM Difficulty Mean', 'CP Difficulty Mean', 'Difficulty Difference', 'Comment Contribution'])

    for task in combined_difficulties['Task'].unique():
        task_difficulties = combined_difficulties.loc[combined_difficulties['Task'] == task]
        cm_difficulty_mean = task_difficulties.loc[task_difficulties['Type'] == 'CM', 'Difficulty'].mean()
        cp_difficulty_mean = task_difficulties.loc[task_difficulties['Type'] == 'CP', 'Difficulty'].mean()
        difficulty_difference = cp_difficulty_mean - cm_difficulty_mean
        comment_contribution = combined_comment_contributions.loc[
            combined_comment_contributions['Task'] == task, 'Comment Contribution'].mean()

        combined_data = pd.concat([combined_data, pd.DataFrame(
            [[task, cm_difficulty_mean, cp_difficulty_mean, difficulty_difference, comment_contribution]],
            columns=['Task', 'CM Difficulty Mean', 'CP Difficulty Mean', 'Difficulty Difference',
                     'Comment Contribution'])])

    combined_data.to_csv(config.PATH_RATINGS_STATISTICS + '/DifficultyDifferenceAndCommentContribution.csv',
                            index=False)

    # statistics if there is a correlation between the difficulty difference and the comment contribution
    print('Difficulty Difference and Comment Contribution')
    print(combined_data[['Difficulty Difference', 'Comment Contribution']].corr(method='spearman'))

