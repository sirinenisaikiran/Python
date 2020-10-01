'''
SimpleDocTemplate
Argument details 
    'pagesize':defaultPageSize,
    'pageTemplates':[],
    'showBoundary':0,
    'leftMargin':inch,
    'rightMargin':inch,
    'topMargin':inch,
    'bottomMargin':inch,
    'allowSplitting':1,
    'title':None,
    'author':None,
    'subject':None,
    'creator':None,
    'producer':None,
    'keywords':[],
    'invariant':None,
    'pageCompression':None,
    '_pageBreakQuick':1,
    'rotation':0,
    '_debug':0,
    'encrypt': None,
    'cropMarks': None,
    'enforceColorSpace': None,
    'displayDocTitle': None,
    'lang': None,
    'initialFontName': None,
    'initialFontSize': None,
    'initialLeading': None,
    'cropBox': None,
    'artBox': None,
    'trimBox': None,
    'bleedBox': None,
    'keepTogetherClass': KeepTogether,
'''

""" 
Paragraph(text, style, bulletText=None, caseSensitive=1)
    text a string of stuff to go into the paragraph.
    style is a style definition as in reportlab.lib.styles.
    bulletText is an optional bullet defintion.
    caseSensitive set this to 0 if you want the markup tags and their attributes to be case-insensitive.

    This class is a flowable that can format a block of text
    into a paragraph with a given style.

    The paragraph Text can contain XML-like markup including the tags:
    <b> ... </b> - bold
    < u [color="red"] [width="pts"] [offset="pts"]> < /u > - underline
        width and offset can be empty meaning use existing canvas line width
        or with an f/F suffix regarded as a fraction of the font size
    < strike > < /strike > - strike through has the same parameters as underline
    <i> ... </i> - italics
    <u> ... </u> - underline
    <strike> ... </strike> - strike through
    <super> ... </super> - superscript
    <sub> ... </sub> - subscript
    <font name=fontfamily/fontname color=colorname size=float>
    <span name=fontfamily/fontname color=colorname backcolor=colorname size=float style=stylename>
    <onDraw name=callable label="a label"/>
    <index [name="callablecanvasattribute"] label="a label"/>
    <link>link text</link>
        attributes of links
            size/fontSize/uwidth/uoffset=num
            name/face/fontName=name
            fg/textColor/color/ucolor=color
            backcolor/backColor/bgcolor=color
            dest/destination/target/href/link=target
            underline=bool turn on underline
    <a>anchor text</a>
        attributes of anchors
            size/fontSize/uwidth/uoffset=num
            fontName=name
            fg/textColor/color/ucolor=color
            backcolor/backColor/bgcolor=color
            href=href
            underline="yes|no"
    <a name="anchorpoint"/>
    <unichar name="unicode character name"/>
    <unichar value="unicode code point"/>
    <img src="path" width="1in" height="1in" valign="bottom"/>
            width="w%" --> fontSize*w/100   idea from Roberto Alsina
            height="h%" --> linewidth*h/100 <ralsina@netmanagers.com.ar>

    The whole may be surrounded by <para> </para> tags

    The <b> and <i> tags will work for the built-in fonts (Helvetica
    /Times / Courier).  For other fonts you need to register a family
    of 4 fonts using reportlab.pdfbase.pdfmetrics.registerFont; then
    use the addMapping function to tell the library that these 4 fonts
    form a family e.g.
    from reportlab.lib.fonts import addMapping
    addMapping('Vera', 0, 0, 'Vera')    #normal
    addMapping('Vera', 0, 1, 'Vera-Italic')    #italic
    addMapping('Vera', 1, 0, 'Vera-Bold')    #bold
    addMapping('Vera', 1, 1, 'Vera-BoldItalic')    #italic and bold

    It will also be able to handle any MathML specified Greek characters.
"""

    
'''
The Spacer class gives us a convenient way to add space between
paragraphs or other flowables, while the Image class gives us a nice way to
insert images into our document
'''

'''
ParagraphStyle defaults 
    'fontName':_baseFontName,
    'fontSize':10,
    'leading':12,
    'leftIndent':0,
    'rightIndent':0,
    'firstLineIndent':0,
    'alignment':TA_LEFT,
    'spaceBefore':0,
    'spaceAfter':0,
    'bulletFontName':_baseFontName,
    'bulletFontSize':10,
    'bulletIndent':0,
    #'bulletColor':black,
    'textColor': black,
    'backColor':None,
    'wordWrap':None,        #None means do nothing special
                            #CJK use Chinese Line breaking
                            #LTR RTL use left to right / right to left
                            #with support from pyfribi2 if available
    'borderWidth': 0,
    'borderPadding': 0,
    'borderColor': None,
    'borderRadius': None,
    'allowWidows': 1,
    'allowOrphans': 0,
    'textTransform':None,   #uppercase lowercase (captitalize not yet) or None or absent
    'endDots':None,         #dots on the last line of left/right justified paras
                            #string or object with text and optional fontName, fontSize, textColor & backColor
                            #dy
    'splitLongWords':1,     #make best efforts to split long words
    'underlineWidth': _baseUnderlineWidth,  #underline width
    'bulletAnchor': 'start',    #where the bullet is anchored ie start, middle, end or numeric
    'justifyLastLine': 0,   #n allow justification on the last line for more than n words 0 means don't bother
    'justifyBreaks': 0,     #justify lines broken with <br/>
    'spaceShrinkage': _spaceShrinkage,  #allow shrinkage of percentage of space to fit on line
    'strikeWidth': _baseStrikeWidth,    #stroke width
    'underlineOffset': _baseUnderlineOffset,    #fraction of fontsize to offset underlines
    'underlineGap': _baseUnderlineGap,      #gap for double/triple underline
    'strikeOffset': _baseStrikeOffset,  #fraction of fontsize to offset strikethrough
    'strikeGap': _baseStrikeGap,        #gap for double/triple strike
    'linkUnderline': _platypus_link_underline,
    #'underlineColor':  None,
    #'strikeColor': None,
    'hyphenationLang': _hyphenationLang,
    #'hyphenationMinWordLength': _hyphenationMinWordLength,
    'embeddedHyphenation': _embeddedHyphenation,
    'uriWasteReduce': _uriWasteReduce,
'''


import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


def form_letter():
    doc = SimpleDocTemplate("form_letter.pdf",
                            pagesize=letter,
                            rightMargin=72,
                            leftMargin=72,
                            topMargin=72,
                            bottomMargin=18)    
    flowables = []
    logo = "python_logo.png"
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"

    formatted_time = time.ctime()
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Waterloo, IA 50158"]

    im = Image(logo, 2*inch, 2*inch)
    flowables.append(im)

    styles = getSampleStyleSheet()
    # Modify the Normal Style
    styles["Normal"].fontSize = 12
    styles["Normal"].leading = 14
    
    # Create a Justify style
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))    

    flowables.append(Paragraph(formatted_time, styles["Normal"]))
    flowables.append(Spacer(1, 12))    

    # Create return address
    flowables.append(Paragraph(full_name, styles["Normal"]))
    for part in address_parts:
        flowables.append(Paragraph(part.strip(), styles["Normal"]))
        
    flowables.append(Spacer(1, 12))  #gap of wifth and height 
    ptext = 'Dear {}:'.format(full_name.split()[0].strip())
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 12))

    ptext = '''
    We would like to welcome you to our subscriber
    base for {magName} Magazine! You will receive {issueNum} issues at
    the excellent introductory price of ${subPrice}. Please respond by
    {limitedDate} to start receiving your subscription and get the
    following free gift: {freeGift}.
    '''.format(magName=magName,
               issueNum=issueNum,
               subPrice=subPrice,
               limitedDate=limitedDate,
               freeGift=freeGift)
    flowables.append(Paragraph(ptext, styles["Justify"]))
    flowables.append(Spacer(1, 12))

    ptext = '''Thank you very much and we look
    forward to serving you.'''

    flowables.append(Paragraph(ptext, styles["Justify"]))
    flowables.append(Spacer(1, 12))
    ptext = 'Sincerely,'
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 48))
    ptext = 'Ima Sucker'
    flowables.append(Paragraph(ptext, styles["Normal"]))
    flowables.append(Spacer(1, 12))
    doc.build(flowables)

if __name__ == '__main__':
    form_letter()    