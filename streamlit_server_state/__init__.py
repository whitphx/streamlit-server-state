import logging

from streamlit.server.server import Server

from .server_state import ServerState as _ServerState
from .server_state_lock import ServerStateLock as _ServerStateLock

logger = logging.getLogger(__name__)

_SERVER_STATE_KEY_ = "_server_state"
_SERVER_STATE_LOCK_KEY_ = "_server_state_lock"

try:
    _server = Server.get_current()
except RuntimeError as e:
    # NOTE: An error can be raised from the line above
    # when the app script uses multiprocessing and `Server.get_current()` is executed
    # in a spawned process because the server object is not initialized in that process.
    # It's unavoidable so ignored with this try-except, then developers have to
    # make sure not to use server-state in the spawned processes.
    logger.warning(
        "Failed to get the server object (%s). "
        "The server-state is not initialized in this process.",
        e,
    )
    _server = None

server_state: _ServerState
if _server:
    if hasattr(_server, _SERVER_STATE_KEY_):
        server_state = getattr(_server, _SERVER_STATE_KEY_)
    else:
        server_state = _ServerState()
        setattr(_server, _SERVER_STATE_KEY_, server_state)

server_state_lock: _ServerStateLock
if _server:
    if hasattr(_server, _SERVER_STATE_LOCK_KEY_):
        server_state_lock = getattr(_server, _SERVER_STATE_LOCK_KEY_)
    else:
        server_state_lock = _ServerStateLock(server_state=server_state)
        setattr(_server, _SERVER_STATE_LOCK_KEY_, server_state_lock)


__all__ = ["server_state", "server_state_lock"]
