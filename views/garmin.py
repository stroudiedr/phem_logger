import streamlit as st
from utils.github import get_download_stats, get_latest_release_url
from utils.carousel import screenshot_carousel

SCREENSHOTS = [
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
]


def render():
    st.title("Garmin watches")
    st.write(
        "PHEM Logger is available for a range of Garmin watch families. "
        "Select your device below. Additional device support is in development."
    )

    counts = get_download_stats()
    tabs = st.tabs(["Fenix", "Forerunner", "Enduro", "Venu", "Instinct"])

    with tabs[0]:
        st.header("Garmin Fenix")
        st.subheader("Fenix 6 series, Fenix 7 series & Fenix 8 Series")

        col_carousel, col_spacer = st.columns(2)
        with col_carousel:
            screenshot_carousel(SCREENSHOTS, key="garmin_fenix")

        st.header("Installation")
        col_pc, col_mac = st.columns(2)

        with col_pc:
            st.subheader("Installation with PC / Laptop")
            st.markdown(
                """
1. Use Garmin cable to usb port
2. Using Explorer navigate to File: Fenix / Garmin / Apps
3. Drag & drop or copy & paste phem_logger_v1-3.prg file to this location
4. Disconnect via eject if possible
5. PHEM Logger found in Apps
"""
            )

        with col_mac:
            st.subheader("Installation with Apple MacBook")
            st.markdown(
                """
1. In internet browser navigate to: https://openmtp.ganeshrvel.com/
2. Click on most appropriate download button depending on age of Apple Mac
3. Double click on downloaded .dmg file & drag to install
4. Use Garmin cable to connect watch to usb port
5. Open & use OpenMTP app to drag phem_logger_v1-3.prg file to folder Garmin/Apps on Watch
6. Close OpenMTP & disconnect watch
7. PHEM Logger will install & then found in Apps
"""
            )

        st.header("Using PHEM Logger")
        st.markdown("**Controls**")
        st.markdown(
            """
- **UP / DOWN** – selection through options
- **START** – enter menus, confirm timings
- **BACK** – return to previous screen, Setting options on main screen
- **BACK then START** – Button lock
"""
        )

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
            st.subheader("Fenix 7 & 8 series")
            st.write(
                "Compatible with Fenix 7, 7S, 7X, 7 Pro, 7S Pro, 7X Pro; "
                "Fenix 8 43mm, 8 47mm, 8 51mm, Fenix E"
            )
            st.metric("Downloads", counts.get("PHEM_Logger_v1-4_Fenix7.prg", "—"))
            url7 = get_latest_release_url("PHEM_Logger_v1-4_Fenix7.prg")
            if url7:
                st.link_button("Download .prg", url7)
            else:
                st.info("Download coming soon")

        st.divider()
        st.header("Version history")
        st.markdown(
            """
<table>
<thead><tr><th>Version</th><th>Date</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>v1.4</td><td>17th April 2026</td><td>Amalgamated Landing &amp; At Scene to form Land / At Scene.<br>Support for Fenix 6.<br>Midazolam drug added.TOR added to Cardiac Arrest menu.</td></tr>
<tr><td>v1.3</td><td>13th April 2026</td><td>Initial release. Core timestamping, event log, job summary. Fenix 7.</td></tr>
</tbody>
</table>
""",
            unsafe_allow_html=True,
        )

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

