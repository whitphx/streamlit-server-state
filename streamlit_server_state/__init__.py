from streamlit.server.server import Server

from .server_state import ServerState as _ServerState
from .server_state_lock import ServerStateLock as _ServerStateLock

_SERVER_STATE_KEY_ = "_server_state"
_SERVER_STATE_LOCK_KEY_ = "_server_state_lock"

_server = Server.get_current()

server_state: _ServerState
if hasattr(_server, _SERVER_STATE_KEY_):
    server_state = getattr(_server, _SERVER_STATE_KEY_)
else:
    server_state = _ServerState()
    setattr(_server, _SERVER_STATE_KEY_, server_state)

server_state_lock: _ServerStateLock
if hasattr(_server, _SERVER_STATE_LOCK_KEY_):
    server_state_lock = getattr(_server, _SERVER_STATE_LOCK_KEY_)
else:
    server_state_lock = _ServerStateLock(server_state=server_state)
    setattr(_server, _SERVER_STATE_LOCK_KEY_, server_state_lock)


__all__ = ["server_state", "server_state_lock"]
