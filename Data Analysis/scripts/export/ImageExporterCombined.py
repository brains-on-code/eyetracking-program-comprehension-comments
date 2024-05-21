import os

import PIL
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from scripts.export.heatmap import Heatmapper
import config


def create_heatmap_image(snippet, fixation_points):
    # find image for the snippet
    try:
        image = Image.open(os.path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
    except FileNotFoundError or TypeError or ValueError or PIL.UnidentifiedImageError:
        print('--> missing screenshot to create image of ' + snippet)
        return

    draw = ImageDraw.Draw(image)

    solutions = pd.read_csv(config.PATH_SNIPPET_SOLUTIONS_CSV, delimiter=';')
    solution = solutions.loc[solutions.Task == snippet, 'Solution'].item()
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=40)
    draw.text((10, 10), "Solution: " + solution, fill=(0, 0, 0), font=font)

    heatmapper = Heatmapper(colours='default', point_diameter=120, point_strength=0.3, opacity=0.65)

    combined_heatmaps_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'CombinedExport', 'Heatmaps')
    if not os.path.exists(combined_heatmaps_dir):
        os.makedirs(combined_heatmaps_dir)

    heatmapper.heatmap_on_img(fixation_points, image).save(
        os.path.join(combined_heatmaps_dir, 'heatmap_' + snippet + '.png'), optimize=True, quality=90)


def create_reveal_image(snippet, fixation_points):
    # find image for the snippet
    try:
        image = Image.open(os.path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
    except FileNotFoundError or TypeError or ValueError or PIL.UnidentifiedImageError:
        print('--> missing screenshot to create image of ' + snippet)
        return

    draw = ImageDraw.Draw(image)

    solutions = pd.read_csv(config.PATH_SNIPPET_SOLUTIONS_CSV, delimiter=';')
    solution = solutions.loc[solutions.Task == snippet, 'Solution'].item()
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=40)
    draw.text((10, 10), "Solution: " + solution, fill=(0, 0, 0), font=font)

    heatmapper = Heatmapper(colours='reveal', point_diameter=150, point_strength=0.2, opacity=0.9)

    combined_reveal_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'CombinedExport', 'Reveal')
    if not os.path.exists(combined_reveal_dir):
        os.makedirs(combined_reveal_dir)

    heatmapper.heatmap_on_img(fixation_points, image).save(
        os.path.join(combined_reveal_dir, 'reveal_' + snippet + '.png'), optimize=True, quality=90)


def export_combined_data(preprocessed_data, type='all'):
    if type == 'scan_path':
        return

    data = pd.read_csv(config.PATH_DEMOGRAPHICS + '/GeneralInfo.csv')

    print('\n## EXPORT COMBINED DATA AS PNG')

    fixations_by_snippet = {}

    # read participant data
    for i, participant in enumerate(preprocessed_data):
        print('-> working on participant: ', participant['id_short'])

        participant_data = data.loc[data.SubjectID == participant['id']]
        screen_width = participant_data['ActualScreenWidth'].item()
        screen_height = participant_data['ActualScreenHeight'].item()

        # iterate through all snippets for each participant
        snippets = participant['gaze_data']['Task'].unique().tolist()

        # reorganize data by snippet and screen size
        for snippet in snippets:
            if snippet not in fixations_by_snippet:
                fixations_by_snippet[snippet] = []

            fixations = [f for f in participant['fixations'] if f['Task'] == snippet]
            fixations_filtered = [f for f in fixations if 0 < f['AveragePositionY'] < screen_height]
            fixations_filtered = [f for f in fixations_filtered if 0 < f['AveragePositionX'] < screen_width]

            for fixation in fixations_filtered:
                x = fixation['AveragePositionX']
                y = fixation['AveragePositionY']
                point = (x, y)
                fixations_by_snippet[snippet].append(point)

    if type == 'all':
        for snippet in fixations_by_snippet:
            create_heatmap_image(snippet, fixations_by_snippet[snippet])
            create_reveal_image(snippet, fixations_by_snippet[snippet])
    elif type == 'heatmap':
        for snippet in fixations_by_snippet:
            create_heatmap_image(snippet, fixations_by_snippet[snippet])
    elif type == 'reveal_image':
        for snippet in fixations_by_snippet:
            create_reveal_image(snippet, fixations_by_snippet[snippet])

    print('-> image combined export done')
