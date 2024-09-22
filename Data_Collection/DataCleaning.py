# %%
import pandas as pd
import pyarrow

# %%
base_raw = r'C:\Users\Ethan\Desktop\league_item_path\Data_Collection\Raw_Data\raw_data_'

df = pd.read_json(base_raw + '1.json')

for i in range(2,21):
    next_df = pd.read_json(base_raw + str(i) + '.json')

    df = pd.concat([df, next_df], ignore_index=True)


# %%
meta = pd.json_normalize(df['metadata'])
info = pd.json_normalize(df['info'])

normal1 = pd.concat([meta.rename(columns={'participants':'participant_id'}), info], axis=1)
normal1 = normal1[normal1['gameMode'] == 'CLASSIC']

# %%
clean = normal1.drop(columns={'participant_id'}).explode('participants')

# %%
participants = pd.json_normalize(clean['participants'])

columns_to_keep = [
    'champExperience', 'champLevel', 'championId', 'championName', 'item0', 'item1', 'item2', 
    'item3', 'item4', 'item5', 'item6', 'profileIcon', 'role', 'summoner1Id', 'summoner2Id', 
    'summonerLevel', 'teamId', 'teamPosition'
]

participants_filtered = participants.loc[:, columns_to_keep]

# %%
teams = pd.json_normalize(clean['teams'])

team0 = pd.json_normalize(teams[0])
team1 = pd.json_normalize(teams[1])

# %%
bans0 = pd.json_normalize(team0['bans'])

replacement_value = {'championId': 0, 'pickTurn': None}

bans0 = bans0.applymap(lambda x: replacement_value if x is None else x)
bans0 = bans0.applymap(lambda x: x['championId'])

bans0 = bans0.rename(columns = {0: 'bans0_1', 1: 'bans0_2', 2: 'bans0_3', 3: 'bans0_4', 4: 'bans0_5'})

# %%
bans1 = pd.json_normalize(team1['bans'])

replacement_value = {'championId': 0, 'pickTurn': None}

bans1 = bans1.applymap(lambda x: replacement_value if x is None else x)
bans1 = bans1.applymap(lambda x: x['championId'])

bans1 = bans1.rename(columns = {0: 'bans1_1', 1: 'bans1_2', 2: 'bans1_3', 3: 'bans1_4', 4: 'bans1_5'})

# %%
bans = pd.concat([bans0, bans1], axis=1)

# %%
final = pd.concat([participants_filtered, bans], axis=1)

# %%
path = r'C:\Users\Ethan\Desktop\league_item_path\Data_Collection\Data\league_data.parquet'
final.to_parquet(path, compression=None, engine='pyarrow')
