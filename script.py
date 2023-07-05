## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re
import pandas as pd

data = []
with open('d.tex', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith('%') or line == '':
            continue
        lx = re.search(r'\\tbLX\{(.*?)\}', line)
        hm = re.search(r'\\tbHM\{(.*?)\}', line)
        ph = re.search(r'\\tbPH\{(.*?)\}', line)
        ps = re.search(r'\\tbPS\{(.*?)\}', line)
        ge = re.search(r'\\tbGE\{(.*?)\}', line)
        op = re.search(r'\\tbOP\{(.*?)\}', line)
        tp = re.search(r'\\tbTP\{(.*?)\}', line)
        pd = re.search(r'\\tbPD\{(.*?)\}', line)
        va = re.search(r'\\tbVA\{(.*?)\}', line)
        sn = re.search(r'\\tbSN \\\tbGE\{(.*?)\}', line)

        lx = lx.group(1) if lx is not None else ''
        hm = hm.group(1) if hm is not None else ''
        ph = ph.group(1) if ph is not None else ''
        ps = ps.group(1) if ps is not None else ''
        ge = ge.group(1) if ge is not None else ''
        op = op.group(1) if op is not None else ''
        tp = tp.group(1) if tp is not None else ''
        pd = pd.group(1) if pd is not None else ''
        va = va.group(1) if va is not None else ''
        sn = sn.group(1) if sn is not None else ''
        
        data.append([lx, hm, ph, ps, ge, op, tp, pd, va, sn])

df = pd.DataFrame(data, columns=['LX', 'HM', 'PH', 'PS', 'GE', 'OP', 'TP', 'PD', 'VA', 'SN'])
df.to_excel('d.xlsx', index=False)
