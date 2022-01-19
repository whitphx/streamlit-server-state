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


def test_delitem():
    state = ServerState()

    with pytest.raises(KeyError):
        del state["foo"]

    state["foo"] = 42
    del state["foo"]
    with pytest.raises(KeyError):
        del state["foo"]
