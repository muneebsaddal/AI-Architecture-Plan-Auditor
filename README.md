# 🌱 Mostadam Site Sustainability Auditor

This project implements a specialized **AI-powered Auditor** for evaluating architectural site and floor plans against the **Mostadam Sustainability Guidelines**. 

It specifically focuses on the **Site Sustainability (SS)** category, automating the verification of Keystone requirements and calculating a compliance score for key credits.

## 🚀 Features
- **Markdown-Driven Intelligence**: Analyzes the full Mostadam ruleset using high-fidelity Markdown sources for maximum accuracy.
- **Vision-Powered Site Analysis**: Uses **GPT-4o Vision** to "see" architectural features such as drainage systems, grease traps, and ecological footprints.
- **Specialized Credit Scope**:
    - **SS-01**: Sewage, Flood, and Rainwater Management (Keystone).
    - **SS-02**: Ecological Assessment & Protection (Keystone).
    - **SS-05**: Heat Island Effect Mitigation (Optional).
- **Compliance Scorer**: Provides a single **Site Sustainability Score (out of 6 pts)** with a detailed methodology report.
- **Keystone Alerts**: Automatically flags failure to meet mandatory Keystone requirements.

## ⚙️ Tech Stack
- **LLM**: OpenAI GPT-4o (Vision) & GPT-4o-mini
- **UI**: Streamlit (Premium Dark Mode Dashboard)
- **Ruleset**: Markdown-based Mostadam Commercial D+C guidelines.

## 🖥️ Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Create a `.env` file with your `OPENAI_API_KEY` or enter it directly in the app sidebar.

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Documentation & Presentation
- **Architecture Overview**: See [architecture_overview.md](architecture_overview.md) for the system flowchart and strategic advantages for presentation.
- **Ruleset**: The auditor uses the [Mostadam_Commercial_Buildings_DC.md](Mostadam_Commercial_Buildings_DC.md) as its ground truth ruleset.
