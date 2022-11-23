from typing import Optional

from ._compat import AppSession, SessionInfo, get_script_run_ctx
from .server import VER_GTE_1_12_1, get_current_server

# Ref: https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92


def get_session_id() -> str:
    ctx = get_script_run_ctx()
    if ctx is None:
        raise Exception("Failed to get the thread context")

    return ctx.session_id


def get_this_session_info() -> Optional[SessionInfo]:
    current_server = get_current_server()

    # The original implementation of SessionState (https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92) has a problem    # noqa: E501
    # as referred to in https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92#gistcomment-3484515,                         # noqa: E501
    # then fixed here.
    # This code only works with streamlit>=0.65, https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92#gistcomment-3418729 # noqa: E501
    session_id = get_session_id()

    if VER_GTE_1_12_1:
        session_info = current_server._runtime._get_session_info(session_id)
    else:
        session_info = current_server._get_session_info(session_id)

    return session_info


def get_this_session() -> AppSession:
    this_session_info = get_this_session_info()
    if this_session_info is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object. "
            "Are you doing something fancy with threads?"
        )
    return this_session_info.session
