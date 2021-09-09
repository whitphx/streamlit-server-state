from typing import Any, Union

Hash = Union[str, int]


def calc_hash(val: Any) -> Hash:
    try:
        return repr(val)
    except Exception:
        return id(val)
