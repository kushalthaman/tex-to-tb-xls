## This is a script to import .tex files formatted using the tb-to-tex library (https://github.com/rebeccaeverson/tb-to-tex/) into an .xlsx file. 

import re 
from openpyxl import Workbook

columns = ["LX","HM", "PH", "PS", "GE", "XV", "XE", "SG", "OP", "TP", "SE", "VA"]

workbook = Workbook()
script = workbook.active
script.append(columns) 

with open("d.tex", r) as file:
	text = file.read()
	entries = text.split("\n")
	for entry in entries:
		if entry.startswith("\\tbLX"):
			if row in locals():
				script.append(row)
		row = [""]*len(columns)
		for ctg, col in enumerate(columns):
			entered_text = "\\tb" + col + ""
			doesMatch = re.search(entered_text, entry)
			if doesMatch is not None: 
				row[ctg] = match.group(1)



if row in locals():
	script.append(row)  

workbook.save("output.xlsx")
