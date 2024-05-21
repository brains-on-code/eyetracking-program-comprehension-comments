import config
from scripts.analyses import AoiMetrics, Demographics, Results, Ratings
from scripts.export import Ogama, ImageExporterCombined, ImageExporterIndividual, ReadingOrderGraphs, \
    ParticipantGazeXYVelocityPlot
from scripts.plots import DemographicPlots, ResultPlots, RatingPlots, VisualAttentionPlots
from scripts.preprocessing import PreprocessingPipeline
from scripts.statistics import AoiMetricStats, ResultStats, RatingStats

############################################################
# STEP 1: Analyse Demographics, Results and Ratings
############################################################
if config.CURRENT_STUDY:
    print('#### STEP 1\nStarting Analysis for Study: ' + config.CURRENT_STUDY)
else:
    raise RuntimeWarning('Could not find necessary configuration for which study should be analysed. Please set '
                         '"CURRENT_STUDY" in the study-specific config file.')

print('Analyse demographics:', config.ANALYSE_DEMOGRAPHICS)
if config.ANALYSE_DEMOGRAPHICS:
    Demographics.analyse_demographics()

print('Analyse results:', config.ANALYSE_RESULTS)
if config.ANALYSE_RESULTS:
    Results.analyse_results()

print('Analyse ratings:', config.ANALYSE_RATINGS)
if config.ANALYSE_RATINGS:
    Ratings.analyse_ratings()

############################################################
# Step 2a: Look for study's raw data and start to preprocess it
############################################################
print('\n### STEP 2\nPreprocessing Raw Eye Tracking Data:')

print('Configuration for overriding preprocessed data:', config.OVERRIDE_PREPROCESSED_DATA)
data_preprocessed = None
if config.OVERRIDE_PREPROCESSED_DATA:
    data_preprocessed = PreprocessingPipeline.preprocess_raw_data()
elif config.USE_PREPROCESSED_DATA:
    data_preprocessed = PreprocessingPipeline.load_preprocessed()
# else if any of the config options needing data preprocessing is set to true, then stop and warn the user
elif config.ANALYSE_GENERAL_METRICS or config.ANALYSE_AOI_METRICS or \
        config.EXPORT_OGAMA or config.GENERATE_XY_VELOCITY_PLOTS or config.GENERATE_HEATMAPS or \
        config.GENERATE_REVEAL_IMAGES or config.GENERATE_SCANPATHS or config.GENERATE_READING_ORDER_GRAPHS:
    raise RuntimeWarning('Could not find preprocessed data. Please set "OVERRIDE_PREPROCESSED_DATA" or '
                         '"USE_PREPROCESSED_DATA" in the study-specific config file.')

############################################################
# Step 3: Analyse Data
############################################################
print('\n### STEP 3\nAnalysing Eye Tracking Data:')

print('Analyse AOI metrics:', config.ANALYSE_AOI_METRICS)
if config.ANALYSE_AOI_METRICS:
    AoiMetrics.run_calculations(data_preprocessed)

############################################################
# Step 4: Perform Statistical Tests
############################################################
print('\n### STEP 4\nPerforming Statistical Tests:')

print('Perform statistical tests:', config.PERFORM_STATISTICAL_TESTS)
if config.PERFORM_STATISTICAL_TESTS:
    ResultStats.calculate_result_stats()
    RatingStats.calculate_rating_stats()
    RatingStats.calculate_aggregated_ratings()
    AoiMetricStats.calculate_visual_attention_stats()
    AoiMetricStats.calculate_linearity_stats()
    AoiMetricStats.calculate_nw_stats()
    AoiMetricStats.calculate_gaze_strategy_stats()

############################################################
# Step 5: Generate Plots
############################################################
print('\n### STEP 5\nGenerating Plots:')

print('Generate plots:', config.GENERATE_PLOTS)
if config.GENERATE_PLOTS:
    DemographicPlots.generate_demographic_plots()
    ResultPlots.generate_result_plots()
    RatingPlots.generate_rating_plots()
    VisualAttentionPlots.generate_visual_attention_plots()

############################################################
# Step 6: Export to Ogama and RTGCT
############################################################
print('\n### STEP 6\nExporting Data:')

print('Export to Ogama:', config.EXPORT_OGAMA)
if config.EXPORT_OGAMA:
    Ogama.export_data(data_preprocessed)
    Ogama.export_trial_aois(data_preprocessed)

############################################################
# Step 7: Visualise Data
############################################################
print('\n### STEP 7\nVisualising Data:')

print('Generate Reading Order Graphs:', config.GENERATE_READING_ORDER_GRAPHS)
if config.GENERATE_READING_ORDER_GRAPHS:
    ReadingOrderGraphs.export_reading_graphs(data_preprocessed)

print('Generate XY Velocity Plots:', config.GENERATE_XY_VELOCITY_PLOTS)
if config.GENERATE_XY_VELOCITY_PLOTS:
    ParticipantGazeXYVelocityPlot.export_xy_velocity_plot(data_preprocessed)

print('Generate Heatmaps:', config.GENERATE_HEATMAPS)
print('Generate Reveal Images:', config.GENERATE_REVEAL_IMAGES)
print('Generate Scanpaths:', config.GENERATE_SCANPATHS)

plots = []
if config.GENERATE_HEATMAPS:
    plots.append('heatmap')
if config.GENERATE_REVEAL_IMAGES:
    plots.append('reveal_image')
if config.GENERATE_SCANPATHS:
    plots.append('scan_path')

for plot in plots:
    ImageExporterIndividual.export_individual_data(data_preprocessed, plot)
    ImageExporterCombined.export_combined_data(data_preprocessed, plot)
