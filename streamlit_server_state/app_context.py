from typing import Optional, Union

try:
    from streamlit.runtime.scriptrunner.script_run_context import (
        SCRIPT_RUN_CONTEXT_ATTR_NAME,
        ScriptRunContext,
    )
except ModuleNotFoundError:
    # streamlit < 1.12.0
    try:
        from streamlit.scriptrunner.script_run_context import (  # type: ignore
            SCRIPT_RUN_CONTEXT_ATTR_NAME,
            ScriptRunContext,
        )
    except ModuleNotFoundError:
        # streamlit < 1.8
        try:
            from streamlit.script_run_context import (  # type: ignore
                SCRIPT_RUN_CONTEXT_ATTR_NAME,
                ScriptRunContext,
            )
        except ModuleNotFoundError:
            from streamlit.report_thread import (  # type: ignore # isort:skip
                REPORT_CONTEXT_ATTR_NAME as SCRIPT_RUN_CONTEXT_ATTR_NAME,
                ReportContext as ScriptRunContext,
            )

try:
    from streamlit.runtime.app_session import AppSession, AppSessionState
except ModuleNotFoundError:
    # streamlit < 1.12.0
    try:
        from streamlit.app_session import AppSession, AppSessionState  # type: ignore
    except ModuleNotFoundError:
        # streamlit < 1.4
        from streamlit.report_session import (  # type: ignore # isort:skip
            ReportSession as AppSession,
            ReportSessionState as AppSessionState,
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
