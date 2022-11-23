# streamlit-server-state
A "server-wide" state shared across the sessions.

[![Tests](https://github.com/whitphx/streamlit-server-state/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/whitphx/streamlit-server-state/actions/workflows/tests.yml?query=branch%3Amain)

[![PyPI](https://img.shields.io/pypi/v/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)
[![PyPI - License](https://img.shields.io/pypi/l/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/streamlit-server-state)](https://pypi.org/project/streamlit-server-state/)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D2ERWFG)

<a href="https://www.buymeacoffee.com/whitphx" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="180" height="50" ></a>

[![GitHub Sponsors](https://img.shields.io/github/sponsors/whitphx?label=Sponsor%20me%20on%20GitHub%20Sponsors&style=social)](https://github.com/sponsors/whitphx)

```python
import streamlit as st

from streamlit_server_state import server_state, server_state_lock

st.title("Global Counter Example")

with server_state_lock["count"]:  # Lock the "count" state for thread-safety
    if "count" not in server_state:
        server_state.count = 0

increment = st.button("Increment")
if increment:
    with server_state_lock.count:
        server_state.count += 1

decrement = st.button("Decrement")
if decrement:
    with server_state_lock.count:
        server_state.count -= 1

st.write("Count = ", server_state.count)

```

As above, the API is similar to [the built-in SessionState](https://blog.streamlit.io/session-state-for-streamlit/), except one major difference - a "lock" object.
The lock object is introduced for thread-safety because the server-state is accessed from multiple sessions, i.e. threads.

## Auto-rerun
When you assign a value to a server-state item, `server-state[key]`,
server-state automatically triggers re-running of all other sessions in which that server-state item is referred to so that all the references to the server-state return the latest value and all the sessions are kept up-to-date.

For example, with this mechanism, the [sample chat app (`app_chat.py`)](./app_chat.py) keeps showing the latest message list for all users.

### Suppressing auto-rerun

When this auto-rerun mechanism is not good for your use case, you can suppress auto-reruns upon the value assignments by using `no_rerun` context as below.
```python
from streamlit_server_state import server_state, no_rerun


with no_rerun:
    server_state["foo"] = 42  # This does not trigger re-running of other sessions
```

### Manually trigger re-running
Upon each value assignment, server-state checks whether the value has been changed and skips re-running if it has not for efficiency.
This works well in most cases, but it does not for example when the value is a complex mutable object and its field is mutated, while such usages are not recommended.

As exceptions, in such cases where the auto-rerun mechanism does not work well, you can manually trigger re-running by using `force_rerun_bound_sessions(key)`.

```python
if "foo" not in server_state:
    server_state["foo"] = SomeComplexObject()

server_state["foo"].field = 42  # If this assignment does not trigger re-running,

force_rerun_bound_sessions("foo")  # You can do this.
```

Background: https://discuss.streamlit.io/t/new-library-streamlit-server-state-a-new-way-to-share-states-across-sessions-on-the-server/14981/10

## Examples
* [`app_global_count`](./app_global_count.py): A sample app like [the official counter example for SessionState](https://blog.streamlit.io/session-state-for-streamlit/) which uses `streamlit-server-state` instead and the counter is shared among all the sessions on the server. This is a nice small example to see the usage and behavior of `streamlit-server-state`. Try to open the app in multiple browser tabs and see the counter is shared among them.
* [`app_global_slider`](./app_global_slider.py): A slider widget (`st.slider`) whose value is shared among all sessions.
* [`app_chat.py`](./app_chat.py): A simple chat app using `streamlit-server-state`.
* [`app_chat_rooms.py`](./app_chat_rooms.py): A simple chat app with room separation.
  [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/whitphx/streamlit-server-state/main/app_chat_rooms.py)

## Resources
* [New library: streamlit-server-state, a new way to share states among the sessions on the server (Streamlit Community)](https://discuss.streamlit.io/t/new-library-streamlit-server-state-a-new-way-to-share-states-among-the-sessions-on-the-server/14981)
