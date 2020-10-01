import os
import comtypes.client
import time


#for constant, check https://docs.microsoft.com/en-us/office/vba/api/excel.xlfileformat
#for other API - check https://docs.microsoft.com/en-us/office/vba/api/overview/excel
xl = comtypes.client.CreateObject('Excel.Application') #would take time 
xl.Visible = True
time.sleep(3)
#should be abs path 
in_file = os.path.abspath('data/empty_book.xlsx')
out_file1 = os.path.abspath('example.pdf')
out_file2 = os.path.abspath('example2.pdf')

books = xl.Workbooks.Open(in_file) 
doc = books.Worksheets[5]  #"charts" #index from 1
doc.SaveAs(out_file1, FileFormat=57) # conversion, wdFormatPDF = 57
doc.Close() 
#xl.Visible = False  #not allowed 
books = xl.Workbooks.Open(in_file) 
doc = books.Worksheets[1]  #"first"
doc.SaveAs(out_file2, FileFormat=57) # conversion, wdFormatPDF = 57
doc.Close() 
xl.Quit() 