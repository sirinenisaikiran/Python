# Add new tags
import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()
ET.SubElement(myroot[0],'speciality')
for x in myroot.iter('speciality'):
    b = 'South Indian Special'
    x.text = str(b)
mytree.write('new2.xml')