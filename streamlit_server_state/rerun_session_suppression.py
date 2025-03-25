import logging

from .app_context import get_app_context
from .session_info import NoSessionError, get_this_session

logger = logging.getLogger(__name__)

_SERVER_STATE_SESSION_RERUN_SUPPRESSION_ATTR_NAME_ = "__SERVER_STATE_SUPPRESS_SESSION_RERUN__"


class NoSessionRerunSuppressor:
    def __enter__(self) -> None:
        logger.debug("Start suppressing setting session rerunning")

        # Context managers used in Streamlit apps should be managed
        # being bound to the app context object
        # following the design of the built-in components
        # that are used in `with` statements.
        # Ref: https://github.com/streamlit/streamlit/blob/1.15.0/lib/streamlit/delta_generator.py#L282-L300 # noqa: E501
        this_session = get_this_session()
        ctx = get_app_context(this_session)

        setattr(ctx, _SERVER_STATE_SESSION_RERUN_SUPPRESSION_ATTR_NAME_, True)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        this_session = get_this_session()
        ctx = get_app_context(this_session)

        delattr(ctx, _SERVER_STATE_SESSION_RERUN_SUPPRESSION_ATTR_NAME_)

        logger.debug("Finished suppressing rerunning for setting session")


no_session_rerun = NoSessionRerunSuppressor()


def is_session_rerun_suppressed() -> bool:
    try:
        this_session = get_this_session()
    except NoSessionError:
        return False

    ctx = get_app_context(this_session)

    session_rerun_suppressed = getattr(ctx, _SERVER_STATE_SESSION_RERUN_SUPPRESSION_ATTR_NAME_, False)
    logger.debug("Check the session-rerun-suppression flag: %r", session_rerun_suppressed)

    return session_rerun_suppressed