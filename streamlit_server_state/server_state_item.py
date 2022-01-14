import threading
import weakref
from typing import Generic, Optional, TypeVar, Union

try:
    from streamlit.app_session import AppSession, AppSessionState
    from streamlit.script_run_context import (
        SCRIPT_RUN_CONTEXT_ATTR_NAME,
        ScriptRunContext,
    )
except ModuleNotFoundError:
    # streamlit < 1.4
    from streamlit.report_session import (  # type: ignore
        ReportSession as AppSession,
        ReportSessionState as AppSessionState,
    )
    from streamlit.report_thread import (  # type: ignore
        REPORT_CONTEXT_ATTR_NAME as SCRIPT_RUN_CONTEXT_ATTR_NAME,
        ReportContext as ScriptRunContext,
    )

from .hash import Hash, calc_hash


def get_app_context(session: AppSession) -> Union[ScriptRunContext, None]:
    # HACK: Get ScriptRunContext from AppSession via ScriptThread
    scriptrunner = session._scriptrunner
    if not scriptrunner:
        return None
    if not scriptrunner._script_thread:
        return None

    script_thread = scriptrunner._script_thread
    ctx: Optional[ScriptRunContext] = getattr(
        script_thread, SCRIPT_RUN_CONTEXT_ATTR_NAME
    )
    return ctx


def is_rerunnable(session: AppSession) -> bool:
    ctx = get_app_context(session)
    if not hasattr(ctx, "_has_script_started"):
        # `ctx._has_script_started` has been introduced since 0.84.2
        # Ref: https://github.com/streamlit/streamlit/compare/0.84.1...0.84.2
        # Ref: https://github.com/streamlit/streamlit/pull/3550
        return True

    if ctx and not ctx._has_script_started:
        # This case is mainly when called from inside callbacks.
        # Callbacks are called after ctx is set and
        # before ctx._has_script_started is set as True.
        # Rel: https://github.com/whitphx/streamlit-server-state/issues/37
        return False
    if session._state == AppSessionState.SHUTDOWN_REQUESTED:
        # This case has no meaning on rerunning and causes an error
        # "Discarding ScriptRequest.RERUN request after shutdown".
        return False
    return True


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

    def _rerun_bound_sessions(self) -> None:
        with self._bound_sessions_lock:
            for session in self._bound_sessions:
                self._rerun_session_if_possible(session)

    def _rerun_session_if_possible(self, session: AppSession) -> None:
        if is_rerunnable(session):
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
