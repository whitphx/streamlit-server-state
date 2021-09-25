from unittest.mock import ANY, Mock

from streamlit_server_state.server_state_item import ServerStateItem


def test_bound_sessions_are_requested_to_rerun_when_value_is_set_or_update():
    session = Mock()

    item = ServerStateItem()
    item.bind_session(session)

    session.request_rerun.assert_not_called()

    item.set_value(42)
    session.request_rerun.assert_has_calls([ANY])

    item.set_value(100)
    session.request_rerun.assert_has_calls([ANY, ANY])


def test_all_bound_sessions_are_requested_to_rerun():
    session1 = Mock()
    session2 = Mock()

    item = ServerStateItem()
    item.bind_session(session1)
    item.bind_session(session2)

    session1.request_rerun.assert_not_called()
    session2.request_rerun.assert_not_called()

    item.set_value(42)
    session1.request_rerun.assert_has_calls([ANY])
    session2.request_rerun.assert_has_calls([ANY])

    item.set_value(100)
    session1.request_rerun.assert_has_calls([ANY, ANY])
    session2.request_rerun.assert_has_calls([ANY, ANY])


def test_bound_sessions_are_not_duplicate():
    session = Mock()

    item = ServerStateItem()
    item.bind_session(session)
    item.bind_session(session)  # Bind the sessoin twice

    session.request_rerun.assert_not_called()

    item.set_value(42)
    session.request_rerun.assert_called_once()


def test_bound_sessions_are_not_requested_to_rerun_when_the_set_value_is_not_changed():
    session = Mock()

    item = ServerStateItem()
    item.bind_session(session)

    session.request_rerun.assert_not_called()

    item.set_value(42)
    session.request_rerun.assert_called_once()

    item.set_value(42)
    session.request_rerun.assert_called_once()  # No new calls


def test_bound_sessions_are_requested_to_rerun_when_a_same_but_mutated_object_is_set():
    session = Mock()

    item = ServerStateItem()
    item.bind_session(session)

    session.request_rerun.assert_not_called()

    item.set_value({})
    session.request_rerun.assert_has_calls([ANY])

    value = item.get_value()
    value["foo"] = 42

    item.set_value(value)
    session.request_rerun.assert_has_calls([ANY, ANY])


def test_object_mutation_triggers_rerun():
    session = Mock()

    item = ServerStateItem()
    item.bind_session(session)

    session.request_rerun.assert_not_called()

    item.set_value({})
    session.request_rerun.assert_has_calls([ANY])

    item.get_value()["foo"] = 42
    session.request_rerun.assert_has_calls([ANY, ANY])
