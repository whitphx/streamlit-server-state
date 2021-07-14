import collections.abc
from typing import Any, Dict, Iterator

from .server_state_item import ServerStateItem, ValueNotSetError


class ServerState(collections.abc.MutableMapping):
    _items: Dict[str, ServerStateItem] = {}

    def _ensure_item(self, k: str) -> ServerStateItem:
        if k in self._items:
            item = self._items[k]
        else:
            item = ServerStateItem()
            self._items[k] = item

        return item

    def _ensure_item_in_this_session(self, k: str) -> ServerStateItem:
        item = self._ensure_item(k)

        item.setup_for_this_session()

        return item

    def __setitem__(self, k: str, v: Any) -> None:
        item = self._ensure_item(k)
        item.set_value(v)

    def __getitem__(self, k: str) -> Any:
        item = self._ensure_item_in_this_session(k)

        try:
            return item.get_value()
        except ValueNotSetError:
            raise KeyError(k)

    def __delitem__(self, v: str) -> None:
        return super().__delitem__(v)

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
        return (k for k, _ in ((k, v) for k, v in self._items.items() if v._is_set))

    def __len__(self) -> int:
        return len([i for i in self._items.values() if i._is_set])
