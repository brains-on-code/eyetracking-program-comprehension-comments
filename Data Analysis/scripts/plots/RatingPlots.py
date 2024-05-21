import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config


def generate_rating_plots():
    # read the rating data
    ratings_by_task = pd.read_csv(os.path.join(config.PATH_RATINGS, 'CombinedDifficultiesByTask.csv'))
    comments_by_task_number = pd.read_csv(
        os.path.join(config.PATH_RATINGS, 'CombinedCommentContributionsByTaskNumber.csv'))

    combined_data = pd.DataFrame()
    combined_data['Task'] = [str(task)[:-2] for task in ratings_by_task['Task']]
    combined_data['Type'] = [str(type)[-2:] for type in ratings_by_task['Task']]
    combined_data['Difficulty'] = ratings_by_task['Difficulty Mean']

    if not os.path.exists(config.PATH_RATINGS_VISUALS):
        os.makedirs(config.PATH_RATINGS_VISUALS)

    plt.rcParams['text.usetex'] = True
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')

    # Creating subplots for rating and comments
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

    # Plotting Difficulty
    sns.barplot(data=combined_data, x='Task', y='Difficulty', hue='Type', palette=['skyblue', 'orange'], ax=axes[0])
    axes[0].set_title('Rating by Task')
    axes[0].set_xlabel('Task')
    axes[0].set_ylabel('Rating')
    axes[0].set_ylim(0, 5)
    axes[0].set_yticks(np.arange(0, 5.1, 0.5))
    axes[0].set_yticklabels(np.arange(0, 5.1, 0.5))
    # set legend to be outside of the plot
    axes[0].legend(loc='upper right', title='Type', bbox_to_anchor=(1.2, 1))

    # Plotting Comments
    sns.barplot(data=comments_by_task_number, x='Task', y='Comment Contribution Mean', palette=['skyblue', 'orange'], ax=axes[1])
    axes[1].set_title('Comments by Task')
    axes[1].set_xlabel('Task')
    axes[1].set_ylabel('Comments')
    axes[1].set_ylim(0, 5)
    axes[1].set_yticks(np.arange(0, 5.1, 0.5))
    axes[1].set_yticklabels(np.arange(0, 5.1, 0.5))

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(os.path.join(config.PATH_RATINGS_VISUALS, 'Rating_by_Task.png'), dpi=300)

