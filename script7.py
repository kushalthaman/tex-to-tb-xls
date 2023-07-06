## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re
import pandas as pd

columns =  ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "PD", "VA", "SE"]

patterns = {
    'LX': r'\\tbLX\{(.*?)\}',
    'HM': r'\\tbHM\{(.*?)\}',
    'PH': r'\\tbPH\{(.*?)\}',
    'PS': r'\\tbPS\{(.*?)\}',
    'GE': r'\\tbGE\{(.*?)\}',
    'XV': r'\\tbXV\{(.*?)\}',
    'XE': r'\\tbXE\{(.*?)\}',
    'SG': r'\\tbSG\{(.*?)\}',
    'OP': r'\\tbOP\{(.*?)\}',
    'TP': r'\\tbTP\{(.*?)\}',
    'PD': r'\\tbPD\{(.*?)\}',
    'VA': r'\\tbVA\{(.*?)\}',
    'SE': r'\\tbSN \\tbGE\{(.*?)\}',
}

sense = None
rows_list = [] # list to hold all rows 
row_dict = {} # for the current row 
with open('b.tex', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('%') or line == '':
            continue  # we want to skip over lines that start with %, as well as lines that are empty (that start with ''). Alternatively we can say if not line.startswith('\tbLX'). 
        for tag, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                if tag == 'LX' and row_dict:
                    if sense:
                        row_dict.update(sense)
                        sense = None
                    rows_list.append(row_dict)
                    row_dict = {tag: match.group(1)}
                else:
                    row_dict[tag] = match.group(1)

        if '\\tbSN' in line:
            if sense:
                row_dict.update(sense)
                rows_list.append(row_dict)
            sense = {'GE': '', 'XV': '', 'XE': ''}

        for tag in ['GE', 'XV', 'XE']:
            match = re.search(fr'\\tb{tag}\{{(.*?)\}}', line)
            if match and sense is not None:
                sense[tag] = match.group(1)

if row_dict:
    if sense:
        row_dict.update(sense)
    rows_list.append(row_dict)

df = pd.DataFrame(rows_list)
df.to_excel('b.xlsx', index=False)
