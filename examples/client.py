from typing import Any

import socketio
from pydantic import BaseModel


class PacketModel(BaseModel):
    content: Any
    content_type: str

sio = socketio.Client()
sio.connect(
    "http://localhost:8000/ws", namespaces="/GreyRook", socketio_path="/ws/socket.io"
)


@sio.on("message", namespace="/GreyRook")
def new_packet(packet):
    print("\nMessage: ", packet)


def call_back(data):
    print("\ncall-back", data)


while True:
    msg = input("Message: ")
    sio.emit(
        "packet",
        PacketModel(content={"message": msg}, content_type="application/json").dict(),
        namespace="/GreyRook",
        callback=call_back,
    )
