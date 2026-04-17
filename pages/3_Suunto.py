import streamlit as st
from utils.analytics import inject_analytics

st.set_page_config(
    page_title="Suunto — PHEM Logger",
    page_icon="assets/icon.png",
    layout="wide",
)

inject_analytics()

st.title("Suunto watches")
st.subheader("Coming soon")
st.write(
    "PHEM Logger for Suunto watches is currently in development. "
    "Register your interest below and we'll let you know when it's available."
)
st.link_button(
    "Register interest",
    "mailto:phemlogger@hotmail.com?subject=PHEM Logger — Suunto interest",
)
