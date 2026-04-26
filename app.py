import streamlit as st
import os
import json
import hashlib
from pathlib import Path
from pipeline.scorer import score_site_sustainability
from pipeline.image_processor import extract_features_with_vision
from dotenv import load_dotenv, set_key

load_dotenv()

SCOPE_OPTIONS = {
    "All": {
        "label": "All",
        "credits": ["SS-01", "SS-02", "SS-05"],
    },
    "SS-01: Rainwater & Sewage": {
        "label": "SS-01: Rainwater & Sewage",
        "credits": ["SS-01"],
    },
    "SS-02: Ecological Protection": {
        "label": "SS-02: Ecological Protection",
        "credits": ["SS-02"],
    },
    "SS-05: Heat Island Effect": {
        "label": "SS-05: Heat Island Effect",
        "credits": ["SS-05"],
    },
}

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Architecture Plan Auditor",
    page_icon="🏗️",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(45deg, #1d976c 0%, #93f9b9 100%);
        color: white; border: none; padding: 10px 20px;
        border-radius: 5px; font-weight: bold;
    }
    .report-card {
        background-color: #161b22; padding: 24px; border-radius: 12px;
        margin-bottom: 20px; border-left: 6px solid #1d976c;
        border-right: 1px solid #1d976c22; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .keystone-met {
        color: #93f9b9; font-weight: bold; font-size: 0.75rem;
        background: rgba(29,151,108,0.2); padding: 4px 10px;
        border-radius: 12px; border: 1px solid #1d976c; letter-spacing: 0.05rem;
    }
    .keystone-fail {
        color: #ff4b4b; font-weight: bold; font-size: 0.75rem;
        background: rgba(255,75,75,0.2); padding: 4px 10px;
        border-radius: 12px; border: 1px solid #ff4b4b; letter-spacing: 0.05rem;
    }
    .status-badge {
        font-size: 0.8rem; color: #8b949e; background: #0d1117;
        padding: 2px 8px; border-radius: 4px; margin-right: 10px;
    }
    .metric-container {
        text-align: center; padding: 25px; background: #1e2130;
        border-radius: 15px; border: 2px solid #1d976c;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .point-display {
        font-family: 'Inter', sans-serif; font-weight: 800;
        font-size: 1.5rem; color: #93f9b9;
    }
    .ai-report-box {
        background-color: #161b22; padding: 24px; border-radius: 12px;
        border-left: 6px solid #4a9eff; margin-top: 10px;
        font-size: 0.95rem; color: #c9d1d9; line-height: 1.8;
    }
    .summary-box {
        background-color: #161b22; padding: 20px; border-radius: 12px;
        border-left: 6px solid #f7c948; margin-top: 10px;
        font-size: 0.95rem; color: #c9d1d9; line-height: 1.8;
    }
    .sidebar-section-title {
        font-size: 1.02rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0.25rem 0 0.35rem 0;
    }
    .rating-panel {
        background: linear-gradient(180deg, rgba(22,27,34,0.96) 0%, rgba(13,17,23,0.96) 100%);
        border: 1px solid rgba(145, 255, 184, 0.18);
        border-radius: 14px;
        padding: 14px 14px 10px 14px;
        margin-bottom: 0.6rem;
    }
    .rating-subtitle {
        color: #8b949e;
        font-size: 0.82rem;
        line-height: 1.45;
        margin-top: 0.35rem;
    }
    .rating-pill {
        display: inline-block;
        margin-top: 0.45rem;
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(29,151,108,0.18);
        color: #93f9b9;
        border: 1px solid rgba(147,249,185,0.35);
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: 0.02rem;
    }
    </style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🏗️ AI Architecture Plan Auditor")
st.write("Evidence-based evaluation for Mostadam Credits **SS-01, SS-02, and SS-05**.")

# ── Disk Cache Helpers ────────────────────────────────────────────────────────
CACHE_DIR = Path(".audit_cache")
CACHE_DIR.mkdir(exist_ok=True)

def _cache_path(filename: str) -> Path:
    """Return disk path for a cached audit result keyed by image filename hash."""
    key = hashlib.md5(filename.encode()).hexdigest()
    return CACHE_DIR / f"{key}.json"

def save_to_cache(filename: str, image_bytes: bytes, result: dict):
    cache = {
        "filename": filename,
        "image_b64": image_bytes.hex(),   # store as hex string
        "result": result,
    }
    with open(_cache_path(filename), "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

def load_from_cache(filename: str):
    p = _cache_path(filename)
    if not p.exists():
        return None, None
    with open(p, "r", encoding="utf-8") as f:
        cache = json.load(f)
    image_bytes = bytes.fromhex(cache["image_b64"])
    return image_bytes, cache["result"]

def load_latest_cache():
    """Load the most-recently-modified cache file (used on fresh page load)."""
    files = sorted(CACHE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None, None, None
    with open(files[0], "r", encoding="utf-8") as f:
        cache = json.load(f)
    image_bytes = bytes.fromhex(cache["image_b64"])
    return image_bytes, cache["result"], cache["filename"]


def filter_credits_by_scope(credits_data: dict, selected_scope: str) -> dict:
    """Return only the credits that belong to the chosen scope."""
    credit_ids = SCOPE_OPTIONS.get(selected_scope, SCOPE_OPTIONS["All"])["credits"]
    return {credit_id: credits_data[credit_id] for credit_id in credit_ids if credit_id in credits_data}


def build_scoped_summary(scope_label: str, credits_data: dict, total_points: int, max_possible: int) -> str:
    """Generate a short summary for the selected scope."""
    if not credits_data:
        return f"No credits were available for the selected scope: {scope_label}."

    credit_parts = []
    for credit_id, info in credits_data.items():
        pts = info.get("points", 0)
        mx = info.get("max_points", 0)
        status = info.get("status", "Unverified")
        credit_parts.append(f"{credit_id} ({pts}/{mx}, {status})")

    joined_credits = "; ".join(credit_parts)
    return (
        f"Scoped to {scope_label}, the dashboard currently shows {len(credits_data)} credit(s) "
        f"with a score of {total_points}/{max_possible}. "
        f"Visible credits: {joined_credits}."
    )


def build_scoped_report(scope_label: str, credits_data: dict, total_points: int, max_possible: int) -> str:
    """Build a filtered narrative report from the visible credit explanations."""
    if not credits_data:
        return f"No credit data was available for the selected scope: {scope_label}."

    lines = [
        f"Scoped Audit Report for {scope_label}",
        f"Scoped score: {total_points}/{max_possible}",
        "",
        "Included credits:",
    ]
    for credit_id, info in credits_data.items():
        pts = info.get("points", 0)
        mx = info.get("max_points", 0)
        status = info.get("status", "Unverified")
        explanation = info.get("explanation", "No explanation provided.").replace("**", "")
        lines.append(f"- {credit_id}: {pts}/{mx} | {status} | {explanation}")

    return "\n".join(lines)

# ── API Key ───────────────────────────────────────────────────────────────────
ENV_FILE = ".env"

def get_api_key():
    """Read API key from env var (already loaded from .env via load_dotenv)."""
    return os.getenv("OPENAI_API_KEY", "").strip()

api_key = get_api_key()

# ── Session State Init ────────────────────────────────────────────────────────
if "audit_result" not in st.session_state:
    st.session_state.audit_result = None
if "audit_image" not in st.session_state:
    st.session_state.audit_image = None
if "audit_filename" not in st.session_state:
    st.session_state.audit_filename = None
if "selected_scope" not in st.session_state:
    st.session_state.selected_scope = "All"

with st.sidebar:

    st.markdown("## 🌟 Mostadam Rating Level")
    logo_path = Path("green_logo.jpg")
    # st.markdown('<div class="rating-panel">', unsafe_allow_html=True)
    rating_col_1, rating_col_2 = st.columns([0.42, 1.0], gap="small")
    with rating_col_1:
        if logo_path.exists():
            st.image(str(logo_path), width=56)
    with rating_col_2:
        # st.markdown(
        #     "<div style='font-weight:800; color:#93f9b9; font-size:1.02rem; line-height:1.1;'>Mostadam rating level</div>",
        #     unsafe_allow_html=True,
        # )
        st.markdown(
            "<div class='rating-pill'>Green</div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        "<div class='rating-subtitle'>"
        "Focus area: Site Sustainability only. Other Mostadam criteria remain outside this dashboard scope."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("## 🔎 Scope Filter")
    current_scope = st.session_state.get("selected_scope", "All")
    st.radio(
        "Select the site sustainability scope",
        options=list(SCOPE_OPTIONS.keys()),
        index=list(SCOPE_OPTIONS.keys()).index(current_scope)
        if current_scope in SCOPE_OPTIONS
        else 0,
        key="selected_scope",
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("## 🔑 API Key")
    if api_key:
        st.success("API Key loaded ✓", icon="✅")
        if st.button("Change API Key"):
            st.session_state.show_api_input = True
    else:
        st.session_state.show_api_input = True

    if st.session_state.get("show_api_input", not bool(api_key)):
        new_key = st.text_input("Enter OpenAI API Key", type="password", key="api_key_input")
        if st.button("Save Key"):
            if new_key.strip():
                set_key(ENV_FILE, "OPENAI_API_KEY", new_key.strip())
                os.environ["OPENAI_API_KEY"] = new_key.strip()
                api_key = new_key.strip()
                st.session_state.show_api_input = False
                st.success("API Key saved to .env and will persist across reloads.")
                st.rerun()

if not api_key:
    st.warning("Please provide an OpenAI API Key in the sidebar to proceed.")
    st.stop()

# Ensure the live environment always has the key (important for pipeline modules)
os.environ["OPENAI_API_KEY"] = api_key

# ── Restore from disk on fresh load ──────────────────────────────────────────
if st.session_state.audit_result is None:
    img_bytes, cached_result, cached_filename = load_latest_cache()
    if cached_result is not None:
        st.session_state.audit_result = cached_result
        st.session_state.audit_image = img_bytes
        st.session_state.audit_filename = cached_filename

# ── File Uploader ─────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("Upload Site/Floor Plan Image", type=["png", "jpg", "jpeg"])

new_upload = (
    uploaded_file is not None
    and uploaded_file.name != st.session_state.audit_filename
)

if new_upload:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.image(uploaded_file, caption="Uploaded Plan", width="stretch")

    with col2:
        with st.status("🏗️ Conducting Strict Evidence Audit...") as audit_status:
            image_bytes = uploaded_file.getvalue()

            st.write("👁️ Scanning for visual evidence...")
            # Re-import with updated env key in case it was just entered
            from pipeline.image_processor import extract_features_with_vision as _extract
            features = _extract(image_bytes, is_path=False)

            st.write("📖 Cross-referencing Mostadam SS Guidelines...")
            from pipeline.scorer import score_site_sustainability as _score
            result_json = _score(features, api_key=api_key)

            audit_status.update(label="Audit Complete!", state="complete", expanded=False)

    image_bytes = uploaded_file.getvalue()
    try:
        parsed = json.loads(result_json)
        st.session_state.audit_result = parsed
        st.session_state.audit_image = image_bytes
        st.session_state.audit_filename = uploaded_file.name
        save_to_cache(uploaded_file.name, image_bytes, parsed)
    except Exception:
        st.session_state.audit_result = {"_parse_error": result_json}
        st.session_state.audit_image = image_bytes
        st.session_state.audit_filename = uploaded_file.name

elif st.session_state.audit_image is not None and uploaded_file is None:
    st.image(
        st.session_state.audit_image,
        caption=f"Cached Plan — {st.session_state.audit_filename}",
        width=500,
    )

# ── Display Results ───────────────────────────────────────────────────────────
selected_scope = st.session_state.selected_scope

if st.session_state.audit_result:
    data = st.session_state.audit_result

    if "_parse_error" in data:
        st.error("Error parsing audit results.")
        st.write(data["_parse_error"])
    else:
        credits_data = data.get("credits", {})
        scoped_credits = filter_credits_by_scope(credits_data, selected_scope)

        st.divider()

        # 1. Big Score
        total_points = sum(c.get("points", 0) for c in scoped_credits.values())
        max_possible = sum(c.get("max_points", 0) for c in scoped_credits.values())
        html_metric = (
            f'<div class="metric-container">'
            f'<h1 style="color: #93f9b9; margin-bottom: 0;">{total_points} / {max_possible}</h1>'
            f'<p style="color: #8b949e; font-size: 1.2rem;">Final Sustainability Audit Score</p>'
            f'<p style="color: #8b949e; font-size: 0.95rem; margin-top: 8px;">'
            f'Scoped to {selected_scope}</p>'
            f'</div>'
        )
        st.markdown(html_metric, unsafe_allow_html=True)

        # 2. Executive Summary
        st.write("### 📝 Audit Executive Summary")
        if selected_scope == "All":
            summary_text = data.get("summary", "").strip()
        else:
            summary_text = build_scoped_summary(selected_scope, scoped_credits, total_points, max_possible)
        if summary_text:
            st.markdown(
                f'<div class="summary-box">{summary_text}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("Summary not available in audit result.")

        # 3. Credit-by-Credit Breakdown
        st.write("### 📋 Credit-by-Credit Score Breakdown")
        for credit_id, info in scoped_credits.items():
            pts = info.get("points", 0)
            mx = info.get("max_points", 0)
            is_keystone = info.get("is_keystone", False)
            keystone_met = info.get("keystone_met", False)
            status_text = info.get("status", "Unverified")
            explanation_str = info.get("explanation", "No explanation provided.").replace("**", "")

            keystone_badge = ""
            if is_keystone:
                keystone_badge = (
                    '<span class="keystone-met">KEYSTONE MET</span>'
                    if keystone_met
                    else '<span class="keystone-fail">KEYSTONE FAILED</span>'
                )

            html_card = (
                f'<div class="report-card">'
                f'<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">'
                f'<div><h4 style="color: #1d976c; margin: 0;">{credit_id}</h4>'
                f'<span class="status-badge">{status_text}</span></div>'
                f'<div style="text-align: right;">'
                f'<div class="point-display">{pts} <span style="font-size: 1rem; color: #8b949e;">/ {mx}</span></div>'
                f'{keystone_badge}</div></div>'
                f'<div style="color: #c9d1d9; border-top: 1px solid #1d976c22; padding-top: 15px; margin-top: 10px; font-size: 0.95rem; line-height: 1.6;">'
                f'{explanation_str}</div></div>'
            )
            st.markdown(html_card, unsafe_allow_html=True)

        # 4. Detailed Audit Report
        if selected_scope == "All":
            report_text = data.get("audit_report", data.get("overall_calculation", "")).strip().replace("**", "")
        else:
            report_text = build_scoped_report(selected_scope, scoped_credits, total_points, max_possible)
        st.write("### 📄 Detailed Audit Report")
        if report_text:
            st.markdown(
                f'<div class="ai-report-box">{report_text.replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("No detailed report was returned by the auditor.")

else:
    st.info("Upload a plan to conduct a strict sustainability audit.")
st.sidebar.markdown("---")
# Clear cache button
if st.sidebar.button("🗑️ Clear Cached Results"):
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
    st.session_state.audit_result = None
    st.session_state.audit_image = None
    st.session_state.audit_filename = None
    st.sidebar.success("Cache cleared.")
    st.rerun()
