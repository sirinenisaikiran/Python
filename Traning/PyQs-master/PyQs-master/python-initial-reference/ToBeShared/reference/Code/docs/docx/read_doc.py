import docx
doc = docx.Document('../data/example.docx')

print("""
Document attributes 
""")
print([a for a in dir(doc) if a.startswith("_") == False])
#[ 'add_heading', 'add_page_break', 'add_paragraph', 'add_picture',
# 'add_section', 'add_table', 'core_properties', 'element', 'inline_shapes', 
# 'paragraphs','part', 'save', 'sections', 'settings', 'styles', 'tables']

print("No of tables in doc")
print(doc.tables)

print("No of styles in doc")
print(list(doc.styles))

print("No of paragraphs in doc:", len(doc.paragraphs))
print(list(doc.paragraphs))

print("Paragraph attributes ")
print([a for a in dir(docx.text.paragraph.Paragraph) if a.startswith("_") == False])


print("First paragraph text")
print(doc.paragraphs[0].text)


print("""Each Paragraph object also has a runs attribute that is a list of Run objects. 
Run objects have a text attribute and any style info on that text """)

print("how many runs in first paragraph ")
print(len(doc.paragraphs[0].runs))

print("Run attributes")
print([a for a in dir(doc.paragraphs[0].runs[0]) if a.startswith("_") == False])



print("Getting the Full Text from a .docx File")


def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


print(getText('../data/example.docx'))