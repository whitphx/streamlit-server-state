try:
    import streamlit.ReportThread as ReportThread
    from streamlit.server.Server import Server, ReportSession
except Exception:
    # Streamlit >= 0.65.0
    import streamlit.report_thread as ReportThread
    from streamlit.server.server import Server, ReportSession

# Ref: https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92


def get_this_session() -> ReportSession:
    ctx = ReportThread.get_report_ctx()

    this_session = None

    current_server = Server.get_current()
    if hasattr(current_server, "_session_infos"):
        # Streamlit < 0.56
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
        s = session_info.session
        if (
            # Streamlit < 0.54.0
            (hasattr(s, "_main_dg") and s._main_dg == ctx.main_dg)
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, "_main_dg") and s.enqueue == ctx.enqueue)
            or
            # Streamlit >= 0.65.2
            (
                not hasattr(s, "_main_dg")
                and s._uploaded_file_mgr == ctx.uploaded_file_mgr
            )
        ):
            this_session = s

    if this_session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object. "
            "Are you doing something fancy with threads?"
        )

    return this_session
