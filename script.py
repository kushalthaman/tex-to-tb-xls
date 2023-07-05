## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re
import pandas as pd

columns =  ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "SE", "VA"]

data = []
with open('d.tex', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if not line.startswith('\tbLX'):
            continue             # we want to skip over lines that start with %, as well as lines that are empty (that start with '') 
        lx = re.search(r'\\tbLX\{(.*?)\}', line)
        hm = re.search(r'\\tbHM\{(.*?)\}', line)
        ph = re.search(r'\\tbPH\{(.*?)\}', line)
        ps = re.search(r'\\tbPS\{(.*?)\}', line)
        ge = re.search(r'\\tbGE\{(.*?)\}', line)
        xv = re.search(r'\\tbXV\{(.*?)\}', line)
        xe = re.search(r'\\tbXE\{(.*?)\}', line)
        sg = re.search(r'\\tbSG\{(.*?)\}', line)
        op = re.search(r'\\tbOP\{(.*?)\}', line)
        tp = re.search(r'\\tbTP\{(.*?)\}', line)
        va = re.search(r'\\tbVA\{(.*?)\}', line)
        se = re.search(r'\\tbSN \\\tbGE\{(.*?)\}', line)

        lx = lx.group(1) if lx is not None else ''
        hm = hm.group(1) if hm is not None else ''
        ph = ph.group(1) if ph is not None else ''
        ps = ps.group(1) if ps is not None else ''
        ge = ge.group(1) if ge is not None else ''
        xv = xv.group(1) if xv is not None else ''
        xe = xe.group(1) if xe is not None else ''
        sg = sg.group(1) if sg is not None else ''
        op = op.group(1) if op is not None else ''
        tp = tp.group(1) if tp is not None else ''
        va = va.group(1) if va is not None else ''
        se = se.group(1) if se is not None else ''
                
        data.append([lx, hm, ph, ps, ge, xv, xe, sg, op, tp, va, se])

df = pd.DataFrame(data, columns=['LX', 'HM', 'PH', 'PS', 'GE', 'SV', 'XE', 'SG', 'OP', 'TP', 'VA', 'SE'])
df.to_excel('d.xlsx', index=False)
