# get reading order lines and reading order aois and visualize them on the snippet
import os

from PIL import Image, ImageDraw

import config


def export_reading_graphs(df):
    # get the snippet names
    for participant in df:
        participant_id = participant['id_short']
        fixations = participant['fixations']
        # get unique snippet names from snippet column in fixations df
        snippet_names = participant['results']['ByTask'].keys()
        # loop over all snippets
        for snippet in snippet_names:
            # get image of snippet and draw on top of it the vertical position time graph
            # get the fixations for the current snippet from the fixations list without loc
            fixations_snippet = [fixation for fixation in fixations if fixation['Task'] == snippet]

            # get the snippet image
            snippet_image = Image.open(os.path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
            draw = ImageDraw.Draw(snippet_image)
            # draw the fixations as position time graph on top of the snippet image
            # get the vertical position of the fixations
            vertical_positions = [fixation['AveragePositionY'] for fixation in fixations_snippet]
            times = [fixation['Data']['ExperimentTime'].values[0] for fixation in fixations_snippet]
            # draw a vertical position time graph on top of the snippet image
            # the vertical position is already in the range of the image height
            for i in range(len(vertical_positions) - 1):
                # the time is in milliseconds and needs to be scaled to the image width to fit the image
                # draw a line from the current fixation to the next fixation
                max_time = max(times)
                min_time = min(times)
                unit_time_width = snippet_image.width / (max_time - min_time)
                # draw smooth curve between fixations
                draw.line((
                    (times[i] - min_time) * unit_time_width,
                    vertical_positions[i],
                    (times[i + 1] - min_time) * unit_time_width,
                    vertical_positions[i + 1]
                ),
                    fill=(255, 0, 0),
                    width=2,
                    joint='curve'
                )

            # save the snippet with the position time graph in ParticipantExport folder
            individual_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'IndividualExport', participant_id,
                                          'ReadingOrderGraphs')
            if not os.path.exists(individual_dir):
                os.makedirs(individual_dir)

            snippet_image.save(os.path.join(individual_dir, snippet + '.png'), optimize=True, quality=90)
