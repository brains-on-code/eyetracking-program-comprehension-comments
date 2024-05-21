CURRENT_STUDY = 'Effect_of_Comments'
KEYWORD_SNIPPET = 'Task'

OVERRIDE_PREPROCESSED_DATA = False
USE_PREPROCESSED_DATA = True

ANALYSE_DEMOGRAPHICS = False
ANALYSE_RESULTS = False
ANALYSE_RATINGS = False
ANALYSE_GENERAL_METRICS = False
ANALYSE_AOI_METRICS = True

PERFORM_STATISTICAL_TESTS = False
GENERATE_PLOTS = False

EXPORT_OGAMA = False
GENERATE_XY_VELOCITY_PLOTS = False
GENERATE_HEATMAPS = False
GENERATE_REVEAL_IMAGES = False
GENERATE_SCANPATHS = False
GENERATE_READING_ORDER_GRAPHS = False

PATH_DATA_RAW = 'data/raw/' + CURRENT_STUDY
PATH_DATA_PREPROCESSED = 'data/preprocessed'

PATH_SNIPPET_IMAGES_DIR = '/Users/Youssef/Development/BA Comments/effect-of-comments/Final Snippets/Images'
PATH_AOI_DIR = '/Users/Youssef/Development/BA Comments/effect-of-comments/Final Snippets/Images/AOIs'
PATH_SNIPPET_SOLUTIONS_CSV = '/Users/Youssef/Development/BA Comments/effect-of-comments/Final Snippets/solutions.csv'
PATH_LINE_READING_ORDER_CSV = '/Users/Youssef/Development/BA Comments/effect-of-comments/Final Snippets/Images/AOIs/Reading_Order_By_Task.csv'

OUTPUT_PATH = 'output/' + CURRENT_STUDY

PATH_DEMOGRAPHICS = OUTPUT_PATH + '/Demographics'
PATH_DEMOGRAPHICS_VISUALS = PATH_DEMOGRAPHICS + '/Plots'

PATH_RESULTS = OUTPUT_PATH + '/Results'
PATH_RESULTS_VISUALS = PATH_RESULTS + '/Plots'
PATH_RESULTS_STATISTICS = PATH_RESULTS + '/Statistics'

PATH_RATINGS = OUTPUT_PATH + '/Ratings'
PATH_RATINGS_VISUALS = PATH_RATINGS + '/Plots'
PATH_RATINGS_STATISTICS = PATH_RATINGS + '/Statistics'

PATH_AOI_METRICS = OUTPUT_PATH + '/AOIMetrics'

PATH_LINEARITY_METRICS = PATH_AOI_METRICS + '/Linearity'
PATH_LINEARITY_METRICS_VISUALS = PATH_LINEARITY_METRICS + '/Plots'
PATH_LINEARITY_METRICS_STATISTICS = PATH_LINEARITY_METRICS + '/Statistics'

PATH_VISUAL_ATTENTION_METRICS = PATH_AOI_METRICS + '/VisualAttention'
PATH_VISUAL_ATTENTION_METRICS_VISUALS = PATH_VISUAL_ATTENTION_METRICS + '/Plots'
PATH_VISUAL_ATTENTION_METRICS_STATISTICS = PATH_VISUAL_ATTENTION_METRICS + '/Statistics'

PATH_GAZE_STRATEGY_METRICS = PATH_AOI_METRICS + '/GazeStrategy'
PATH_GAZE_STRATEGY_METRICS_VISUALS = PATH_GAZE_STRATEGY_METRICS + '/Plots'
PATH_GAZE_STRATEGY_METRICS_STATISTICS = PATH_GAZE_STRATEGY_METRICS + '/Statistics'

PATH_SNIPPET_OVERLAYS = OUTPUT_PATH + '/SnippetOverlays'
PATH_XY_VELOCITY_PLOTS = OUTPUT_PATH + '/XYVelocityPlots'

EXPORTS_PATH = 'output/' + CURRENT_STUDY + '/Exports'
PATH_OGAMA = EXPORTS_PATH + '/Ogama'
PATH_RTGCT = EXPORTS_PATH + '/RTGCT'

TEMPORAL_RESOLUTION = 60
VELOCITY_THRESHOLD = 150

SNIPPETS = ['Task1CM',
            'Task1CP',
            'Task2CM',
            'Task2CP',
            'Task3CM',
            'Task3CP',
            'Task4CM',
            'Task4CP',
            'Task5CM',
            'Task5CP',
            'Task6CM',
            'Task6CP',
            'Task7CM',
            'Task7CP',
            'Task8CM',
            'Task8CP',
            'Task9CM',
            'Task9CP',
            'Task10CM',
            'Task10CP',
            'Task11CM',
            'Task11CP',
            'Task12CM',
            'Task12CP']

SNIPPETS_UNIQUE = ['Task1',
                   'Task2',
                   'Task3',
                   'Task4',
                   'Task5',
                   'Task6',
                   'Task7',
                   'Task8',
                   'Task9',
                   'Task10',
                   'Task11',
                   'Task12']
