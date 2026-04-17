import streamlit as st
from utils.analytics import inject_analytics
from utils.github import get_download_stats, get_latest_release_url
from utils.carousel import screenshot_carousel

st.set_page_config(
    page_title="Garmin — PHEM Logger",
    page_icon="assets/icon.png",
    layout="wide",
)

inject_analytics()

st.title("Garmin watches")
st.write(
    "PHEM Logger is available for a range of Garmin watch families. "
    "Select your device below. Additional device support is in development."
)

counts = get_download_stats()

tabs = st.tabs(["Fenix", "Forerunner", "Enduro", "Venu", "Instinct"])

# ── Fenix tab ──────────────────────────────────────────────────────────────────
with tabs[0]:
    st.header("Garmin Fenix")
    st.subheader("Fenix 6 series and Fenix 7 series")

    # Screenshots
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
        key="garmin_fenix",
    )

    # Installation
    st.header("Installation")
    st.markdown(
        """
1. Go to the **Download** section below and download the `.prg` file for your Fenix series.
2. Connect your Garmin Fenix watch to your computer via USB cable.
3. Open the watch in Finder (macOS) or File Explorer (Windows) — it appears as a USB drive.
4. Navigate to `GARMIN/APPS/` on the watch storage.
5. Copy the `.prg` file into the `GARMIN/APPS/` folder.
6. Safely eject the watch.
7. The app will appear in your Garmin activity/app list.
"""
    )

    # Usage
    st.header("Using PHEM Logger")
    st.markdown(
        """
1. Open PHEM Logger from your Garmin apps list when on scene.
2. Press the **top button** to log a timestamp event.
3. Use the **down button** to scroll through logged events.
4. At end of job, review the summary screen for all event times.
5. Power cycle the watch to reset for a new job.
"""
    )

    # Download cards
    st.header("Download")
    dl1, dl2 = st.columns(2)

    with dl1:
        st.subheader("Fenix 6 series")
        st.write("Compatible with Fenix 6, 6S, 6X, 6 Pro, 6S Pro, 6X Pro")
        st.metric("Downloads", counts.get("PHEM_Logger_v1-4_Fenix6.prg", "—"))
        url6 = get_latest_release_url("PHEM_Logger_v1-4_Fenix6.prg")
        if url6:
            st.link_button("Download .prg", url6)
        else:
            st.info("Download coming soon")

    with dl2:
        st.subheader("Fenix 7 series")
        st.write("Compatible with Fenix 7, 7S, 7X, 7 Pro, 7S Pro, 7X Pro")
        st.metric("Downloads", counts.get("PHEM_Logger_v1-4_Fenix7.prg", "—"))
        url7 = get_latest_release_url("PHEM_Logger_v1-4_Fenix7.prg")
        if url7:
            st.link_button("Download .prg", url7)
        else:
            st.info("Download coming soon")

    st.caption("PHEM Logger is intended for simulation and training use only. This is not a medical device.")

# ── Coming soon tabs ───────────────────────────────────────────────────────────
coming_soon = [
    ("Forerunner", "Forerunner"),
    ("Enduro", "Enduro"),
    ("Venu", "Venu"),
    ("Instinct", "Instinct"),
]
for tab, (label, device) in zip(tabs[1:], coming_soon):
    with tab:
        st.info(
            f"Support for {label} is in development. Check back soon, or email "
            "phemlogger@hotmail.com to register your interest."
        )
        st.link_button(
            "Register interest",
            f"mailto:phemlogger@hotmail.com?subject=PHEM Logger — {device} interest",
        )

# ── Shared sections ────────────────────────────────────────────────────────────
st.divider()

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

st.header("Version history")
st.markdown(
    """
| Version | Date | Notes |
|---|---|---|
| v1.0.0 | TBC | Initial release. Core timestamping, event log, job summary. Fenix 6 and Fenix 7. |
"""
)
