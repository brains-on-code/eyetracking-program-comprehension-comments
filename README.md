# Replication Package for "The Effect Of Comments On Program Comprehension: An Eye-Tracking Study"

This repository contains the replication package for the paper "The Effect Of Comments On Program Comprehension: An Eye-Tracking Study"

## Repository Structure

### 1. Study

This folder contains materials related to the study design and data collection.

### 2. Data Analysis

This folder contains all necessary files and scripts for data processing and analysis. The 'data' sub-folder contains the raw data files collected during the study. The 'output' sub-folder contains the processed data files and analysis results. Further details on the data analysis pipeline are provided in the 'README.md' file in the 'Data Analysis' folder.

### 3. Post-Questionnaire

This folder includes the post-questionnaire and rating templates used in the study.

### 4. Final Snippets

This folder contains the final code snippets used in the study along with additional resources. The `Images` sub-folder contains visual representations of the snippets with AOI overlays, which can be useful for analysis.

## Instructions for Replication

### Study

1. Run the study program by opening the `Study` folder in Microsoft Visual Studio and running the `Study.sln` solution file.

2. Administer the post-questionnaire to participants after they complete the study tasks.

### Data Analysis

3. Install the required Python dependencies:

    ```bash
    pip install -r data_analysis/requirements.txt
    ```

4. Copy the raw data files from the 'Study' folder to the 'Data Analysis' folder.

5. Set the configuration parameters in the `config.py` file in the `Data Analysis` folder.

6. Run the data analysis pipeline:
    ```bash
    python data_analysis/RunPipelineData.py
    ```

## Contact

For any questions or issues related to this replication package, please contact Youssef Abdelsalam at [s8yoabde@stud.uni-saarland.de].
