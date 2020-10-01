
'''  
TableStyle(cmds=None, parent=None, **kw)
The cmds argument is just a list of tuples that define what cell formatting you want to apply.
The first element in the tuple is the cell formatting command
Thesecond and third elements define the cell coordinates that the formatting
will apply to. The coordinates are (column, row),
The -1 in the second set of coordinates tells ReportLab that we want the formatting
to extend across all the columns from left-to-right. 
When you use negative values for cell coordinates, you will basically count backwards from the
other end of the table,
ie  apply the formatting from (0, 0) to (-1, 0), what you are saying is that you want the formatting to apply to the
entire first row of the table

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
    
    #Example 
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
'''   
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.units import inch,cm,mm #72.0 ,28.34, 2.83
from reportlab.pdfgen import canvas

from reportlab.lib.validators import Auto
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.shapes import Drawing, String


PAGE_HEIGHT=defaultPageSize[1] #841.8897637795277
PAGE_WIDTH=defaultPageSize[0]  #595.2755905511812
styles = getSampleStyleSheet()
Title = "Hello world"
pageinfo = "platypus example"

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
    doc = SimpleDocTemplate("myreport.pdf",
                        leftMargin = 0.75*inch,
                        rightMargin = 0.75*inch,
                        topMargin = 1*inch,
                        bottomMargin = 1*inch)
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
    Story.append(PageBreak())
    #A drawing 
    Story.append(pie_chart_with_legend()) 
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

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
    return drawing

def add_legend(draw_obj, chart, data):
    legend = Legend()
    legend.alignment = 'right'
    legend.x = 10
    legend.y = 70
    legend.colorNamePairs = Auto(obj=chart)
    draw_obj.add(legend)


if __name__ == "__main__":
    go()    