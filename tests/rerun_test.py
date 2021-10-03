from unittest.mock import ANY, Mock, patch

import pytest

from streamlit_server_state.rerun import make_force_rerun_bound_sessions
from streamlit_server_state.server_state import ServerState


@pytest.fixture
def patch_is_rerunnable():
    with patch(
        "streamlit_server_state.server_state_item.is_rerunnable"
    ) as mock_is_rerunnable:
        mock_is_rerunnable.return_value = True
        yield


@pytest.fixture
def patched_this_session():
    with patch(
        "streamlit_server_state.server_state.get_this_session_info"
    ) as mock_get_this_session_info:
        this_session_info = Mock()
        mock_get_this_session_info.return_value = this_session_info
        this_session = this_session_info.session
        yield this_session


def test_bound_sessions_are_requested_to_rerun(
    patch_is_rerunnable, patched_this_session
):
    server_state = ServerState()
    force_rerun_bound_sessions = make_force_rerun_bound_sessions(server_state)

    server_state["foo"] = 42
    server_state["bar"] = 43

    server_state["foo"]  # This session subscribes the "foo" in the server-state.

    patched_this_session.request_rerun.assert_not_called()

    # No session subscribes the key `bar`.
    force_rerun_bound_sessions("bar")

    patched_this_session.request_rerun.assert_not_called()

    # The session subscribes the key `foo`, so it reruns.
    force_rerun_bound_sessions("foo")

    patched_this_session.request_rerun.assert_has_calls([ANY])
