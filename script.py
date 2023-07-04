## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re 
from openpyxl import Workbook
import pandas as pd

columns = ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "SE", "VA"]

def process_tex_to_excel(tex_filepath, xlsx_filepath):
    with open(tex_filepath, 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', ' ')

    dictionary = {}

    pattern = re.compile(r'\\tb([a-zA-Z]+)\{(.+?)\}')
    matches = re.findall(pattern, data)

    for match in matches:
        category, value = match
        if category == "LX":
            current_lexeme = value
            dictionary[current_lexeme] = {}
        elif current_lexeme:
            dictionary[current_lexeme][category] = value
            
    df = pd.DataFrame(dictionary).T
    df.to_excel(xlsx_filepath)

process_tex_to_excel('d.tex', 'd.xlsx')
