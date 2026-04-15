import streamlit as st
import os
import json
from pipeline.scorer import score_site_sustainability
from pipeline.image_processor import extract_features_with_vision
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Site Sustainability Auditor", page_icon="🌱", layout="wide")

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
    .status-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e2130;
        border: 1px solid #1d976c;
    }
    .report-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 5px solid #1d976c;
    }
    .metric-container {
        text-align: center;
        padding: 20px;
        background: #1e2130;
        border-radius: 15px;
        border: 2px solid #1d976c;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Site Sustainability Auditor")
st.write("Specialized evaluation for Mostadam Credits **SS-01, SS-02, and SS-05**.")

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
        with st.status("🏗️ Auditing Site Sustainability...") as status:
            # 1. Save temp image
            with open("temp_plan_ss.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Extract Vision Features
            st.write("👁️ Analyzing Spatial Signals...")
            features = extract_features_with_vision("temp_plan_ss.png")
            
            # 3. Score against Markdown Rules
            st.write("📖 Cross-referencing Mostadam SS Guidelines...")
            result_json = score_site_sustainability(features)
            
            status.update(label="Audit Complete!", state="complete", expanded=False)

    # --- Display Results ---
    st.divider()
    
    try:
        data = json.loads(result_json)
        
        # 1. Big Score Metric
        score = data.get("score", 0)
        max_score = data.get("max_score", 6)
        
        st.markdown(f"""
            <div class="metric-container">
                <h1 style="color: #93f9b9; margin-bottom: 0;">{score} / {max_score}</h1>
                <p style="color: #8b949e; font-size: 1.2rem;">Site Sustainability Score</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. Executive Summary
        st.write("### 📝 Executive Summary")
        st.info(data.get("summary", "No summary available."))
        
        # 3. Detailed Report
        st.write("### 📋 Detailed Compliance Report")
        detailed = data.get("detailed_report", {})
        
        for credit, report in detailed.items():
            with st.container():
                st.markdown(f"""
                    <div class="report-card">
                        <h4 style="color: #1d976c; margin-top: 0;">{credit}</h4>
                        <p style="color: #c9d1d9;">{report}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # 4. Calculation Logic
        with st.expander("🔍 View Scoring Methodology & Vision Signals"):
            st.write(data.get("calculation_logic", "Logic not provided."))
            st.write("---")
            st.markdown("### 👁️ AI Vision: Extracted Site Signals")
            
            # Clean and render the vision signals
            signal_lines = features.split('\n')
            for line in signal_lines:
                clean_line = line.strip().replace("**", "")  # Remove markdown bolding
                if clean_line:
                    # Identify category headers by emojis
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
    st.info("Upload a plan to analyze Site Sustainability compliance.")

# Footer info
st.sidebar.markdown("---")
st.sidebar.write("**Scope Focus:**")
st.sidebar.write("- **SS-01:** Rainwater & Sewage")
st.sidebar.write("- **SS-02:** Ecological Protection")
st.sidebar.write("- **SS-05:** Heat Island Effect")
