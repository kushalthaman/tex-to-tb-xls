## Obolo Bible -> Text File with all words period-separated and stripped of tone marks

import re
import pandas as pd

rows_list = []  # list to hold all rows 
chars_list = []  # holds all unique characters from PH

text = ""
with open("whole_bible.txt", "r") as file:
    text = file.read()

# text_file = open("whole_bible.txt", "w")
# n = text_file.write(text)
# text_file.close()

# char_list = {}
# for char in text:
#     if char not in char_list:
#         char_list[char] = hex(ord(char))

# print(char_list)

dividers = " 1\n,.2:3“!”4567890-?();‘’–[]"
capitals = "IBEMAUÒOCSÌNÀÎPGKTYǸLJRDFỌWÈÙÔH"
consonants = "fknrmbwjsyltgpdchǹ" + "BMCSNPGKTYǸLJRDFWH"
vowels = "uoeiaîọèìùòàôâêû" + "IEAUÒOÌÀÎỌÈÙÔ"
v_nasal = '̄'

for char in dividers:
    text = text.replace(char, ".")

# could do with a dictionary but doesnt matter for this scale
def accent_strip(c):
    if c == "Ò" or c == "Ô":
        return "O"
    elif c == "Ì" or c == "Î":
        return "I"
    elif c == "À":
        return "A"
    elif c == "Ǹ":
        return "N"
    elif c == "È":
        return "E"
    elif c == "Ù":
        return "U"
    elif c == "ǹ":
        return "n"
    elif c == "î" or c == "ì":
        return "i"
    elif c == "è" or c == "ê":
        return "e"
    elif c == "ù" or c == "û":
        return "u"
    elif c == "ò" or c == "ô":
        return "o"
    elif c == "à" or c == "â":
        return "a"
    
    else:
        return c

result = ["."]
for char in text:
    if char in dividers and result[-1] != ".":
        result.append(".")
    elif char in consonants + vowels:
        result.append(accent_strip(char))
    elif char == v_nasal:
        result.append(char)

if result[-1] == ".":
    result.pop()
result.pop(0)

result = ''.join(result)

text_file = open("neat_bible.txt", "w")
n = text_file.write(result)
text_file.close()

words = {}
for word in result.split("."):
    if word == "":
        continue
    neut = word.lower()
    if neut in words and words[neut] > 0:
        words[neut] += 1
    elif neut in words and words[neut] < 0:
        words[neut] -= 1
        if word[0] not in capitals:
            words[neut] = words[neut]*-1 # type frequency is negative for words which only appear with uppercase initial characters (likely proper nouns)
    else:
        words[neut] = 1 if word[0].islower() else -1

data = list(words.items())
word_table = pd.DataFrame(data, columns=["Segmental Token", "Token Frequency"])
word_table.sort_values(by = 'Token Frequency', ascending = False, inplace = True, kind = 'quicksort')
word_table.to_excel("WordTable.xlsx", index=False)
