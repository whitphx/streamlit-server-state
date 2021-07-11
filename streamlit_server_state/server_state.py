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

    def __contains__(self, k: object) -> bool:
        if not isinstance(k, str):
            return False

        item = self._ensure_item_in_this_session(k)

        return item._is_set

    def __iter__(self) -> Iterator[str]:
        return self._items.__iter__()

    def __len__(self) -> int:
        return self._items.__len__()
