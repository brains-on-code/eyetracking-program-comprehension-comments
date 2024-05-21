from statsmodels.regression.mixed_linear_model import MixedLM
import statsmodels.api as sm
import pandas as pd

# Load the data from the provided CSV file
file_path = '/Users/Youssef/Development/BA Comments/Data Analysis/output/Effect_of_Comments/Results/CombinedResults.csv'
data = pd.read_csv(file_path)
# convert correct column to int using .loc[row_indexer,col_indexer] = value
data.loc[:, 'Correct'] = data.loc[:, 'Correct'].astype(int)

# Preparing a report for the individual task models
individual_task_results = []

# Iterate through each task
for task_number in data['Task_Number'].unique():
    # Filter data for the specific task
    task_data = data[data['Task_Number'] == task_number]

    # Mixed Linear Model for Correctness for each task
    model_correctness_task = MixedLM.from_formula("Correct ~ Task_Type", task_data, groups=task_data["SubjectID"])
    result_correctness_task = model_correctness_task.fit()

    # Mixed Linear Model for Time for each task
    model_time_task = MixedLM.from_formula("Time ~ Task_Type", task_data, groups=task_data["SubjectID"])
    result_time_task = model_time_task.fit()

    # Append the results
    individual_task_results.append({
        'Task_Number': task_number,
        'Correctness_Intercept': result_correctness_task.params['Intercept'],
        'Correctness_Effect_of_CP': result_correctness_task.params['Task_Type[T.CP]'],
        'Correctness_P_Value': result_correctness_task.pvalues['Task_Type[T.CP]'],
        'Time_Intercept': result_time_task.params['Intercept'],
        'Time_Effect_of_CP': result_time_task.params['Task_Type[T.CP]'],
        'Time_P_Value': result_time_task.pvalues['Task_Type[T.CP]']
    })

# Convert the results to a DataFrame
individual_task_results_df = pd.DataFrame(individual_task_results)

# Print the results
print(individual_task_results_df)