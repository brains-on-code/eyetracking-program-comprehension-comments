import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config


def generate_demographic_plots():
    # read the demographic data
    demographics_data = pd.read_csv(os.path.join(config.PATH_DEMOGRAPHICS, 'GeneralInfo.csv'))
    demographics_data['Age'] = 2023 - demographics_data['Age']
    if not os.path.exists(config.PATH_DEMOGRAPHICS_VISUALS):
        os.makedirs(config.PATH_DEMOGRAPHICS_VISUALS)

    # make font size bigger
    plt.rc('font', size=16)

    plt.figure(figsize=(15, 6))

    # Age Boxplot with recalculated ages
    plt.subplot(1, 3, 1)
    sns.boxplot(y=demographics_data['Age'], color='lightblue')
    plt.ylabel('Age')
    plt.xlabel('Age Distribution')
    plt.grid(False)

    # Java Experience Boxplot
    plt.subplot(1, 3, 2)
    sns.boxplot(y=demographics_data['JavaExperience'], color='lightgreen')
    plt.ylabel('Years')
    plt.xlabel('Programming Experience')
    plt.grid(False)

    # Overall Experience Boxplot
    plt.subplot(1, 3, 3)
    sns.boxplot(y=demographics_data['OverallExperience'], color='lightcoral')
    plt.ylabel('Years')
    plt.xlabel('Overall Experience')
    plt.grid(False)

    # Adjust layout
    plt.tight_layout()
    plt.savefig(os.path.join(config.PATH_DEMOGRAPHICS_VISUALS, 'Demographics.pdf'), dpi=600, bbox_inches='tight')
    plt.close()
