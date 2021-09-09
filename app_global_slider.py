import streamlit as st

from streamlit_server_state import server_state, server_state_lock

st.title("Globally Shared Slider Example")
st.markdown(
    "Open this app in multiple tabs/windows and "
    "see the slider value is shared and synchronized across the sessions."
)

with server_state_lock["slider_value"]:
    if "slider_value" not in server_state:
        server_state.slider_value = 50  # Initial value
    server_state.slider_value = st.slider(
        "Shared value", min_value=0, max_value=100, value=server_state.slider_value
    )
