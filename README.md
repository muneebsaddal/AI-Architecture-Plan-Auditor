# AI Architecture Plan Auditor

This project implements a Proof of Concept (PoC) for an AI-powered architectural plan evaluator. The system takes a floor plan image and a set of sustainability rules (in PDF format), extracts features and rules using AI (specifically LLMs and image processing), and then generates a sustainability score with detailed explanations based on the provided rules.

## Features
- **Intelligent PDF Parser**: Automatically extracts sustainability rules from the **Mostadam PDF** (Commercial Buildings D+C).
- **Vision-Based Feature Extraction**: Uses **GPT-4o Vision** to analyze floor plan layouts, identifying rooms, windows, doors, and spatial orientations without local dependencies.
- **AI Scoring Engine**: Evaluates identified features against summarized rules to provide a score (1-5) for Daylight, Ventilation, and Efficiency.
- **Rule Traceability**: Generates reports that clearly cite the specific rules used for the evaluation.
- **Modern UI**: A responsive Streamlit dashboard for interactive demos.

## 🛠️ Tech Stack
- **AI**: OpenAI GPT-4o (Vision) & GPT-4o-mini
- **Frontend**: Streamlit
- **PDF Processing**: pdfplumber
- **Backend Logic**: Python-dotenv & modular pipeline architecture

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   Rename `.env.example` to `.env` and add your `OPENAI_API_KEY`. Alternatively, enter it directly in the app sidebar.

3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Presentation Materials
- See `architecture_overview.md` for a high-resolution Mermaid flowchart of the system architecture.
