import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config


def generate_result_plots():
    # read the result data
    results_by_task = pd.read_csv(os.path.join(config.PATH_RESULTS, 'CombinedResultsByTask.csv'))

    combined_data = pd.DataFrame()
    combined_data['Task'] = [str(task)[:-2] for task in results_by_task['Task']]
    combined_data['Type'] = [str(type)[-2:] for type in results_by_task['Task']]
    combined_data['Accuracy'] = results_by_task['Accuracy']
    combined_data['Time'] = results_by_task['Time']
    # time_sd_cm = results_by_task[results_by_task['Task'].str.contains('CM')]['Time_SD'].values
    # time_sd_cp = results_by_task[results_by_task['Task'].str.contains('CP')]['Time_SD'].values
    # Concatenate the two arrays into a 2D array
    # time_sd_grouped = np.array([time_sd_cm, time_sd_cp])

    if not os.path.exists(config.PATH_RESULTS_VISUALS):
        os.makedirs(config.PATH_RESULTS_VISUALS)

    plt.rcParams['text.usetex'] = True
    sns.set(font_scale=1.5)
    sns.set_style('whitegrid')

    # Creating subplots for Accuracy and Time
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(12, 10))

    # Plotting Accuracy
    sns.barplot(data=combined_data, x='Task', y='Accuracy', hue='Type', palette=['skyblue', 'orange'], ax=axes[0])
    axes[0].set_title('Accuracy by Task')
    axes[0].set_xlabel('Task')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_ylim(0, 100)
    axes[0].set_yticks(np.arange(0, 101, 10))
    axes[0].set_yticklabels(np.arange(0, 101, 10))
    # set legend to be outside of the plot
    axes[0].legend(loc='upper right', title='Type', bbox_to_anchor=(1.2, 1))

    # Plotting Time with error bars for standard deviation from Time_SD
    sns.barplot(data=combined_data, x='Task', y='Time', hue='Type', palette=['skyblue', 'orange'], ax=axes[1])
    axes[1].set_title('Time by Task')
    axes[1].set_xlabel('Task')
    axes[1].set_ylabel('Time')
    axes[1].set_ylim(0, 350)
    axes[1].set_yticks(np.arange(0, 351, 50))
    axes[1].set_yticklabels(np.arange(0, 351, 50))
    # set legend to be outside of the plot
    axes[1].legend(loc='upper right', title='Type', bbox_to_anchor=(1.2, 1))

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(os.path.join(config.PATH_RESULTS_VISUALS, 'Accuracy_by_Task.png'), dpi=300)

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

    # Subplot for Accuracy
    ax1 = axes[0]
    for task in combined_data['Task']:
        subset = combined_data[combined_data['Task'] == task]
        cm_accuracy = subset[subset['Type'] == 'CM']['Accuracy'].values[0]
        cp_accuracy = subset[subset['Type'] == 'CP']['Accuracy'].values[0]

        ax1.plot([cm_accuracy, cp_accuracy], [task, task], color='grey', alpha=0.4, linewidth=1, zorder=1)
        ax1.scatter(cm_accuracy, task, color='skyblue', alpha=1, zorder=2)
        ax1.scatter(cp_accuracy, task, color='orange', alpha=1, zorder=2)

    ax1.set_xticks(np.arange(0, 101, 10))
    ax1.set_xticklabels(np.arange(0, 101, 10))
    ax1.set_xlabel('Accuracy (%)')
    ax1.set_ylabel('Task')

    # Subplot for Time
    ax2 = axes[1]
    for task in combined_data['Task']:
        subset = combined_data[combined_data['Task'] == task]
        cm_time = subset[subset['Type'] == 'CM']['Time'].values[0]
        cp_time = subset[subset['Type'] == 'CP']['Time'].values[0]

        ax2.plot([cm_time, cp_time], [task, task], color='grey', alpha=0.4, linewidth=1, zorder=1)
        ax2.scatter(cm_time, task, color='skyblue', alpha=1, zorder=2)
        ax2.scatter(cp_time, task, color='orange', alpha=1, zorder=2)

    ax2.set_xticks(np.arange(0, 351, 50))
    ax2.set_xticklabels(np.arange(0, 351, 50))
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Task')

    plt.tight_layout()
    plt.savefig(os.path.join(config.PATH_RESULTS_VISUALS, 'Accuracy_Time_Lollipop.png'), dpi=300)
