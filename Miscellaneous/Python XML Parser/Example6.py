# Remove attributes
import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()

for x in myroot:
    print(x[0])
    x.remove(x[0])
mytree.write('new4.xml')