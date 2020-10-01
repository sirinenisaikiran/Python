import xml.etree.ElementTree as ET
data = '''<metadata>
  <food>
    <item name="breakfast">Idly</item>
    <price>20₹</price>
    <description>Two idlys with chutney</description>
    <calories>553</calories>
  </food>
  <food>
    <item name="breakfast">Paper dosa</item>
    <price>25₹</price>
    <description>Plain papaer dosa with chutney</description>
    <calories>400</calories>
  </food>
</metadata>'''

myroot = ET.fromstring(data)
print(myroot.tag)