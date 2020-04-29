import struct
import os

def encode_msg_size(size: int) -> bytes:
    return struct.pack("<I", size)

def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack("<I", size_bytes)[0]

def create_msg(content: bytes) -> bytes:
    #content=str(content).encode("utf8")
    size = len(content)
    return encode_msg_size(size) + content
def get_message(fifo: int) -> bytes:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size)
    return msg_content
