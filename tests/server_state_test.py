import pytest

from streamlit_server_state.server_state import ServerState


def test_forbidden_key():
    state = ServerState()

    with pytest.raises(KeyError):
        state["__items__"] = 42

    with pytest.raises(KeyError):
        state["__items__"]

    with pytest.raises(KeyError):
        del state["__items__"]
