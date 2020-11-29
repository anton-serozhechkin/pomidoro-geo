import logging
import asyncio
import uvicorn
from uvicorn.loops.uvloop import uvloop_setup
from starlette.applications import Starlette
from starlette.responses import JSONResponse
import socketio

# Set some basic logging
logging.basicConfig(
    level=2,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

# Create a basic app
sio = socketio.AsyncServer(async_mode='asgi')
star_app = Starlette(debug=True)
app = socketio.ASGIApp(sio, star_app)


@star_app.route('/')
async def homepage(request):
    return JSONResponse({'hello': 'world'})


@sio.on('connect')
async def connect(sid, environ):
    logging.info(f"connect {sid}")


@sio.on('message')
async def message(sid, data):
    logging.info(f"message {data}")
    # await device.set(data)


@sio.on('disconnect')
async def disconnect(sid):
    logging.info(f'disconnect {sid}')


# Set up the event loop
async def start_background_tasks():
    while True:
        logging.info(f"Background tasks that ticks every 10s.")
        await sio.sleep(10.0)


async def start_uvicorn():
    uvicorn.run(app, host='0.0.0.0', port=8000)


async def main(loop):
    bg_task = loop.create_task(start_background_tasks())
    uv_task = loop.create_task(start_uvicorn())
    await asyncio.wait([bg_task, uv_task])

if __name__ == '__main__':
    uvloop_setup()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()