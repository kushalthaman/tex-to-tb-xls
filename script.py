## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re 
from openpyxl import Workbook
import pandas as pd

columns = ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "SE", "VA"]

def process_tex_to_excel(tex_filepath, xlsx_filepath):
    with open(tex_filepath, 'r', encoding='utf-8') as file:
        data = file.read().replace('\n', ' ')

    pattern = re.compile(r'\\tbLX\{(.+?)\}')
    LX_list = re.findall(pattern, data)

    dictionary = {}
    for LX in LX_list:
        dictionary[LX] = {}

    categories = ['LX', 'HM', 'PH', 'PS', 'GE', 'OP', 'TP', 'PD', 'SE', 'VA', 'XV', 'XE', 'ex']
    for category in categories:
        pattern = re.compile(r'\\tb' + category + '\{(.+?)\}')
        category_list = re.findall(pattern, data)
        
        for item in category_list:
            LX, value = item.split('}', 1)
            dictionary[LX][category] = value.strip('{} ')

    df = pd.DataFrame(dictionary).T
    df.to_excel(xlsx_filepath)

process_tex_to_excel('d.tex', 'd.xlsx')
