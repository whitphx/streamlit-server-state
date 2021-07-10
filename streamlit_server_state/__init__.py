import threading
import weakref
from typing import Generic, TypeVar

from streamlit.report_session import ReportSession
from streamlit.server.server import Server

from .streamlit_session_state import get_this_session_info

StateValueT = TypeVar("StateValueT")


class ServerState(Generic[StateValueT]):
    _value: StateValueT
    _value_lock: threading.Lock

    _bound_sessions: "weakref.WeakSet[ReportSession]"
    _bound_sessions_lock: threading.Lock

    def __init__(self, value: StateValueT) -> None:
        self._value = value
        self._value_lock = threading.Lock()

        self._bound_sessions = weakref.WeakSet()
        self._bound_sessions_lock = threading.Lock()

    def _setup_for_this_session(self) -> None:
        this_session_info = get_this_session_info()
        if this_session_info is None:
            raise RuntimeError(
                "Oh noes. Couldn't get your Streamlit Session object. "
                "Are you doing something fancy with threads?"
            )
        this_session = this_session_info.session
        with self._bound_sessions_lock:
            self._bound_sessions.add(this_session)

    def _rerun_bound_sessions(self) -> None:
        with self._bound_sessions_lock:
            for session in self._bound_sessions:
                session.request_rerun()  # HACK: XD

    def set_value(self, value: StateValueT) -> None:
        with self._value_lock:
            self._value = value

        self._rerun_bound_sessions()

    def get_value(self) -> StateValueT:
        with self._value_lock:
            return self._value


SERVER_STATE_KEY_PREFIX = "_server_state_"


def use_server_state(key: str, initial_value: StateValueT) -> ServerState[StateValueT]:
    server = Server.get_current()

    attr_name = f"{SERVER_STATE_KEY_PREFIX}{key}"

    server_state: ServerState[StateValueT]
    if not hasattr(server, attr_name):
        server_state = ServerState(initial_value)
        setattr(server, attr_name, server_state)
    else:
        server_state = getattr(server, attr_name)

    server_state._setup_for_this_session()

    return server_state
