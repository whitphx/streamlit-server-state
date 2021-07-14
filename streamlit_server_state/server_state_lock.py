import collections.abc
import threading
from typing import Iterator

from streamlit_server_state.server_state import ServerState


class ServerStateLock(collections.abc.Mapping):
    _server_state: ServerState

    def __init__(self, server_state: ServerState) -> None:
        self._server_state = server_state

    def __getitem__(self, k: str) -> threading.RLock:
        item = self._server_state._ensure_item(k)

        return item._value_lock

    def __getattr__(self, k: str) -> threading.RLock:
        return self.__getitem__(k)

    def __contains__(self, k: object) -> bool:
        return k in self._server_state._items

    def __iter__(self) -> Iterator[str]:
        return (k for k in self._server_state._items.keys())

    def __len__(self) -> int:
        return self._server_state._items.__len__()
