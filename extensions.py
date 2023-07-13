## Creates vowel, ATR, excluded, PH + Syl, Syl Count

import pandas as pd

#cons_list = ["h", "n", "ŋ", "b", "r", "d", "k", "s", "t", "f", "g", "z", "m", "l", "p", "w", "y", "ʧ", "ɲ", "v", "g", "ʣ"]

all_cons = "hnŋbrdkstfgzmlpwyʧɲvgʣ"
all_vowels = "aáàâãạåeéèêɛiíìîɪoóòôõɔuúùûʊ"
# extra_chars = "- "
exclude_list = ",\\Dạå᷈"
digraphs = ["gb", "kp", "ŋm", "dz"]
pATR_list = "eiou"
nATR_list = "aɛɪɔʊ"
dipthongs = ["ie", "uo", "ɪɛ", "ʊɔ"]
tones = {"á":"H", "é":"H", "í":"H", "ó":"H", "ú" : "H", "à":"L", "è":"L", "ì":"L", "ò":"L", "ù":"L", "â":"HL", "ê":"HL", "ô" : "HL", "û": "HL", "ǎ":"LH"}

def first_seg(ind, word):
    if ind+1 < len(word) and word[ind] + word[ind+1] in digraphs:
        ind += 1
    for char in word[ind+1:]:
        if char in all_cons + all_vowels:
            return char
    return False

def is_exclude(word):
    for char in word:
        if char in exclude_list:
            return True
    return False

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

def syllabify(word):  # not sensible for excluded words
    result = ""
    prev_seg = None

    # if this is 
    for ind, char in enumerate(word):
        if not (prev_seg == None or prev_seg + char in digraphs):
            prev_stripped = accent_strip(prev_seg)
            cur_stripped = accent_strip(char)
            if (prev_seg in all_vowels and char in all_vowels) and (prev_stripped != cur_stripped and prev_stripped + cur_stripped not in dipthongs):
                result += "."
            elif prev_seg and prev_seg in all_cons and char in all_cons:
                result += "."
            elif prev_seg and prev_seg in all_vowels and char in all_cons and first_seg(ind, word) and first_seg(ind, word) in all_vowels:
                result += "."

        result += char

        if char in all_cons or char in all_vowels:
            prev_seg = char

    return result

def count_syl(word):
    return word.count(".") + 1

def vowelize(word):
    vowels = [accent_strip(char) for char in word if char.lower() in all_vowels]
    return "".join(vowels)

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

df = pd.read_excel("DagaareDict.xlsx")

df["PH"] = df["PH"].astype(str)

df["Vowels"] = df["PH"].apply(vowelize)

df["ATR"] = df["Vowels"].apply(ATR_val)

df["PH + Syl"] = df["PH"].apply(syllabify)

df["Syl Count"] = df["PH + Syl"].apply(count_syl)

df["Excluded"] = df["PH"].apply(is_exclude)


df.to_excel("DagaareDict.xlsx", index = False)
