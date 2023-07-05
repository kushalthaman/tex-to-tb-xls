## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re
import pandas as pd

columns =  ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "SE", "VA"]

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
    'VA': r'\\tbVA\{(.*?)\}',
    'SE': r'\\tbSN \\tbGE\{(.*?)\}',
}

rows_list = [] # list to hold all rows 
row_dict = {} # for the current row 
with open('d.tex', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('%') or line == '':
            continue  # we want to skip over lines that start with %, as well as lines that are empty (that start with '') 
        
        for tag, pattern in patterns.items():
            match = re.search(pattern, line)
            if match:
                if tag == 'LX' and row_dict:
                    rows_list.append(row_dict)
                    row_dict = {}
                row_dict[tag] = match.group(1)

if row_dict:
    rows_list.append(row_dict)
    
df = pd.DataFrame(rows_list, columns=columns)
df.to_excel('d.xlsx', index=False)
