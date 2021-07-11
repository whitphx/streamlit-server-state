import streamlit as st

from streamlit_server_state import server_state


def main():
    def on_message_input():
        new_message = st.session_state["message_input"]
        chat_messages = server_state["chat_messages"] + [new_message]
        server_state["chat_messages"] = chat_messages

    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []

    st.text_input("Message", key="message_input", on_change=on_message_input)

    st.write(server_state["chat_messages"])

    for k in server_state:
        st.write(k)
    st.write(st.session_state)


if __name__ == "__main__":
    main()
