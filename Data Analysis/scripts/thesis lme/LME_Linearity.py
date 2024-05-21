import pandas as pd
import statsmodels.formula.api as smf
from numpy.linalg import LinAlgError
from statsmodels.stats.multitest import multipletests

import config

# Load your data
va_path = config.PATH_LINEARITY_METRICS + '/NW_Metrics_All.csv'
data = pd.read_csv(va_path)

# Split 'Task' into 'TaskID' and 'Type' if needed
data[['TaskID', 'Type']] = data['Task'].str.extract(r'(Task\d+)(CM|CP)')

# keep only the relevant columns
data = data[['Participant', 'TaskID', 'Type', 'Story_Global_Naive', 'Exec_Global_Naive', 'Story_Global_Dynamic',
             'Exec_Global_Dynamic']]

# Define the metrics to analyze
metrics = [
    'Story_Global_Naive', 'Exec_Global_Naive',
    'Story_Global_Dynamic', 'Exec_Global_Dynamic',
]


# Function to fit models and extract info
def fit_models_and_extract_info(data, metrics):
    task_results = {}

    # Iterate through each task
    for task_id in data['TaskID'].unique():
        task_data = data[data['TaskID'] == task_id]
        task_results[task_id] = {}

        # Iterate through each metric
        for metric in metrics:
            model = smf.mixedlm(f"{metric} ~ Type", task_data, groups=task_data["Participant"])
            try:
                result = model.fit()
            except LinAlgError:
                result = model.fit(method=['powell', 'lbfgs'])

            # Extract relevant information
            intercept = result.params.get('Intercept', 0)
            effect_cp = result.params.get('Type[T.CP]', 0)
            p_value = result.pvalues.get('Type[T.CP]', 1)

            # Store in structured dictionary
            task_results[task_id][metric] = {'intercept': intercept, 'effect_cp': effect_cp, 'p_value': p_value}

    # Apply FDR correction and format results
    for task_id, metrics in task_results.items():
        p_values = [info['p_value'] for info in metrics.values()]
        _, corrected, _, _ = multipletests(p_values, method='fdr_bh')

        for metric, corr_p, in zip(metrics.keys(), corrected):
            task_results[task_id][metric]['corrected_p_value'] = corr_p

    return task_results

def fit_models_and_extract_info_overall(data, metrics):
    task_results = {}

    # Iterate through each metric
    for metric in metrics:
        model = smf.mixedlm(f"{metric} ~ Type", data, groups=data["Participant"])
        try:
            result = model.fit()
        except LinAlgError:
            result = model.fit(method=['powell', 'lbfgs'])

        # Extract relevant information
        intercept = result.params.get('Intercept', 0)
        effect_cp = result.params.get('Type[T.CP]', 0)
        p_value = result.pvalues.get('Type[T.CP]', 1)

        # Store in structured dictionary
        task_results[metric] = {'intercept': intercept, 'effect_cp': effect_cp, 'p_value': p_value}

    # Apply FDR correction and format results
    p_values = [info['p_value'] for info in task_results.values()]
    _, corrected, _, _ = multipletests(p_values, method='fdr_bh')

    for metric, corr_p, in zip(task_results.keys(), corrected):
        task_results[metric]['corrected_p_value'] = corr_p

    return task_results


# Fit models and extract info
extracted_info = fit_models_and_extract_info(data, metrics)

# Convert the results with the dictionaries to a DataFrame
# make the columns a multiindex
extracted_info_df = pd.DataFrame.from_dict({(i, j): extracted_info[i][j]
                                            for i in extracted_info.keys()
                                            for j in extracted_info[i].keys()},
                                           orient='index')
# save the results
extracted_info_df.to_csv('/Users/Youssef/Desktop/ExtractedInfo.csv')
