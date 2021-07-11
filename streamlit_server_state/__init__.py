from streamlit.server.server import Server

from .server_state import ServerState as _ServerState

_SERVER_STATE_KEY_ = "_server_state"

server_state: _ServerState

_server = Server.get_current()
if hasattr(_server, _SERVER_STATE_KEY_):
    server_state = getattr(_server, _SERVER_STATE_KEY_)
else:
    server_state = _ServerState()
    setattr(_server, _SERVER_STATE_KEY_, server_state)


__all__ = ["server_state"]
