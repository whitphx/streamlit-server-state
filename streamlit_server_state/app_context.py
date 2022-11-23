from typing import Optional, Union

from ._compat import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
    AppSession,
    AppSessionState,
    ScriptRunContext,
)


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
