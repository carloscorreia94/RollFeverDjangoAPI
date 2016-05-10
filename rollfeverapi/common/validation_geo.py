import re

# Radius is in Meters
MIN_RADIUS = 100
MAX_RADIUS = 10000
DEFAULT_RADIUS = 1000


def check_radius(radius):
    return MAX_RADIUS >= int(radius) >= MIN_RADIUS


def check_coordinates(lat,lng):
    coords = lat + "," + lng
    return re.match('^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$',coords)