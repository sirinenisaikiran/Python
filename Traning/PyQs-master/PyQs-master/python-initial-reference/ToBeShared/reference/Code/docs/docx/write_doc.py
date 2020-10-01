from docx import Document
from docx.shared import Inches

document = Document()

document.add_heading('Document Title', 0)

p = document.add_paragraph('A plain paragraph having some ')
p.add_run('bold').bold = True
p.add_run(' and some ')
p.add_run('italic.').italic = True
p.add_run('text with emphasis.').style = 'Emphasis' #Applying a character style

document.add_heading('Heading, level 1', level=1)
document.add_paragraph('Intense quote', style='Intense Quote')

document.add_paragraph(
    'first item in unordered list', style='List Bullet'
)
document.add_paragraph(
    'first item in ordered list', style='List Number'
)

document.add_picture('../data/monty-truth.png', width=Inches(1.25))

document.add_page_break()

records = (
    (3, '101', 'Spam'),
    (7, '422', 'Eggs'),
    (4, '631', 'Spam, spam, eggs, and spam')
)

table = document.add_table(rows=1, cols=3)

print("Table attributes ")
print([a for a in dir(table) if a.startswith("_") == False])

#dir(table)
#['add_column', 'add_row', 'alignment', 'autofit','cell', 'column_cells', 
#'columns', 'part', 'row_cells', 'rows', 'style', 'table', 'table_direction']

table.style = 'Table Grid'
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Qty'
hdr_cells[1].text = 'Id'
hdr_cells[2].text = 'Desc'

from docx.enum.text import WD_ALIGN_PARAGRAPH
#make it bold and Center
for i in range(3):
    run = hdr_cells[i].paragraphs[0].runs[0]
    run.bold = True
    run.underline = True
    hdr_cells[i].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


for qty, id, desc in records:
    row_cells = table.add_row().cells
    row_cells[0].text = str(qty)
    row_cells[1].text = id
    row_cells[2].text = desc



document.save('demo.docx')