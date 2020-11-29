import socketio
from socketio.asyncio_namespace import AsyncNamespace
from pydantic import BaseModel, ValidationError
from typing import Any
from logging import info
from .app.models import db
from .app.models.user import User


def get_app():
    app = FastAPI()
    db.init_app(app)
    return app

app = get_app()


class PacketModel(BaseModel):
    content: Any
    content_type: str


class GreyRookNameSpace(AsyncNamespace):
    # functions that have on_ prefix recognized as event
    async def on_connect(self, sid, *args, **kwargs):  # on connect event
        info(f"{sid}: Welcome!:)")

    async def on_disconnect(self, sid):  # on disconnect event
        info(f"{sid}: Bye!:(")

    async def on_packet(self, environ, *args, **kwargs):  # on packet event
        user = await User.get_or_404(1)
        try:  # Packet Validation
            packet = PacketModel(**args[0])
        except ValidationError as ex:
            return PacketModel(
                content=str(ex.args), content_type="application/txt"
            ).dict()  # Call-Back
        print('PACKET', packet, user.to_dict())
        await self.process_packet(packet)
        # await self.emit(
        #     "message", packet.dict(), namespace=self.namespace
        # )  # Emit to name-space
        return PacketModel(
            content="Delivered", content_type="application/txt"
        ).dict()  # Call-Back

    async def process_packet(self, packet: PacketModel):
        # some processing on packet
        # store in db
        # stream processing
        # upload chunks
        # etc
        pass


mgr = socketio.AsyncRedisManager(
    "redis://localhost/0"
)  # Message Queue is for working with distributed applications
sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="*"
)
sio.register_namespace(GreyRookNameSpace("/GreyRook"))  # register the namespace
asgi = socketio.ASGIApp(sio)

app.mount("/ws", asgi)  # mount Socket.Io to FastApi with /ws path


class SampleResponseModel(BaseModel):
    message: str


class Sample400ResponseModel(BaseModel):
    detail: str


@app.get("/", description="some description",
         responses={200: {'model': SampleResponseModel},
                    400: {'model': Sample400ResponseModel}})
async def index():
    return {"message": "Welcome to GreyRook!"}


"""
gunicorn app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3001  

horizontal scaling is the solution for high scale architecture
issue:  https://github.com/miguelgrinberg/Flask-SocketIO/issues/267#issuecomment-220525641
Gunicorn is limited to one worker because its load balancer does not provide sticky sessions,
 a requirement of the Socket.IO server. But nothing prevents you from running several 
 gunicorn instances, each with one worker, with nginx as load balancer in front of them.
Side note, be aware that Socket.IO is a stateful protocol. 
To use more than one worker it is required that you also run a message queue, 
which the workers use to communicate and coordinate.
"""
