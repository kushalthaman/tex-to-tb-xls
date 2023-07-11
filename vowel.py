## Creates vowel and ATR column

import pandas as pd

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
    vowels = [accent_strip(char) for char in word if char.lower() in "aáàâãạåeéèêɛiíìîɪoóòôõɔuúùûʊ"]
    return "".join(vowels)

def ATR_val(vowels):
    pATR_list = ["e", "i", "o", "u"]
    nATR_list = ["a", "ɛ", "ɪ", "ɔ", "ʊ"]

    pATR = False
    nATR = False

    for vowel in vowels:
        if vowel in pATR_list:
            pATR = True
        if vowel in nATR_list:
            nATR = True
    
    if pATR and nATR:
        return "Nonharmonizing"
    if pATR:
        return "+"
    if nATR:
        return "-"
    return "error"

df = pd.read_excel("DagaareDict.xlsx")

df["PH"] = df["PH"].astype(str)

df["Vowels"] = df["PH"].apply(vowelize)

df["ATR"] = df["Vowels"].apply(ATR_val)

df.to_excel("DagaareDict.xlsx", index = False)
