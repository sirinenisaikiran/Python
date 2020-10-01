# Clearning first food tag
import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()
myroot[0].clear()
mytree.write('new5.xml')