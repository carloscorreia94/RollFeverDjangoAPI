from math import radians, degrees, cos
from spots.serializers import SpotNearbySerializer
from spots.models import Spot


EARTH_RADIUS = 6371

def nearby(lat,lng,radius):
    radius = float(radius) / 1000
    lat = float(lat)
    lng = float(lng)

    maxLat = lat + degrees(radius/EARTH_RADIUS)
    minLat = lat - degrees(radius/EARTH_RADIUS)

    maxLng = lng + degrees(radius/EARTH_RADIUS/cos(radians(lat)))
    minLng = lng - degrees(radius/EARTH_RADIUS/cos(radians(lat)))

    lat = radians(lat)
    lng = radians(lng)


    rawSet = Spot.objects.raw('Select id, name, lat, lng, \
            acos(sin(%s)*sin(radians(lat)) + cos(%s)*cos(radians(lat))*cos(radians(lng)-%s)) * %s As D \
        From ( \
            Select id, name, lat, lng \
            From spots_spot \
            Where lat Between %s And %s \
              And lng Between %s And %s \
        ) As FirstCut \
        Where acos(sin(%s)*sin(radians(lat)) + cos(%s)*cos(radians(lat))*cos(radians(lng)-%s)) * %s < %s \
        Order by D', [lat,lat,lng,EARTH_RADIUS,minLat,maxLat,minLng,maxLng,lat,lat,lng,EARTH_RADIUS,radius])
    serializer = SpotNearbySerializer(rawSet,many=True)
    return serializer.data