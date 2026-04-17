# CLAUDE.md — phem-logger-site

## Project overview

A public-facing Streamlit web application to advertise and distribute PHEM Logger, a Garmin Connect IQ watch application for prehospital clinicians. The site provides information, screenshots, installation instructions, and direct `.prg` sideload file downloads.

Distribution is via sideloading only — the app is not available on the Garmin Connect IQ Store.

**Spec**: `SPEC.md` is the authoritative source of truth for all page content, structure, and behaviour. Read it before making any changes.

---

## Repository structure

```
phem-logger-site/
├── Home.py                        ← Streamlit entry point
├── pages/
│   ├── 1_Garmin.py
│   ├── 2_Apple_Watch.py
│   └── 3_Suunto.py
├── utils/
│   ├── __init__.py
│   ├── github.py                  ← GitHub Releases API helpers
│   └── analytics.py               ← GoatCounter injection
├── assets/
│   ├── icon.png                   ← provided by user
│   ├── banner.png                 ← provided by user
│   └── screenshots/
│       ├── fenix_home.png
│       ├── fenix_log.png
│       └── fenix_summary.png
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── SPEC.md
├── CLAUDE.md
└── README.md
```

---

## Tech stack

| Layer | Choice |
|---|---|
| Framework | Streamlit >= 1.35.0 |
| Language | Python 3.11+ |
| Download hosting | GitHub Releases (separate repo: `phem-logger-releases`) |
| Analytics | GoatCounter (free tier) |
| Deployment | Streamlit Community Cloud |
| Dependencies | `streamlit`, `requests` only |

---

## Configuration values

These must be set by the user before deployment. They are defined in one place each — do not hardcode them elsewhere.

| File | Variable | Description |
|---|---|---|
| `utils/github.py` | `GITHUB_OWNER` | GitHub username |
| `utils/github.py` | `GITHUB_REPO` | `phem-logger-releases` |
| `utils/analytics.py` | GoatCounter URL | e.g. `https://phem-logger.goatcounter.com/count` |

---

## Key conventions

### Page structure
Every page file must follow this order:
1. `st.set_page_config(...)` — must be the first Streamlit call
2. Imports and utility calls
3. `inject_analytics()` — call early in the page body
4. Page content sections in the order defined in `SPEC.md`

### Asset handling
Always guard image loads with `os.path.exists()`. Never let a missing asset crash the page — show `st.info("Screenshots coming soon")` as fallback.

```python
import os
if os.path.exists("assets/screenshots/fenix_home.png"):
    st.image("assets/screenshots/fenix_home.png", caption="Home screen")
else:
    st.info("Screenshot coming soon")
```

### GitHub API caching
Decorate `get_download_stats()` with `@st.cache_data(ttl=300)` to cache responses for 5 minutes. This prevents rate-limiting on the GitHub API during high traffic.

### Download buttons
Always fetch the download URL dynamically via `get_latest_release_url()` rather than hardcoding URLs. This ensures download links automatically reflect the latest GitHub release without code changes.

If the URL cannot be fetched (network error, asset not yet published), display `st.info("Download coming soon")` — never show a broken link.

### Coming soon sections
Garmin device families other than Fenix, and the Apple Watch and Suunto pages, use a standard coming soon pattern:

```python
st.info("Support for [Device] is in development. Check back soon.")
st.link_button(
    "Register interest",
    "mailto:phemlogger@hotmail.com?subject=PHEM Logger — [Device] interest"
)
```

### Disclaimer
The following disclaimer must appear in two places and must not be removed:
- Home page footer (via `st.caption`)
- Garmin page Download section (via `st.caption` below download cards)

> PHEM Logger is intended for simulation and training use only. This is not a medical device.

### Sidebar navigation
Streamlit generates sidebar navigation automatically from the `pages/` directory. Do not add manual sidebar code.

---

## Do not

- Use `st.experimental_*` APIs — use stable equivalents only
- Hardcode GitHub release asset URLs — always fetch dynamically
- Hardcode the current version string — fetch from the GitHub API latest release tag, with a fallback of `v1.0.0`
- Add authentication, login, or user accounts — this is a fully public site
- Add a database or server-side storage — all persistence is via GitHub Releases
- Remove or soften the simulation/training disclaimer

---

## Adding a new device family

When a new Garmin device family is ready (e.g. Forerunner):

1. Add a new tab in the `st.tabs()` call in `pages/1_Garmin.py`
2. Replace the coming soon placeholder with screenshots, instructions, and download cards following the Fenix section as a template
3. Add the new `.prg` asset to a new GitHub release in `phem-logger-releases` using the naming convention `PHEM_Logger_[Family][Series].prg`
4. Update the version history table at the bottom of `pages/1_Garmin.py`
5. Update the `Supported devices` metric on `Home.py`

When a new platform is ready (Apple Watch, Suunto):

1. Replace the full content of the relevant page file following the Garmin page as a template
2. Create a new releases repo or add assets to `phem-logger-releases` as appropriate
3. Update `utils/github.py` if a different repo is used for that platform

---

## Deployment

**Streamlit Community Cloud**:
1. Push repo to GitHub (`phem-logger-site`)
2. Go to share.streamlit.io
3. New app → select repo → branch: `main` → entry point: `Home.py`
4. Deploy

**GitHub releases repo** (`phem-logger-releases`) must exist and have at least one release with `.prg` assets attached before the download section will show live buttons. The site handles a missing/empty releases repo gracefully — download buttons fall back to "coming soon".

---

## Contact

Suggestions and feedback: phemlogger@hotmail.com
