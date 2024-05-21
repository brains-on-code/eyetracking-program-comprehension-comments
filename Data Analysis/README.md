# Eye-Tracking Analysis #

This repository contains a collection of Python scripts for analyzing eye-tracking data from program-comprehension experiments. It includes a structured pipeline for preprocessing, analyzing, and visualizing eye-tracking data, along with statistical analysis.

**Disclaimer: The code is specific to our use case and may need substantial changes to work with other setups.**

## Setup

The project is compatible with Python 3.8 and was developed using the [PyCharms IDE](https://www.jetbrains.com/pycharm/). Before running the analysis, ensure that you've configured your environment according to the `requirements.txt` file.

### Installation

1. Ensure Python 3.8 is installed on your system.
2. Clone the repository or download the source code.
3. Install the required dependencies:

```shell
pip install -r requirements.txt
```

### Structure

The repository is structured as follows:

```
.
├── data
│   ├── preprocessed
│   │   └── PreprocessedData.pkl
│   └── raw
│       └── *StudyName*
│           └── *Trial_ID*
│               └── GazeData_*.csv
│               └── GeneralInfo_*.csv
│               └── Ratings_*.csv
│               └── Results_*.csv
├── output : Destination for generated outputs
├── scripts
│   ├── analyses : Scripts for analyzing demographics, results, ratings, and AOI metrics.
│   ├── export : Scripts for exporting data for further use or visualization.
│   ├── plots : Scripts for creating visual representations of the analysis results.
│   ├── preprocessing : Scripts for preprocessing raw data.
│   ├── statistics : Scripts for conducting statistical tests to evaluate the data.
│   ├── thesis lme : Scripts for LME models included in the thesis.
│   ├── thesis plots : Scripts for plots included in the thesis.
│   ├── thesis tables : Scripts for table images included in the thesis.
│   └── utils : Supporting util functions.
├── config.py : Configuration file for the analysis pipeline.
└── requirements.txt : Required Python packages for the analysis.
└── RunPipelineData.py : Script to execute the entire analysis pipeline.
```

## Usage and Workflow

Configure config.py with the specific settings for your experiment.

The analysis pipeline is divided into several steps, each corresponding to scripts within the `scripts/` directory.

Run `RunPipelineData.py` to execute the entire pipeline, or refer to individual scripts for specific analyses or visualizations.


## Related Repositories

* [EyeLink Ogama Connector](https://github.com/peitek/eyelink-ogama-connector)
* [Eye-Tracking Analyses](https://github.com/peitek/eyetracking-analyses)
* [Eye-Tracking Visualization Pipeline](https://github.com/peitek/eyetracking-visualizations)


# License #

```
MIT License

Copyright (c) 2019 Norman Peitek, 2024 Youssef Abdelsalam
```