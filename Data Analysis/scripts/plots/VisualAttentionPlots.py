import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config


def generate_visual_attention_plots():
    # read the result data
    visual_attention_data = pd.read_csv(
        os.path.join(config.PATH_VISUAL_ATTENTION_METRICS, 'VisualAttention_Metrics_By_Task.csv'))

    combined_data = pd.DataFrame()
    combined_data['Task'] = [str(task)[:-2] for task in visual_attention_data['Task']]
    combined_data['Type'] = [str(type)[-2:] for type in visual_attention_data['Task']]
    combined_data['AoiFixations_Count'] = visual_attention_data['AoiFixations_Count']
    combined_data['AoiFixations_Duration'] = visual_attention_data['AoiFixations_Duration']
    combined_data['CodeFixations_Count'] = visual_attention_data['CodeFixations_Count']
    combined_data['CodeFixations_Duration'] = visual_attention_data['CodeFixations_Duration']
    combined_data['CommentFixations_Count'] = visual_attention_data['CommentFixations_Count']
    combined_data['CommentFixations_Duration'] = visual_attention_data['CommentFixations_Duration']

    if not os.path.exists(config.PATH_VISUAL_ATTENTION_METRICS_VISUALS):
        os.makedirs(config.PATH_VISUAL_ATTENTION_METRICS_VISUALS)

    plt.rcParams['text.usetex'] = True
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')

    # Lollipop plot of Accuracy and Time
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    # no border around the plot
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)
    axes[0].spines['bottom'].set_visible(False)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)
    axes[1].spines['bottom'].set_visible(False)
    # grid lines only for y-axis
    axes[0].grid(axis='y')
    axes[1].grid(axis='y')

    # Subplot for Code Fixations Count
    ax1 = axes[0]
    for task in combined_data['Task']:
        subset = combined_data[combined_data['Task'] == task]
        cm_aoi_fixations_count = subset[subset['Type'] == 'CM']['AoiFixations_Count'].values[0]
        cp_aoi_fixations_count = subset[subset['Type'] == 'CP']['AoiFixations_Count'].values[0]
        cm_code_fixations_count = subset[subset['Type'] == 'CM']['CodeFixations_Count'].values[0]
        cp_code_fixations_count = subset[subset['Type'] == 'CP']['CodeFixations_Count'].values[0]
        # cm_comment_fixations_count = subset[subset['Type'] == 'CM']['CommentFixations_Count'].values[0]
        # cp_comment_fixations_count = subset[subset['Type'] == 'CP']['CommentFixations_Count'].values[0]

        ax1.plot([cm_aoi_fixations_count, cp_aoi_fixations_count], [task, task], color='lightgreen', alpha=0.4, linewidth=1,
                 zorder=1)
        ax1.plot([cm_code_fixations_count, cp_code_fixations_count], [task, task], color='grey', alpha=0.4, linewidth=1,
                 zorder=1)
        # ax1.plot([cm_comment_fixations_count, cp_comment_fixations_count], [task, task], color='lightgreen', alpha=0.4,
        #         linewidth=1, zorder=1)
        ax1.scatter(cm_aoi_fixations_count, task, color='lightblue', alpha=1, zorder=2)
        ax1.scatter(cp_aoi_fixations_count, task, color='darkblue', alpha=1, zorder=2)
        ax1.scatter(cm_code_fixations_count, task, color='lightblue', alpha=1, zorder=2)
        ax1.scatter(cp_code_fixations_count, task, color='darkgreen', alpha=1, zorder=2)
        # ax1.scatter(cm_comment_fixations_count, task, color='lightgreen', alpha=1, zorder=2)
        # ax1.scatter(cp_comment_fixations_count, task, color='darkgreen', alpha=1, zorder=2)

    ax1.set_xticks(np.arange(0, 601, 100))
    ax1.set_xticklabels(np.arange(0, 601, 100))
    ax1.set_xlabel('Code Fixations Count')
    ax1.set_ylabel('Task')
    # set legend to be outside of the plot
    ax1.legend(loc='upper right', title='Type', bbox_to_anchor=(1.2, 1))

    # Subplot for Time
    ax2 = axes[1]
    for task in combined_data['Task']:
        subset = combined_data[combined_data['Task'] == task]
        cm_code_fixations_duration = subset[subset['Type'] == 'CM']['CodeFixations_Duration'].values[0]
        cp_code_fixations_duration = subset[subset['Type'] == 'CP']['CodeFixations_Duration'].values[0]

        ax2.plot([cm_code_fixations_duration, cp_code_fixations_duration], [task, task], color='grey', alpha=0.4,
                 linewidth=1, zorder=1)
        ax2.scatter(cm_code_fixations_duration, task, color='skyblue', alpha=1, zorder=2)
        ax2.scatter(cp_code_fixations_duration, task, color='orange', alpha=1, zorder=2)

    ax2.set_xticks(np.arange(0, 351, 50))
    ax2.set_xticklabels(np.arange(0, 351, 50))
    ax2.set_xlabel('Code Fixations Duration (in seconds)')
    ax2.set_ylabel('Task')

    plt.tight_layout()
    plt.savefig(os.path.join(config.PATH_VISUAL_ATTENTION_METRICS_VISUALS, 'VisualAttention_Metrics_By_Task.png'),
                dpi=300)
