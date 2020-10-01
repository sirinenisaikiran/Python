import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()

for x in myroot.iter('description'):
    a = str(x.text) + ' description has been added'
    x.text = str(a)
    x.set('updated','yes')
mytree.write('new.xml')