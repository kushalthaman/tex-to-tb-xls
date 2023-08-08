import pandas as pd
import numpy as np

## Sanity checks

df = pd.read_csv('aamulehti-1999.csv', sep='\t')
print(df.head())

df_gold = df[(df['is.gold'] == 1) & (df['frequency'] > 99)]

gold0_df = df[df['is.gold'] == 0]

null_gold1 = gold0_df['gold1'].isnull().sum()
print(f"Rows with 'is.gold' == 0 and null 'gold1': {null_gold1}")

high_freq_gold0_df = gold0_df[gold0_df['frequency'] > 99]
print(f"Rows with 'is.gold' == 0 and frequency > 99: {len(high_freq_gold0_df)}")

gold_na_df = df[df['is.gold'].isnull()]
non_null_gold1 = gold_na_df['gold1'].notnull().sum()
print(f"Rows with 'is.gold' == NA and non-null 'gold1': {non_null_gold1}")

high_freq_gold_na_df = gold_na_df[gold_na_df['frequency'] >= 100]
print(f"Rows with 'is.gold' == NA and frequency >= 100: {len(high_freq_gold_na_df)}")

df_gold = df[(df['is-gold'] == 1) & (df['freq'] > 99)]
print(f"Rows with 'is-gold' == 1 and freq > 99: {len(df_gold)}")

## syllabary 

syllabary1 = set()
for col in ["gold1", "gold2", "gold3"]: 
    syllabary1.update(filtered_df[col].dropna().tolist())

syllabary2 = set()
for col in ["lem-P1", "lem-P2", "lem-P3"]:  
    syllabary2.update(filtered_df[col].str.replace("'", "").dropna().tolist()) # remove accent marks? 

print("Syllabary 1:", syllabary1)
print("Syllabary 2:", syllabary2)
