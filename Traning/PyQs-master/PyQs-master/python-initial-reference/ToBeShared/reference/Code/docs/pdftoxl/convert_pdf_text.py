from PyPDF2 import PdfFileReader
import sys 

DEBUG = True
def print_d(*args, **kwargs):
    if DEBUG :
        print(*args, **kwargs)
    return None


discard_text = [
'Round ',
'No',
'Institute',
'Academic Program Name',
'Quota',
'Category',
'Seat Pool',
'Opening ',
'Rank',
'Closing Rank',
'Joint Seat Allocation 2019',
"If the Closing/Opening rank has a suffix 'P', it indicates that the corresponding rank is from Preparatory Rank List. ", 
]

header = [
'Round No',
'Institute',
'Academic Program Name',
'Quota',
'Category',
'Seat Pool',
'Opening Rank',
'Closing Rank',
]
consume_lines = 8

def discard(text):
    for e in discard_text:
        if  e == text : 
            return True
    return False
    

def process(lst):
    print("Now processing...")
    out_llist = []
    input = "".join(lst)
    in_s = [ line for line in input.split("\n") if not discard(line)]
    start = 0 
    end = consume_lines
    i = 0
    while len(in_s[start:end]) > 0:    
        token = in_s[start:end]
        out_llist.append(token)
        print_d("token(",i+1,")",token)
        start = end
        end += consume_lines
        i +=1
    return out_llist
    

path1 = "closing and opening rank_page_1.pdf"
dest_filename = "closing and opening rank.xlsx"

all_text = []
with open(path1, 'rb') as f:
    pdf = PdfFileReader(f)
    n = pdf.getNumPages()
    print("No pages:", n )
    for i in range(n):
        print(".", end="")
        sys.stdout.flush()
        page = pdf.getPage(i)    
        text = page.extractText()
        all_text.append(text)

print()
#print(all_text)
llist = process(all_text)    

print("writing excel file")
 
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

wb = Workbook()

ws1 = wb.active
ws1.title = "ranks"

ws1.append(header)
for row in llist:
    ws1.append(row)

wb.save(filename = dest_filename)
