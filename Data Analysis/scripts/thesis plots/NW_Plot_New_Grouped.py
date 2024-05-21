import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import config

# Load the data
file_path = config.PATH_LINEARITY_METRICS + '/NW_Metrics_All.csv'
data = pd.read_csv(file_path)

# Relevant columns for global metrics
global_metrics_columns = ['Type', 'Story_Global_Naive', 'Exec_Global_Naive',
                          'Story_Global_Dynamic', 'Exec_Global_Dynamic']

# Processing the data
grouped_data = data[global_metrics_columns].groupby('Type').mean().reset_index()
melted_data = pd.melt(grouped_data, id_vars=['Type'],
                      value_vars=global_metrics_columns[1:],
                      var_name='Metric', value_name='Value')


sorted_tasks = sorted(melted_data['Type'].unique())

# Reordering the dataframe
sorted_melted_data = pd.DataFrame()
for task in sorted_tasks:
    sorted_melted_data = pd.concat([sorted_melted_data, melted_data[melted_data['Type'] == task]])

# Defining markers and adjusting task positions
markers = ["o", "s", "^", "D"]  # Different shapes for each metric
task_positions = {}
current_position = 0
for i in range(1, 2):  # Assuming 1 tasks
    task_cm = f"CM"
    task_cp = f"CP"
    task_positions[task_cm] = current_position
    task_positions[task_cp] = current_position + 1

# Reverse the task positions
task_positions = {task: max(task_positions.values()) - pos for task, pos in task_positions.items()}

# Creating the plot
plt.figure(figsize=(10, 3))
# set font size
plt.rcParams.update({'font.size': 16})
for metric, marker in zip(global_metrics_columns[1:], markers):
    metric_data = sorted_melted_data[sorted_melted_data['Metric'] == metric].copy()
    metric_data['Position'] = metric_data['Type'].map(task_positions)
    sns.set_palette(sns.color_palette("rocket", 4))
    sns.scatterplot(x='Value', y='Position', data=metric_data, label=metric, marker=marker, s=100)

# Connecting all points with their respective point in the other type
#for i in range(1, 2):
task_cm = f"CM"
task_cp = f"CP"
cm_data = sorted_melted_data[sorted_melted_data['Type'] == task_cm].copy()
cp_data = sorted_melted_data[sorted_melted_data['Type'] == task_cp].copy()
for cm_value, cp_value in zip(cm_data['Value'], cp_data['Value']):
    plt.plot([cm_value, cp_value], [task_positions[task_cm], task_positions[task_cp]], color='gray', linestyle='--', linewidth=1)


plt.yticks(list(task_positions.values()), list(task_positions.keys()))
plt.xlabel('N-W Score')
plt.ylabel('')
plt.legend(title='Metric', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save the plot
plt.savefig('/Users/Youssef/Desktop/NW_Plot_New_Grouped.pdf', dpi=600)

plt.show()