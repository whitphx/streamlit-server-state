import collections.abc
from typing import Any, Dict, Iterator

from .server_state_item import ServerStateItem, ValueNotSetError
from .session_info import get_this_session_info


class ServerState(collections.abc.MutableMapping):
    # NOTE: This is initialized only once across all the instances of this class.
    # It is not a problem because the instance is singleton.
    # However, it can be in tests where multiple instances are created.
    # So, `self.__items__.clear()` is called inside `__init__` just for tests.
    __items__: Dict[str, ServerStateItem] = {}

    def __init__(self) -> None:
        super().__init__()
        self.__items__.clear()

    def _ensure_item(self, k: str) -> ServerStateItem:
        if k in self.__items__:
            item = self.__items__[k]
        else:
            item = ServerStateItem()
            self.__items__[k] = item

        return item

    def _ensure_item_in_this_session(self, k: str) -> ServerStateItem:
        item = self._ensure_item(k)

        this_session_info = get_this_session_info()
        if this_session_info is None:
            raise RuntimeError(
                "Oh noes. Couldn't get your Streamlit Session object. "
                "Are you doing something fancy with threads?"
            )
        this_session = this_session_info.session
        item.bind_session(this_session)

        return item

    def __setitem__(self, k: str, v: Any) -> None:
        if k == "__items__":
            raise KeyError(f'Attr name "{k}" is forbidden')

        item = self._ensure_item(k)
        item.set_value(v)

    def __getitem__(self, k: str) -> Any:
        if k == "__items__":
            raise KeyError(f'Attr name "{k}" is forbidden')

        item = self._ensure_item_in_this_session(k)

        try:
            return item.get_value()
        except ValueNotSetError:
            raise KeyError(k)

    def __delitem__(self, k: str) -> None:
        if k == "__items__":
            raise KeyError(f'Attr name "{k}" is forbidden')

        del self.__items__[k]

    def __setattr__(self, name: str, value: Any) -> None:
        return self.__setitem__(name, value)

    def __getattr__(self, k: str) -> Any:
        return self.__getitem__(k)

    def __delattr__(self, k) -> None:
        return self.__delitem__(k)

    def __contains__(self, k: object) -> bool:
        if not isinstance(k, str):
            return False

        item = self._ensure_item_in_this_session(k)

        return item._is_set

    def __iter__(self) -> Iterator[str]:
        return (k for k, _ in ((k, v) for k, v in self.__items__.items() if v._is_set))

    def __len__(self) -> int:
        return len([i for i in self.__items__.values() if i._is_set])
