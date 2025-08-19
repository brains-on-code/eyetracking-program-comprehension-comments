# Replication Package for "The Effect Of Comments On Program Comprehension: An Eye-Tracking Study"

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This repository contains the replication package for the paper "The Effect Of Comments On Program Comprehension: An Eye-Tracking Study", accepted at Empirical Software Engineering.

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

### Eye Tracker Specifications
In our study, we used the Tobii EyeX\footnote{https://help.tobii.com/hc/en-us/articles/212818309-Specifications-for-EyeX} eye tracker to collect gaze data at a frequency of 60\,Hz. The Tobii EyeX is a portable eye tracker that utilizes near-infrared light to track the position of the eyes. It has a tracking population of 95\%, ensuring precise measurements.
The Tobii EyeX is compatible with screens up to 27 inches and has an operating distance range of 50 - 90 cm. The track box dimensions, representing the area where eye movements can be accurately captured, are approximately 40 x 30 cm at a distance of 75 cm. 
To ensure accurate eye-tracking measurements, we instructed participants to position themselves at the right distance and position to the Tobii EyeX according to the manufacturer's instructions. 

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

## License

This repository is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

## Contact

For any questions or issues related to this replication package, please contact Youssef Abdelsalam at [abdelsalam@cs.uni-saarland.de].
