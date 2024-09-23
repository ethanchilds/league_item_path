# %%
import pandas as pd
import pyarrow
import numpy as np

# %%
path = r'Data_Collection\Data\league_data.parquet'
df = pd.read_parquet(path)
df = df.drop(['item6', 'item3', 'item4', 'item5'], axis=1)

# %%
items = set([2501, 2502, 2503, 2504, 3001, 3002, 3003, 3004, 3005, 3006,
            3009, 3010, 3011, 3013, 3020, 3026, 3031, 3032, 3033, 3036,
            3040, 3041, 3042, 3046, 3047, 3050, 3053, 3065, 3068, 3071, 
            3072, 3073, 3074, 3075, 3078, 3083, 3084, 3085, 3087, 3089, 
            3091, 3094, 3095, 3100, 3102, 3107, 3109, 3110, 3111, 3115, 
            3116, 3117, 3118, 3121, 3124, 3135, 3137, 3139, 3142, 3143,
            3152, 3153, 3156, 3157, 3158, 3161, 3165, 3179, 3181, 3190,
            3193, 3222, 3302, 3504, 3508, 3742, 3748, 4005, 4401, 4628,
            4629, 4633, 4636, 4637, 4643, 4644, 4645, 4646, 6035, 6333, 
            6609, 6610, 6616, 6617, 6620, 6621, 6631, 6653, 6655, 6657,
            6662, 6664, 6665, 6667, 6672, 6673, 6675, 6676, 6692, 6694,
            6695, 6696, 6697, 6698, 6701, 8001, 8020])

# %%
df['item0'] = df['item0'].apply(lambda x: 0 if x not in items else x)
df['item1'] = df['item1'].apply(lambda x: 0 if x not in items else x)
df['item2'] = df['item2'].apply(lambda x: 0 if x not in items else x)

# %%
df['item0'] = df['item0'].replace({0: np.nan})
df.loc[df['item0'].isna(), 'item0'] = df.groupby(['championName'])['item0'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')

df['item1'] = df['item1'].replace({0: np.nan})
df.loc[df['item1'].isna(), 'item1'] = df.groupby(['championName'])['item1'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')

df['item2'] = df['item2'].replace({0: np.nan})
df.loc[df['item2'].isna(), 'item2'] = df.groupby(['championName'])['item2'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')

# %%
one_hot_encoded_data = pd.get_dummies(df, columns = ['championName', 'teamPosition', 'role'])

one_hot_encoded_data.info()

# %%
path = r'Modeling\model_ready.parquet'
one_hot_encoded_data.to_parquet(path, compression=None, engine='pyarrow')
