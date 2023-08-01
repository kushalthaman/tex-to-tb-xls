import pandas as pd

df = pd.read_csv('path_to_your_file.csv')

df_gold = df[df['is.gold'] == 1]
df_freq = df_gold[df_gold['freq'] > 99]

syllabary1 = df_freq[['gold1', 'gold2', 'gold3']].values.flatten()
syllabary1 = pd.Series(syllabary1).dropna().unique()
syllabary2 = df_freq['lem-P1'].unique()

df_not_gold = df[df['is.gold'] == 0]
df_high_freq = df_not_gold[df_not_gold['freq'] > 99]

df_na_gold = df[df['is.gold'].isna()]
df_empty_gold1 = df_na_gold[df_na_gold['gold1'].isna()]
