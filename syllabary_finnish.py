import pandas as pd



selected_data = data[(data['is-gold'] == 1) & (data['freq'] > 99)]

syllabary1 = pd.concat([selected_data['gold1'], selected_data['gold2'], selected_data['gold3']]).dropna()
syllabary2 = pd.concat([selected_data['lem-P1'], selected_data['lem-P2'], selected_data['lem-P3'], selected_data['lem-P4']]).dropna()
syllabary2 = syllabary2.str.replace("'", "")

residue_data = data[(data['is-gold'] == 0) | (data['is-gold'].isna())]
residue_data_gold0 = residue_data[(residue_data['is-gold'] == 0) & (residue_data['freq'] > 99)]

residue_data_gold_na = residue_data[(data['is-gold'].isna()) & (residue_data['freq'] < 100)]

print(f"Number of rows in the selected data: {len(selected_data)}")
print(f"Number of unique syllables in Syllabary 1: {len(syllabary1.unique())}")
print(f"Number of unique syllables in Syllabary 2: {len(syllabary2.unique())}")
print(f"Number of residue rows with 'is-gold' == 0 and 'freq' > 99: {len(residue_data_gold0)}")
print(f"Number of residue rows with 'is-gold' == NA and 'freq' < 100: {len(residue_data_gold_na)}")
