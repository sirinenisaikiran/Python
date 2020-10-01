# Remove attributes
import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()

for x in myroot:
    x[0].attrib.pop('name')
# myroot[0][0].attrib.pop('name')
mytree.write('new3.xml')