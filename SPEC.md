# PHEM Logger — website specification

## Overview

A public-facing Streamlit web application to advertise and distribute PHEM Logger, a Garmin Connect IQ watch application for prehospital clinicians. The site provides information, screenshots, installation instructions, and direct download of `.prg` sideload files. Distribution is via sideloading only — the app is not available on the Garmin Connect IQ Store.

The site is designed to scale to additional watch platforms (Apple Watch, Suunto) and additional Garmin device families over time.

---

## Deployment target

- **Platform**: Streamlit Community Cloud (free tier)
- **Repo**: GitHub (new repository, name: `phem-logger-site`)
- **Entry point**: `Home.py`
- **Python**: 3.11+

---

## Repository structure

```
phem-logger-site/
├── Home.py
├── pages/
│   ├── 1_Garmin.py
│   ├── 2_Apple_Watch.py
│   └── 3_Suunto.py
├── assets/
│   ├── icon.png                  ← app icon (provided by user)
│   ├── banner.png                ← hero banner image (provided by user)
│   └── screenshots/
│       ├── fenix_home.png        ← placeholder until provided
│       ├── fenix_log.png         ← placeholder until provided
│       └── fenix_summary.png     ← placeholder until provided
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── README.md
```

---

## Dependencies

**`requirements.txt`**:
```
streamlit>=1.35.0
requests>=2.31.0
```

**`.streamlit/config.toml`**:
```toml
[theme]
primaryColor = "#1D9E75"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F1EFE8"
textColor = "#2C2C2A"
font = "sans serif"

[server]
headless = true
```

---

## GitHub integration

All download buttons link directly to GitHub Release assets in the **`phem-logger-releases`** GitHub repository (separate from the site repo, used purely for release asset hosting).

### Release asset naming convention

```
PHEM_Logger_Fenix6.prg
PHEM_Logger_Fenix7.prg
```

### Download count

The site fetches download counts from the GitHub Releases API on page load. This is a read-only public API call — no authentication required for public repos.

```python
import requests

GITHUB_OWNER = "your-github-username"
GITHUB_REPO = "phem-logger-releases"

def get_download_stats():
    """
    Returns dict of {asset_name: download_count} for all release assets,
    plus a 'total' key with the sum across all releases.
    Returns empty dict on failure (network error, rate limit etc).
    """
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

def get_latest_release_url(asset_name):
    """
    Returns the browser_download_url for a named asset in the latest release.
    Returns None if not found.
    """
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
```

Place these helper functions in a shared module: `utils/github.py`.

---

## Analytics

GoatCounter is injected on every page via a Streamlit HTML component. Register a free account at goatcounter.com and obtain a site code (e.g. `phem-logger`).

Inject on every page using:

```python
import streamlit.components.v1 as components

def inject_analytics():
    components.html(
        """
        <script
            data-goatcounter="https://phem-logger.goatcounter.com/count"
            async src="//gc.zgo.at/count.js">
        </script>
        """,
        height=0
    )
```

Place this function in `utils/analytics.py` and call `inject_analytics()` at the top of every page file.

---

## Shared utilities

Create a `utils/` directory:

```
utils/
├── __init__.py
├── github.py       ← get_download_stats(), get_latest_release_url()
└── analytics.py    ← inject_analytics()
```

---

## Page specifications

---

### Home.py

**Purpose**: Landing page. Introduces PHEM Logger, shows key features, displays screenshots, and provides a contact/suggestions link.

**Sections in order**:

#### 1. Page config
```python
st.set_page_config(
    page_title="PHEM Logger",
    page_icon="assets/icon.png",
    layout="wide"
)
```

#### 2. Analytics injection
Call `inject_analytics()`.

#### 3. Banner
Display `assets/banner.png` full width using `st.image("assets/banner.png", use_column_width=True)`.

#### 4. Header
```
PHEM Logger
Precision timestamping for prehospital clinicians
```
Use `st.title` and `st.subheader`. Display the app icon alongside using columns.

#### 5. About section
Heading: `About`

Body text (editable placeholder — user will refine):
> PHEM Logger is a Garmin Connect IQ application designed for prehospital emergency clinicians. It runs directly on your Garmin watch, allowing you to record precise event timestamps during a job — hands-free and glove-friendly. Designed for use by HEMS crews, BASICS doctors, and air ambulance teams.
>
> The app is distributed via sideloading and is intended for simulation and training use only.

#### 6. Download stats strip
Pull live from GitHub API using `get_download_stats()`. Display as three metric columns:

| Metric | Value |
|---|---|
| Total downloads | `counts["total"]` or `—` if unavailable |
| Current version | Pulled from latest release tag via API, or hardcoded fallback `v1.0.0` |
| Supported devices | `Garmin Fenix 6 & 7` (static, update as more added) |

Use `st.metric()` for each.

#### 7. Screenshots
Heading: `Screenshots`

Display screenshots in a three-column grid:
- `assets/screenshots/fenix_home.png`
- `assets/screenshots/fenix_log.png`
- `assets/screenshots/fenix_summary.png`

Each with a caption. If image files are missing, display a `st.info("Screenshots coming soon")` placeholder instead — check with `os.path.exists()`.

#### 8. Features section
Heading: `Features`

Display as a two-column grid of feature cards using `st.columns`. Each card uses `st.markdown` with a short heading and one-line description.

Features list:
- **One-tap timestamping** — Log precise event times with a single button press
- **Glove-friendly UI** — Large targets designed for use in full PPE
- **On-device storage** — No phone or data connection required
- **Job summary** — Review all timestamps at end of job
- **Lightweight** — Minimal battery and memory impact
- **Free to download** — Distributed directly, no store required

#### 9. Contact / suggestions
Heading: `Suggestions & contact`

Body:
> Have a feature suggestion, found a bug, or want to request support for a new device? Get in touch — feedback from clinicians directly shapes development.

Button (using `st.link_button`):
```python
st.link_button("Email phemlogger@hotmail.com", "mailto:phemlogger@hotmail.com")
```

#### 10. Footer
Small muted text at bottom:
```
PHEM Logger is intended for simulation and training use only.
© [current year] PHEM Logger. Not a medical device.
```
Use `st.caption()`.

---

### pages/1_Garmin.py

**Purpose**: All Garmin device family support. Currently active: Fenix. All other families show a coming soon placeholder.

**Page config**:
```python
st.set_page_config(page_title="Garmin — PHEM Logger", page_icon="assets/icon.png", layout="wide")
```

**Sections in order**:

#### 1. Analytics injection

#### 2. Page heading
```
Garmin watches
```
`st.title("Garmin watches")`

Brief intro:
> PHEM Logger is available for a range of Garmin watch families. Select your device below. Additional device support is in development.

#### 3. Device family tabs
Use `st.tabs()` with the following tab labels:
```python
tabs = st.tabs(["Fenix", "Forerunner", "Enduro", "Venu", "Instinct"])
```

---

#### Tab: Fenix

**Heading**: `Garmin Fenix`
**Subheading**: `Fenix 6 series and Fenix 7 series`

##### Screenshots
Three-column grid, same pattern as Home page:
- `assets/screenshots/fenix_home.png`
- `assets/screenshots/fenix_log.png`
- `assets/screenshots/fenix_summary.png`

##### Installation instructions
Heading: `Installation`

Numbered steps using `st.markdown`:
1. Go to the **Download** section below and download the `.prg` file for your Fenix series.
2. Connect your Garmin Fenix watch to your computer via USB cable.
3. Open the watch in Finder (macOS) or File Explorer (Windows) — it appears as a USB drive.
4. Navigate to `GARMIN/APPS/` on the watch storage.
5. Copy the `.prg` file into the `GARMIN/APPS/` folder.
6. Safely eject the watch.
7. The app will appear in your Garmin activity/app list.

##### Usage instructions
Heading: `Using PHEM Logger`

Numbered steps:
1. Open PHEM Logger from your Garmin apps list when on scene.
2. Press the **top button** to log a timestamp event.
3. Use the **down button** to scroll through logged events.
4. At end of job, review the summary screen for all event times.
5. Power cycle the watch to reset for a new job.

##### Download
Heading: `Download`

Display two download cards side by side using `st.columns(2)`.

**Left column — Fenix 6**:
- Label: `Fenix 6 series`
- Description: `Compatible with Fenix 6, 6S, 6X, 6 Pro, 6S Pro, 6X Pro`
- Download count: `counts.get("PHEM_Logger_Fenix6.prg", "—")`
- Button: fetch URL via `get_latest_release_url("PHEM_Logger_Fenix6.prg")`. If URL available, show `st.link_button("Download .prg", url)`. If unavailable, show `st.info("Download coming soon")`.

**Right column — Fenix 7**:
- Label: `Fenix 7 series`
- Description: `Compatible with Fenix 7, 7S, 7X, 7 Pro, 7S Pro, 7X Pro`
- Download count: `counts.get("PHEM_Logger_Fenix7.prg", "—")`
- Button: same pattern for `PHEM_Logger_Fenix7.prg`.

Below both cards, display in `st.caption`:
> PHEM Logger is intended for simulation and training use only. This is not a medical device.

---

#### Tabs: Forerunner, Enduro, Venu, Instinct

Each of these four tabs displays an identical coming soon placeholder:

```python
st.info("Support for [Device Family] is in development. Check back soon, or email phemlogger@hotmail.com to register your interest.")
st.link_button("Register interest", "mailto:phemlogger@hotmail.com?subject=PHEM Logger — [Device] interest")
```

---

#### Shared Garmin sections (below all tabs)

##### Features
Heading: `Features`
`st.divider()` above this section.

Same feature list as Home page, rendered the same way (two-column grid). This is intentionally duplicated so the Garmin page is self-contained.

##### Version history
Heading: `Version history`

Display as a table using `st.dataframe()` or `st.markdown` table:

| Version | Date | Notes |
|---|---|---|
| v1.0.0 | TBC | Initial release. Core timestamping, event log, job summary. Fenix 6 and Fenix 7. |

Add new rows here as versions are released. Dates are strings — no date parsing needed.

---

### pages/2_Apple_Watch.py

**Purpose**: Placeholder page for future Apple Watch support.

**Page config**:
```python
st.set_page_config(page_title="Apple Watch — PHEM Logger", page_icon="assets/icon.png", layout="wide")
```

**Content**:
```python
st.title("Apple Watch")
st.subheader("Coming soon")
st.write("PHEM Logger for Apple Watch is currently in development. Register your interest below and we'll let you know when it's available.")
st.link_button("Register interest", "mailto:phemlogger@hotmail.com?subject=PHEM Logger — Apple Watch interest")
inject_analytics()
```

---

### pages/3_Suunto.py

**Purpose**: Placeholder page for future Suunto support.

**Page config**:
```python
st.set_page_config(page_title="Suunto — PHEM Logger", page_icon="assets/icon.png", layout="wide")
```

**Content**: Same pattern as Apple Watch page, substituting "Suunto watches" as the title and adjusting the email subject line.

---

## Asset requirements

The following files must be provided by the user before deployment. The code should handle missing assets gracefully using `os.path.exists()` checks, displaying a placeholder message rather than crashing.

| File | Description |
|---|---|
| `assets/icon.png` | App icon. Recommended 512×512px, square. |
| `assets/banner.png` | Hero banner for Home page. Recommended 1200×400px. |
| `assets/screenshots/fenix_home.png` | Fenix watch face screenshot |
| `assets/screenshots/fenix_log.png` | Fenix event log screenshot |
| `assets/screenshots/fenix_summary.png` | Fenix job summary screenshot |

---

## GitHub releases repository

A **separate** GitHub repository named `phem-logger-releases` is used solely for hosting `.prg` release assets. This keeps the site repo clean.

### Setup steps (for user, not Claude Code):
1. Create a new public GitHub repository: `phem-logger-releases`
2. Create a release tagged `v1.0.0`
3. Attach `PHEM_Logger_Fenix6.prg` and `PHEM_Logger_Fenix7.prg` as release assets
4. Update `GITHUB_OWNER` and `GITHUB_REPO` in `utils/github.py` with your actual GitHub username

---

## Configuration values to update before deployment

These values are placeholders in the code and must be updated by the user:

| Location | Variable | Value to set |
|---|---|---|
| `utils/github.py` | `GITHUB_OWNER` | Your GitHub username |
| `utils/github.py` | `GITHUB_REPO` | `phem-logger-releases` |
| `utils/analytics.py` | GoatCounter URL | Your GoatCounter site URL |

---

## Streamlit Community Cloud deployment

1. Push the completed repo to GitHub (`phem-logger-site`)
2. Go to share.streamlit.io and sign in with GitHub
3. Click **New app**
4. Select repo: `phem-logger-site`, branch: `main`, entry point: `Home.py`
5. Click **Deploy**

The app will be available at `https://phem-logger.streamlit.app` (or similar — exact subdomain assigned by Streamlit).

---

## Notes for Claude Code

- All pages must call `inject_analytics()` at the top of the page body (after `set_page_config`)
- Use `st.cache_data(ttl=300)` on `get_download_stats()` to avoid hammering the GitHub API on every page load — cache for 5 minutes
- Use `os.path.exists()` before every `st.image()` call — missing assets must show an info placeholder, not raise an exception
- The disclaimer "intended for simulation and training use only" must appear on the Download section of the Garmin page and in the Home page footer
- Do not use `st.experimental_*` APIs — use stable equivalents only
- Sidebar navigation is auto-generated by Streamlit from the `pages/` directory — no manual sidebar code needed
