import requests
import streamlit as st

GITHUB_OWNER = "stroudiedr"
GITHUB_REPO = "phem_logger"


@st.cache_data(ttl=300)
def get_download_stats():
    """Returns {asset_name: download_count, 'total': int} across all releases. Empty dict on failure."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        releases = response.json()
        counts = {}
        total = 0
        for release in releases:
            for asset in release.get("assets", []):
                name = asset["name"]
                count = asset["download_count"]
                counts[name] = counts.get(name, 0) + count
                total += count
        counts["total"] = total
        return counts
    except Exception:
        return {}


@st.cache_data(ttl=300)
def get_latest_release_url(asset_name):
    """Returns browser_download_url for a named asset in the latest release, or None."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        release = response.json()
        for asset in release.get("assets", []):
            if asset["name"] == asset_name:
                return asset["browser_download_url"]
        return None
    except Exception:
        return None


@st.cache_data(ttl=300)
def get_latest_version():
    """Returns the latest release tag name, or 'v1.0.0' as fallback."""
    try:
        url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        release = response.json()
        return release.get("tag_name", "v1.0.0")
    except Exception:
        return "v1.0.0"
