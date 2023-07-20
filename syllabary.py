import pandas as pd

all_vowels = "aáàâãạåeéèêɛiíìîɪoóòôõɔuúùûʊ"
all_cons = "hnŋbrdkstfgzmlpwyʧɲvgʣ"
dipthongs = ["ie", "uo", "ɪɛ", "ʊɔ"]

labials = "bpfvm"
coronals = "tdnlrdzʧɲszj"
dorsals = "kgŋ"
glottals = "h"
doubles = ["kp", "gb", "ŋm", "w"]

stops = ["bpmtdnɲkgŋ", "kp", "gb", "ŋm"] # need to reformat
fricatives = "fvszh"
liquids = "rl"
affricates = ["ʧ", "dz"]
approximants = "jw"

back_vowels = "uʊoɔ"
round_vowels = "uʊoɔ"
high_vowels = "iɪuʊ"

voiced = ["bvmdnlrdzɲzjgŋ", "gb", "ŋm", "w"]

# duplicated from extensions.py
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

# duplicated from extensions.py
def vowelize(word):
    vowels = [accent_strip(char) for char in word if char.lower() in all_vowels or char == "."]
    return "".join(vowels)

# returns the segmental structure of input syllable as a string of Cs and Vs
def templatize(syl):
    result = ""
    for char in syl:
        if char in all_vowels:
            result += "V"
        elif char in all_cons:
            result += "C"
    return result.replace("CC", "C")


def make_syllabary(df):
    syllables = []
    # vowels_list = ["a","á","à","â","ã","ạ","å","a","e","é","è","ê","ɛ","i","í","ì","î","ɪ","o","ó","ò","ô","õ","ɔ","u","ú","ù","û","ʊ"]
    # consonants_list = list(all_cons)

    column_entries = df["PH + Syl"].astype(str)

    # collects all syllables
    for word, excluded in zip (column_entries.tolist(), df["Excluded"].tolist()):
        if excluded: # excluded words should not be considered
            continue
        word_syls = word.split(".")
        syl_1 = [word_syls[0].replace("-", ""), True] # removed dashes, must remember to document that we did this
        syllables.append(syl_1)
        word_syls.pop(0)
        for syl in word_syls:
            syllables.append([syl.replace("-", ""), False])

    # repeated_vowels = [v + v for v in vowels_list] 
    # long_vowels = repeated_vowels + dipthongs

    # determines if a syllable is heavy (if it has a coda or a long nucleus)
    # a heavy syllable is labeled as "true"
    def syllable_weight(template):
        # return any(sub_s.endswith(tuple(consonants_list)) or sub_s.endswith(tuple(long_vowels)) for sub_s in s.split('.')) # wrong results in some entries, like "dã́ã́" (98)
        # also dubious of labeling "C" as heavy (if there are real C-only syllables, C is def the nucleus)
        return "VC" in template or "VV" in template

    syllabary = pd.DataFrame(syllables, columns=["Syllable", "Initial"])
    
    syllabary['Type Frequency'] = syllabary.groupby(["Syllable", "Initial"]).transform('size')

    syllabary = syllabary.drop_duplicates(keep="last")

    syllabary['Vowel'] = syllabary['Syllable'].apply(vowelize)

    syllabary["Template"] = syllabary["Syllable"].apply(templatize)

    syllabary['Syllable Weight'] = syllabary['Template'].apply(syllable_weight)
    
    return syllabary

def export_templates(syllabary):
    template_entries = syllabary["Template"].astype(str)
    count_entries = syllabary["Type Frequency"].astype(int)

    templates = {}

    for template, count in zip(template_entries, count_entries):
        if template not in templates:
            templates[template] = count
        else:
            templates[template] += count

    print(templates)

    data = list(templates.items())
    template_table = pd.DataFrame(data, columns=["Template", "Type Frequency"])
    template_table.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')
    template_table.to_excel("TemplateTable.xlsx", index=False)


def segment(syl): 
    onset = ""
    nucleus = ""
    coda = ""

    first_non_consonant = False 
    
    if templatize(syl) == "C":
        return [onset, syl, coda]

    for ch in syl: 
        if first_non_consonant == False and ch not in list(all_cons):
            first_non_consonant = True
        if first_non_consonant == True and ch in list(all_cons):
            coda += ch
        if first_non_consonant == False: 
            onset += ch
    return [onset, "", coda]


labials = "bpfvm"
coronals = "tdnlrdzʧɲszj"
dorsals = "kgŋ"
glottals = "h"
doubles = ["kp", "gb", "ŋm", "w"]

def place(seg):
    if len(seg) == 0:
        return ""
    else: 
        if seg in labials:
            return "Labial"
        elif seg in coronals:
            return "Coronal"
        elif seg in dorsals:
            return "Dorsal"
        elif seg in glottals: 
            return "Glottal"
        elif seg in doubles: 
            return "Double"

def place_coda(syl):
    _, _, coda = segment(syl)
    return place(coda)

def place_onset(syl):
    onset, _, _ = segment(syl)
    return place(onset)

def place_nuc(syl):
    _, nuc, _ = segment(syl)
    return place(nuc)

df = pd.read_excel("DagaareDict.xlsx")
syllabary = make_syllabary(df)
syllabary.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')

export_templates(syllabary)

syllabary.to_excel("DagaareSyllabary.xlsx", index=False)
