import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('FinnishTemplateTable1.xlsx', engine='openpyxl')

simple_templates = ["VVC", "VV", "VC", "V", "CVVC", "CVV", "CVC", "CV"]
complex_templates = ["CCCVCC", "CCCVVC", "VCCC", "CCCV", "VVCC", "CVVCC", "CVCCC", "CCCVC", "CCVVC", "CCVV", "CCVCC", "VCC", "CCVC", "CCV", "CVCC", "CCCVCC", "CCCVVC", "VCCC"]

simple_df = df[df['Template'].isin(simple_templates)].groupby('Template').sum()['Type Frequency'].sort_values(ascending=False)
complex_df = df[df['Template'].isin(complex_templates)].groupby('Template').sum()['Type Frequency'].sort_values(ascending=False)

plt.figure(figsize=(10, 6))
simple_df.plot(kind='barh')
plt.ylabel('Simple Templates')
plt.xlabel('Type Frequency')
plt.title('Text frequencies of syllables with Simple Margins')
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
complex_df.plot(kind='barh')
plt.ylabel('Complex Templates')
plt.xlabel('Type Frequency')
plt.title('Text frequencies of syllables with Complex Margins')
plt.tight_layout()
plt.show()
