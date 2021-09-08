from typing import Any


def hash(val: Any) -> str:
    try:
        r = repr(val)
    except Exception:
        r = id(val)
    return r
