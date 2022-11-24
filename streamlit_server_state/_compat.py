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
    from streamlit.runtime.scriptrunner import get_script_run_ctx
except ModuleNotFoundError:
    # streamlit < 1.12.0
    try:
        from streamlit.scriptrunner import get_script_run_ctx  # type: ignore
    except ModuleNotFoundError:
        # streamlit < 1.8
        try:
            from streamlit.script_run_context import get_script_run_ctx  # type: ignore
        except ModuleNotFoundError:
            # streamlit < 1.4
            from streamlit.report_thread import (  # type: ignore # isort:skip
                get_report_ctx as get_script_run_ctx,
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

try:
    from streamlit.runtime.runtime import SessionInfo
except ModuleNotFoundError:
    # streamlit < 1.12.1
    try:
        from streamlit.web.server.server import SessionInfo  # type: ignore
    except ModuleNotFoundError:
        # streamlit < 1.12.0
        from streamlit.server.server import SessionInfo  # type: ignore


__all__ = [
    "SCRIPT_RUN_CONTEXT_ATTR_NAME",
    "ScriptRunContext",
    "get_script_run_ctx",
    "AppSession",
    "AppSessionState",
    "SessionInfo",
]
