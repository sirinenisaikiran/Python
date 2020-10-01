print("""
Presentation Consists of slides , each slide might created 
from layout(created in master slide)
layout is composed of many preformatted placeholders(kind of shape)
OR a slide can be created from many Shapes 
Each slide has a shape tree(.shapes) that holds its shapes(created directly or via layout)


Presentation has list of slides, each slide has list of shapes 
Each shape might have text_frame, text_frame has list of paragraphs
Each paragraph has list of runs, each run has .text 
""")

from pptx import Presentation

prs = Presentation('../data/example.pptx')

# text_runs will be populated with a list of strings,
# one for each text run in presentation
text_runs = []

for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                text_runs.append(run.text)
                
print(text_runs)