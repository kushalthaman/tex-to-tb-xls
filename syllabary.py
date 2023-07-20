import pandas as pd

all_vowels = "aáàâãạåeéèêɛiíìîɪoóòôõɔuúùûʊ"
all_cons = "hnŋbrdkstfgzmlpwyʧɲvgʣ"
dipthongs = ["ie", "uo", "ɪɛ", "ʊɔ"]

labials = "bpfvm"
coronals = "tdnlrdzʧɲszy"
dorsals = "kgŋ"
glottals = "h"
doubles = "kpgbŋmw"

stops = "gbŋmtdnɲkp"
fricatives = "fvszh"
liquids = "rl"
affricates = "ʧdz"
approximants = "yw"

back_vowels = "uʊoɔ"
round_vowels = "uʊoɔ"
high_vowels = "iɪuʊ"

voiced = "gbvdnlrdzɲzyŋmw"

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



def export_ONC(syllabary):
    onsets = {}
    nuclei = {}
    codas= {}
    
    syllable_entries = syllabary["Syllable"].astype(str)
    count_entries = syllabary["Type Frequency"].astype(int)

    for syllable, count in zip(syllable_entries, count_entries):
        onset, nuc, coda = segment(syllable)
        if onset not in onsets:
            onsets[onset] = count
        else:
            onsets[onset] += count
        if nuc not in nuclei:
            nuclei[nuc] = count
        else:
            nuclei[nuc] += count
        if coda not in codas:
            codas[coda] = count
        else:
            codas[coda] += count

    data1 = list(onsets.items())
    o_table = pd.DataFrame(data1, columns=["Onset", "Type Frequency"])
    o_table.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')
    o_table.to_excel("OnsetTable.xlsx", index=False)

    data2 = list(nuclei.items())
    n_table = pd.DataFrame(data2, columns=["Nucleus", "Type Frequency"])
    n_table.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')
    n_table.to_excel("NucleiTable.xlsx", index=False)

    data3 = list(codas.items())
    c_table = pd.DataFrame(data3, columns=["Coda", "Type Frequency"])
    c_table.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')
    c_table.to_excel("CodaTable.xlsx", index=False)


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

def manner(seg):
    if len(seg) == 0:
        return ""
    else: 
        if seg in stops:
            return "Stop"
        elif seg in fricatives:
            return "Fricative"
        elif seg in liquids:
            return "Liquid"
        elif seg in affricates: 
            return "Affricate"
        elif seg in approximants: 
            return "Approximant"

def manner_coda(syl):
    _, _, coda = segment(syl)
    return manner(coda)

def manner_onset(syl):
    onset, _, _ = segment(syl)
    return manner(onset)

def manner_nuc(syl):
    _, nuc, _ = segment(syl)
    return manner(nuc)

voiced = "gbvdnlrdzɲzjŋmw"

def voice(seg):
    if len(seg) == 0:
        return ""
    else: 
        return seg in voiced
        
def voice_coda(syl):
    _, _, coda = segment(syl)
    return voice(coda)

def voice_onset(syl):
    onset, _, _ = segment(syl)
    return voice(onset)

def voice_nuc(syl):
    _, nuc, _ = segment(syl)
    return voice(nuc)

def ATR_val(vowels):
    pATR = False
    nATR = False

    for vowel in vowels:
        if vowel in pATR_list:
            pATR = True
        if vowel in nATR_list:
            nATR = True
    
    if pATR and nATR:
        return "Nonharmonic"
    if pATR:
        return True
    if nATR:
        return False
    return "error"

# nasal_chars = ["̃", "ã", "õ"]
def nasalize(word):
    result = ""
    for char in word:
        if char == "̃":
            result = result [:-1] + "N"
        elif char in "õã":
            result += "N"
        elif char in all_vowels:
            result += "O"
        elif char == ".":
            result += "."
            
    return "N" in result # in extensions this returns a string, modified here to return a boolean

def tonalize(syllabified_word, do_syllabify):
    tonalized_word = ""
    last_tone = None

    for char in syllabified_word:
        if char == ".":
            tonalized_word += char
            last_tone = None  
        elif char in tones and last_tone != tones[char]:
            tonalized_word += tones[char]
            last_tone = tones[char]

    if not do_syllabify:
        tonalized_word = tonalized_word.replace(".", "")
        
    return tonalized_word

back_vowels = "uuʊʊooɔɔuoʊɔ"
# front_vowels = "iɪeɛ"
# "a"
round_vowels = "uuʊʊooɔɔuoʊɔ"
high_vowels = "iiɪɪuuʊʊieɪɛ"
low_vowels = "aa"
# mid_vowels = "eɛoɔ"

# diphthongs = ["ie", "uo", "ɪɛ", "ʊɔ"]

# front-central-back (back column with values true,null,false)
# high-mid-low (high boolean column AND low boolean column, mid are false,false)
# round-unround (boolean round column)

def height_high(vowel):
    return vowel in high_vowels

def height_low(vowel):
    return vowel in low_vowels

def round(vowel):
    return vowel in round_vowels

def back(vowel):
    if "a" in vowel:
        return ""
    return vowel in back_vowels
    

df = pd.read_excel("DagaareDict.xlsx")
syllabary = make_syllabary(df)
syllabary.sort_values(by = 'Type Frequency', ascending = False, inplace = True, kind = 'quicksort')

export_templates(syllabary)

syllabary['Place-Ons'] = syllabary['Syllable'].apply(place_onset)
syllabary['Place-Nuc'] = syllabary['Syllable'].apply(place_nuc)
syllabary['Place-Coda'] = syllabary['Syllable'].apply(place_coda)

syllabary['Manner-Ons'] = syllabary['Syllable'].apply(manner_onset)
syllabary['Manner-Nuc'] = syllabary['Syllable'].apply(manner_nuc)
syllabary['Manner-Coda'] = syllabary['Syllable'].apply(manner_coda)

syllabary['Voice-Ons'] = syllabary['Syllable'].apply(voice_onset)
syllabary['Voice-Nuc'] = syllabary['Syllable'].apply(voice_nuc)
syllabary['Voice-Coda'] = syllabary['Syllable'].apply(voice_coda)

syllabary['ATR'] = syllabary['Vowel'].apply(ATR_val)
syllabary['Tone'] = syllabary['Syllable'].apply(tonalize, do_syllabify = False)
syllabary['Nasal'] = syllabary['Syllable'].apply(nasalize)

syllabary['Round'] = syllabary['Vowel'].apply(round)
syllabary['High'] = syllabary['Vowel'].apply(height_high)
syllabary['Low'] = syllabary['Vowel'].apply(height_low)
syllabary['Back'] = syllabary['Vowel'].apply(back)

syllabary.to_excel("DagaareSyllabary.xlsx", index=False)
