import xml.etree.ElementTree as ET
mytree = ET.parse('Sample.xml')
myroot = mytree.getroot()
# print(myroot)
# print(myroot.tag)
# print(myroot[0].tag)
# print(myroot[0].attrib)
#
# for x in myroot[0]:
#     print(x.tag, x.attrib)
# for x in myroot[0]:
#     print(x.text)
# for x in myroot[0]:
#         print(x.tag, x.attrib, x.text)

for x in myroot.findall('food'):
    item = x.find('item').text
    price = x.find('price').text
    print(item,price)