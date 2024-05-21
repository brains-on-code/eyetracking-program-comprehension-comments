import os

import seaborn as sns
from matplotlib import pyplot as plt


def plot_accuracy_score(df, stats_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df['Accuracy'], label='Accuracy', color='blue', alpha=0.6)
    plt.plot(df.index, df['Score'], marker='o', color='red', label='Score')
    plt.xlabel('Task')
    plt.ylabel('Value')
    plt.title('Accuracy and Score Comparison')
    plt.xticks(df.index)
    plt.legend()
    plt.savefig(os.path.join(stats_dir, 'AccuracyScoreComparison.png'), bbox_inches='tight', dpi=300)
    plt.close()


def plot_correct_count(df, stats_dir):
    plt.figure(figsize=(10, 6))
    plt.bar(df.index, df['Correct_Count'], label='Correct Count', color='green', alpha=0.6)
    plt.bar(df.index, df['TimeOut_Count'], bottom=df['Correct_Count'], label='TimeOut Count', color='red', alpha=0.6)
    plt.xlabel('Task')
    plt.ylabel('Count')
    plt.title('Correct Count and TimeOut Count Comparison')
    plt.xticks(df.index)
    plt.legend()
    plt.savefig(os.path.join(stats_dir, 'CorrectTimeOutCountComparison.png'), bbox_inches='tight', dpi=300)
    plt.close()


def plot_time_normalized_time(df, stats_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Time'], marker='o', label='Time', color='blue')
    plt.plot(df.index, df['Normalized_Time'], marker='s', label='Normalized Time', color='red')
    plt.xlabel('Task')
    plt.ylabel('Value')
    plt.title('Time and Normalized Time Comparison')
    plt.xticks(df.index)
    plt.legend()
    plt.savefig(os.path.join(stats_dir, 'TimeNormalizedTimeComparison.png'), bbox_inches='tight', dpi=300)
    plt.close()


def plot_correct_only_time_normalized_correct_only_time(df, stats_dir):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Correct_Only_Time'], marker='o', label='Correct Only Time', color='green')
    plt.plot(df.index, df['Normalized_Correct_Only_Time'], marker='s', label='Normalized Correct Only Time',
             color='orange')
    plt.xlabel('Task')
    plt.ylabel('Value')
    plt.title('Correct Only Time and Normalized Correct Only Time Comparison')
    plt.xticks(df.index)
    plt.legend()
    plt.savefig(os.path.join(stats_dir, 'CorrectOnlyTimeNormalizedCorrectOnlyTimeComparison.png'), bbox_inches='tight',
                dpi=300)
    plt.close()


# Plot proportion of correct answers to incorrect answers
def plot_correct_incorrect(results_df, stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    # Calculate the count of correct and incorrect answers for each task type
    correctness_counts = results_df.groupby(['Task_Type', 'Correct']).size().unstack().fillna(0)
    # Plot the count of correct and incorrect answers
    correctness_counts.plot(kind='bar', stacked=True)
    plt.xlabel('Task Type')
    plt.ylabel('Count')
    plt.title('Correctness Count by Task Type')
    plt.savefig(os.path.join(stats_dir, 'CorrectnessCountByTaskType.png'), bbox_inches='tight', dpi=300)
    plt.close()


# Plot accuracy by task type
def plot_accuracy_by_task_type(participant_results, individual_stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    sns.barplot(x='Task_Type', y='Correct', data=participant_results, palette="Blues_d")
    plt.xlabel('Task Type')
    plt.ylabel('Accuracy (%)')
    plt.title('Accuracy by Task Type')
    plt.savefig(os.path.join(individual_stats_dir, 'AccuracyByTaskType.png'), bbox_inches='tight', dpi=300)
    plt.close()


# Plot time by task
def plot_time_by_task(participant_results, individual_stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    sns.barplot(x='Task', y='Time', data=participant_results, palette="Blues_d")
    plt.xlabel('Task')
    plt.ylabel('Time (s)')
    plt.title('Time by Task')
    plt.savefig(os.path.join(individual_stats_dir, 'TimeByTask.png'), bbox_inches='tight', dpi=300)
    plt.close()


# Plot time by task type
def plot_time_by_task_type(participant_results, individual_stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    sns.barplot(x='Task_Type', y='Time', data=participant_results, palette="Blues_d")
    plt.xlabel('Task Type')
    plt.ylabel('Time (s)')
    plt.title('Time by Task Type')
    plt.savefig(os.path.join(individual_stats_dir, 'TimeByTaskType.png'), bbox_inches='tight', dpi=300)
    plt.close()


# Plot score by task
def plot_score_by_task(participant_results, individual_stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    sns.barplot(x='Task', y='Score', data=participant_results, palette="Blues_d")
    plt.xlabel('Task')
    plt.ylabel('Score')
    plt.title('Score by Task')
    plt.savefig(os.path.join(individual_stats_dir, 'ScoreByTask.png'), bbox_inches='tight', dpi=300)
    plt.close()


# Plot score by task type
def plot_score_by_task_type(participant_results, individual_stats_dir):
    plt.figure(figsize=(10, 5))
    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1)
    sns.barplot(x='Task_Type', y='Score', data=participant_results, palette="Blues_d")
    plt.xlabel('Task Type')
    plt.ylabel('Score')
    plt.title('Score by Task Type')
    plt.savefig(os.path.join(individual_stats_dir, 'ScoreByTaskType.png'), bbox_inches='tight', dpi=300)
    plt.close()
