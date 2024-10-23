import streamlit as st

from streamlit_server_state import server_state, server_state_lock

with server_state_lock["rooms"]:
    if "rooms" not in server_state:
        server_state["rooms"] = []

rooms: list[str] = server_state["rooms"]

room = st.sidebar.radio("Select room", rooms)

with st.sidebar.form("New room"):

    def on_create():
        new_room_name = st.session_state.new_room_name
        with server_state_lock["rooms"]:
            server_state["rooms"] = server_state["rooms"] + [new_room_name]

    st.text_input("Room name", key="new_room_name")
    st.form_submit_button("Create a new room", on_click=on_create)

if not room:
    st.stop()

room_key = f"room_{room}"
with server_state_lock[room_key]:
    if room_key not in server_state:
        server_state[room_key] = []

st.header(room)

nickname = st.text_input("Nick name", key=f"nickname_{room}")
if not nickname:
    st.warning("Set your nick name.")
    st.stop()

message_input_key = f"message_input_{room}"


def on_message_input():
    new_message_text = st.session_state[message_input_key]
    if not new_message_text:
        return

    new_message_packet = {
        "nickname": nickname,
        "text": new_message_text,
    }

    with server_state_lock[room_key]:
        server_state[room_key] = server_state[room_key] + [new_message_packet]


st.text_input("Message", key=message_input_key, on_change=on_message_input)

st.subheader("Messages:")
st.write(server_state[room_key])
