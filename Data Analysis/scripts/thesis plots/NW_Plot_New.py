import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import config

# Load the data
file_path = config.PATH_LINEARITY_METRICS + '/NW_Metrics_All.csv'
data = pd.read_csv(file_path)

# Relevant columns for global metrics
global_metrics_columns = ['Task', 'Story_Global_Naive', 'Exec_Global_Naive',
                          'Story_Global_Dynamic', 'Exec_Global_Dynamic']

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

# Defining markers and adjusting task positions
markers = ["o", "s", "^", "D"]  # Different shapes for each metric
task_positions = {}
current_position = 0
for i in range(1, 13):  # Assuming 12 tasks
    task = f"Snippet {i}"
    task_cm = f"{i} CM"
    task_cp = f"{i} CP"
    task_positions[task] = current_position
    task_positions[task_cm] = current_position + 4
    task_positions[task_cp] = current_position + 8
    current_position += 14

# Reverse the task positions
task_positions = {task: max(task_positions.values()) - pos for task, pos in task_positions.items()}


def getPositions(metric_data, task_positions):
    positions = []
    for index, row in metric_data.iterrows():
        task = row['Task']
        task_number = task[4:-2]
        if 'CM' in task:
            task = f"{task_number} CM"
        elif 'CP' in task:
            task = f"{task_number} CP"
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

# Connecting all cm points with their respective cp point with a dashed line in the color of the metric
for i in range(1, 13):
    task_cm = f"Task{i}CM"
    task_cp = f"Task{i}CP"
    task_cm_data = sorted_melted_data[sorted_melted_data['Task'] == task_cm]
    task_cp_data = sorted_melted_data[sorted_melted_data['Task'] == task_cp]
    for metric in global_metrics_columns[1:]:
        metric_cm_data = task_cm_data[task_cm_data['Metric'] == metric]
        metric_cp_data = task_cp_data[task_cp_data['Metric'] == metric]
        plt.plot([metric_cm_data['Value'].values[0], metric_cp_data['Value'].values[0]],
                 [task_positions[f'{i} CM'], task_positions[f'{i} CP']],
                 linestyle='--', linewidth=2, color=sns.color_palette("rocket", 4)[global_metrics_columns[1:].index(metric)])

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
plt.legend(loc='upper center', ncol=4, frameon=False, borderaxespad=0, bbox_to_anchor=(0.5, 1.05))
plt.tight_layout()

# Save the plot
plt.savefig('/Users/Youssef/Desktop/NW_Plot_New_Connected.pdf', dpi=600)

plt.show()