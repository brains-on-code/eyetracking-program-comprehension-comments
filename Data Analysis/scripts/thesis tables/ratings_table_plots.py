import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import config


def get_data(file_path):
    data = pd.read_csv(file_path)
    # Transform the data to get the frequency of each Likert scale response per task
    if file_path.endswith('CombinedDifficulties.csv'):
        data_counts = data.groupby(['Task', 'Type', 'Difficulty']).size().unstack(fill_value=0)
    else:
        data_counts = data.groupby(['Task', 'Comment Contribution']).size().unstack(fill_value=0)
    # Normalize the data to get percentages for 100% stacked bar charts
    data_percentage = data_counts.div(data_counts.sum(axis=1), axis=0)
    return data_counts, data_percentage


def version1(data, type):
    for task, counts in data.iterrows():
        fig, ax = plt.subplots(figsize=(3, 1), dpi=300)
        # Identifying the rating with the highest frequency for highlighting
        # if two ratings have the same frequency, both are highlighted
        max_rating = counts[counts == counts.max()].index

        # Coloring all bars grey and highlighting the max with a more appealing color
        colors = ['lightgrey' if rating not in max_rating else '#e392be' for rating in counts.index]
        # Creating the bar chart
        bars = counts.plot(kind='bar', color=colors, legend=False, align='edge', width=0.9)
        # make space between bars smaller
        # Setting the y-axis limits
        ax.set_ylim(0, 20)
        # Removing all lines, axes, and padding
        ax.axis('off')
        ax.grid(False)
        fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

        # Adding horizontal labels inside the bars
        for bar in bars.containers:
            ax.bar_label(bar, label_type='edge', padding=3, rotation=0, fontsize=12, color='black')

        plt.tight_layout()
        # Saving the plot
        file_name = f'/Users/Youssef/Downloads/{type}_bar_chart_{task}.png'
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0)
        plt.close()


def version2(data, type):
    for task in data.index:
        fig, ax = plt.subplots(figsize=(5, 2), dpi=600)

        # Plot the data with a horizontal bar chart
        data.loc[[task]].plot(kind='barh', stacked=True, color=sns.color_palette("Purples", n_colors=5), legend=False, ax=ax, width=1 if type == 'difficulty' else 2)
        ax.set_aspect('equal')
        if type == 'difficulty':
            ax.set_xlim(0, 10)
        else:
            ax.set_xlim(0, 20)
        ax.axis('off')
        # Adding frequency in bold inside each bar
        cum_value = 0  # To track the cumulative position for text labels
        for idx, value in enumerate(data.loc[task]):
            # Skip zero values
            if value == 0:
                continue

            # Add text label
            # White text for dark blue bars, black text for light blue bars
            text_color = 'black' if idx < 3 else 'white'
            text = data.loc[task].iloc[idx]
            ax.text(cum_value + value / 2, 0, text, va='center', ha='center', color=text_color, weight='bold', fontsize=12)
            cum_value += value

        # Save plot to file with no padding
        file_name = f'/Users/Youssef/Downloads/{type}_bar_chart_{task}.png'
        plt.savefig(file_name, bbox_inches='tight', pad_inches=0, dpi=600)
        plt.close('all')


if __name__ == '__main__':
    difficulty_file_path = config.PATH_RATINGS + 'CombinedDifficulties.csv'
    comment_file_path = config.PATH_RATINGS + 'CombinedCommentContributions.csv'
    difficulty_data_counts, difficulty_data_percentage = get_data(difficulty_file_path)
    comments_data_counts, comments_data_percentage = get_data(comment_file_path)
    # Creating and saving individual bar charts for each task
    version2(difficulty_data_counts, 'difficulty')
    version2(comments_data_counts, 'comments')
