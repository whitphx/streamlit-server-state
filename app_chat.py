import streamlit as st

from streamlit_server_state import server_state, server_state_lock

nickname = st.text_input("Nick name", key="nickname")
if not nickname:
    st.stop()


def on_message_input():
    new_message_text = st.session_state["message_input"]
    if not new_message_text:
        return

    new_message_packet = {
        "nickname": nickname,
        "text": new_message_text,
    }
    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]


with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []

st.text_input("Message", key="message_input", on_change=on_message_input)

st.write(server_state["chat_messages"])
