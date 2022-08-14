import logging

import streamlit as st

logger = logging.getLogger(__name__)

_server = None


def is_modern_streamlit() -> bool:
    try:
        major, minor, patch = [int(s) for s in st.__version__.split(".")]
        return major >= 1 and minor >= 12
    except Exception:
        return False


def get_current_server():
    global _server
    if _server:
        return _server

    if is_modern_streamlit():
        logger.debug(
            "The running Streamlit version is gte 1.12.0. "
            "Try to get the server instance"
        )

        import gc

        from streamlit.web.server.server import Server

        servers = [obj for obj in gc.get_objects() if isinstance(obj, Server)]

        if len(servers) == 0:
            raise RuntimeError("Unexpectedly no server exists")
        if len(servers) > 1:
            logger.warning(
                "Unexpectedly multiple server instances exist. Use the first one."
            )

        _server = servers[0]
    else:
        logger.debug(
            "The running Streamlit version is less than 1.12.0. "
            "Call Server.get_current()"
        )
        try:
            from streamlit.web.server.server import Server
        except ModuleNotFoundError:
            # streamlit < 1.12.0
            from streamlit.server.server import Server

        _server = Server.get_current()

    return _server
