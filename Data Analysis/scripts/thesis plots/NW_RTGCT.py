import pandas as pd

import config

aoi_map = pd.read_csv(config.PATH_LINEARITY_METRICS + '/Snippet_AOI_Reading_Order_Map.csv')
# drop AOIMap Column
aoi_map = aoi_map.drop(columns=['AOIMap'])

# for each snippet (row) make the following in one file
# AOIName (from array)	FixationDuration (1)	Stimulus (Snippet Name)	Participant (Name of the column)
# iterate over the rows
with open('/Users/Youssef/Desktop/aoi_map_new_without_codeonly.csv', 'w') as f:
    f.write('AOIName,FixationDuration,Stimulus,Participant\n')
    for index, row in aoi_map.iterrows():
        # get the snippet name
        snippet_name = row['SnippetName']
        if 'CM' in snippet_name:
            continue
        # get the data for the participant for each participant (StoryOrderCodeFirst	StoryOrderCommentFirst	StoryOrderCodeOnly	ExecutionOrderCodeFirst	ExecutionOrderCommentFirst	ExecutionOrderCodeOnly	StoryOrderGlobal	ExecutionOrderGlobal)
        for column in aoi_map.columns[1:]:
            if 'Global' in column:
                continue
            if 'CodeOnly' in column:
                continue
            # get the AOIName from the array in that column and make for each int in the array a row
            # convert to array of ints to split
            aoi_name = row[column]
            # split the array
            aoi_name = aoi_name.lstrip('[').rstrip(']').split(',')
            # get the fixation duration for that AOIName
            fixation_duration = 1
            # get the participant name
            participant = column
            # get the stimulus name
            stimulus = snippet_name
            # write to file
            for aoi in aoi_name:
                f.write(f'{aoi},{fixation_duration},{stimulus},{participant}\n')
