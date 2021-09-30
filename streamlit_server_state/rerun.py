from .server_state import ServerState


def make_force_rerun_bound_sessions(server_state: ServerState):
    def force_rerun_bound_sessions(key: str):
        server_state.__items__[key]._rerun_bound_sessions()

    return force_rerun_bound_sessions
