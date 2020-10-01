import os
import comtypes.client
import time


#for constant, https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype
#or PowerPoint, start it, press ALT+F11 to open the VBA editor, 
#press F2 to open the Object Browser then search on SaveAs to get this list. 
#Click on any constant name to see the value of the constant at the bottom of the dialog.

#for other methods, check https://docs.microsoft.com/en-us/office/vba/api/overview/powerpoint
ppt = comtypes.client.CreateObject('Powerpoint.Application') #would take time 
ppt.Visible = True
time.sleep(3)
#should be abs path 
in_file = os.path.abspath('../data/example.pptx')
out_file1 = os.path.abspath('example.pdf')
out_file2 = os.path.abspath('example2.pdf')

doc=ppt.Presentations.Open(in_file) 
doc.SaveAs(out_file1, FileFormat=32) # conversion, wdFormatPDF = 32
doc.Close() 
#ppt.Visible = False  #not allowed 
doc = ppt.Presentations.Open(in_file) 
doc.SaveAs(out_file2, FileFormat=32) # conversion, wdFormatPDF = 32
doc.Close() 
ppt.Quit() 