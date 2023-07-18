import pandas as pd

def make_syllabary(df, column):
    syllables = []
    vowels = ["a","á","à","â","ã","ạ","å","a","e","é","è","ê","ɛ","i","í","ì","î","ɪ","o","ó","ò","ô","õ","ɔ","u","ú","ù","û","ʊ"]
    
    for word in df[column].tolist():
        syllables.extend(word.split('.'))
    
    syllabary = pd.DataFrame(syllables, columns=["syllable"])
    syllabary['Type Frequency'] = syllabary.groupby('syllable')['syllable'].transform('count')

    def all_vowels(word):
        return [vowel for vowel in vowels if vowel in word]

    syllabary['Vowel'] = syllabary['syllable'].apply(all_vowels)
        
    return syllabary

df = pd.read_excel("DagaareDict.xlsx")
syllabary = make_syllabary(df, column = "PH+Syl")
syllabary.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')
syllabary.to_excel("DagaareSyllabary.xlsx", index=False)

  
