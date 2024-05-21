import os

import pandas as pd
from scipy.stats import wilcoxon
from statsmodels.stats.multitest import multipletests

import config


def calculate_visual_attention_stats():
    visual_attention_metrics_by_task = pd.read_csv(
        config.PATH_VISUAL_ATTENTION_METRICS + '/VisualAttention_Metrics_All.csv')

    metrics_map = {'AllFixations_Count': 'two-sided',
                   'AllFixations_Duration': 'two-sided',
                   'AoiFixations_Count': 'two-sided',
                   'AoiFixations_Duration': 'two-sided',
                   'CodeFixations_Count': 'less',
                   'CodeFixations_Duration': 'less',
                   'CommentFixations_Count': 'greater',
                   'CommentFixations_Duration': 'greater',
                   }

    results = pd.DataFrame(columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])

    for metric_to_be_tested, alternative in metrics_map.items():
        print('Metric: ' + metric_to_be_tested)

        cp_data = visual_attention_metrics_by_task.loc[
            visual_attention_metrics_by_task['Task'].str.contains('CP'), metric_to_be_tested]
        cm_data = visual_attention_metrics_by_task.loc[
            visual_attention_metrics_by_task['Task'].str.contains('CM'), metric_to_be_tested]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(cp_data, cm_data, alternative=alternative)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_to_be_tested}:')
        print(f't = {stat}, p = {p_value}')
        print(f'CP: {cp_data.mean()}')
        print(f'CM: {cm_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if alternative == 'two-sided':
            if p_value < alpha:
                print(f'The difference in {metric_to_be_tested} between CP and CM is statistically significant. \n')
            else:
                print(f'The difference in {metric_to_be_tested} between CP and CM is not statistically significant. \n')
        elif alternative == 'less':
            if p_value < alpha:
                print(f'CP has a significantly negative effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly negative effect on {metric_to_be_tested}.')
        elif alternative == 'greater':
            if p_value < alpha:
                print(f'CP has a significantly positive effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly positive effect on {metric_to_be_tested}.')

        # Save the results
        results = pd.concat([results, pd.DataFrame(
            [[metric_to_be_tested, alternative, cm_data.mean(), cp_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(results['P-Value'], alpha=0.05, method='fdr_bh')
    results['Corrected P-Value'] = statsmodels_results[1]
    results['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_VISUAL_ATTENTION_METRICS_STATISTICS):
        os.makedirs(config.PATH_VISUAL_ATTENTION_METRICS_STATISTICS)

    results = results.round(3)
    results.to_csv(config.PATH_VISUAL_ATTENTION_METRICS_STATISTICS + '/Visual_Attention_By_Task.csv', index=False)


def calculate_linearity_stats():
    linearity_metrics_by_task = pd.read_csv(config.PATH_LINEARITY_METRICS + '/Linearity_Metrics_By_Task.csv')

    metrics_map = {'VerticalNext': 'two-sided',
                   'VerticalLater': 'two-sided',
                   'Regression': 'two-sided',
                   'HorizontalLater': 'two-sided',
                   'LineRegression': 'two-sided',
                   'SaccadeLength': 'two-sided'
                   }

    results_task = pd.DataFrame(columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])

    for metric_to_be_tested, alternative in metrics_map.items():
        print('Metric: ' + metric_to_be_tested)

        cp_task_data = linearity_metrics_by_task.loc[
            linearity_metrics_by_task['Task'].str.contains('CP'), metric_to_be_tested]
        cm_task_data = linearity_metrics_by_task.loc[
            linearity_metrics_by_task['Task'].str.contains('CM'), metric_to_be_tested]

        # Perform the Wilcoxon Signed Rank Test
        stat_task, p_value_task = wilcoxon(cp_task_data, cm_task_data, alternative=alternative)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_to_be_tested} between Task CP and Task CM:')
        print(f't = {stat_task}, p = {p_value_task}')
        print(f'CP: {cp_task_data.mean()}')
        print(f'CM: {cm_task_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if alternative == 'two-sided':
            if p_value_task < alpha:
                print(f'The difference in {metric_to_be_tested} between CP and CM is statistically significant. \n')
            else:
                print(f'The difference in {metric_to_be_tested} between CP and CM is not statistically significant. \n')
        elif alternative == 'less':  # one-tailed, negative effect
            if p_value_task < alpha:
                print(f'CP has a significantly negative effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly negative effect on {metric_to_be_tested}.')
        elif alternative == 'greater':  # one-tailed, positive effect
            if p_value_task < alpha:
                print(f'CP has a significantly positive effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly positive effect on {metric_to_be_tested}.')

        # Save the results
        results_task = pd.concat([results_task, pd.DataFrame(
            [[metric_to_be_tested, alternative, cm_task_data.mean(), cp_task_data.mean(), stat_task, p_value_task]],
            columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(results_task['P-Value'], alpha=0.05, method='fdr_bh')
    results_task['Corrected P-Value'] = statsmodels_results[1]
    results_task['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_LINEARITY_METRICS_STATISTICS):
        os.makedirs(config.PATH_LINEARITY_METRICS_STATISTICS)

    results_task = results_task.round(3)
    results_task.to_csv(config.PATH_LINEARITY_METRICS_STATISTICS + '/Linearity_By_Task.csv', index=False)


def calculate_nw_stats():
    nw_by_task = pd.read_csv(config.PATH_LINEARITY_METRICS + '/NW_Metrics_By_Task.csv')
    nw_by_task = nw_by_task.loc[:, ~nw_by_task.columns.str.contains('_Reps')]

    # calculate_code_only_cm_cp(nw_by_task)
    calculate_naive_dynamic_cp(nw_by_task)
    calculate_story_exec_cp(nw_by_task)
    calculate_code_first_comment_first_cp(nw_by_task)


def calculate_code_only_cm_cp(nw_by_task):
    # keep only the code-only metrics and task columns
    nw_by_task = nw_by_task.loc[:, nw_by_task.columns.str.contains('CodeOnly|Task')]
    # save grouped csv
    nw_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/CodeOnly_By_Task.csv', index=False)

    code_only_cm_cp_metrics = {'Story_CodeOnly_Naive': 'less',
                               'Exec_CodeOnly_Naive': 'less',
                               'Story_CodeOnly_Dynamic': 'less',
                               'Exec_CodeOnly_Dynamic': 'less',
                               }
    code_only_cm_cp_results = pd.DataFrame(
        columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])

    for metric_to_be_tested, alternative in code_only_cm_cp_metrics.items():
        print('Metric: ' + metric_to_be_tested)

        cp_data = nw_by_task.loc[nw_by_task['Task'].str.contains('CP'), metric_to_be_tested]
        cm_data = nw_by_task.loc[nw_by_task['Task'].str.contains('CM'), metric_to_be_tested]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(cp_data, cm_data, alternative=alternative)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_to_be_tested}:')
        print(f't = {stat}, p = {p_value}')
        print(f'CP: {cp_data.mean()}')
        print(f'CM: {cm_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if alternative == 'two-sided':
            if p_value < alpha:
                print(f'The difference in {metric_to_be_tested} between CP and CM is statistically significant. \n')
            else:
                print(f'The difference in {metric_to_be_tested} between CP and CM is not statistically significant. \n')
        elif alternative == 'less':
            if p_value < alpha:
                print(f'CP has a significantly negative effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly negative effect on {metric_to_be_tested}.')
        elif alternative == 'greater':
            if p_value < alpha:
                print(f'CP has a significantly positive effect on {metric_to_be_tested}.')
            else:
                print(f'CP does not have a significantly positive effect on {metric_to_be_tested}.')

        # Save the results
        code_only_cm_cp_results = pd.concat([code_only_cm_cp_results, pd.DataFrame(
            [[metric_to_be_tested, alternative, cm_data.mean(), cp_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'CM Mean', 'CP Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(code_only_cm_cp_results['P-Value'], alpha=0.05, method='fdr_bh')
    code_only_cm_cp_results['Corrected P-Value'] = statsmodels_results[1]
    code_only_cm_cp_results['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS)

    code_only_cm_cp_results = code_only_cm_cp_results.round(3)
    code_only_cm_cp_results.to_csv(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS + '/CodeOnly_By_Task.csv', index=False)


def calculate_naive_dynamic_cp(nw_by_task):
    nw_by_task = nw_by_task.loc[:, nw_by_task.columns.str.contains('Task|Naive|Dynamic')]
    # save grouped csv
    nw_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/NaiveDynamic_By_Task.csv', index=False)
    # here we want to compare the naive and dynamic scores for each task within each task
    naive_column_names = [col for col in nw_by_task.columns if 'Naive' in col and 'Global' not in col and 'CodeOnly' not in col]
    dynamic_column_names = [col for col in nw_by_task.columns if 'Dynamic' in col and 'Global' not in col and 'CodeOnly' not in col]

    naive_dynamic_results = pd.DataFrame(
        columns=['Metric', 'Effect Direction', 'Naive Mean', 'Dynamic Mean', 'Statistic', 'P-Value'])

    for naive_column_name, dynamic_column_name in zip(naive_column_names, dynamic_column_names):
        metric_name = naive_column_name.split('_Naive')[0]
        print('Metric: ' + metric_name)

        naive_data = nw_by_task[naive_column_name]
        dynamic_data = nw_by_task[dynamic_column_name]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(naive_data, dynamic_data)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_name}:')
        print(f't = {stat}, p = {p_value}')
        print(f'Naive: {naive_data.mean()}')
        print(f'Dynamic: {dynamic_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if p_value < alpha:
            print(f'Naive Calculation has a significantly negative effect on {metric_name}.')
        else:
            print(f'Naive Calculation does not have a significantly negative effect on {metric_name}.')

        # Save the results
        naive_dynamic_results = pd.concat([naive_dynamic_results, pd.DataFrame(
            [[metric_name, 'two-sided', naive_data.mean(), dynamic_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'Naive Mean', 'Dynamic Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(naive_dynamic_results['P-Value'], alpha=0.05, method='fdr_bh')
    naive_dynamic_results['Corrected P-Value'] = statsmodels_results[1]
    naive_dynamic_results['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS)

    naive_dynamic_results = naive_dynamic_results.round(3)
    naive_dynamic_results.to_csv(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS + '/NaiveDynamic_By_Task.csv', index=False)


def calculate_story_exec_cp(nw_by_task):
    nw_by_task = nw_by_task.loc[:, nw_by_task.columns.str.contains('Task|Story|Exec')]
    # save grouped csv
    nw_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/StoryExec_By_Task.csv', index=False)
    # here we want to compare the story and exec scores for each task within each task
    story_column_names = [col for col in nw_by_task.columns if 'Story' in col and 'Global' not in col and 'CodeOnly' not in col]
    exec_column_names = [col for col in nw_by_task.columns if 'Exec' in col and 'Global' not in col and 'CodeOnly' not in col]

    story_exec_results = pd.DataFrame(
        columns=['Metric', 'Effect Direction', 'Story Mean', 'Exec Mean', 'Statistic', 'P-Value'])

    for story_column_name, exec_column_name in zip(story_column_names, exec_column_names):
        metric_name = story_column_name.split('Story_')[1]
        print('Metric: ' + metric_name)

        story_data = nw_by_task[story_column_name]
        exec_data = nw_by_task[exec_column_name]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(story_data, exec_data)

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_name}:')
        print(f't = {stat}, p = {p_value}')
        print(f'Story: {story_data.mean()}')
        print(f'Exec: {exec_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if p_value < alpha:
            print(f'Story has a significantly negative effect on {metric_name}.')
        else:
            print(f'Story does not have a significantly negative effect on {metric_name}.')

        # Save the results
        story_exec_results = pd.concat([story_exec_results, pd.DataFrame(
            [[metric_name, 'two-sided', story_data.mean(), exec_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'Story Mean', 'Exec Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(story_exec_results['P-Value'], alpha=0.05, method='fdr_bh')
    story_exec_results['Corrected P-Value'] = statsmodels_results[1]
    story_exec_results['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS)

    story_exec_results = story_exec_results.round(3)
    story_exec_results.to_csv(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS + '/StoryExec_By_Task.csv', index=False)


def calculate_code_first_comment_first_cp(nw_by_task):
    nw_by_task = nw_by_task.loc[:, nw_by_task.columns.str.contains('Task|CodeFirst|CommentFirst')]
    # save grouped csv
    nw_by_task.to_csv(config.PATH_LINEARITY_METRICS + '/CodeFirstCommentFirst_By_Task.csv', index=False)
    # here we want to compare the code-first and comment-first scores for each task within each task
    code_first_column_names = [col for col in nw_by_task.columns if 'CodeFirst' in col]
    comment_first_column_names = [col for col in nw_by_task.columns if 'CommentFirst' in col]

    code_first_comment_first_cp_results = pd.DataFrame(
        columns=['Metric', 'Effect Direction', 'CodeFirst Mean', 'CommentFirst Mean', 'Statistic', 'P-Value'])

    for code_first_column_name, comment_first_column_name in zip(code_first_column_names, comment_first_column_names):
        metric_name = code_first_column_name.split('_CodeFirst_')[0] + '_' + \
                      code_first_column_name.split('_CodeFirst_')[1]
        print('Metric: ' + metric_name)

        code_first_data = nw_by_task[code_first_column_name]
        comment_first_data = nw_by_task[comment_first_column_name]

        # Perform the Wilcoxon Signed Rank Test
        stat, p_value = wilcoxon(code_first_data, comment_first_data, alternative='two-sided')

        # Output the test results
        print(f'Wilcoxon Signed Rank Test for {metric_name}:')
        print(f't = {stat}, p = {p_value}')
        print(f'CodeFirst: {code_first_data.mean()}')
        print(f'CommentFirst: {comment_first_data.mean()} \n')

        alpha = 0.05
        # print if one-tailed or two-tailed and direction of effect
        if p_value < alpha:
            print(f'CodeFirst has a significantly negative effect on {metric_name}.')
        else:
            print(f'CodeFirst does not have a significantly negative effect on {metric_name}.')

        # Save the results
        code_first_comment_first_cp_results = pd.concat([code_first_comment_first_cp_results, pd.DataFrame(
            [[metric_name, 'two-sided', code_first_data.mean(), comment_first_data.mean(), stat, p_value]],
            columns=['Metric', 'Effect Direction', 'CodeFirst Mean', 'CommentFirst Mean', 'Statistic', 'P-Value'])])

    # perform FDR correction for multiple comparisons
    statsmodels_results = multipletests(code_first_comment_first_cp_results['P-Value'], alpha=0.05, method='fdr_bh')
    code_first_comment_first_cp_results['Corrected P-Value'] = statsmodels_results[1]
    code_first_comment_first_cp_results['Reject Null Hypothesis'] = statsmodels_results[0]

    # Save the results to a csv file
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS)

    code_first_comment_first_cp_results = code_first_comment_first_cp_results.round(3)
    code_first_comment_first_cp_results.to_csv(
        config.PATH_GAZE_STRATEGY_METRICS_STATISTICS + '/CodeFirstCommentFirst_By_Task.csv', index=False)


def calculate_gaze_strategy_stats():
    gaze_strategy_metrics_by_task = pd.read_csv(
        config.PATH_GAZE_STRATEGY_METRICS + '/GazeStrategy_Metrics_By_Task.csv')

    # here we want to compare the code-first and comment-first scores for each task within each task
    code_to_comment_data = gaze_strategy_metrics_by_task['CodeToComment_Count']
    comment_to_code_data = gaze_strategy_metrics_by_task['CommentToCode_Count']

    # Perform the Wilcoxon Signed Rank Test
    stat, p_value = wilcoxon(code_to_comment_data, comment_to_code_data, alternative='two-sided')

    # Output the test results
    print(f'Wilcoxon Signed Rank Test for CodeToComment and CommentToCode:')
    print(f't = {stat}, p = {p_value}')
    print(f'CodeToComment: {code_to_comment_data.mean()}')
    print(f'CommentToCode: {comment_to_code_data.mean()} \n')

    alpha = 0.05
    # print if one-tailed or two-tailed and direction of effect
    if p_value < alpha:
        print(
            f'The difference between CodeToComment and CommentToCode is statistically significant. \n')
    else:
        print(
            f'The difference between CodeToComment and CommentToCode is not statistically significant. \n')

    # Save the results to a csv file
    if not os.path.exists(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS):
        os.makedirs(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS)

    results = pd.DataFrame(
        columns=['Metric', 'Effect Direction', 'CodeToComment Mean', 'CommentToCode Mean', 'Statistic', 'P-Value'])
    results = pd.concat([results, pd.DataFrame(
        [['Gaze Strategy', 'two-sided', code_to_comment_data.mean(), comment_to_code_data.mean(), stat,
          p_value]],
        columns=['Metric', 'Effect Direction', 'CodeToComment Mean', 'CommentToCode Mean', 'Statistic', 'P-Value'])])

    results = results.round(3)
    results.to_csv(config.PATH_GAZE_STRATEGY_METRICS_STATISTICS + '/GazeStrategy_By_Task.csv', index=False)
