from streamlit_server_state.server_state import ServerState
from streamlit_server_state.server_state_lock import ServerStateLock


def test_lock_object_has_the_same_keys():
    server_state = ServerState()
    server_state_lock = ServerStateLock(server_state)

    server_state["foo"] = 42

    assert "foo" in server_state_lock
    assert "bar" not in server_state_lock
