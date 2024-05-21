import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config


def analyse_demographics():
    if not os.path.exists(config.PATH_DEMOGRAPHICS):
        os.makedirs(config.PATH_DEMOGRAPHICS)

    combined_data = pd.DataFrame()
    # Iterate through participant folders
    for directory in os.listdir(config.PATH_DATA_RAW):
        # ignore hidden files
        if str(directory).startswith('.'):
            continue
        # Get participant id from folder name
        participant_id = str(directory).split("_")[1]
        general_info_file_path = os.path.join(str(config.PATH_DATA_RAW), str(directory),
                                              "GeneralInfo_" + str(participant_id) + ".csv")
        # Check if GeneralInfo file exists in participant folder
        if not os.path.isfile(general_info_file_path):
            print("General info file not found for participant: " + participant_id)
            continue

        participant_data = pd.read_csv(general_info_file_path, delimiter=";")
        participant_data = participant_data.rename(columns={'OverallExperienc': 'OverallExperience'})
        combined_data = pd.concat([combined_data, participant_data], ignore_index=True)

    # Save the combined data to a new GeneralInfo.csv file
    combined_data.to_csv(config.PATH_DEMOGRAPHICS + "/GeneralInfo.csv", index=False)

    # Demographics
    generate_general_info_file(combined_data)

    # Create and save graphs/plots using seaborn
    # generate_general_info_plots(combined_data, config.PATH_DEMOGRAPHICS_VISUALS)

    print("Demographic data analysis and visualization completed.")


def generate_general_info_file(combined_data):
    total_participants = len(combined_data)
    gender_counts = combined_data['Gender'].value_counts()
    age_mean = combined_data['Age'].mean()
    age_sd = combined_data['Age'].std()
    education_counts = combined_data['Education'].value_counts()
    job_counts = combined_data['Job'].value_counts()
    java_experience_counts = combined_data['JavaKnowledge'].value_counts()
    glasses_count = combined_data['Glasses'].value_counts()
    eye_problems_count = combined_data['EyeProblems'].value_counts()
    # Create a txt file with the calculated data
    with open(os.path.join(config.PATH_DEMOGRAPHICS, "GeneralInfo.txt"), "w") as text_file:
        text_file.write(f"Total participants: {total_participants}\n")
        text_file.write(f"Males: {gender_counts[0]}\n")
        text_file.write(f"Females: {gender_counts[1]}\n")
        text_file.write(f"Mean age: {age_mean:.2f}\n")
        text_file.write(f"Age standard deviation: {age_sd:.2f}\n")
        text_file.write("--------------------------------\n")
        text_file.write(f"Education distribution:\n{education_counts}\n")
        text_file.write("--------------------------------\n")
        text_file.write(f"Job distribution:\n{job_counts}\n")
        text_file.write("--------------------------------\n")
        text_file.write(f"Java experience distribution:\n{java_experience_counts}\n")
        text_file.write("--------------------------------\n")
        text_file.write(f"Glasses distribution:\n{glasses_count}\n")
        text_file.write("--------------------------------\n")
        text_file.write(f"Eye problems distribution:\n{eye_problems_count}\n")


def generate_general_info_plots(combined_data, demographic_visuals_path):
    if not os.path.exists(demographic_visuals_path):
        os.makedirs(demographic_visuals_path)
    # Gender distribution
    plt.figure(figsize=(10, 6))
    gender_counts = combined_data['Gender'].value_counts()
    sns.barplot(x=gender_counts.index, y=gender_counts.values)
    plt.title('Gender Distribution')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(gender_counts.values)) + 1))
    gender_plot_path = os.path.join(demographic_visuals_path, "gender_distribution.png")
    plt.savefig(gender_plot_path)
    plt.close()
    # Age distribution
    plt.figure(figsize=(10, 6))
    age_counts = combined_data['Age'].value_counts()
    sns.barplot(x=age_counts.index, y=age_counts.values)
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(age_counts.values)) + 1))
    age_plot_path = os.path.join(demographic_visuals_path, "age_distribution.png")
    plt.savefig(age_plot_path)
    plt.close()
    # Education
    plt.figure(figsize=(10, 6))
    education_counts = combined_data['Education'].value_counts()
    sns.barplot(x=education_counts.index, y=education_counts.values)
    plt.title('Education Distribution')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(education_counts.values)) + 1))
    education_plot_path = os.path.join(demographic_visuals_path, "education_distribution.png")
    plt.savefig(education_plot_path)
    plt.close()
    # Job
    plt.figure(figsize=(10, 6))
    job_counts = combined_data['Job'].value_counts()
    sns.barplot(x=job_counts.index, y=job_counts.values)
    plt.title('Job Distribution')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(job_counts.values)) + 1))
    job_plot_path = os.path.join(demographic_visuals_path, "job_distribution.png")
    plt.savefig(job_plot_path)
    plt.close()
    # Java Experience distribution
    plt.figure(figsize=(10, 6))
    java_experience_counts = combined_data['JavaKnowledge'].value_counts()
    sns.barplot(x=java_experience_counts.index, y=java_experience_counts.values)
    plt.title('Java Experience Distribution')
    plt.xlabel('Java Experience Level')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(java_experience_counts.values)) + 1))
    java_experience_plot_path = os.path.join(demographic_visuals_path, "java_experience_distribution.png")
    plt.savefig(java_experience_plot_path)
    plt.close()
    # Glasses distribution
    plt.figure(figsize=(10, 6))
    glasses_count = combined_data['Glasses'].value_counts()
    sns.barplot(x=glasses_count.index, y=glasses_count.values)
    plt.title('Glasses Distribution')
    plt.xlabel('Glasses Usage')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(glasses_count.values)) + 1))
    glasses_plot_path = os.path.join(demographic_visuals_path, "glasses_distribution.png")
    plt.savefig(glasses_plot_path)
    plt.close()
    # Eye Problems distribution
    plt.figure(figsize=(10, 6))
    eye_problems_count = combined_data['EyeProblems'].value_counts()
    sns.barplot(x=eye_problems_count.index, y=eye_problems_count.values)
    plt.title('Eye Problems Distribution')
    plt.xlabel('Eye Problems')
    plt.ylabel('Number of Participants')
    plt.yticks(range(int(max(eye_problems_count.values)) + 1))
    eye_problems_plot_path = os.path.join(demographic_visuals_path, "eye_problems_distribution.png")
    plt.savefig(eye_problems_plot_path)
    plt.close()

