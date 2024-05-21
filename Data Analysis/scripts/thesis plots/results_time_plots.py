# Load the correctness data from results per task
import numpy as np
import pandas as pd
from adjustText import adjust_text
from matplotlib import pyplot as plt

import config

correctness_file_path_new = '/Users/Youssef/Development/BA Comments/Data Analysis/output/Effect_of_Comments/Results/CombinedResultsByTask.csv'
correctness_data_new = pd.read_csv(correctness_file_path_new)
pastel_colors_swapped = {'CM': '#FFB347', 'CP': '#77DD77'}

# Splitting the 'Task' field into separate 'Task' and 'Type' fields
correctness_data_new[['Task', 'Type']] = correctness_data_new['Task'].str.extract(r'(Task\d+)(CM|CP)')

# Grouping the data by task and type, then calculating the mean correctness
mean_correctness_per_task_new = correctness_data_new.groupby(['Task', 'Type']).mean()['Time'].unstack()

# Extracting the correctness data for the scatter plot
X_correctness_new = mean_correctness_per_task_new.values


# Function to calculate perpendicular distance from the line y = x for correctness data
def distance_from_diagonal_correctness_new(point):
    x, y = point
    return (y - x) / np.sqrt(2)  # Distance from y = x


# Calculating the distances for each task in the correctness data
distances_correctness_new = np.apply_along_axis(distance_from_diagonal_correctness_new, 1, X_correctness_new)

# Creating the plot with increased font size and black crosses on the diagonal
fig, ax = plt.subplots(figsize=(8, 8))

# Removing the grids
ax.grid(False)
plt.rcParams['font.size'] = 16

# Plotting each lollipop with the specified pastel colors
for i, point in enumerate(X_correctness_new):
    x, y = point
    distance = distance_from_diagonal_correctness_new(point)
    color = 'black' if (-10 <= distance <= 10) else pastel_colors_swapped['CM'] if distance > 10 else \
    pastel_colors_swapped['CP'] if distance < -10 else 'lightgrey'

    # Plotting the line from the diagonal to the point (with swapped axes)
    ax.plot([x, x], [x, y], color=color, alpha=0.9, linewidth=1.5)

    # Plotting the circle (with swapped axes)
    ax.scatter(x, y, color=color, alpha=0.9, s=50)

# Swapped labels for the axes with increased font size
ax.set_xlabel('Mean Time for Comments Missing (CM) in s', fontsize=16)
ax.set_ylabel('Mean Time for Comments Present (CP) in s', fontsize=16)
ax.set_xlim(0, 400)
ax.set_ylim(0, 400)
ax.set_xticks(range(0, 401, 50))
ax.set_yticks(range(0, 401, 50))
# set the font size of the ticks on the axes
ax.tick_params(axis='both', which='major', labelsize=16)

# Plotting the diagonal line in light gray
ax.plot([0, 400], [0, 400], color='lightgray', linestyle='--')

# Adding task labels with increased font size
texts = []
for i, point in enumerate(X_correctness_new):
    # strip 'Task' from task name
    task_name = mean_correctness_per_task_new.index[i].strip('Task')
    text = ax.text(point[0] + 5, point[1], task_name, fontsize=16, ha='left')
    texts.append(text)

adjust_text(texts)

# File path for saving with corrected axes labels and increased font size
correctness_plot_file_path_corrected_new = '/Users/Youssef/Desktop/Time_Scatter_Plot.pdf'
fig.savefig(correctness_plot_file_path_corrected_new, bbox_inches='tight', dpi=600)