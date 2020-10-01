print("Printing metadata..")
path = '../data/example.pdf'

from PyPDF2 import PdfFileReader

def get_info(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()
    print(str(info).encode('ascii','ignore').decode())
    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title
    return (author, creator, producer, subject, title)


get_info(path)


print("Extracting Text From PDFs")
#PyPDF2 has limited support for extracting text from PDFs. 
#It doesn't have built-in support for extracting images

#to extract the text from the first page of the PDF 

from PyPDF2 import PdfFileReader

def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        # get the first page
        page = pdf.getPage(0)
        print(page)
        print('Page type: {}'.format(str(type(page))))
        text = page.extractText()
        return text 


print(text_extractor(path))

print("Splitting PDFs")
#The PyPDF2 package gives the ability to split up a single PDF into multiple ones. 


import os.path 
from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output_filename = '{}_page_{}.pdf'.format(fname, page+1)
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(output_filename))


pdf_splitter(path)

print("Merging Multiple PDFs Together")

import glob

from PyPDF2 import PdfFileWriter, PdfFileReader

def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)

paths = ['../data/example.pdf', '../data/example1.pdf']
merger('pdf_merger.pdf', paths)


print("Rotating Pages..")
#you must rotate in 90 degrees increments. 
#You can rotate the PDF pages either clockwise or counterclockwise. 


from PyPDF2 import PdfFileWriter, PdfFileReader

def rotator(path):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(path)
    page1 = pdf_reader.getPage(0).rotateClockwise(90)
    pdf_writer.addPage(page1)
    page2 = pdf_reader.getPage(1).rotateCounterClockwise(90)
    pdf_writer.addPage(page2)
    with open('pdf_rotator.pdf', 'wb') as fh:
        pdf_writer.write(fh)

rotator(path)

print("Overlaying/Watermarking Pages")
#supports merging PDF pages together or overlaying pages on top of each other. 


from PyPDF2 import PdfFileWriter, PdfFileReader

def watermark(input_pdf, output_pdf, watermark_pdf):
    watermark = PdfFileReader(watermark_pdf)
    watermark_page = watermark.getPage(0)
    pdf = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        pdf_page = pdf.getPage(page)
        pdf_page.mergePage(watermark_page)
        pdf_writer.addPage(pdf_page)
    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

watermark(input_pdf=path, 
              output_pdf='watermarked_w9.pdf',
              watermark_pdf='../data/watermark.pdf')


print("PDF Encryption")


from PyPDF2 import PdfFileWriter, PdfFileReader

def encrypt(input_pdf, output_pdf, password):
    pdf_writer = PdfFileWriter()
    pdf_reader = PdfFileReader(input_pdf)
    for page in range(pdf_reader.getNumPages()):
        pdf_writer.addPage(pdf_reader.getPage(page))
    pdf_writer.encrypt(user_pwd=password, owner_pwd=None, use_128bit=True)
    with open(output_pdf, 'wb') as fh:
        pdf_writer.write(fh)

encrypt(input_pdf=path,
            output_pdf='encrypted.pdf',
            password='blowfish')