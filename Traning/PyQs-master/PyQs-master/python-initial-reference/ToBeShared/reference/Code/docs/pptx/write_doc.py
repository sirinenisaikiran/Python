from pptx import Presentation
import pptx 

prs = Presentation()

print("""
Presentation attributes 
""")
print([a for a in dir(prs) if a.startswith("_") == False])


print("""
Slide Layout attributes 
""")
print([a for a in dir(pptx.slide.SlideLayout) if a.startswith("_") == False])


print("No of layouts in ppt:", len(prs.slide_layouts))
print({ i: s.name for i,s in enumerate(prs.slide_layouts)})
#{0: 'Title Slide', 1: 'Title and Content', 2: 'Section Header', 
#3: 'Two Content', 4: 'Comparison', 5: 'Title Only', 6: 'Blank', 
#7: 'Content with Caption', 8: 'Picture with Caption', 
#9: 'Title and Vertical Text', 10: 'Vertical Title and Text'}




print("Add title and some text using ", prs.slide_layouts[0].name)

title_slide_layout = prs.slide_layouts[0]
slide = prs.slides.add_slide(title_slide_layout)

print("""
slide.shapes attributes 
""")
print([a for a in dir(slide.shapes) if a.startswith("_") == False])
print("No of Shapes in this slide :", len(slide.shapes))

print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})

print("""
slide.placeholder attributes 
""")
print([a for a in dir(slide.placeholders[1]) if a.startswith("_") == False])


title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Hello, World!"
subtitle.text = "first automated pptx!"

#Adding a bullet slide 
bullet_slide_layout = prs.slide_layouts[1]

slide = prs.slides.add_slide(bullet_slide_layout)
title = slide.shapes.title

body = slide.shapes.placeholders[1]

title.text = 'Adding a Bullet Slide'

tf = body.text_frame
tf.text = 'Find the bullet slide layout'

p = tf.add_paragraph()
p.text = 'Use text_frame.text for above bullet'
p.level = 1

p = tf.add_paragraph()
p.text = 'Use text_frame.add_paragraph() for subsequent bullets'
p.level = 2

print()
print("Adding a bullet slide ", prs.slide_layouts[1].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})


#add textbox

from pptx.util import Inches, Pt

blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)



left = top = width = height = Inches(1)
body = slide.shapes.add_textbox(left, top, width, height)
tf = body.text_frame

tf.text = "This is text inside a textbox"

p = tf.add_paragraph()
p.text = "This is a second paragraph that's bold"
p.font.bold = True

p = tf.add_paragraph()
p.text = "This is a third paragraph that's big"
p.font.size = Pt(40)

print()
print("Adding a Picture slide ", prs.slide_layouts[6].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})


#add_picture() example

img_path = '../data/monty-truth.png'

blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

left = top = Inches(1)
pic = slide.shapes.add_picture(img_path, left, top)

left = Inches(5)
height = Inches(5.5)
pic = slide.shapes.add_picture(img_path, left, top, height=height)

print()
print("Adding a Picture slide ", prs.slide_layouts[6].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})


#add_shape() example
#Constants representing each of the available auto shapes (like MSO_SHAPE.ROUNDED_RECT, MSO_SHAPE.CHEVRON, etc.) are listed on the autoshape-types page.
from pptx.enum.shapes import MSO_SHAPE

title_only_slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(title_only_slide_layout)

slide.shapes.title.text = 'Adding an AutoShape'

left = Inches(0.93)  # 0.93" centers this overall set of shapes
top = Inches(3.0)
width = Inches(1.75)
height = Inches(1.0)

body = slide.shapes.add_shape(MSO_SHAPE.PENTAGON, left, top, width, height)
body.text = 'Step 1'

left = left + width - Inches(0.4)
width = Inches(2.0)  # chevrons need more width for visual balance

for n in range(2, 6):
    body = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, left, top, width, height)
    body.text = 'Step %d' % n
    left = left + width - Inches(0.4)

print()
print("Adding an Auto Shape using", prs.slide_layouts[5].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})
   
    
#add_table() example

title_only_slide_layout = prs.slide_layouts[5]
slide = prs.slides.add_slide(title_only_slide_layout)

slide.shapes.title.text = 'Adding a Table'

rows = cols = 2
left = top = Inches(2.0)
width = Inches(6.0)
height = Inches(0.8)

table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# set column widths
table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(4.0)

# write column headings
table.cell(0, 0).text = 'Foo'
table.cell(0, 1).text = 'Bar'

#make it bold and Center
from pptx.enum.text import PP_ALIGN
for i in range(2):
    run = table.cell(0, i).text_frame.paragraphs[0].runs[0]
    run.bold = True
    run.underline = True
    table.cell(0, i).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER


# write body cells
table.cell(1, 0).text = 'Baz'
table.cell(1, 1).text = 'Qux'
print()
print("Adding table using ", prs.slide_layouts[5].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})
print("""
table attributes 
""")
print([a for a in dir(table) if a.startswith("_") == False])


#Add a chart 
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt

slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = 'Adding a chart'

chart_data = ChartData()
chart_data.categories = ['East', 'West', 'Midwest']
chart_data.add_series('Q1 Sales', (19.2, 21.4, 16.7))
chart_data.add_series('Q2 Sales', (22.3, 28.6, 15.2))
chart_data.add_series('Q3 Sales', (20.4, 26.3, 14.2))

x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
chart = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
).chart

from pptx.enum.chart import XL_TICK_MARK

category_axis = chart.category_axis
category_axis.has_major_gridlines = True
category_axis.minor_tick_mark = XL_TICK_MARK.OUTSIDE
category_axis.tick_labels.font.italic = True
category_axis.tick_labels.font.size = Pt(24)

value_axis = chart.value_axis
value_axis.maximum_scale = 50.0
value_axis.minor_tick_mark = XL_TICK_MARK.OUTSIDE
value_axis.has_minor_gridlines = True

tick_labels = value_axis.tick_labels
tick_labels.number_format = '0"%"'
tick_labels.font.bold = True
tick_labels.font.size = Pt(14)
print()
print("Adding chart using ", prs.slide_layouts[5].name)
print("containg no of shapes ", len(slide.shapes))
print("containg placeholders ", { i: s.name for i,s in enumerate(slide.placeholders)})
print("""
chart attributes 
""")
print([a for a in dir(chart) if a.startswith("_") == False])
print("""
Other chart types 
""")
print([a for a in dir(XL_CHART_TYPE) if a.startswith("_") == False])


prs.save('test.pptx')

