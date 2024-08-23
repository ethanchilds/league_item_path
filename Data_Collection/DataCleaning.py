# %%
import pandas as pd

#%%
df = pd.read_json(r"C:\Users\ee11c\OneDrive\Desktop\league_item_path\Data_Collection\Raw_Data\raw_data_1.json")

df

# %%
base_raw = r'C:\Users\ee11c\OneDrive\Desktop\league_item_path\Data_Collection\Raw_Data\raw_data_'

for i in range(1,21):
