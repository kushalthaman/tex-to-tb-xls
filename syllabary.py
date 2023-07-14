import pandas as pd

def make_syllabary(df, column):
    syllables = []
    for word in df[column].tolist():
        syllables.extend(word.split('.'))
    
    syllabary = pd.DataFrame(syllables, columns=["syllable"])
    syllabary['frequency'] = syllabary.groupby('syllable')['syllable'].transform('count')
    return syllabary

df = pd.read_excel("DagaareDict.xlsx")
syllabary = make_syllabary(df, column = "PH+Syl")
syllabary.to_excel("DagaareSyllabary.xlsx", index=False)

  
