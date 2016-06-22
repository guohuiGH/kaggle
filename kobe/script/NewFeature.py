import numpy as np
import pandas as pd

from xgboost.sklearn import XGBClassifier
from sklearn.cross_validation import cross_val_score

# Load data and roughly clean it, then sort as game date
df = pd.read_csv("../data.csv")
df.drop(['game_event_id', 'game_id', 'lat', 'lon', 'team_id', 'team_name'], axis=1, inplace=True)
df.sort('game_date',  inplace=True)
mask = df['shot_made_flag'].isnull()


# Clean data
actiontypes = dict(df.action_type.value_counts())
df['type'] = df.apply(lambda row: row['action_type'] if actiontypes[row['action_type']] > 20\
                          else row['combined_shot_type'], axis=1)
df.drop(['action_type', 'combined_shot_type'], axis=1, inplace=True)

df['away'] = df.matchup.str.contains('@')
df.drop('matchup', axis=1, inplace=True)

df['distance'] = df.apply(lambda row: row['shot_distance'] if row['shot_distance'] <45 else 45, axis=1)

df['time_remaining'] = df.apply(lambda row: row['minutes_remaining'] * 60 + row['seconds_remaining'], axis=1)
df['last_moments'] = df.apply(lambda row: 1 if row['time_remaining'] < 3 else 0, axis=1)

data = pd.get_dummies(df['type'],prefix="action_type")

features=["away", "period", "playoffs", "shot_type", "shot_zone_area", "shot_zone_basic", "season",
           "shot_zone_range", "opponent", "distance", "minutes_remaining", "last_moments"]
for f in features:
    data = pd.concat([data, pd.get_dummies(df[f], prefix=f),], axis=1)

data.to_csv('../data/temp.csv')
