#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import pandas as pd
import math
df = pd.read_csv('../data.csv')
df.drop(['game_event_id','game_id','lat','lon','loc_x','loc_y','team_id','team_name','game_date'],axis=1)

#process
df['time_remaining'] = df.apply(lambda row: math.sqrt(row['minutes_remaining']*60+ row['seconds_remaining']), axis=1)
df['last_moment'] = df.apply(lambda row: 1 if row['time_remaining'] < 3 else 0, axis=1)
df.drop(['seconds_remaining'], axis=1)

df['mat'] = df.apply(lambda row: 1 if '@' in row['matchup'] else 0, axis=1)


df['sea'] = df.apply(lambda row: int(row['season'].split('-')[0])-1998, axis=1)

df['place'] = df.apply(lambda row: row['matchup'].split(' ')[2] if row['matchup'].split(' ')[1]=='@' else row['matchup'][0], axis=1)

df.drop(['matchup','season'],axis=1,inplace=True)
#category
data = pd.DataFrame()

continue_features=['shot_id','shot_made_flag','shot_distance','minutes_remaining','sea','last_moment', 'mat']
for f in continue_features:
    data = pd.concat([data,df.loc[:,[f]]],axis=1)

category_features=['place','action_type','combined_shot_type','period','playoffs','shot_type','shot_zone_area','shot_zone_basic','shot_zone_range', 'opponent']
for f in category_features:
    data = pd.concat([data, pd.get_dummies(df[f],prefix=f)],axis=1)

data.set_index('shot_id', inplace=True)
data.to_csv('d.csv', index=False)
