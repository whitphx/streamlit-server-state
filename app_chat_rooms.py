import streamlit as st

from streamlit_server_state import server_state


def main():
    if "rooms" not in server_state:
        server_state["rooms"] = []

    rooms = server_state["rooms"]

    room = st.sidebar.radio("Select room", rooms)

    with st.sidebar.form("New room"):

        def on_create():
            new_room_name = st.session_state.new_room_name
            rooms.append(new_room_name)
            server_state["rooms"] = rooms

        st.text_input("Room name", key="new_room_name")
        st.form_submit_button("Create", on_click=on_create)

    room_key = f"room_{room}"
    if room_key not in server_state:
        server_state[room_key] = []

    st.header(room)

    nickname = st.text_input("Nick name", key=f"nickname_{room}")
    if not nickname:
        st.warning("Set your nick name.")
        return

    message_input_key = f"message_input_{room}"

    def on_message_input():
        new_message_text = st.session_state[message_input_key]
        if not new_message_text:
            return

        new_message_packet = {
            "nickname": nickname,
            "text": new_message_text,
        }
        server_state[room_key] = server_state[room_key] + [new_message_packet]

    st.text_input("Message", key=message_input_key, on_change=on_message_input)

    st.subheader("Messages:")
    st.write(server_state[room_key])


if __name__ == "__main__":
    main()
