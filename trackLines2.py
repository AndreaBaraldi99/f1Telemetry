from xml.etree import ElementTree as ET
from shapely.geometry import LineString
import simplekml

def create_parallel_lines(kml_file, output_kml, distance):
  """
  Creates parallel lines to a line defined in a KML file.

  Args:
    kml_file: The path of the input KML file.
    output_kml: The path of the output KML file.
    distance: The distance of the parallel lines from the center line (in meters).
  """

  # Load the KML and extract the line geometry
  kml_string = open(kml_file, 'r').read()
  doc = ET.fromstring(kml_string)

  # Find the Placemark with the name "Line"
  line_placemarks = doc.findall(".//{http://www.opengis.net/kml/2.2}Placemark[.//{http://www.opengis.net/kml/2.2}LineString]")

  # Extract the coordinates from the LineString
  line_coords = line_placemarks.find(".//{http://www.opengis.net/kml/2.2}LineString").findall(".//{http://www.opengis.net/kml/2.2}coordinates")[0].text.split()
  line_coords = [(float(coord.split(',')[0]), float(coord.split(',')[1])) for coord in line_coords]

  # Create a LineString from Shapely
  line = LineString(line_coords)

  # Create the parallel lines
  left_line = line.parallel_offset(distance, 'left')
  right_line = line.parallel_offset(distance, 'right')

  # Create a new KML and add the lines
  kml = simplekml.Kml()
  ls = kml.newlinestring(name="Left Line")
  ls.coords = list(left_line.coords)
  ls = kml.newlinestring(name="Right Line")
  ls.coords = list(right_line.coords)
  ls = kml.newlinestring(name="Original Line")
  ls.coords = line_coords

  # Save the new KML
  kml.save(output_kml)

# Example of usage
input_kml = "Red Bull Ring - RedBull 1.kml"
output_kml = "output.kml"
distance = 10

create_parallel_lines(input_kml, output_kml, distance)