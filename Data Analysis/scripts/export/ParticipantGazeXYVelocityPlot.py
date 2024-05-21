import os

import matplotlib.pyplot as plt

import config


def export_xy_velocity_plot(group_df, group=None):
    for participant_df in group_df:
        export_xy_velocity_plot_participant(participant_df, group)


def export_xy_velocity_plot_participant(participant_df, group):
    print('\nPlotting gaze data for participant:', participant_df['id_short'])
    plt.figure(figsize=(50, 8))

    gaze_data_time = participant_df['gaze_data']['ExperimentTime'].values

    plt.clf()
    plt.subplot(3, 1, 1)
    plt.ylabel('Gaze (x Axis)')
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosX'].values, label='X', color='lightgray')
    # plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosXSmooth'].values, label='Y', color='dimgray', alpha=0.5)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.ylabel('Gaze (y Axis)')
    plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosY'].values, label='Y', color='lightgray')
    # plt.plot(gaze_data_time, participant_df['gaze_data']['GazePosYSmooth'].values, label='Y', color='dimgray', alpha=0.5)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.xlabel('Experiment Time')
    plt.ylabel('Velocity (Pixel/100msec)')
    plt.plot(gaze_data_time, participant_df['gaze_data']['Velocity'].values, label='Velocity', color='red')
    # plt.plot(gaze_data_time, participant_df['gaze_data']['VelocitySmooth'].values, label='Velocity Smoothed', color='mistyrose')
    plt.legend()

    plt.tight_layout()

    # file_add = ''
    # if not group:
    #    file_add = group + '_'
    # else:
    file_add = participant_df['id_short'] + '_Gaze_XY_Velocity_Plot.png'

    if not os.path.exists(config.PATH_XY_VELOCITY_PLOTS):
        os.makedirs(config.PATH_XY_VELOCITY_PLOTS)

    plt.savefig(os.path.join(config.PATH_XY_VELOCITY_PLOTS, file_add), dpi=300)
    plt.close()

    print('-> plotting gaze data done')
