import xml.etree.ElementTree as ET
import math
import fastkml.geometry
import numpy as np
import fastkml
from shapely import *

def read_kml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = root.find('.//kml:coordinates', namespace).text
    return [list(map(float, coord.split(','))) for coord in coordinates.strip().split()]

def calculate_parallel_lines(coordinates):
    central_line = LineString(coordinates=coordinates)
    buff = buffer(central_line, distance=0.00015, cap_style='round')
    return buff.boundary, central_line

def create_kml(buff, central_line, output_filename):
    k = fastkml.kml.KML()
    ns = "{http://www.opengis.net/kml/2.2}"
    d = fastkml.kml.Document(ns=ns)
    k.append(d)
    p = fastkml.kml.Placemark(ns=ns, name="Boundaries")
    linestyle = fastkml.styles.LineStyle(
        ns=ns,
        color='ff0000ff',
        width=2)
    style = fastkml.styles.Style(ns=ns, styles=[linestyle])
    p.append_style(style)
    p.geometry = buff
    d.append(p)
    c = fastkml.kml.Placemark(ns=ns, name='Original Line')
    c.geometry = central_line
    linestyle = fastkml.styles.LineStyle(
        ns=ns,
        color='ff00ffff',
        width=2)
    style = fastkml.styles.Style(ns=ns, styles=[linestyle])
    c.append_style(style)
    d.append(c)
    xml = k.to_string(prettyprint=True)
    with open(output_filename, "w") as text_file:
        text_file.write(xml)

# Uso
input_filename = 'Red Bull Ring - RedBull 1.kml'
output_filename = 'output.kml'

# Nel main
original_line = read_kml(input_filename)
buff, central_line = calculate_parallel_lines(original_line)
create_kml(buff, central_line, output_filename)