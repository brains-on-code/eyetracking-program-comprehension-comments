import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import config


def analyse_ratings():
    combined_comment_contributions = pd.DataFrame()
    combined_difficulties = pd.DataFrame()
    # Iterate through participant folders
    for directory in os.listdir(config.PATH_DATA_RAW):
        # ignore hidden files
        if str(directory).startswith('.'):
            continue
        # Get participant id from folder name
        participant_id = str(directory).split("_")[1]
        ratings_participant_file_path = os.path.join(str(config.PATH_DATA_RAW), str(directory),
                                                     "Ratings_" + str(participant_id) + ".csv")
        # Check if Ratings file exists in participant folder
        if os.path.isfile(ratings_participant_file_path):
            participant_ratings = pd.read_csv(ratings_participant_file_path, delimiter=";")
            # take only the relevant columns
            task_comment_contribution = participant_ratings[['Task', 'Comment Contribution']]
            # add participant id to each row
            task_comment_contribution['ParticipantID'] = participant_id
            task_difficulty = participant_ratings[['Task', 'Type', 'Difficulty']]
            # add participant id to each row
            task_difficulty['ParticipantID'] = participant_id
            combined_comment_contributions = pd.concat([combined_comment_contributions, task_comment_contribution])
            combined_difficulties = pd.concat([combined_difficulties, task_difficulty])

            # Create directory for individual participant stats
            individual_stats_dir = os.path.join(config.PATH_RATINGS, 'Individual', participant_id)
            if not os.path.exists(individual_stats_dir):
                os.makedirs(individual_stats_dir)
            # Save individual participant ratings to csv
            participant_ratings.to_csv(os.path.join(individual_stats_dir, 'Ratings.csv'), index=False)
            task_comment_contribution.to_csv(os.path.join(individual_stats_dir, 'CommentContribution.csv'),
                                             index=False)
            task_difficulty.to_csv(os.path.join(individual_stats_dir, 'Difficulty.csv'), index=False)
        else:
            print("Ratings file not found for participant: " + participant_id)

    # Save combined ratings to csv
    combined_comment_contributions.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedCommentContributions.csv'), index=False)
    combined_comment_contributions = combined_comment_contributions.round(1)
    combined_difficulties.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedDifficulties.csv'), index=False)

    combined_comment_contributions_task = pd.DataFrame()
    combined_comment_contributions_task['Comment Contribution Mean'] = combined_comment_contributions.groupby(['Task']).agg({'Comment Contribution': ['mean']})
    combined_comment_contributions_task['Comment Contribution SD'] = combined_comment_contributions.groupby(['Task']).agg({'Comment Contribution': ['std']})
    combined_comment_contributions_task = combined_comment_contributions_task.reindex(config.SNIPPETS_UNIQUE)
    combined_comment_contributions_task = combined_comment_contributions_task.round(1)
    combined_comment_contributions_task.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedCommentContributionsByTaskNumber.csv'), index=True)

    combined_difficulties_task = pd.DataFrame()
    combined_difficulties_task['CM Difficulty Mean'] = combined_difficulties[combined_difficulties['Type'] == 'CM'].groupby(['Task']).agg({'Difficulty': ['mean']})
    combined_difficulties_task['CP Difficulty Mean'] = combined_difficulties[combined_difficulties['Type'] == 'CP'].groupby(['Task']).agg({'Difficulty': ['mean']})
    combined_difficulties_task['Overall Difficulty Mean'] = combined_difficulties.groupby(['Task']).agg({'Difficulty': ['mean']})
    combined_difficulties_task['Overall Difficulty SD'] = combined_difficulties.groupby(['Task']).agg({'Difficulty': ['std']})
    combined_difficulties_task = combined_difficulties_task.reindex(config.SNIPPETS_UNIQUE)
    combined_difficulties_task = combined_difficulties_task.round(1)
    combined_difficulties_task.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedDifficultiesByTaskNumber.csv'), index=True)

    combined_difficulties_type = pd.DataFrame()
    combined_difficulties_type['Difficulty Mean'] = combined_difficulties.groupby(['Type']).agg({'Difficulty': ['mean']})
    combined_difficulties_type['Difficulty SD'] = combined_difficulties.groupby(['Type']).agg({'Difficulty': ['std']})
    combined_difficulties_type = combined_difficulties_type.round(1)
    combined_difficulties_type.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedDifficultiesByType.csv'), index=True)

    combined_difficulties_task_type = pd.DataFrame()
    combined_difficulties_task_type['Difficulty Mean'] = combined_difficulties.groupby(['Task', 'Type']).agg({'Difficulty': ['mean']})
    combined_difficulties_task_type['Difficulty SD'] = combined_difficulties.groupby(['Task', 'Type']).agg({'Difficulty': ['std']})
    combined_difficulties_task_type.index = combined_difficulties_task_type.index.map(lambda x: '{}{}'.format(x[0], x[1]))
    combined_difficulties_task_type.index.name = 'Task'
    combined_difficulties_task_type = combined_difficulties_task_type.reindex(config.SNIPPETS)
    combined_difficulties_task_type = combined_difficulties_task_type.round(1)
    combined_difficulties_task_type.to_csv(os.path.join(config.PATH_RATINGS, 'CombinedDifficultiesByTask.csv'), index=True)
