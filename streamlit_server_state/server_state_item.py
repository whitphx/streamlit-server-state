import threading
import weakref
from typing import Generic, Optional, TypeVar

from streamlit.proto.ClientState_pb2 import ClientState

from .app_context import AppSession, is_rerunnable
from .hash import Hash, calc_hash
from .rerun_suppression import is_rerun_suppressed
from .rerun_session_suppression import is_session_rerun_suppressed

StateValueT = TypeVar("StateValueT")


class ValueNotSetError(Exception):
    pass


class ServerStateItem(Generic[StateValueT]):
    _is_set: bool
    _value: StateValueT
    _value_hash: Optional[Hash]
    _value_lock: threading.RLock

    _bound_sessions: "weakref.WeakSet[AppSession]"
    _bound_sessions_lock: threading.Lock

    def __init__(self) -> None:
        self._is_set = False
        self._value_hash = None
        self._value_lock = threading.RLock()

        self._bound_sessions = weakref.WeakSet()
        self._bound_sessions_lock = threading.Lock()

    def bind_session(self, session: AppSession) -> None:
        with self._bound_sessions_lock:
            if session not in self._bound_sessions:
                self._bound_sessions.add(session)

    def _rerun_bound_sessions(self, setting_session = None, refresh_fragments = None) -> None:
        with self._bound_sessions_lock:
            for session in self._bound_sessions:
                if session is setting_session and is_session_rerun_suppressed():
                    continue
                else:
                    if refresh_fragments and session.id in refresh_fragments:
                        session_fragment_id = refresh_fragments[session.id]
                    else:
                        session_fragment_id = None
                    self._rerun_session_if_possible(session, fragment_id=session_fragment_id)

    def _rerun_session_if_possible(self, session: AppSession, fragment_id: str = None) -> None:
        if is_rerunnable(session):
            if fragment_id is None:
                session.request_rerun(client_state=None)
            else:
                session.request_rerun(client_state=ClientState(fragment_id=fragment_id, is_auto_rerun=False))

    def _on_set(self, setting_session: Optional[AppSession], refresh_fragments = None) -> None:
        new_value_hash = calc_hash(self._value)
        if not is_rerun_suppressed():
            if self._value_hash is None or self._value_hash != new_value_hash:
                self._rerun_bound_sessions(setting_session, refresh_fragments)

        self._value_hash = new_value_hash

    def set_value(self, value: StateValueT, setting_session = None, refresh_fragments = None) -> None:
        with self._value_lock:
            self._is_set = True
            self._value = value

        self._on_set(setting_session, refresh_fragments)

    def get_value(self) -> StateValueT:
        with self._value_lock:
            if not self._is_set:
                raise ValueNotSetError
            return self._value