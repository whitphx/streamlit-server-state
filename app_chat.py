import streamlit as st
from streamlit_server_state import use_server_state


def main():
    chat_messages_state = use_server_state("chat_messages", []);

    message = st.text_input("Message")
    send = st.button("Send")
    if message and send:
        chat_messages = chat_messages_state.get_value() + [message]
        chat_messages_state.set_value(chat_messages)

    st.write(chat_messages_state.get_value())


if __name__ == "__main__":
    main()
