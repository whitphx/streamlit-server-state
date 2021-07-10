import streamlit as st

from streamlit_server_state import use_server_state


def main():
    def on_message_input():
        new_message = st.session_state["message_input"]
        chat_messages = chat_messages_state.get_value() + [new_message]
        chat_messages_state.set_value(chat_messages)

    chat_messages_state = use_server_state("chat_messages", [])

    st.text_input("Message", key="message_input", on_change=on_message_input)

    st.write(chat_messages_state.get_value())


if __name__ == "__main__":
    main()
