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
