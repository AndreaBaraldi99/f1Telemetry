import xml.etree.ElementTree as ET
import math
import numpy as np


def read_kml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    coordinates = root.find('.//kml:coordinates', namespace).text
    return [list(map(float, coord.split(','))) for coord in coordinates.strip().split()]

def calculate_parallel_point(lat, lon, d, bearing):
    R = 6371000  # raggio della Terra in metri
    bearing_rad = math.radians(bearing)
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(d/R) + 
                            math.cos(lat_rad) * math.sin(d/R) * math.cos(bearing_rad))
    new_lon_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(d/R) * math.cos(lat_rad),
                                       math.cos(d/R) - math.sin(lat_rad) * math.sin(new_lat_rad))
    
    return math.degrees(new_lat_rad), math.degrees(new_lon_rad)

def calculate_parallel_lines(coordinates, distance):
    left_line = []
    right_line = []
    for i in range(len(coordinates) - 1):
        lat1, lon1 = coordinates[i][:2]  # Prendi solo i primi due valori
        lat2, lon2 = coordinates[i+1][:2]  # Prendi solo i primi due valori
        
        bearing = math.degrees(math.atan2(lon2 - lon1, lat2 - lat1))
        
        left_lat, left_lon = calculate_parallel_point(lat1, lon1, distance, bearing - 90)
        right_lat, right_lon = calculate_parallel_point(lat1, lon1, distance, bearing + 90)
        
        left_line.append((left_lat, left_lon))
        right_line.append((right_lat, right_lon))
    
    # Aggiungi l'ultimo punto
    last_lat, last_lon = coordinates[-1][:2]  # Prendi solo i primi due valori
    left_line.append(calculate_parallel_point(last_lat, last_lon, distance, bearing - 90))
    right_line.append(calculate_parallel_point(last_lat, last_lon, distance, bearing + 90))
    
    return left_line, right_line

def create_kml(original_line, left_line, right_line, output_filename):
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, 'Document')
    
    for name, line in [("Original", original_line), ("Left", left_line), ("Right", right_line)]:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = name
        style = ET.SubElement(placemark, 'Style')
        linestyle = ET.SubElement(style, 'LineStyle')
        ET.SubElement(linestyle, 'color').text = "ff0000ff"
        ET.SubElement(linestyle, 'width').text = "2"
        linestring = ET.SubElement(placemark, 'LineString')
        coordinates = ET.SubElement(linestring, 'coordinates')
        coordinates.text = ' '.join([f"{point[0]},{point[1]},0" for point in line])
    
    tree = ET.ElementTree(kml)
    tree.write(output_filename, encoding='utf-8', xml_declaration=True)

# Uso
input_filename = 'Red Bull Ring - RedBull 1.kml'
output_filename = 'output.kml'
distance = 15  # metri

# Nel main
original_line = read_kml(input_filename)
left_line, right_line = calculate_parallel_lines(original_line, distance)
create_kml(original_line, left_line, right_line, output_filename)