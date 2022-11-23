from .rerun_suppression import is_rerun_suppressed
from .server_state import ServerState


class RerunSuppressedError(Exception):
    pass


def make_force_rerun_bound_sessions(server_state: ServerState):
    def force_rerun_bound_sessions(key: str):
        if is_rerun_suppressed():
            raise RerunSuppressedError(
                "force_rerun_bound_sessions() cannot be used in the no_rerun context."
            )

        server_state.__items__[key]._rerun_bound_sessions()

    return force_rerun_bound_sessions
