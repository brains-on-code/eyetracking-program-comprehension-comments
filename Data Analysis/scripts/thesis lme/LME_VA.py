import pandas as pd
import statsmodels.formula.api as smf
from numpy.linalg import LinAlgError
from statsmodels.stats.multitest import multipletests

# Load your data
va_path = '/Users/Youssef/Development/BA Comments/Data Analysis/output/Effect_of_Comments/AOIMetrics/VisualAttention/VisualAttention_Metrics_All.csv'
data = pd.read_csv(va_path)

# Split 'Task' into 'TaskID' and 'Type' if needed
data[['TaskID', 'Type']] = data['Task'].str.extract(r'(Task\d+)(CM|CP)')

# Define the metrics to analyze
metrics = [
    "AllFixations_Count", "AllFixations_Duration",
    "AoiFixations_Count", "AoiFixations_Duration",
    "CodeFixations_Count", "CodeFixations_Duration",
    "CommentFixations_Count", "CommentFixations_Duration"
]


# Function to fit models and extract p-values
def fit_models_and_extract_info(data, metrics):
    task_results = {}

    # Iterate through each task
    for task_id in data['TaskID'].unique():
        task_data = data[data['TaskID'] == task_id]
        task_results[task_id] = {}

        # Fit models for each metric and store p-values
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


# Fit models and extract info
task_results = fit_models_and_extract_info(data, metrics)

# Convert to DataFrame
task_results_df = pd.DataFrame.from_dict({(i, j): task_results[i][j]
                                           for i in task_results.keys()
                                           for j in task_results[i].keys()},
                                         orient='index')

# save the results
task_results_df.to_csv('/Users/Youssef/Desktop/LME_VA.csv')
