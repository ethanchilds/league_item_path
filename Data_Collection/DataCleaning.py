# %%
import pandas as pd

# %%
base_raw = r'C:\Users\ee11c\OneDrive\Desktop\league_item_path\Data_Collection\Raw_Data\raw_data_'

df = pd.read_json(base_raw + '1.json')

for i in range(2,21):
    next_df = pd.read_json(base_raw + str(i) + '.json')

    df = pd.concat([df, next_df], ignore_index=True)


# %%
meta = pd.json_normalize(df['metadata'])
info = pd.json_normalize(df['info'])

normal1 = pd.concat([meta.rename(columns={'participants':'participant_id'}), info], axis=1)

# %%
participant = pd.json_normalize(normal1['participants'])
team = pd.json_normalize(normal1['teams'])

normal2 = pd.concat([normal1.drop(columns=['participants', 'teams']), participant, team.rename(columns={'0':"blue", '1':"red"})], axis=1)

# %%
normal2.head(1)
# %%
