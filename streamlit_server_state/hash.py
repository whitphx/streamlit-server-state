from typing import Any, Union

Hash = Union[str, int]


def hash(val: Any) -> Hash:
    r: Hash
    try:
        r = repr(val)
    except Exception:
        r = id(val)
    return r
