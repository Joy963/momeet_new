#!/usr/bin/env python
# coding=utf-8

import sys
from city import CITY_DATA
import xml.etree.cElementTree as et
reload(sys)  
sys.setdefaultencoding('utf-8')


r = et.ElementTree(file='a.xml').getroot()
a = et.SubElement(r, 'array')

for city in CITY_DATA:
    d = et.SubElement(a, 'dict')

    k1 = et.SubElement(d, 'key')
    k1.text = 'State'

    s1 = et.SubElement(d, 'string')
    s1.text = city.get('name')

    k2 = et.SubElement(d, 'key')
    k2.text = 'StateId'

    s2 = et.SubElement(d, 'string')
    s2.text = str(city.get('id'))

    k3 = et.SubElement(d, 'key')
    k3.text = 'Cities'

    array = et.SubElement(d, 'array')
    for xx in city.get('cities'):
        dict = et.SubElement(array, 'dict')

        k4 = et.SubElement(dict, 'key')
        k4.text = 'city'

        s4 = et.SubElement(dict, 'string')
        s4.text = xx.get('name')

        k5 = et.SubElement(dict, 'key')
        k5.text = 'cityId'

        s5 = et.SubElement(dict, 'string')
        s5.text = str(xx.get('id'))

t = et.ElementTree(r)
t.write('a.xml')
