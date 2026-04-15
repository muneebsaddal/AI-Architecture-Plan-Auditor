import streamlit as st
import os
import json
from pipeline.scorer import score_site_sustainability
from pipeline.image_processor import extract_features_with_vision
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Strict Site Sustainability Auditor", page_icon="⚖️", layout="wide")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #1d976c 0%, #93f9b9 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .report-card {
        background-color: #161b22;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 6px solid #1d976c;
        border-right: 1px solid #1d976c22;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .keystone-met {
        color: #93f9b9;
        font-weight: bold;
        font-size: 0.75rem;
        background: rgba(29, 151, 108, 0.2);
        padding: 4px 10px;
        border-radius: 12px;
        border: 1px solid #1d976c;
        letter-spacing: 0.05rem;
    }
    .keystone-fail {
        color: #ff4b4b;
        font-weight: bold;
        font-size: 0.75rem;
        background: rgba(255, 75, 75, 0.2);
        padding: 4px 10px;
        border-radius: 12px;
        border: 1px solid #ff4b4b;
        letter-spacing: 0.05rem;
    }
    .status-badge {
        font-size: 0.8rem;
        color: #8b949e;
        background: #0d1117;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 10px;
    }
    .metric-container {
        text-align: center;
        padding: 25px;
        background: #1e2130;
        border-radius: 15px;
        border: 2px solid #1d976c;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .point-display {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        color: #93f9b9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚖️ Strict Site Sustainability Auditor")
st.write("Specialized, evidence-based evaluation for Mostadam Credits **SS-01, SS-02, and SS-05**.")

# Check for API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    with st.sidebar:
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key

if not api_key:
    st.warning("Please provide an OpenAI API Key in the sidebar to proceed.")
    st.stop()

uploaded_file = st.file_uploader("Upload Site/Floor Plan Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(uploaded_file, caption="Uploaded Plan", use_container_width=True)
        
    with col2:
        with st.status("🏗️ Conducting Strict Evidence Audit...") as status:
            # 1. Save temp image
            with open("temp_plan_ss.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Extract Vision Features
            st.write("👁️ Scanning for visual evidence...")
            features = extract_features_with_vision("temp_plan_ss.png")
            
            # 3. Score against Markdown Rules
            st.write("📖 Cross-referencing under Strict Mode...")
            result_json = score_site_sustainability(features)
            
            status.update(label="Audit Complete!", state="complete", expanded=False)

    # --- Display Results ---
    st.divider()
    
    try:
        data = json.loads(result_json)
        credits_data = data.get("credits", {})
        
        # 1. Total Score Calculation
        total_points = sum(c.get("points", 0) for c in credits_data.values())
        max_possible = sum(c.get("max_points", 0) for c in credits_data.values())
        
        st.markdown(f"""
            <div class="metric-container">
                <h1 style="color: #93f9b9; margin-bottom: 0;">{total_points} / {max_possible}</h1>
                <p style="color: #8b949e; font-size: 1.2rem;">Final Sustainability Audit Score</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Executive Summary
        st.write("### 📝 Audit Executive Summary")
        st.info(data.get("summary", "No summary available."))
        
        # 3. Detailed Report (RE-BEAUTIFIED & BUG-FIXED)
        st.write("### 📋 Credit-by-Credit Score Breakdown")
        
        for credit_id, info in credits_data.items():
            pts = info.get("points", 0)
            mx = info.get("max_points", 0)
            is_keystone = info.get("is_keystone", False)
            keystone_met = info.get("keystone_met", False)
            status_text = info.get("status", "Unverified")
            
            keystone_badge = ""
            if is_keystone:
                if keystone_met:
                    keystone_badge = '<span class="keystone-met">KEYSTONE MET</span>'
                else:
                    keystone_badge = '<span class="keystone-fail">KEYSTONE FAILED</span>'

            with st.container():
                st.markdown(f"""
                    <div class="report-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div>
                                <h4 style="color: #1d976c; margin: 0;">{credit_id}</h4>
                                <span class="status-badge">{status_text}</span>
                            </div>
                            <div style="text-align: right;">
                                <div class="point-display">{pts} <span style="font-size: 1rem; color: #8b949e;">/ {mx}</span></div>
                                {keystone_badge}
                            </div>
                        </div>
                        <div style="color: #c9d1d9; border-top: 1px solid #1d976c22; padding-top: 15px; margin-top: 10px; font-size: 0.95rem; line-height: 1.6;">
                            {info.get('explanation', '')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # 4. Calculation Logic & Vision Signals
        with st.expander("🔍 Audit Methodology & Visual Evidence Scanner"):
            st.write(data.get("overall_calculation", "Logic not provided."))
            st.write("---")
            st.markdown("### 👁️ AI Vision: Identified Site Evidence")
            
            # Clean and render the vision signals
            signal_lines = features.split('\n')
            for line in signal_lines:
                clean_line = line.strip().replace("**", "")
                if clean_line:
                    if any(emoji in clean_line for emoji in ["🚰", "🍳", "🌦️", "🌳", "🔥", "📐"]):
                        st.markdown(f"""
                            <div style="background-color: #1e2130; padding: 12px; border-radius: 8px; border-left: 4px solid #93f9b9; margin-top: 15px; margin-bottom: 8px;">
                                <span style="color: #93f9b9; font-weight: 700; font-size: 1.1rem; font-family: 'Inter', sans-serif;">{clean_line}</span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="margin-left: 25px; color: #c9d1d9; font-size: 0.95rem; line-height: 1.6; font-family: 'Inter', sans-serif;">
                                • {clean_line}
                            </div>
                        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error parsing audit results: {e}")
        st.write("### Raw Analysis")
        st.write(result_json)

else:
    st.info("Upload a plan to conduct a strict sustainability audit.")

# Footer info
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚖️ Auditor Settings")
st.sidebar.write("**Mode:** STRICT EVIDENCE")
st.sidebar.write("**Assumption Cap:** 25%")
st.sidebar.markdown("---")
st.sidebar.write("**Scope Focus:**")
st.sidebar.write("- **SS-01:** Rainwater & Sewage")
st.sidebar.write("- **SS-02:** Ecological Protection")
st.sidebar.write("- **SS-05:** Heat Island Effect")
