import streamlit as st
from utils.analytics import inject_analytics
from utils.github import get_download_stats, get_latest_version
from utils.carousel import screenshot_carousel

st.set_page_config(
    page_title="PHEM Logger",
    page_icon="assets/icon.png",
    layout="wide",
)

inject_analytics()

# Banner
if os.path.exists("assets/banner.png"):
    st.image("assets/banner.png", use_column_width=True)

# Header
col_icon, col_title = st.columns([1, 8])
with col_icon:
    if os.path.exists("assets/icon.png"):
        st.image("assets/icon.png", width=80)
with col_title:
    st.title("PHEM Logger")
    st.subheader("Precision timestamping for prehospital clinicians")

# About
st.header("About")
st.write(
    "PHEM Logger is a Garmin Connect IQ application designed for prehospital emergency "
    "clinicians. It runs directly on your Garmin watch, allowing you to record precise "
    "event timestamps during a job — hands-free and glove-friendly. Designed for use by "
    "HEMS crews, BASICS doctors, and air ambulance teams."
)
st.write(
    "The app is distributed via sideloading and is intended for simulation and training use only."
)

# Download stats strip
counts = get_download_stats()
version = get_latest_version()

m1, m2, m3 = st.columns(3)
m1.metric("Total downloads", counts.get("total", "—"))
m2.metric("Current version", version)
m3.metric("Supported devices", "Garmin Fenix 6 & 7")

# Screenshots
st.header("Screenshots")
screenshot_carousel(
    [
        ("assets/screenshots/fenix_cover.png", "PHEM Logger"),
        ("assets/screenshots/fenix_01 - Front.png", "Watch face"),
        ("assets/screenshots/fenix_02 - Start.png", "Start screen"),
        ("assets/screenshots/fenix_05 - Menu.png", "Menu"),
        ("assets/screenshots/fenix_06 - Job timings1.png", "Job timings"),
        ("assets/screenshots/fenix_07 - job timings - en route.png", "Job timings — en route"),
        ("assets/screenshots/fenix_08 - At scene timer.png", "At scene timer"),
        ("assets/screenshots/fenix_09 - Drugs menu.png", "Drugs menu"),
        ("assets/screenshots/fenix_11 - Interventions menu.png", "Interventions menu"),
        ("assets/screenshots/fenix_12 - Cardiac arrest menu.png", "Cardiac arrest menu"),
        ("assets/screenshots/fenix_13 - Handover summary.png", "Handover summary"),
        ("assets/screenshots/fenix_15 - jobs list.png", "Jobs list"),
    ],
    key="home",
)

# Features
st.header("Features")
features = [
    ("One-tap timestamping", "Log precise event times with a single button press"),
    ("Glove-friendly UI", "Large targets designed for use in full PPE"),
    ("On-device storage", "No phone or data connection required"),
    ("Job summary", "Review all timestamps at end of job"),
    ("Lightweight", "Minimal battery and memory impact"),
    ("Free to download", "Distributed directly, no store required"),
]
fc1, fc2 = st.columns(2)
for i, (title, desc) in enumerate(features):
    col = fc1 if i % 2 == 0 else fc2
    with col:
        st.markdown(f"**{title}** — {desc}")

# Suggestions & contact
st.header("Suggestions & contact")
st.write(
    "Have a feature suggestion, found a bug, or want to request support for a new device? "
    "Get in touch — feedback from clinicians directly shapes development."
)
st.link_button("Email phemlogger@hotmail.com", "mailto:phemlogger@hotmail.com")

# Footer
st.divider()
st.caption(
    "PHEM Logger is intended for simulation and training use only. "
    "© 2026 PHEM Logger. Not a medical device."
)
