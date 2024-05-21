# Load the correctness data from results per task
import numpy as np
import pandas as pd
from adjustText import adjust_text
from matplotlib import pyplot as plt

import config

ratings_file_path = '/Users/Youssef/Development/BA Comments/Data Analysis/output/Effect_of_Comments/Ratings/CombinedDifficulties.csv'
ratings_data = pd.read_csv(ratings_file_path)
pastel_colors_swapped = {'CM': '#FFB347', 'CP': '#77DD77'}

mean_difficulty_per_task = ratings_data.groupby(['Task', 'Type']).mean().unstack()
mean_difficulty_per_task.columns = mean_difficulty_per_task.columns.droplevel()

# Extracting the data for clustering
X_task = mean_difficulty_per_task.values


# Function to calculate perpendicular distance from the line y = x for correctness data
def distance_from_diagonal_correctness_new(point):
    x, y = point
    return (y - x) / np.sqrt(2)  # Distance from y = x


# Calculating the distances for each task in the correctness data
distances_correctness_new = np.apply_along_axis(distance_from_diagonal_correctness_new, 1, X_task)

# Creating the plot with increased font size and black crosses on the diagonal
fig, ax = plt.subplots(figsize=(8, 8))

# Removing the grids
ax.grid(False)
plt.rcParams['font.size'] = 16


# Plotting each lollipop with the specified pastel colors
for i, point in enumerate(X_task):
    x, y = point
    distance = distance_from_diagonal_correctness_new(point)
    color = 'black' if (-0.25 <= distance <= 0.25) else pastel_colors_swapped['CM'] if distance > 0.25 else \
    pastel_colors_swapped['CP'] if distance < -0.25 else 'lightgrey'

    # Plotting the line from the diagonal to the point (with swapped axes)
    ax.plot([x, x], [x, y], color=color, alpha=0.9, linewidth=3)

    # Plotting the circle (with swapped axes)
    ax.scatter(x, y, color=color, alpha=0.9, s=80)

# Swapped labels for the axes with increased font size
ax.set_xlabel('Mean Difficulty for Comments Missing (CM) in %', fontsize=16)
ax.set_ylabel('Mean Difficulty for Comments Present (CP) in %', fontsize=16)
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)
ax.set_xticks(range(0, 6, 1))
ax.set_yticks(range(0, 6, 1))
# set the font size of the ticks on the axes
ax.tick_params(axis='both', which='major', labelsize=16)

# Plotting the diagonal line in light gray
ax.plot([0, 5], [0, 5], color='lightgray', linestyle='--')

# add task column to x_task with Task + number + 1 like Task 1, Task 2, ...
task_column = []
for i in range(1, 13):
    task_column.append(f'{i}')

texts = []
for i, point in enumerate(X_task):
    # Adding text to the plot and to the texts list
    text = ax.text(point[0] + 0.05, point[1], task_column[i], fontsize=16, ha='left')
    texts.append(text)

adjust_text(texts)

# File path for saving with corrected axes labels and increased font size
ratings_plot_file_path_corrected_new = '/Users/Youssef/Downloads/Ratings_Scatter_Plot.png'
fig.savefig(ratings_plot_file_path_corrected_new, bbox_inches='tight', dpi=600)