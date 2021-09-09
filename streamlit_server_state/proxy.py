from typing import Any, Callable, Generic, TypeVar

import wrapt


def is_immutable(val: Any) -> bool:
    return isinstance(val, (int, float, bool, str, bytes, tuple, range))  # TODO


WrappedT = TypeVar("WrappedT")


class ObjectProxy(wrapt.ObjectProxy, Generic[WrappedT]):
    __slots__ = ["__on_set__"]

    def __init__(self, wrapped: WrappedT, on_set: Callable[[], None]):
        setattr(self, "__on_set__", on_set)
        super().__init__(wrapped)

    def __setattr__(self, name, value):
        ret = super().__setattr__(name, value)

        if name.startswith("_self_"):
            # Override wrapt's default behavior.
            # An exception with `_self_` prefix is not necessary for this class.
            object.__delattr__(self, name)
            setattr(self.__wrapped__, name, value)

        if name != "__on_set__":
            on_set = getattr(self, "__on_set__")
            on_set()

        return ret

    def __setitem__(self, key, value):
        ret = super().__setitem__(key, value)
        self.__on_set__()
        return ret

    def __setslice__(self, i, j, value):
        ret = super().__setslice__(i, j, value)
        self.__on_set__()
        return ret

    def __repr__(self):
        return "<{} at 0x{:x} for {} at 0x{:x} {}>".format(
            type(self).__name__,
            id(self),
            type(self.__wrapped__).__name__,
            id(self.__wrapped__),
            repr(self.__wrapped__),
        )
