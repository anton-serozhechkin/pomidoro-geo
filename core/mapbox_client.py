from mapbox import Geocoder, Directions
import json
from socketio import AsyncNamespace
import httpx
import requests
from .config import MAPBOX_ACCESS_TOKEN

"""
    data = {'info': {'orderId': 1234,
                      'coruierId': 657,
                      'profile': 'mapbox/walking',
                      'language': 'ru',
                      'token': 'fbvuefvudb43'
                      'started': True
                      },
            'origin': {'type': 'Feature',
                      'geometry': {
                                  'type': 'Point',
                                  'coordinates': [-122.7282, 45.5801]
                                  }
                      },
            'destination': {'type': 'Feature',
                            'search_type': 'input,'
                            'geometry': {
                                'type': 'Point', 
                                'coordinates': [-122.6153, 45.4882]
                                        }
                              }
            'current_loc': {
                            'coordinates': [-122.6153, 45.4882],
                            'last_update': '2020-08-12 15:34'
                            }
            }
"""

class BaseNamespace(AsyncNamespace):

    base_url = "https://api.mapbox.com"
    token = MAPBOX_ACCESS_TOKEN
    client = httpx.AsyncClient(http2=True)
    geocoder = Geocoder(access_token=MAPBOX_ACCESS_TOKEN)
    service = Directions()


    async def controller_params(self, sid, session, params):
        geometry_coor = params['destination']['geometry']['coordinates']
        if params['info']['started']:
            current_loc_coordinates = params['current_loc']['coordinates']
            isochrone_point = "{}/isochrone/v1/{}/{},{}?contours_minutes=1&access_token={}".format(
                                                        base_url,
                                                        session[sid]['profile'],
                                                        current_loc_coordinates[0],
                                                        current_loc_coordinates[1],
                                                        token)
            responce = requests.get(isochrone_point)
            return await responce.json()
        else:
            if geometry_coor[0] and geometry_coor[1]:
                response = service.directions([origin, destination], profile='mapbox/{}'.format(session['profile']),
                                    geometries='geojson', overview=False,
                                    language=session['sid']['lang'], steps=True)
                return await response.json()
            else:
                if params['destination']['search_type']:
                    return await find_route_input(params)
                else:
                    return await find_route_by_point(params)


    async def find_route_input(self, session, params):
        url_direction_api = geocoder.forward(params['adress'], limit=params['limit'], country=['ua'], languages=session['sid']['lang'])
        responce = []
        i = 1
        await for data in url_direction_api.geojson()['features']:
            responce.append({i: {"id": data['id'], "place_name": data['place_name'],
                        "lon": data['geometry']['coordinates'][0],
                        "lat": data['geometry']['coordinates'][1],
                        "place_id": data['context'][0]['id']}})
            i += 1
        return await responce


    async def full_route(session, params):
        response = service.directions([origin, destination], profile='mapbox/walking',
                                    geometries='geojson', overview=False,
                                    language=params['language'], steps=True)
        return await response.json()

    async def find_route_by_point(params):
        responce = 

def is_valid_profiles(profile):
    if profile in service.valid_profiles: 
        return True
    else:
        return False


def check_status_code(status_code):
    if status_code == 200:
        return True
    else:
        return False

#while True:
#find_route_input({'adress': 'улица мира', 'limit': '8', 'lang': ['ru']})
#is_valid_profiles('mapbox/driving')
#response = geocoder.forward("200 queen street")
#print(response.status_code)
#print(response.headers['Content-Type'])
#print(response.geojson()['features'])
#first = response.geojson()['features'][0]
#print(first['place_name'])
