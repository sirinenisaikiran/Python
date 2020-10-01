import os
import comtypes.client
import time


#for constant, check https://docs.microsoft.com/en-us/office/vba/api/word.wdsaveformat
#for other API, check https://docs.microsoft.com/en-us/office/vba/api/overview/word
#CreateObject(progid, clsctx=None, machine=None, interface=None, dynamic=False, pServerInfo=None)
word = comtypes.client.CreateObject('Word.Application') #would take time 
word.Visible = True
time.sleep(3)

#should be abs path 
in_file = os.path.abspath('../data/example.docx')
out_file1 = os.path.abspath('example.pdf')
out_file2 = os.path.abspath('example2.pdf')

doc=word.Documents.Open(in_file) # open docx file 1
doc.SaveAs(out_file1, FileFormat=17) # conversion, wdFormatPDF = 17
doc.Close() # close docx file 1
word.Visible = False
# convert docx file 2 to pdf file 2
doc = word.Documents.Open(in_file) # open docx file 2
doc.SaveAs(out_file2, FileFormat=17) # conversion, wdFormatPDF = 17
doc.Close() # close docx file 2   
word.Quit() # close Word Application 
