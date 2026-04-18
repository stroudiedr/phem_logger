import streamlit as st


def render():
    st.title("Apple Watch")
    st.subheader("Coming soon")
    st.write(
        "PHEM Logger for Apple Watch is currently in development. "
        "Register your interest below and we'll let you know when it's available."
    )
    st.link_button(
        "Register interest",
        "mailto:phemlogger@hotmail.com?subject=PHEM Logger — Apple Watch interest",
    )
