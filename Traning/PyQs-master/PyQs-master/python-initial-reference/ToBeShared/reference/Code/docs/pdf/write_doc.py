##ReportLab - hello_reportlab.py

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4, landscape, letter 
from reportlab.lib.units import inch,cm,mm #72.0 ,28.34, 2.83
from reportlab.lib import colors

c = canvas.Canvas("01.hello.pdf")
c.drawString(100, 100, "(100,100) Welcome to Reportlab!")
c.drawString(100, 200, "(100,200) Welcome to Reportlab!")
c.drawString(100, 400, "(100,400) Welcome to Reportlab!")
c.drawString(400, 400, "(400,400) Welcome to Reportlab!")
#c.showPage() #closes this page and display 

def writeMultiline(my_canvas, text, prefix=None):
    #next page 
    my_canvas.showPage()
    # Create textobject
    textobject = my_canvas.beginText()
    # Set text location (x, y)
    textobject.setTextOrigin(10, 730)
    # Set font face and size
    textobject.setFont('Times-Roman', 12)
    # Change text color
    if prefix:
        textobject.setFillColor(colors.red)
        # Write a line of text + carriage return
        textobject.textLine(text=prefix)
    #or for multiline 
    #dont trim leading whitepages 
    #textLines(self, stuff, trim=1)
    textobject.setFillColor(colors.black)
    textobject.textLines(text, trim=0)
    # Write text to the canvas
    my_canvas.drawText(textobject)

#Now page 2 onwards , show styles and page configuration 
PAGE_HEIGHT=defaultPageSize[1] #841.8897637795277
PAGE_WIDTH=defaultPageSize[0]  #595.2755905511812
styles = getSampleStyleSheet()
text = "Default PAGE_HEIGHT=%f,PAGE_WIDTH=%f, inch=%f,cm=%f,mm=%f" % (PAGE_HEIGHT,PAGE_WIDTH, inch,cm,mm)
writeMultiline(c,  text)
text = "A4=%s,landscape(letter)=%s, letter=%s" % (A4,landscape(letter), letter)
writeMultiline(c,  text)

text = ""

def getAllVars(obj):
    global text 
    sd = dir(obj)
    for v in sorted(sd):
        if not callable(getattr(obj, v)) and not v.startswith("_") and v != 'defaults':
            text += " ".join( ["\n", "    ", str(v), ":", str(getattr(obj, v))])

#styles.list() prints to stdout , so writes own function 
def list2(sls):
    global text 
    ss = list(sls.byName.items())
    ss.sort()
    alii = {}
    for (alias, style) in list(sls.byAlias.items()):
        alii[style] = alias
    for (name, style) in ss:
        alias = alii.get(style, None)
        text +=  " ".join([str(name), "alias=", str(alias)])
        getAllVars(style)
        text += "\n##\n"


list2(styles)
strings = text.split("##")
writeMultiline(c,  strings[0], "List of styles")  
for text in strings[1:]:
    writeMultiline(c,  text) #one styles in one page , else we need to calulate string height 

#Next page 
def rotate_demo(my_canvas):
    my_canvas.showPage()
    my_canvas.translate(inch, inch)
    my_canvas.setFont('Helvetica', 14)
    my_canvas.drawString(inch, inch, 'Normal')
    my_canvas.line(inch, inch, inch+100, inch)

    my_canvas.rotate(45)
    my_canvas.drawString(inch, -inch, '45 degrees')
    my_canvas.line(inch, inch, inch+100, inch)

    my_canvas.rotate(45)
    my_canvas.drawString(inch, -inch, '90 degrees')
    my_canvas.line(inch, inch, inch+100, inch)

rotate_demo(c)


##String Alignment 

def string_alignment(my_canvas):
    my_canvas.showPage()
    width, height = letter
    
    my_canvas.drawString(80, 700, 'Standard String')
    my_canvas.drawRightString(80, 680, 'Right String')
    
    numbers = [987.15, 42, -1,234.56, (456.78)]
    y = 650
    for number in numbers:
        my_canvas.drawAlignedString(60, y, str(number))
        y -= 20
    
    my_canvas.drawCentredString(width / 2, 550, 'Centered String')
    



string_alignment(c)

    
##Drawing 

def draw_shapes(my_canvas):
    my_canvas.showPage()    
    my_canvas.setStrokeColorRGB(0.2, 0.5, 0.3)
    #rect(self, x, y, width, height, stroke=1, fill=0)
    my_canvas.rect(10, 740, 100, 80, stroke=1, fill=0)
    #ellipse(self, x1, y1, x2, y2, stroke=1, fill=0)
    my_canvas.ellipse(10, 680, 100, 630, stroke=1, fill=1)
    #wedge(self, x1,y1, x2,y2, startAng, extent, stroke=1, fill=0)
    my_canvas.wedge(10, 600, 100, 550, 45, 90, stroke=1, fill=0)
    #circle(self, x_cen, y_cen, r, stroke=1, fill=0)
    my_canvas.circle(300, 600, 50)

    my_canvas.setLineWidth(.3)
    my_canvas.line(30, 500, 580, 500)
    
    my_canvas.setFont('Helvetica', 10)
    x = 30
    grays = [0.0, 0.25, 0.50, 0.75, 1.0]
    for gray in grays:
        my_canvas.setFillGray(gray)
        my_canvas.circle(x, 400, 20, fill=1)
        gray_str = "Gray={gray}".format(gray=gray)
        my_canvas.setFillGray(0.0)
        my_canvas.drawString(x-10, 300, gray_str)
        x += 75

draw_shapes(c)

        
##Image 
def add_image(my_canvas, image_path):
    my_canvas.showPage()
    my_canvas.drawImage(image_path, 30, 600, width=100, height=100)


image_path = '../data/python_logo.png'
add_image(c,image_path)
    
#Now save 
c.save()


##ReportLab - font_demo.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def font_demo(my_canvas, fonts):
    pos_y = 750
    for font in fonts:
        my_canvas.setFont(font, 12)
        my_canvas.drawString(30, pos_y, font)
        pos_y -= 10

if __name__ == '__main__':
    my_canvas = canvas.Canvas("02.font_demo.pdf",
                              pagesize=letter)
    fonts = my_canvas.getAvailableFonts()
    font_demo(my_canvas, fonts)
    my_canvas.save()



        
        
print("""
The ReportLab engineers describe PLATYPUS as having several layers(from highest to lowest level):
DocTemplates 
    the outermost container of your page
PageTemplates 
    specifies the layout of your page
Frames 
    kind of like a sizer in a desktop user interface.
    Basically it provides a region that contains other flowables
Flowables 
    A text or graphic element that can be 'flowed'
    across page boundaries, such as a paragraph of text. This does
    not include footers and headers.
pdfgen.Canvas 
    The lowest level of ReportLab, It will actually receive its instructions
    from one or more of the upper layers and 'paint' your documentaccordingly.
""")

##ReportLab -  hello_platypus.py
'''When you create an instance of SimpleDocTemplate, it will
contain one or more other PageTemplates that are a description of the
layout of each of the pages of your document

BaseDocTemplate(self, filename,
    pagesize=defaultPageSize,
    pageTemplates=[],
    showBoundary=0,
    leftMargin=inch,
    rightMargin=inch,
    topMargin=inch,
    bottomMargin=inch,
    allowSplitting=1,
    title=None,
    author=None,
    _pageBreakQuick=1,
    encrypt=None)

The filename parameter is the only one required ,pass a string in for this parameter that can be the
PDF’s file name or object that implements a write method, such as StringIO, BytesIO, file or
socket type.

showBoundary parameter that you can use to turn on the boundaries of
the frames in your document

The allowSplitting parameter tells ReportLab that it should try to split
each Flowable across the Frames.

encrypt parameter that defaults to None, that is unencrypted. 
If you pass in a string object, that will be the user’s password to the document. 
Alternatively, you can pass an instance of reportlab.lib.pdfencrypt.StandardEncryption to encrypt
your PDF, which will give you more control over the encryption settings.

'''

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def hello():
    doc = SimpleDocTemplate("03.hello_platypus.pdf",
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    styles = getSampleStyleSheet()

    flowables = []

    text = "Hello, I'm a Paragraph"
    para = Paragraph(text, style=styles["Normal"])
    flowables.append(para)

    doc.build(flowables)

if __name__ == '__main__':
    hello()  
        

##ReportLab -  flowable_orientation.py
'''
set the pagesize parameter to equal landscape(letter). 
The landscape function just takes a page size and sets it to landscape

'''

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.platypus import Frame, PageTemplate, NextPageTemplate, Spacer
'''
The PageBreak class inserts a page break in your document,
the NextPageTemplate tells ReportLab what template to use starting on
the next page while the Spacer class will add space between the flowables
'''

def alternate_orientations():
    doc = SimpleDocTemplate("04.orientations.pdf",
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    margin = 0.5 * inch
    frame = Frame(margin, margin, doc.width, doc.height, id='frame')
    '''
    PageTemplate(id=None,frames=[],onPage=_doNothing, onPageEnd=_doNothing,
                 pagesize=None, autoNextPageTemplate=None,
                 cropBox=None,
                 artBox=None,
                 trimBox=None,
                 bleedBox=None,
                 )
    '''
    portrait_template = PageTemplate(id='portrait',
                                     frames=[frame],
                                     pagesize=letter)
    landscape_template = PageTemplate(id='landscape',
                                      frames=[frame],
                                      pagesize=landscape(letter))
    doc.addPageTemplates([portrait_template, landscape_template])

    story = []
    story.append(Paragraph('This is a page in portrait orientation', normal))

    # Change to landscape orientation
    story.append(NextPageTemplate('landscape'))  #name is from PageTemplate
    story.append(PageBreak())
    story.append(Spacer(inch, 2*inch))
    story.append(Paragraph('This is a page in landscape orientation', normal))

    # Change back to portrait
    story.append(NextPageTemplate('portrait'))
    story.append(PageBreak())
    story.append(Paragraph("Now we're back in portrait mode again", normal))

    doc.build(story)

if __name__ == '__main__':
    alternate_orientations()
    
    
        
##ReportLab - paragraph_inline_images.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def paragraph_inline_images():
    doc = SimpleDocTemplate("06.paragraph_inline_images.pdf",
                            pagesize=letter
                            )
    styles = getSampleStyleSheet()

    flowables = []

    ptext = '''Here is a picture:
    <img src="../data/python_logo.png" width="50" height="50"/> in the
    middle of our text'''
    p = Paragraph(ptext, styles['Normal'])
    flowables.append(p)

    doc.build(flowables)

if __name__ == '__main__':
    paragraph_inline_images()

        
##ReportLab -     paragraph_bullets.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def paragraph_bullets():
    doc = SimpleDocTemplate("07.paragraph_bullets.pdf",
                            pagesize=letter
                            )
    styles = getSampleStyleSheet()

    flowables = []

    ptext = "I'm a custom bulletted paragraph"
    para = Paragraph(ptext, style=styles["Normal"], bulletText='-')
    flowables.append(para)

    ptext = "This is a normal bullet"
    para = Paragraph(ptext, style=styles["Normal"], bulletText='•')
    flowables.append(para)

    ptext = "<bullet>&bull;</bullet>This text uses the bullet tag"
    para = Paragraph(ptext, style=styles["Normal"])
    flowables.append(para)

    doc.build(flowables)

if __name__ == '__main__':
    paragraph_bullets()   
        
##ReportLab - paragraph_fonts.py

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def paragraph_fonts():
    doc = SimpleDocTemplate("08.paragraph_fonts.pdf",
                            pagesize=letter
                            )
    styles = getSampleStyleSheet()

    flowables = []

    ptext = "<font name=helvetica size=12>Welcome to Reportlab! " \
            "(helvetica)</font>"
    para = Paragraph(ptext, style=styles["Normal"])
    flowables.append(para)

    ptext = "<font face=courier size=14>Welcome to Reportlab! " \
            "(courier)</font>"
    para = Paragraph(ptext, style=styles["Normal"])
    flowables.append(para)

    ptext = "<font name=times-roman size=16>Welcome to Reportlab! " \
            "(times-roman)</font>"
    para = Paragraph(ptext, style=styles["Normal"])
    flowables.append(para)

    doc.build(flowables)

if __name__ == '__main__':
    paragraph_fonts()

        

##ReportLab - absolute_pos_flowable.py
'''
a class named Flowable that is a Python abstract class which has the following methods:
    draw
    wrap
    split (optionally)
Instead the calling draw, user should call drawOn(self, canvas, x, y) which will call draw internally.
The wrapOn(self, canv, aW, aH) calculates how to wrap the text in your paragraph based on that information.
'''

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def mixed():
    my_canvas = canvas.Canvas("09.mixed_flowables.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    width, height = letter
    print("width, height for letter", width, height)
    text = "Hello, I'm a Paragraph" * 100
    para = Paragraph(text, style=styles["Normal"])
    para.wrapOn(my_canvas, width, height)
    para.drawOn(my_canvas, 20, 760) #x,y for drawing 

    my_canvas.save()

if __name__ == '__main__':
    mixed()
    
##ReportLab - two_column_demo.py

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Frame


def frame_demo():
    my_canvas = Canvas("10.frame_demo.pdf",
                       pagesize=letter)

    styles = getSampleStyleSheet()
    normal = styles['Normal']
    heading = styles['Heading1']

    flowables = []
    flowables.append(Paragraph('Heading #1', heading))
    flowables.append(Paragraph('Paragraph #1', normal))

    right_flowables = []
    right_flowables.append(Paragraph('Heading #2', heading))
    right_flowables.append(Paragraph('ipsum lorem', normal))
    #A Frame is a container that is itself contained within a PageTemplate
    #Frame(x1, y1, width, height, leftPadding=6, bottomPadding=6,
    #        rightPadding=6, topPadding=6, id=None, showBoundary=0)
    left_frame = Frame(inch, inch, width=3*inch, height=9*inch, showBoundary=1)
    right_frame = Frame(4*inch, inch, width=3*inch, height=9*inch)

    left_frame.addFromList(flowables, my_canvas)
    right_frame.addFromList(right_flowables, my_canvas)

    my_canvas.save()

if __name__ == '__main__':
    frame_demo()            
        
        
        
##ReportLab -   table_with_images.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, Image

def table_with_images():
    doc = SimpleDocTemplate("11.table_with_images.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    img = Image("../data/python_logo.png", 50, 50)

    ptext = 'This is some <font color=blue size=14>formatted</font> text'
    p = Paragraph(ptext, styles['Normal'])

    data = [['col_{}'.format(x) for x in range(1, 6)],
            [p for x in range(1, 6)],
            [img, img, img, img, img]
            ]

    #TableStyle(cmds=None, parent=None, **kw)
    #The cmds argument is just a list of tuples that define what cell formatting you want to apply.
    #The first element in the tuple is the cell formatting command
    #Thesecond and third elements define the cell coordinates that the formatting
    #will apply to. The coordinates are (column, row),
    #The -1 in the second set of coordinates tells ReportLab that we want the formatting
    #to extend across all the columns from left-to-right. 
    #When you use negative values for cell coordinates, you will basically count backwards from the
    #other end of the table,
    #ie  apply the formatting from (0, 0) to (-1, 0), what you are saying is that you want the formatting to apply to the
    #entire first row of the table
    '''
    Command                 Description
    ALIGNMENT (or ALIGN)    LEFT, RIGHT, CENTRE/CENTER or DECIMAL
    BACKGROUND              The cell's background color
    FONT                    The font name to be applied (optionally can add font size and leading)
    FONTNAME (orFACE)       The font name
    FONTSIZE (or SIZE)      The size of the font in points (leading will likely get out of sync)
    LEADING                 The leading space in points
    TEXTCOLOR               The color name string or (R,G,B) tuple
    LEFTPADDING             The amount of left padding as an integer(default: 6)
    RIGHTPADDING            The amount of right padding as an integer (default: 6)
    BOTTOMPADDING The amount of bottom padding as an integer(default: 3)
    TOPPADDING The amount of top padding as an integer(default: 3)
    COLBACKGROUNDS A list of colors that ReportLab will cycle through
    ROWBACKGROUNDS A list of colors that ReportLab will cycle through
    VALIGN TOP, MIDDLE or the default of BOTTOM

    BACKGROUND command
        It will actually take a ReportLab color from reportlab.lib.colors, 
        a string name or a numeric tuple / list. 
        if tuple, tuple must contain the following information:
        (DIRECTION, startColor, endColor). The DIRECTION element needs to
        be either VERTICAL or HORIZONTAL. This will apply the color as a
        gradient
    The GRID command 
        is actually equivalent to applying the BOX and INNERGRID commands. 
        Basically BOX will apply lines to the outside of the specified cells 
        while INNERGRID will add lines inbetween the cells.
    '''
    tblstyle = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), #0.25 is line width
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ])
    tblstyle2 = TableStyle([('BACKGROUND', (0, 0), (-1, 0),
                            ["HORIZONTAL", colors.red, colors.blue]),
                            ('TEXTCOLOR', (0, 1), (-1, 1), colors.blue)
                            ])                      
    tblstyle3 = TableStyle([('FONT', (0, 1), (-1, 1), 'Helvetica', 24)
                            ])
    tblstyle4 = TableStyle([('FONT', (0, 1), (-1, 1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, 1), 24)
                            ])
    tblstyle5 = TableStyle([('FONT', (0, 0), (-1, 0), 'Times-Roman'),
                            ('FONT', (0, 1), (-1, 1), 'Helvetica', 24),
                            ('FONT', (0, 2), (-1, 2), 'Courier', 12)
                            ])     
    tblstyle6 = TableStyle(
                        [('LINEABOVE', (0, 0), (-1, 0), 0.5, colors.red),
                        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.blue),
                        ('LINEBEFORE', (0, 0), (0, -1), 2.5, colors.orange),
                        ('LINEAFTER', (-1, 0), (-1, -1), 3.5, colors.green),
                        ])            
    tblstyle7 = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ('ALIGN', (0, 0), (0, -1), 'CENTER'), # first    column
                            ('VALIGN', (1, 0), (1, -1), 'MIDDLE'), # second   colu\                    mn
                            ('ALIGN', (2, 0), (2, -1), 'CENTER'), # middle   colu\  mn
                            ('VALIGN', (2, 0), (2, -1), 'MIDDLE'), # middle colu\               mn
                            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'), # last column
                            ])

    tblstyle8 = TableStyle([('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.gray, colors.white]),
                            ('COLBACKGROUNDS', (0,0), (-1,-1),    [colors.red, colors.white, colors.blue])
                            ])     
    #(SPAN, (begin_col, begin_row), (end_col, end, row))
    #for spanning cells 
    tblstyle9 = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ('SPAN', (0, -1), (1, -1))
                            ])
    #Table(data, colWidths=None, rowHeights=None, style=None, splitByRow=1,
    #repeatRows=0, repeatCols=0, rowSplitRange=None, spaceBefore=None,
    #spaceAfter=None)
    tbl = Table(data)
    tbl2 = Table(data, colWidths=[55 for x in range(5)],
            rowHeights=[45 for x in range(len(data))]
            )
    tbl.setStyle(tblstyle)
    story.append(tbl)

    doc.build(story)

if __name__ == '__main__':
    table_with_images()     
        
##ReportLab -  Complex document  
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4,landscape, letter
from reportlab.lib.units import inch,cm,mm #72.0 ,28.34, 2.83
from reportlab.pdfgen import canvas

PAGE_HEIGHT=defaultPageSize[1] #841.8897637795277
PAGE_WIDTH=defaultPageSize[0]  #595.2755905511812
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"


#check all instance variables 
def getAllVars(msg,obj):
    print(msg)
    sd = dir(obj)
    for v in sorted(sd):
        if not callable(getattr(obj, v)) and not v.startswith("_"):
            print("\t", v, " : ", getattr(obj, v))

def myFirstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(inch, 0.75 * inch,"First Page / %s" % pageinfo)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch,"Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def go():
    doc = SimpleDocTemplate("12.myreport.pdf",
                        leftMargin = 0.75*inch,
                        rightMargin = 0.75*inch,
                        topMargin = 1*inch,
                        bottomMargin = 1*inch)
    getAllVars("\nCurrent values of SimpleDocTemplate",doc)    
    Story = [Spacer(1,2*inch)]  #width, height,
    style = styles["Normal"]
    for i in range(10):
        bogustext = ("Paragraph number <b>%s</b> " % i) *20
        p = Paragraph(bogustext, style)
        Story.append(p)
        Story.append(Spacer(1,0.2*inch))
    Story.append(PageBreak())
    NormalStyle = tables.TableStyle([
        ('BOX',(0,0),(-1,-1),0.45,colors.blue),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
        ('BACKGROUND',(0,0),(-1,-1),colors.lightblue)
        ])
    mytable = tables.Table([('test','test'),('test2','test2'),('test3','test3')],
                colWidths = 1* inch,rowHeights= 0.25 *inch,style = NormalStyle)
    Story.append(mytable)    
    [getAllVars("\nCurrent values of " + str(e),e) for e in Story]
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

if __name__ == "__main__":
    go()      
        
##ReportLab -  pie_chart_with_legend.py

from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String


def pie_chart_with_legend():
    data = list(range(15, 105, 15))
    drawing = Drawing(width=400, height=200)
    my_title = String(170, 40, 'My Pie Chart', fontSize=14)
    pie = Pie()
    pie.sideLabels = True

    pie.x = 150
    pie.y = 65

    pie.data = data
    pie.labels = [letter for letter in 'abcdefg']
    pie.slices.strokeWidth = 0.5
    drawing.add(my_title)
    drawing.add(pie)
    add_legend(drawing, pie, data)
    drawing.save(formats=['pdf'], outDir='.',
                 fnRoot='13.pie_chart_with_legend')


def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


if __name__ == '__main__':
    pie_chart_with_legend()


        
##ReportLab -       line_plot_demo.py

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.widgets.markers import makeMarker


def line_plot_demo():
    d = Drawing(400, 400)
    line = LinePlot()
    line.x = 50
    line.y = 85
    line.height = 150
    line.width = 250
    line.lineLabelFormat = '%2.0f'

    data = [
            ((1,1), (2,2), (2.5,1), (3,3), (4,5)),
            ((1,2), (2,3), (2.5,2), (3.5,5), (4,6))
        ]
    line.data = data

    line.lines[0].strokeColor = colors.green
    line.lines[1].strokeColor = colors.blue
    line.lines[0].strokeWidth = 3

    line.lines[0].symbol = makeMarker('Circle')
    line.lines[1].symbol = makeMarker('Hexagon')

    line.xValueAxis.valueMin = 0
    line.xValueAxis.valueMax = 10
    line.xValueAxis.valueSteps = [1, 2, 4]
    line.xValueAxis.labelTextFormat = '%2.1f'

    line.yValueAxis.valueMin = 0
    line.yValueAxis.valueMax = 12

    d.add(line, '')
    d.save(formats=['pdf'], outDir='.', fnRoot='14.line_plot_demo')


if __name__ == '__main__':
    line_plot_demo() 
        
##ReportLab - simple_line_chart.py

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.platypus import SimpleDocTemplate


def simple_line_chart():
    d = Drawing(280, 250)
    line = HorizontalLineChart()
    line.x = 50
    line.y = 85
    line.height = 150
    line.width = 250
    
    data = [[1, 2, 3, None, None, None, 5],
            [10, 5, 2, 6, 8, 3, 5]
            ]
    line.data = data
    line.categoryAxis.categoryNames = [
        'Dogs', 'Cats', 'Mice', 'Hamsters',
        'Parakeets', 'Gerbils', 'Fish'
    ]

    line.lines[0].strokeColor = colors.green
    line.lines[1].strokeColor = colors.blue
    line.lines[0].strokeWidth = 3
    line.categoryAxis.labels.angle = 45
    line.categoryAxis.labels.dy = -15
    
    d.add(line, '')

    doc = SimpleDocTemplate('15.simple_line_chart.pdf')
    story = []
    story.append(d)
    doc.build(story)

if __name__ == '__main__':
    simple_line_chart()


        
##ReportLab -     simple_bar_chart.py

from reportlab.lib.colors import PCMYKColor
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart


def simple_bar_chart():
    d = Drawing(280, 250)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    data = [[1, 2, 3, None, None, None, 5],
            [10, 5, 2, 6, 8, 3, 5],
            [5, 7, 2, 8, 8, 2, 5],
            [2, 10, 2, 1, 8, 9, 5],
            ]
    bar.data = data
    bar.categoryAxis.categoryNames = ['Year1', 'Year2', 'Year3',
                                      'Year4', 'Year5', 'Year6',
                                      'Year7']

    bar.bars[0].fillColor = PCMYKColor(0,100,100,40,alpha=85)
    bar.bars[1].fillColor = PCMYKColor(23,51,0,4,alpha=85)
    
    d.add(bar, '')

    d.save(formats=['pdf'], outDir='.', fnRoot='16.simple_bar_chart')

if __name__ == '__main__':
    simple_bar_chart()   
        

        
##ReportLab -    simple_stacked_bar_chart.py

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.platypus import SimpleDocTemplate


def simple_stacked_bar_chart():
    """
    Creates a bar chart in a PDF
    """
    d = Drawing(280, 250)
    bar = VerticalBarChart()
    bar.x = 50
    bar.y = 85
    data = [[1, 2, 3, None, None, None, 5],
            [10, 5, 2, 6, 8, 3, 5]
            ]
    bar.data = data
    bar.categoryAxis.categoryNames = ['Year1', 'Year2', 'Year3',
                                      'Year4', 'Year5', 'Year6',
                                      'Year7']

    bar.bars[0].fillColor = colors.green
    bar.bars[1].fillColor = colors.blue
    bar.categoryAxis.labels.angle = 45
    bar.categoryAxis.labels.dy = -15
    bar.categoryAxis.style = 'stacked'
    
    d.add(bar, '')

    doc = SimpleDocTemplate('17.simple_stacked_bar_chart.pdf')
    story = []
    story.append(d)
    doc.build(story)

if __name__ == '__main__':
    simple_stacked_bar_chart()    
        
##ReportLab - simple_horizontal_bar_chart.py

from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.platypus import SimpleDocTemplate


def simple_horizontal_bar_chart():
    d = Drawing(280, 250)
    bar = HorizontalBarChart()
    bar.x = 50
    bar.y = 85
    bar.height = 225
    bar.width = 250
    data = [[1, 2, 3, None, None],
            [10, 5, 2, 6, 8],
            [5, 7, 2, 8, 8],
            [2, 10, 2, 1, 8],
            ]
    bar.data = data
    bar.categoryAxis.categoryNames = ['Year1', 'Year2', 'Year3',
                                      'Year4', 'Year5', 'Year6',
                                      'Year7']

    bar.bars[0].fillColor = colors.green
    bar.bars[1].fillColor = colors.blue
    bar.bars[2].fillColor = colors.red
    bar.bars[3].fillColor = colors.purple
    
    bar.categoryAxis.labels.angle = 45
    bar.categoryAxis.labels.dx = -15
    
    d.add(bar, '')

    doc = SimpleDocTemplate('18.simple_horizontal_bar_chart.pdf')
    story = []
    story.append(d)
    doc.build(story)

if __name__ == '__main__':
    simple_horizontal_bar_chart()

##ReportLab - 3D vertical bar 
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart3D
from reportlab.platypus import SimpleDocTemplate, PageBreak


def simple_vertical_3d_bar_chart():
    d = Drawing(280, 250)
    bar = VerticalBarChart3D()
    bar.x = 50
    bar.y = 85
    bar.height = 225
    bar.width = 350
    data = [[1, 2, 3, None, None],
            [10, 5, 2, 6, 8],
            [5, 7, 2, 8, 8],
            [2, 10, 2, 1, 8],
            ]
    bar.data = data
    bar.categoryAxis.categoryNames = ['Year1', 'Year2', 'Year3',
                                      'Year4', 'Year5', 'Year6',
                                      'Year7']
    bar.bars[0].fillColor = colors.green
    bar.bars[1].fillColor = colors.blue
    bar.bars[2].fillColor = colors.red
    bar.bars[3].fillColor = colors.purple    
    bar.categoryAxis.labels.angle = 45
    bar.categoryAxis.labels.dy = -15    
    d.add(bar, '')
    doc = SimpleDocTemplate('19.simple_vertical_3d_bar_chart.pdf')
    story = []
    story.append(d)
    story.append(PageBreak())
    story.append(d)
    doc.build(story)

if __name__ == '__main__':
    simple_vertical_3d_bar_chart()


    
    