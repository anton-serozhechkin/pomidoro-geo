from mapbox import Geocoder, Directions
import dotenv
import os
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN')

geocoder = Geocoder(access_token=MAPBOX_ACCESS_TOKEN)

service = Directions()



def full_route(params):
    origin = {
       'type': 'Feature',
       'properties': {'name': 'Portland, OR'},
       'geometry': {
           'type': 'Point',
           'coordinates': [-122.7282, 45.5801]}}
    destination = {
       'type': 'Feature',
       'properties': {'name': 'Bend, OR'},
       'geometry': {
           'type': 'Point',
           'coordinates': [-121.3153, 44.0582]}}
    response = service.directions([origin, destination], profile='mapbox/driving', geometries='geojson', overview=False, language=params['language'], steps=True)
    return print(response.json())
    
full_route(params={'language': 'ru'})
#response = geocoder.forward("200 queen street")
#print(response.status_code)
#print(response.headers['Content-Type'])
#print(response.geojson()['features'])
#first = response.geojson()['features'][0]
#print(first['place_name'])
