from typing import Any, Optional, Tuple, Union

ReprHash = Union[str, int]
ObjDictHash = Optional[str]
Hash = Tuple[ReprHash, ObjDictHash]


def calc_hash(val: Any) -> Hash:
    dict_hash: ObjDictHash = None
    if hasattr(val, "__dict__") and isinstance(val.__dict__, dict):
        dict_hash = repr(val.__dict__)

    repr_hash: ReprHash
    try:
        repr_hash = repr(val)
    except Exception:
        repr_hash = id(val)

    return (repr_hash, dict_hash)
