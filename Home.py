import base64
import os
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent
from utils.analytics import inject_analytics
from utils.carousel import screenshot_carousel
from views import garmin, apple_watch, suunto

st.set_page_config(
    page_title="PHEM Logger",
    page_icon="assets/icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """<style>
    [data-testid="collapsedControl"] {display: none;}
    [data-testid="stSidebar"] {display: none;}

    /* Larger tab labels */
    [data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p,
    .stTabs [data-baseweb="tab"] {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }

    /* Larger body text */
    [data-testid="stMarkdownContainer"] p,
    .stMarkdown p,
    div[data-testid="stText"] {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    </style>""",
    unsafe_allow_html=True,
)

inject_analytics()

tab_home, tab_garmin, tab_apple, tab_suunto = st.tabs(
    ["Home", "Garmin", "Apple Watch", "Suunto"]
)

# ── Home tab ───────────────────────────────────────────────────────────────────
with tab_home:
    # Banner at reduced height
    banner_path = ROOT / "assets/banner.png"
    if banner_path.exists():
        with open(banner_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<img src="data:image/png;base64,{b64}" '
            'style="width:100%;max-height:200px;object-fit:cover;border-radius:6px;">',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

    # Header
    col_icon, col_title = st.columns([1, 8])
    with col_icon:
        icon_path = ROOT / "assets/icon.png"
        if icon_path.exists():
            st.image(str(icon_path), width=80)
    with col_title:
        st.title("PHEM Logger")
        st.subheader("Precision timestamping for prehospital clinicians")

    # About + stats in two columns
    st.header("About")
    col_about, col_stats = st.columns(2)

    with col_about:
        st.write(
            "A job timing and documentation tool for pre-hospital emergency medicine professionals."
        )
        st.write(
            "PHEM Logger provides accurate, real-time timestamping of key events during patient "
            "encounters — supporting clinical governance, audit, and handover documentation."
        )

    with col_stats:
        m1, m2 = st.columns(2)
        m1.metric("**Current version**", "1.4")
        m2.metric("**Supported devices**", "Garmin Fenix 6, 7 & 8")

    # Features
    st.header("Features")

    st.write(
        "**Designed for:** Enhanced Care Teams (air and land based), "
        "Paramedic crews, and First Responders."
    )

    st.markdown("##### Job timeline recording")
    st.write("Accurate timestamps for each stage of a job:")
    st.markdown(
        "- 999 call, First person on scene, Mobile, Landing / At scene, At patient\n"
        "- Leave scene, Go to hospital, At hospital, Handover, Stand Down"
    )

    st.markdown("##### Medication timestamp recording")
    st.write("Records the time of clinician-administered medications:")
    st.markdown(
        "- Adrenaline (bolus & infusion)\n"
        "- Fentanyl, Ketamine, Rocuronium, Levetiracetam, Metaraminol, Midazolam\n"
        "- Morphine, Paracetamol, Tranexamic acid"
    )

    st.markdown("##### Intervention timestamp recording")
    st.write("Records the time of clinician-performed interventions:")
    st.markdown(
        "- Airway management, Blood products, Arterial access, Ultrasound, PHEA\n"
        "- Mapleson C, Ventilation changes\n"
        "- IV access, Sedation, Fracture manipulation"
    )

    st.markdown("##### Cardiac arrest event recording")
    st.write(
        "Timestamps for key cardiac arrest events to support post-event audit and "
        "Utstein-format reporting:"
    )
    st.markdown("- Asystole, PEA, VF/VT, ROSC, Shock, Mechanical CPR, TOR, PLE")

    st.markdown("##### Job review")
    st.write(
        "Easy display of current and previous job timings for review and documentation purposes."
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Contact
    st.header("Suggestions & contact")
    st.write(
        "Have a feature suggestion, found a bug, or want to request support for a new device? "
        "Get in touch — feedback from clinicians directly shapes development."
    )
    st.link_button("Email phemlogger@hotmail.com", "mailto:phemlogger@hotmail.com")

    # Footer
    st.divider()
    st.caption("© 2026 PHEM Logger. Not a medical device. Please use watches responsibly.")

# ── Other tabs ─────────────────────────────────────────────────────────────────
with tab_garmin:
    garmin.render()

with tab_apple:
    apple_watch.render()

with tab_suunto:
    suunto.render()
