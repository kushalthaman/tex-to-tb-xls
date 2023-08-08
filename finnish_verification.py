#Finnish verification
import pandas as pd
import numpy as np

df = pd.read_csv('aamulehti-1999.csv', sep=',')
print(df.head())

# print("Columns Below:")
# print(df.columns.tolist())

df_gold = df[(df['is-gold'] == 1) & (df['freq'] > 99)]
gold0_df = df[df['is-gold'] == 0]

null_gold1 = gold0_df['gold1'].isnull().sum()
print(f"Rows with 'is-gold' == 0 and null 'gold1': {null_gold1}")

high_freq_gold0_df = gold0_df[gold0_df['freq'] > 99]
print(f"Rows with 'is-gold' == 0 and freq > 99: {len(high_freq_gold0_df)}")

gold_na_df = df[df['is-gold'].isnull()]
non_null_gold1 = gold_na_df['gold1'].notnull().sum()
print(f"Rows with 'is-gold' == NA and non-null 'gold1': {non_null_gold1}")

high_freq_gold_na_df = gold_na_df[gold_na_df['freq'] >= 100]
print(f"Rows with 'is-gold' == NA and freq >= 100: {len(high_freq_gold_na_df)}")

df_gold = df[(df['is-gold'] == 1) & (df['freq'] > 99)]
print(f"Rows with 'is-gold' == 1 and freq > 99: {len(df_gold)}")
