import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config

# Load the data
file_path = config.PATH_LINEARITY_METRICS + '/NW_Metrics_All.csv'
data = pd.read_csv(file_path)

# Relevant columns for global metrics
global_metrics_columns = ['Task', 'Story_CodeFirst_Naive', 'Exec_CodeFirst_Naive', 'Story_CodeFirst_Dynamic',
                          'Exec_CodeFirst_Dynamic',
                          'Story_CommentFirst_Naive', 'Exec_CommentFirst_Naive', 'Story_CommentFirst_Dynamic',
                          'Exec_CommentFirst_Dynamic', ]
# 'Story_CodeOnly_Naive', 'Exec_CodeOnly_Naive', 'Story_CodeOnly_Dynamic',
# 'Exec_CodeOnly_Dynamic']

# Processing the data
grouped_data = data[global_metrics_columns].groupby('Task').mean().reset_index()
melted_data = pd.melt(grouped_data, id_vars=['Task'],
                      value_vars=global_metrics_columns[1:],
                      var_name='Metric', value_name='Value')


# Sort the tasks in a specific order
def custom_task_sort(task):
    number = int(task[4:-2])
    task_type = task[-2:]
    return (number, task_type)


sorted_tasks = sorted(melted_data['Task'].unique(), key=custom_task_sort)

# Reordering the dataframe
sorted_melted_data = pd.DataFrame()
for task in sorted_tasks:
    sorted_melted_data = pd.concat([sorted_melted_data, melted_data[melted_data['Task'] == task]])

# remove CM Tasks
sorted_melted_data = sorted_melted_data[~sorted_melted_data['Task'].str.contains('CM')]

# Defining markers and adjusting task positions
markers = ["o", "s", "^", "D"]  # Different shapes for each metric
markers = markers * 2
task_positions = {}
current_position = 0
for i in range(1, 13):  # Assuming 12 tasks
    task = f"Snippet {i}"
    task_code_first = f"{i} Code First"
    task_comment_first = f"{i} Comment First"
    # task_code_only = f"{i} Code Only"
    task_positions[task] = current_position
    task_positions[task_code_first] = current_position + 4
    task_positions[task_comment_first] = current_position + 8
    # task_positions[task_code_only] = current_position + 4
    current_position += 14

# Reverse the task positions
task_positions = {task: max(task_positions.values()) - pos for task, pos in task_positions.items()}


def getPositions(metric_data, task_positions):
    positions = []
    for index, row in metric_data.iterrows():
        task = row['Task']
        task_number = task[4:-2]
        metric = row['Metric']
        if 'CodeFirst' in metric:
            task = f"{task_number} Code First"
        elif 'CommentFirst' in metric:
            task = f"{task_number} Comment First"
        # elif 'CodeOnly' in metric:
        #    task = f"{task_number} Code Only"
        positions.append(task_positions[task])
    return positions


# Creating the plot
plt.figure(figsize=(25, 25))
# set font size
plt.rcParams.update({'font.size': 28})
for metric, marker in zip(global_metrics_columns[1:], markers):
    metric_data = sorted_melted_data[sorted_melted_data['Metric'] == metric].copy()
    metric_data['Position'] = getPositions(metric_data, task_positions)
    sns.set_palette(sns.color_palette("rocket", 4))
    sns.scatterplot(x='Value', y='Position', data=metric_data, label=metric, marker=marker, s=200)

# Connecting each code first with each respective comment first metric for each task with a dashed line in the color of the metric
for i in range(1, 13):
    task_data = sorted_melted_data[sorted_melted_data['Task'] == f"Task{i}CP"]
    for metric in ['Story', 'Exec']:
        for type in ['Naive', 'Dynamic']:
            code_first_data = task_data[task_data['Metric'] == f"{metric}_CodeFirst_{type}"]
            comment_first_data = task_data[task_data['Metric'] == f"{metric}_CommentFirst_{type}"]
            plt.plot([code_first_data['Value'].values[0], comment_first_data['Value'].values[0]],
                     [task_positions[f"{i} Code First"], task_positions[f"{i} Comment First"]],
                     linestyle='--', linewidth=2, color=sns.color_palette("rocket", 4)[
                global_metrics_columns[1:].index(f"{metric}_CodeFirst_{type}")])
# all horizontal lines for each task
for task, pos in task_positions.items():
    if 'Snippet' in task:
        continue
    plt.axhline(y=pos, color='gray', linestyle='--', linewidth=1, alpha=0.3)

# remove task number from task position metrics (1 Code First -> Code First, but keep Task 1)
y_ticks = {}
for task, pos in task_positions.items():
    if 'Snippet' in task:
        y_ticks[pos] = task
    else:
        y_ticks[pos] = task[2:]

plt.yticks(list(y_ticks.keys()), list(y_ticks.values()))
plt.xlabel('N-W Score')
plt.ylabel('')
# make legend outside the plot on the top and one line with no padding to the plot
plt.legend(loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.5, 1.125))
plt.tight_layout()

# Save the plot
plt.savefig('/Users/Youssef/Desktop/NW_Plot_Gaze_Strategy.pdf', dpi=600)

plt.show()
