import numpy as np
import pandas as pd
import scipy.signal


class GazeDataPreprocessing:
    @staticmethod
    def cartesian_velocity(x, y, t):
        dx, dy, dt = np.diff(x), np.diff(y), np.diff(t)

        vx = dx / dt
        vy = dy / dt

        dr = np.sqrt(vx * vx + vy * vy)
        return dr

    @staticmethod
    def preprocess_data_frames(gaze_data_frames, velocity_threshold):
        return [GazeDataPreprocessing.preprocess_data_frame(gdf, velocity_threshold) for gdf in
                gaze_data_frames]

    @staticmethod
    def preprocess_data_frame(gdf, velocity_threshold):
        gdf = GazeDataPreprocessing.drop_duplicate_timestamps(gdf)
        gdf = GazeDataPreprocessing.smooth_data(gdf)
        gdf = GazeDataPreprocessing.calculate_velocity(gdf)
        gdf = GazeDataPreprocessing.detect_gaze_events(gdf, velocity_threshold)

        return gdf

    @staticmethod
    def smooth_data(gdf):
        gaze_x = gdf['GazePosX'].dropna()
        gaze_y = gdf['GazePosY'].dropna()
        gaze_x_smooth = scipy.signal.savgol_filter(gaze_x, 5, 3)
        gaze_y_smooth = scipy.signal.savgol_filter(gaze_y, 5, 3)
        gdf['GazePosXSmooth'] = pd.Series(gaze_x_smooth)
        gdf['GazePosYSmooth'] = pd.Series(gaze_y_smooth)
        return gdf

    @staticmethod
    def calculate_velocity(gdf):
        velocity = GazeDataPreprocessing.cartesian_velocity(gdf['GazePosX'].values, gdf['GazePosY'].values,
                                                            gdf['ExperimentTime'].values)
        velocity = np.multiply(velocity, 100)
        # add first value as nan
        velocity = np.insert(velocity, 0, 0)
        gdf['Velocity'] = pd.Series(velocity)

        velocity_smooth = GazeDataPreprocessing.cartesian_velocity(gdf['GazePosXSmooth'].values,
                                                                   gdf['GazePosYSmooth'].values,
                                                                   gdf['ExperimentTime'].values)
        velocity_smooth = np.multiply(velocity_smooth, 100)
        # add first value as nan
        velocity_smooth = np.insert(velocity_smooth, 0, 0)
        gdf['VelocitySmooth'] = pd.Series(velocity_smooth)

        return gdf

    @staticmethod
    def detect_gaze_event_based_on_velocity(row, column, velocity_threshold):
        if row[column] > velocity_threshold:
            return 'Saccade'
        else:
            return 'Fixation'

    @staticmethod
    def detect_gaze_events(gdf, velocity_threshold):
        gdf['Gaze_Event'] = gdf.apply(
            lambda row: GazeDataPreprocessing.detect_gaze_event_based_on_velocity(row, 'Velocity', velocity_threshold),
            axis=1)
        gdf['Gaze_EventSmooth'] = gdf.apply(
            lambda row: GazeDataPreprocessing.detect_gaze_event_based_on_velocity(row, 'VelocitySmooth',
                                                                                  velocity_threshold), axis=1)
        return gdf

    @staticmethod
    def drop_duplicate_timestamps(gdf):
        # drop duplicate timestamps
        gdf = gdf.drop_duplicates(subset=['ExperimentTime'], keep='first')
        return gdf
