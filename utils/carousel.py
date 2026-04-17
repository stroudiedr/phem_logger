import os
import streamlit as st


def screenshot_carousel(screenshots: list[tuple[str, str]], key: str) -> None:
    """
    Render a prev/next carousel for a list of (path, caption) tuples.
    Only existing files are included. Falls back to st.info if none exist.

    Args:
        screenshots: list of (file_path, caption) pairs
        key: unique key prefix for session state (use a different key per page)
    """
    available = [(p, c) for p, c in screenshots if os.path.exists(p)]

    if not available:
        st.info("Screenshots coming soon")
        return

    idx_key = f"_carousel_idx_{key}"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0

    n = len(available)
    idx = st.session_state[idx_key]

    # Navigation row: prev | counter | next
    col_prev, col_counter, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.button("◀", key=f"{key}_prev", disabled=(n <= 1)):
            st.session_state[idx_key] = (idx - 1) % n
            st.rerun()
    with col_counter:
        st.caption(f"{idx + 1} / {n}")
    with col_next:
        if st.button("▶", key=f"{key}_next", disabled=(n <= 1)):
            st.session_state[idx_key] = (idx + 1) % n
            st.rerun()

    path, caption = available[st.session_state[idx_key]]
    # Centre the image without stretching it to full width
    _, img_col, _ = st.columns([1, 4, 1])
    with img_col:
        st.image(path, caption=caption)
