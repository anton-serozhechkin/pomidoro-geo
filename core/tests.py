from mapbox import Geocoder, Directions
import json
from socketio import AsyncNamespace
import requests
from config import MAPBOX_ACCESS_TOKEN
import asyncio


geocoder = Geocoder(access_token=MAPBOX_ACCESS_TOKEN)
service = Directions()


async def full_route(params):
        response = service.directions([origin, destination], profile='mapbox/walking',
                                      geometries='geojson', overview=False,
                                      language=params['language'], steps=True)
        return response.json()


async def check_courier_position(profile, current_loc_coordinates, token):
    base_url = "https://api.mapbox.com"
    req = "{}/isochrone/v1/{}/{},{}?contours_minutes=1&access_token={}".format(
                                                        base_url,
                                                        profile,
                                                        current_loc_coordinates[0],
                                                        current_loc_coordinates[1],
                                                        token)
    responce = requests.get(req)
    return responce.json()['features'][0]

loop = asyncio.get_event_loop()
loop.run_until_complete(check_courier_position('mapbox/walking', [-122.7282, 45.5801], MAPBOX_ACCESS_TOKEN), full_route({'language': 'ua', 'profile': 'mapbox/walking'}))