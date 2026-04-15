import streamlit as st
import os
import json
from pipeline.pdf_parser import extract_pdf_text
from pipeline.scorer import extract_rules, score_plan
from pipeline.image_processor import extract_features_with_vision
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Floorplan Auditor", page_icon="🏗️", layout="wide")

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
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
        border: 1px solid #4facfe;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏗️ AI Architecture Plan Auditor")
st.write("Evaluate floor plans against Mostadam sustainability rules automatically.")

# Minimal UI - Mostadam PDF is hardcoded
PDF_PATH = "Mostadam for Commercial Buildings (D+C).pdf"

if not os.path.exists(PDF_PATH):
    st.error(f"Missing rules file: {PDF_PATH}. Please ensure it is in the project root.")
    st.stop()

# Sidebar for API config or status
with st.sidebar:
    st.header("Settings")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter OpenAI API Key", type="password")
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    if api_key:
        st.success("API Key Active")
    else:
        st.warning("Please provide an API Key.")

uploaded_file = st.file_uploader("Upload Floor Plan Image", type=["png", "jpg", "jpeg"])

if uploaded_file and api_key:
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(uploaded_file, caption="Uploaded Floor Plan", use_container_width=True)
        
    with col2:
        with st.status("🚀 Processing...", expanded=True) as status:
            # 1. Save temp image
            with open("temp_plan.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # 2. Extract Rules (Cache this in a real app, but here we do it once)
            st.write("🔍 Extracting Sustainability Rules...")
            pdf_text = extract_pdf_text(PDF_PATH)
            rules = extract_rules(pdf_text)
            
            # 3. Extract Image Features
            st.write("🧠 Analyzing Floor Plan Layout...")
            features = extract_features_with_vision("temp_plan.png")
            
            # 4. Scoring
            st.write("⚖️ Evaluating Compliance...")
            result_json = score_plan(features, rules)
            
            status.update(label="Analysis Complete!", state="complete", expanded=False)

    # Display Results
    st.divider()
    
    try:
        data = json.loads(result_json)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Daylight", f"{data.get('daylight', 0)}/5")
        c2.metric("Ventilation", f"{data.get('ventilation', 0)}/5")
        c3.metric("Efficiency", f"{data.get('efficiency', 0)}/5")
        
        st.subheader("Summary")
        st.info(data.get("summary", "No summary available."))
        
        st.subheader("Rule Traceability")
        st.code(data.get("traceability", "No traceability data."))
        
    except Exception as e:
        st.subheader("Raw Analysis")
        st.write(result_json)
    
    with st.expander("View Extracted Signals"):
        st.write("### Extracted Rules")
        st.write(rules)
        st.write("### Extracted Features")
        st.write(features)

else:
    if not uploaded_file:
        st.info("Please upload a floor plan image to begin evaluation.")
