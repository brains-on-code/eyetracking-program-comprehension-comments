import os

import pandas as pd

import config


def get_story_order_code_first(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_story_order = reading_order.loc[reading_order['Task'] == snippet_name, 'StoryOrder'].item().split(', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_story_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CPC' in aoi_name:
                order.append(int(aoi_name.split('CPC')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_1.split('CPL')[1]))
                order.append(int(aoi_name_2.split('CPC')[1]))
            else:
                order.append(int(aoi_name_2.split('CPL')[1]))
                order.append(int(aoi_name_1.split('CPC')[1]))

    return order


def get_story_order_comment_first(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_story_order = reading_order.loc[reading_order['Task'] == snippet_name, 'StoryOrder'].item().split(', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_story_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CPC' in aoi_name:
                order.append(int(aoi_name.split('CPC')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_2.split('CPC')[1]))
                order.append(int(aoi_name_1.split('CPL')[1]))
            else:
                order.append(int(aoi_name_1.split('CPC')[1]))
                order.append(int(aoi_name_2.split('CPL')[1]))

    return order


def get_story_order_code_only(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_story_order = reading_order.loc[reading_order['Task'] == snippet_name, 'StoryOrder'].item().split(', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_story_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CML' in aoi_name:
                order.append(int(aoi_name.split('CML')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_1.split('CPL')[1]))
            elif 'CPL' in aoi_name_2:
                order.append(int(aoi_name_2.split('CPL')[1]))

    return order


def get_story_order_global(snippet_name, reading_order):
    snippet_story_order = reading_order.loc[reading_order['Task'] == snippet_name, 'StoryOrder'].item().split(', ')
    # convert the list of strings to a list of ints
    snippet_story_order = list(map(int, snippet_story_order))

    return snippet_story_order


def get_execution_order_code_first(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_execution_order = reading_order.loc[reading_order['Task'] == snippet_name, 'ExecutionOrder'].item().split(
        ', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_execution_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CPC' in aoi_name:
                order.append(int(aoi_name.split('CPC')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_1.split('CPL')[1]))
                order.append(int(aoi_name_2.split('CPC')[1]))
            else:
                order.append(int(aoi_name_2.split('CPL')[1]))
                order.append(int(aoi_name_1.split('CPC')[1]))

    return order


def get_execution_order_comment_first(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_execution_order = reading_order.loc[reading_order['Task'] == snippet_name, 'ExecutionOrder'].item().split(
        ', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_execution_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CPC' in aoi_name:
                order.append(int(aoi_name.split('CPC')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_2.split('CPC')[1]))
                order.append(int(aoi_name_1.split('CPL')[1]))
            else:
                order.append(int(aoi_name_1.split('CPC')[1]))
                order.append(int(aoi_name_2.split('CPL')[1]))

    return order


def get_execution_order_code_only(snippet_name, reading_order):
    order = []
    aois = get_snippet_aois(snippet_name)
    snippet_execution_order = reading_order.loc[reading_order['Task'] == snippet_name, 'ExecutionOrder'].item().split(
        ', ')
    # loop over snippet story order and locate all entries in aois where the line number matches the snippet story order
    for line_number in snippet_execution_order:
        matched_aois = aois.loc[aois['LineNumber'] == int(line_number)]
        if len(matched_aois) == 1:
            aoi_name = matched_aois['AOIName'].item()
            if 'CPL' in aoi_name:
                order.append(int(aoi_name.split('CPL')[1]))
            elif 'CML' in aoi_name:
                order.append(int(aoi_name.split('CML')[1]))
        else:
            aoi_name_1 = matched_aois.iloc[0]['AOIName']
            aoi_name_2 = matched_aois.iloc[1]['AOIName']
            if 'CPL' in aoi_name_1:
                order.append(int(aoi_name_1.split('CPL')[1]))
            elif 'CPL' in aoi_name_2:
                order.append(int(aoi_name_2.split('CPL')[1]))

    return order


def get_execution_order_global(snippet_name, reading_order):
    snippet_execution_order = reading_order.loc[reading_order['Task'] == snippet_name, 'ExecutionOrder'].item().split(
        ', ')
    # convert the list of strings to a list of ints
    snippet_execution_order = list(map(int, snippet_execution_order))

    return snippet_execution_order


def get_aoi_map(aois):
    # get the AOI points from the ShapePts column containing a string and return a map
    # with the AOI name as key and the AOI points as value
    aoi_map = {}

    for index, row in aois.iterrows():
        aoi_points = row['ShapePts']
        p0_x = float(aoi_points.split(' ')[0].split(';')[0].split('(')[1])
        p0_y = float(aoi_points.split(' ')[0].split(';')[1].split(')')[0])
        p1_x = float(aoi_points.split(' ')[1].split(';')[0].split('(')[1])
        p2_y = float(aoi_points.split(' ')[2].split(';')[1].split(')')[0])
        line = row['LineNumber']
        aoi_map[row['AOIName']] = [p0_x, p0_y, p1_x, p2_y, line]

    return aoi_map


def get_snippet_aois(snippet_name):
    file_name = snippet_name + ' aois.txt'

    df = pd.read_csv(os.path.join(config.PATH_AOI_DIR, file_name), sep='\t')
    df = df[['SnippetName', 'LineNumber', 'ShapeName', 'ShapePts']]
    df.rename(index=str, inplace=True, columns={'SnippetName': 'Stimulus', 'ShapeName': 'AOIName'})
    return df


def compute_aois(snippet):
    aois = get_snippet_aois(snippet)
    aoi_map = get_aoi_map(aois)
    reading_order = pd.read_csv(config.PATH_LINE_READING_ORDER_CSV, sep=';')
    story_order = [get_story_order_code_first(snippet, reading_order),
                   get_story_order_comment_first(snippet, reading_order),
                   get_story_order_code_only(snippet, reading_order),
                   get_story_order_global(snippet, reading_order)]
    execution_order = [get_execution_order_code_first(snippet, reading_order),
                       get_execution_order_comment_first(snippet, reading_order),
                       get_execution_order_code_only(snippet, reading_order),
                       get_execution_order_global(snippet, reading_order)]

    return [aoi_map, story_order, execution_order]


def generate_snippet_aoi_reading_order_map():
    # create a csv file with the following columns:
    snippets = config.SNIPPETS
    df = pd.DataFrame(columns=['SnippetName', 'AOIMap', 'StoryOrderCodeFirst', 'StoryOrderCommentFirst',
                               'StoryOrderCodeOnly', 'ExecutionOrderCodeFirst', 'ExecutionOrderCommentFirst',
                               'ExecutionOrderCodeOnly'])
    snippets_info = {}
    for snippet in snippets:
        aoi_map, story_order, execution_order = compute_aois(snippet)
        df = pd.concat(
            [df, pd.DataFrame([[snippet, aoi_map, story_order[0], story_order[1], story_order[2], story_order[3],
                                execution_order[0], execution_order[1], execution_order[2], execution_order[3]]],
                              columns=['SnippetName', 'AOIMap',
                                       'StoryOrderCodeFirst',
                                       'StoryOrderCommentFirst',
                                       'StoryOrderCodeOnly',
                                       'StoryOrderGlobal',
                                       'ExecutionOrderCodeFirst',
                                       'ExecutionOrderCommentFirst',
                                       'ExecutionOrderCodeOnly',
                                       'ExecutionOrderGlobal'])])
        snippets_info[snippet] = [aoi_map, story_order, execution_order]

    df.to_csv(config.PATH_LINEARITY_METRICS + '/Snippet_AOI_Reading_Order_Map.csv', index=False)

    return snippets_info
