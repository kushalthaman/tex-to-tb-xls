import pandas as pd

all_vowels = "aáàâãạåeéèêɛiíìîɪoóòôõɔuúùûʊ"
all_cons = "hnŋbrdkstfgzmlpwyʧɲvgʣ"

def accent_strip(c):
    if c == "á" or c == "à" or c == "â" or c == "ã" or c == "ạ" or c == "å":  # ạ å very strange
        return "a"
    if c == "é" or c == "è" or c == "ê":
        return "e"
    if c == "í" or c == "ì" or c == "î":
        return "i"
    if c == "ó" or c == "ò" or c == "ô" or c == "õ":
        return "o"
    if c == "ú" or c == "ù" or c == "û":
        return "u"
    
    return c

def vowelize(word):
    vowels = [accent_strip(char) for char in word if char.lower() in all_vowels or char == "."]
    return "".join(vowels)

def templatize(syl):
    result = ""
    for char in syl:
        if char in all_vowels:
            result += "V"
        elif char in all_cons:
            result += "C"
    return result.replace("CC", "C")


def make_syllabary(df, column):
    syllables = []
    # vowels = ["a","á","à","â","ã","ạ","å","a","e","é","è","ê","ɛ","i","í","ì","î","ɪ","o","ó","ò","ô","õ","ɔ","u","ú","ù","û","ʊ"]

    column_entries = df[column].astype(str)

    for word in column_entries.tolist():
        word_syls = word.split(".")
        syl_1 = [word_syls[0].replace("-", ""), True] # removed dashes, must remember to document that we did this
        syllables.append(syl_1)
        word_syls.pop(0)
        for syl in word_syls:
            syllables.append([syl.replace("-", ""), False])
    
    syllabary = pd.DataFrame(syllables, columns=["Syllable", "Initial"])
    syllabary['Type Frequency'] = syllabary.groupby(["Syllable", "Initial"]).transform('size')

    syllabary = syllabary.drop_duplicates(keep="last")

    syllabary['Vowels'] = syllabary['Syllable'].apply(vowelize)

    syllabary["Template"] = syllabary["Syllable"].apply(templatize)
    
    return syllabary

def print_templates(syllabary):
    column_entries = syllabary["Template"].astype(str)

    templates = {}

    for template in column_entries:
        if template not in templates:
            templates[template] = 1
        else:
            templates[template] += 1

    print(templates)




df = pd.read_excel("DagaareDict.xlsx")
syllabary = make_syllabary(df, column = "PH + Syl")
syllabary.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')

print_templates(syllabary)

syllabary.to_excel("DagaareSyllabary.xlsx", index=False)
