## This is a script to convert .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re
import pandas as pd

patterns = {
    'LX': r"\\tbLX\{(.*?)\}",
    'PH': r"\\tbPH\{(.*?)\}",
    'PS': r"\\tbPS\{(.*?)\}",
    'GE': r"\\tbGE\{(.*?)\}",
    'SG': r"\\tbSG\{(.*?)\}",
    'OP': r"\\tbOP\{(.*?)\}",
    'TP': r"\\tbTP\{(.*?)\}",
    'PD': r"\\tbPD\{(.*?)\}",
    'VA': r"\\tbVA\{(.*?)\}",
}

rows_list = []  # list to hold all rows 
chars_list = []  # holds all unique characters from PH
with open("DictText.tex", "r") as file:
    text = file.read()
    comment_pattern = r"%.*\n"
    text = re.sub(comment_pattern, " ", text)  # removes all commented-out text
    begin_pattern = r"\\begin.*\n"
    text = re.sub(begin_pattern, "", text)  # removes \begin lines
    end_pattern = r"\\end.*\n"
    text = re.sub(end_pattern, "", text)  # removes \end lines
    text = re.sub(r"\n", " ", text)

    entries = text.split("\\tbLX")
    entries.pop(0)  # removes empty entry

    for entry in entries:
        row_dict = {}
        entry = "\\tbLX" + entry
        for tag, pattern in patterns.items():
            match = re.search(pattern, entry)
            if match:
                row_dict[tag] = match.group(1)
                if tag == "PH":  #
                    for char in match.group(1):  #
                        if char not in chars_list:  #
                            chars_list.append(char)  #
                    
            else:
                row_dict[tag] = ""  # forces preservation of the column order defined in patterns
        row_dict["Tail"] = entry
        rows_list.append(row_dict)

print(chars_list)

df = pd.DataFrame(rows_list)
df.to_excel("DagaareDict.xlsx", index = False)
