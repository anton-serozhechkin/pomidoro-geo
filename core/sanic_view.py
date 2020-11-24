import asyncio

from sanic import Sanic
from sanic.response import json

import socketio

sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)


@app.route('/gs/route', methods=['GET'])
async def index(request):
    response = controller_customer_adress(request.query_string)
    #return json(response)


async def controller_customer_adress(request):
    if request['customer_addr']:
        
    else:


