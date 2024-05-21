import os
from os import path

import PIL
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

from scripts.export.heatmap import Heatmapper
import config


def create_scanpath_image(participant_id, snippet, fixations_filtered, solutions):
    # find image for the snippet
    try:
        image = Image.open(path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
    except FileNotFoundError or TypeError or ValueError or PIL.UnidentifiedImageError:
        print('--> missing screen shot to create image of' + snippet)
        return

    draw = ImageDraw.Draw(image)

    # draw gaze path on top of image
    if len(fixations_filtered) == 0:
        print('--> no fixations for ', snippet)
        return

    previous_fixation = fixations_filtered[0]
    fixations_filtered.pop(0)
    for fixation in fixations_filtered:
        draw.line((
            previous_fixation['AveragePositionX'],
            previous_fixation['AveragePositionY'],
            fixation['AveragePositionX'],
            fixation['AveragePositionY']
        ),
            fill=(255, 0, 0),
            width=2
        )
        previous_fixation = fixation

    # draw solution and participant response
    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=40)

    solution = solutions.loc[solutions.Task == snippet, 'Solution'].item()
    # participant_responses = responses.loc[responses.SubjectID == participant['id']]
    # response = participant_responses.loc[participant_responses.Snippet == snippet, 'Result'].item()
    # time = participant_responses.loc[participant_responses.Snippet == snippet, 'Time'].item()

    draw.text((10, 10), "Solution: " + solution, fill=(0, 0, 0), font=font)
    # draw.text((10, 60), "Antwort: " + response, fill=(0, 0, 0), font=font)
    # draw.text((10, 110), "Zeit: %3.1fs" % (int(time) / 1000.0), fill=(0, 0, 0), font=font)

    participant_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'IndividualExport', participant_id, 'Scanpaths')
    if not os.path.exists(participant_dir):
        os.makedirs(participant_dir)

    # save png
    image.save(participant_dir + '/scanpath_' + snippet + '.png', optimize=True, quality=90)


def create_heatmap_image(participant_id, snippet, fixation_points):
    # find image for the snippet
    try:
        image = Image.open(path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
    except FileNotFoundError or TypeError or ValueError or PIL.UnidentifiedImageError:
        print('--> missing screen shot to create image of ' + snippet)
        return

    participant_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'IndividualExport', participant_id, 'Heatmaps')
    if not os.path.exists(participant_dir):
        os.makedirs(participant_dir)

    heatmapper = Heatmapper(colours='default', point_diameter=120, point_strength=0.3, opacity=0.65)
    heatmapper.heatmap_on_img(fixation_points, image).save(participant_dir + '/heatmap_' + snippet + '.png',
                                                           optimize=True, quality=90)


def create_reveal_image(participant_id, snippet, fixation_points):
    # find image for the snippet
    try:
        image = Image.open(path.join(config.PATH_SNIPPET_IMAGES_DIR, snippet + '.png'))
    except FileNotFoundError or TypeError or ValueError or PIL.UnidentifiedImageError:
        print('--> missing screen shot to create image of ' + snippet)
        return

    participant_dir = os.path.join(config.PATH_SNIPPET_OVERLAYS, 'IndividualExport', participant_id, 'Reveal')
    if not os.path.exists(participant_dir):
        os.makedirs(participant_dir)

    heatmapper = Heatmapper(colours='reveal', point_diameter=150, point_strength=0.2, opacity=0.9)
    heatmapper.heatmap_on_img(fixation_points, image).save(participant_dir + '/reveal_' + snippet + '.png',
                                                           optimize=True, quality=90)


def export_individual_data(preprocessed_data, type='all'):
    print('\n## EXPORT INDIVIDUAL DATA AS PNG')
    # read solutions
    solutions = pd.read_csv(config.PATH_SNIPPET_SOLUTIONS_CSV, delimiter=';')
    # responses = pd.read_csv(path.join('studies', config.CURRENT_STUDY, 'BehavioralData_Results.csv'), delimiter=';')

    data = pd.read_csv(config.PATH_DEMOGRAPHICS + '/GeneralInfo.csv')

    # read participant data
    for i, participant in enumerate(preprocessed_data):
        print('-> working on participant: ', participant['id_short'])

        participant_data = data.loc[data.SubjectID == participant['id']]
        screen_width = participant_data['ActualScreenWidth'].item()
        screen_height = participant_data['ActualScreenHeight'].item()

        # iterate through all snippets for each participant
        snippets = participant['gaze_data']['Task'].unique().tolist()

        for snippet in snippets:
            fixations = [f for f in participant['fixations'] if f['Task'] == snippet]
            fixations_filtered = [f for f in fixations if 0 < f['AveragePositionY'] < screen_height]
            fixations_filtered = [f for f in fixations_filtered if 0 < f['AveragePositionX'] < screen_width]

            fixations_points = []

            for fixation in fixations_filtered:
                x = fixation['AveragePositionX']
                y = fixation['AveragePositionY']
                point = (x, y)
                fixations_points.append(point)

            if type == 'all':
                create_heatmap_image(participant['id_short'], snippet, fixations_points)
                create_reveal_image(participant['id_short'], snippet, fixations_points)
                create_scanpath_image(participant['id_short'], snippet, fixations_filtered, solutions)
            if type == 'heatmap':
                create_heatmap_image(participant['id_short'], snippet, fixations_points)
            if type == 'reveal_image':
                create_reveal_image(participant['id_short'], snippet, fixations_points)
            if type == 'scan_path':
                create_scanpath_image(participant['id_short'], snippet, fixations_filtered, solutions)

    print('-> export of participant data as images done!')
