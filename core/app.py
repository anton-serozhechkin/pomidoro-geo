import asyncio
import uvicorn
import socketio
from logging import info
from mapbox_client import 
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins="*", 
                           kwargs={'logger': True, 'ping_interval': 2})

app = socketio.ASGIApp(sio, static_files={
    '/': 'app.html',
})

class PomGeoNameSpace(socketio.AsyncNamespace):
    
    # must call background
    async def check_session(self, sid, params):
        # check user settings
        info("User with sid {sid} try to join.")
        session = sio.get_session(sid)
        if session:
            info("User with sid {} already has a session.".format(sid))
            await self.join(sid, session, params)
            return await session
        else:
            info("Create new session for user with sid {}.".format(sid))
            async with sio.session(sid) as session:
                session[sid] = {}
                session[sid]['username'] = params['info']['username']
                session[sid]['orderId'] = params['info']['orderId']
                session[sid]['profile'] = params['info']['profile']
                session[sid]['lang'] = params['info']['language']
                await self.join(sid, session, params)
                return await session


    async def join(self, sid, session, params):
        sio.enter_room(sid)
        info("User with username {} entered to room: {}".format(session[sid]['username'], sid))
    
    
    async def leave_room(self, sid, session):
        sio.leave_room(sid)
        info("User with username {} leave the room: {}".format(session[sid]['username'], sid))
    
    
    async def close(self, sid, session):
        await sio.close_room(sid)
        info("Room {} for user {} was closed.".format(sid, session[sid]['username']))
    

    async def send_room_message(self, sid, params):
        session = await self.check_session(sid, params)
        asyncio.sleep(1)
        message = await controller_params(sid, session, params)
        asyncio.sleep(4)
        await sio.emit('response', {'data': message}, room=sid)
    
    
    def disconnect_request(self, sid, session):
        await sio.disconnect(sid)
        info("User with username {}, room {} was disconnected.".format(session[sid]['username'], sid))
    

    """
    async def check_token(id_user: str):

    @sio.on('find_route')
    async def find_route(sid, **kwargs):
        call_controller = await controller_params(sid, **kwargs)

    async def is_couirier_exist(self, id: str):
        if id:
            responce = await check_token(id)
            return responce
        else:
            return False
    """

#mgr = socketio.AsyncRedisManager(
#    "redis://localhost/0"
#)  # Message Queue is for working with distributed applications

sio.register_namespace(PomGeoNameSpace("/gs/route/"))  # register the namespace


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5002)
