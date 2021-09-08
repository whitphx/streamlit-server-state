import threading
import weakref
from typing import Generic, Optional, TypeVar

from streamlit.report_session import ReportSession

from .hash import Hash, calc_hash

StateValueT = TypeVar("StateValueT")


class ValueNotSetError(Exception):
    pass


class ServerStateItem(Generic[StateValueT]):
    _is_set: bool
    _value: StateValueT
    _value_hash: Optional[Hash]
    _value_lock: threading.RLock

    _bound_sessions: "weakref.WeakSet[ReportSession]"
    _bound_sessions_lock: threading.Lock

    def __init__(self) -> None:
        self._is_set = False
        self._value_hash = None
        self._value_lock = threading.RLock()

        self._bound_sessions = weakref.WeakSet()
        self._bound_sessions_lock = threading.Lock()

    def bind_session(self, session: ReportSession) -> None:
        with self._bound_sessions_lock:
            if session not in self._bound_sessions:
                self._bound_sessions.add(session)

    def _rerun_bound_sessions(self) -> None:
        with self._bound_sessions_lock:
            for session in self._bound_sessions:
                session.request_rerun(client_state=None)  # HACK: XD

    def _on_set(self):
        new_value_hash = calc_hash(self._value)
        if self._value_hash is None or self._value_hash != new_value_hash:
            self._rerun_bound_sessions()

        self._value_hash = new_value_hash

    def set_value(self, value: StateValueT) -> None:
        with self._value_lock:
            self._is_set = True
            self._value = value

        self._on_set()

    def get_value(self) -> StateValueT:
        with self._value_lock:
            if not self._is_set:
                raise ValueNotSetError
            return self._value
