import threading
import weakref
from typing import Generic, TypeVar

from streamlit.report_session import ReportSession

StateValueT = TypeVar("StateValueT")


class ValueNotSetError(Exception):
    pass


class ServerStateItem(Generic[StateValueT]):
    _is_set: bool
    _value: StateValueT
    _value_lock: threading.RLock

    _bound_sessions: "weakref.WeakSet[ReportSession]"
    _bound_sessions_lock: threading.Lock

    def __init__(self) -> None:
        self._is_set = False
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

    def set_value(self, value: StateValueT) -> None:
        with self._value_lock:
            changed = not self._is_set or self._value != value
            self._is_set = True
            self._value = value

        if changed:
            self._rerun_bound_sessions()

    def get_value(self) -> StateValueT:
        with self._value_lock:
            if not self._is_set:
                raise ValueNotSetError
            return self._value
