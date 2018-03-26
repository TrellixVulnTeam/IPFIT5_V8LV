from __future__ import print_function
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import simplekml
import sys

#https://github.com/ianare/exif-samples/tree/master/jpg

__authors__ = ["Chapin Bryce", "Preston Miller"]
__date__ = 20170815
__description__ = "Utility to gather EXIF data from images"

parser = argparse.ArgumentParser(
    description=__description__,
    epilog="Developed by {} on {}".format(", ".join(__authors__), __date__)
)
parser.add_argument('PICTURE_FILE', help="Path to picture")
args = parser.parse_args()

gmaps = "https://www.google.com/maps?q={},{}"
open_maps = "http://www.openstreetmap.org/?mlat={}&mlon={}"


def process_coords(coord):
    coord_deg = 0
    for count, values in enumerate(coord):
        coord_deg += (float(values[0]) / values[1]) / 60**count
    return coord_deg


img_file = Image.open(args.PICTURE_FILE)
exif_data = img_file._getexif()

if exif_data is None:
    print("Geen EXIF data gevonden!")
    sys.exit()

for name, value in exif_data.items():
    gps_tag = TAGS.get(name, name)
    if gps_tag is not 'GPSInfo':
        continue

    lat_ref = value[1] == u'N'
    lat = process_coords(value[2])
    if not lat_ref:
        lat = lat * -1

    lon_ref = value[3] == u'E'
    lon = process_coords(value[4])
    if not lon_ref:
        lon = lon * -1

    kml = simplekml.Kml()
    kml.newpoint(name=args.PICTURE_FILE, coords=[(lon, lat)])
    kml.save(args.PICTURE_FILE + ".kml")

    print("GPS Coördinaten: {}, {}".format(lat, lon))
    print("Google Maps URL: {}".format(gmaps.format(lat, lon)))
    print("OpenStreetMap URL: {}".format(open_maps.format(lat, lon)))
    print("KML Bestand {} aangemaakt".format(args.PICTURE_FILE + ".kml"))