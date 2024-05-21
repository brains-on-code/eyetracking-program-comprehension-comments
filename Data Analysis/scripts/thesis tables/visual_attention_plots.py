from matplotlib import pyplot as plt
import matplotlib.font_manager as fm


def create_individual_bar_chart_scaled(value, is_count, task_type, fixation_type, file_name, max_scale):
    pastel_colors = {'CM': '#FFB347', 'CP': '#77DD77'}
    color = pastel_colors.get(task_type, 'grey')

    plt.rcParams['font.family'] = 'CMU Serif'


    # Create figure and axis
    fig, ax = plt.subplots(figsize=(5, 1), dpi=600)
    # Plot the data with a horizontal bar chart and set the height of the bar to 1
    ax.barh([0], [value], color=color, height=1)

    ax.set_xlim(0, max_scale)  # Use consistent scale for all charts
    ax.set_ylim(-0.7, 0.7)  # Set the height of the bar to 1

    # Remove all lines, axes, and padding
    ax.axis('off')

    # make background transparent
    fig.patch.set_alpha(0)

    # Add text inside the bar
    text_color = 'black'
    # make text in the center of the whole plot and not the bar and align it to the right
    # keep decimals for duration metrics
    if value != 0:
        ax.text(max_scale / 2, 0, f'{value:.1f}' if not is_count else f'{value:.0f}', va='center', ha='center',
                color=text_color, fontsize=36)

    else:
        # put '-' in the center of the whole plot and not the bar and align it to the right
        ax.text(max_scale / 2, 0, '-', va='center', ha='center', color=text_color, fontsize=36)

    # Save the plot
    file_name = f'/Users/Youssef/Downloads/{file_name}.pdf'
    plt.savefig(file_name, bbox_inches='tight', pad_inches=0, dpi=600)
    plt.close()


def version1():
    values_to_plot = {
        'AllFixations_CM_Count': 525.11,
        'AllFixations_CP_Count': 579.10,
        'AOIFixations_CM_Count': 358.36,
        'AOIFixations_CP_Count': 396.64,
        'CodeFixations_CM_Count': 358.36,
        'CodeFixations_CP_Count': 304.51,
        'CommentFixations_CM_Count': 0,
        'CommentFixations_CP_Count': 92.13,
        'AllFixations_CM_Duration': 177.03,
        'AllFixations_CP_Duration': 171.39,
        'AOIFixations_CM_Duration': 123.90,
        'AOIFixations_CP_Duration': 121.19,
        'CodeFixations_CM_Duration': 123.90,
        'CodeFixations_CP_Duration': 100.32,
        'CommentFixations_CM_Duration': 0,
        'CommentFixations_CP_Duration': 20.87
    }

    # Create individual bar charts with the same scale
    for key, value in values_to_plot.items():
        fixation_type, task_type, metric = key.split('_')
        is_count = metric == 'Count'
        # set max value to max of count metrics if it's a count metric (has _Count in the key)
        # otherwise set max value to max of duration metrics
        if is_count:
            max_value = 579.10
        else:
            max_value = 177.03
        create_individual_bar_chart_scaled(value, is_count, task_type, fixation_type, key, max_value)


if __name__ == '__main__':
    version1()
