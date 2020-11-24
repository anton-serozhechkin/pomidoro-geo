import socketio
import eventlet

# create a Socket.IO server
sio = socketio.AsyncServer(async_mode='sanic')
app = Sanic()
sio.attach(app)
# wrap with ASGI application
app = socketio.ASGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
async def my_event(sid, data):
    print('message ', data)


if __name__ == '__main__':
    app.run()