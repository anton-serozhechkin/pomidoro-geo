from mapbox import Geocoder, Directions
import json
from socketio import AsyncNamespace
import requests
from config import MAPBOX_ACCESS_TOKEN
import asyncio


geocoder = Geocoder(access_token=MAPBOX_ACCESS_TOKEN)
service = Directions()


async def controller_params(sid, session, params):
    # if the courier started delivery
    # value by key 'started' == True
    if params['info']['started']:
        # get courier current location
        current_loc_coordinates = params['current_loc']['coordinates']

        isochrone_point = "https://api.mapbox.com/isochrone/v1/"\
                          "{}/{},{}?contours_minutes=1&access_token={}".format(session[sid]['profile'],
                                                                               current_loc_coordinates[0],
                                                                               current_loc_coordinates[1],
                                                                               MAPBOX_ACCESS_TOKEN)
        responce = requests.get(isochrone_point)
        return responce.json()['features'][0]
    else:
        geometry_coor = params['destination']['geometry']['coordinates']
        if geometry_coor[0] and geometry_coor[1]:
            response = service.directions([params['origin'], params['destination']], 
                                            profile='mapbox/{}'.format(session[sid]['profile']),
                                            geometries='geojson', overview=False,
                                            language=session[sid]['lang'], steps=True)
            return response.json()
        else:
            if params['destination']['search_type']:
                return find_route_input(sid, session, params)
            #else:
            #    return find_route_by_point(sid, session, params)


async def find_route_input(sid, session, params):
    url_direction_api = geocoder.forward(params['adress'],
                                        limit=6, country=['ua'],
                                        languages=session[sid]['lang'])
    responce = []
    i = 1
    for data in url_direction_api.geojson()['features']:
        responce.append({i: {"id": data['id'], "place_name": data['place_name'],
                    "lon": data['geometry']['coordinates'][0],
                    "lat": data['geometry']['coordinates'][1],
                    "place_id": data['context'][0]['id']}})
        i += 1
    return responce


async def full_route(session, params):
    response = service.directions([origin, destination], profile=params['info']['profile'],
                                  geometries='geojson', overview=False,
                                  language=params['info']['language'], steps=True)
    return response.json()


# async def find_route_by_point(params):
#     responce = 



#response = geocoder.forward("200 queen street")
#print(response.status_code)
#first = response.geojson()['features'][0]
#print(first['place_name'])
