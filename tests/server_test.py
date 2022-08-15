from unittest.mock import patch

import pytest

from streamlit_server_state.server import _is_modern_architecture


@pytest.mark.parametrize(
    "version,expected",
    [
        ("0.90.0", False),
        ("1.0.0", False),
        ("1.11.0", False),
        ("1.11.1", False),
        ("1.12.0", True),
        ("1.12.1", True),
        ("1.13.0", True),
        ("1.11", False),
        ("1.13", True),
        ("foo", False),
    ],
)
def test__is_modern_architecture(version, expected):
    import streamlit

    with patch.object(streamlit, "__version__", version):
        assert _is_modern_architecture() == expected
