# 🏗️ AI Architecture Plan Auditor

> **An AI-powered proof-of-concept that audits architectural floor plans against green building sustainability standards — combining multimodal vision AI, structured LLM reasoning, and a premium real-time dashboard.**

---

## 🎯 What This Project Does

Traditional sustainability audits require a certified consultant to manually review drawings for hours. This project replaces that effort with a **three-stage AI pipeline** that:

1. **Sees** the floor plan using GPT-4o Vision — detecting drainage systems, ecological zones, roof types, and kitchen layouts.
2. **Reasons** against the official Mostadam ruleset — a 399 KB Markdown-parsed knowledge base — applying strict evidence-only scoring logic.
3. **Reports** a structured compliance verdict — per-credit scores, keystone pass/fail flags, a narrative executive summary, and a detailed audit report — all rendered in an interactive Streamlit dashboard.

---

## ✨ Key Technical Highlights

| Capability | Implementation |
|---|---|
| 🖼️ **Multimodal AI** | GPT-4o Vision for visual feature extraction from 2D architectural images |
| 🧠 **Structured LLM Reasoning** | GPT-4o JSON-mode for deterministic, schema-enforced audit scoring |
| 📄 **Domain Knowledge Injection** | 399 KB Mostadam regulatory Markdown injected as full LLM context |
| 🔒 **Strict Evidence Mode** | 25% assumption cap enforced in prompt — AI cannot fill gaps with assumptions |
| ⚠️ **Keystone Logic** | Automatic pass/fail detection for mandatory certification prerequisites |
| 💾 **Cross-Reload Persistence** | Disk-based JSON cache — audit results survive full browser/server reloads |
| 🔑 **Secure Key Management** | API key persisted to `.env` via `python-dotenv` — survives server restarts |
| 🎨 **Premium UI** | Dark-mode Streamlit dashboard with custom CSS, glassmorphism cards, gradient buttons |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    Streamlit Dark Dashboard                      │
└──────────────┬──────────────────────────┬───────────────────────┘
               │                          │
       Upload Image                  API Key (→ .env)
               │                          │
               ▼                          ▼
┌──────────────────────┐     ┌──────────────────────────────────┐
│  image_processor.py  │     │         scorer.py                │
│                      │     │                                  │
│  GPT-4o Vision API   │────▶│  GPT-4o (JSON mode)              │
│  Feature Extraction  │     │  + Mostadam Rules (399 KB MD)    │
│                      │     │  + Strict Evidence Prompt        │
└──────────────────────┘     └───────────────┬──────────────────┘
                                             │
                                    Structured JSON
                                             │
                              ┌──────────────▼──────────────┐
                              │        Disk Cache            │
                              │    .audit_cache/*.json       │
                              │  (persists across reloads)   │
                              └──────────────┬───────────────┘
                                             │
                              ┌──────────────▼──────────────┐
                              │       Dashboard Render       │
                              │  • Score (x/6)               │
                              │  • Executive Summary         │
                              │  • Credit Cards (SS-01/02/05)│
                              │  • Keystone Badges           │
                              │  • Detailed Audit Report     │
                              └─────────────────────────────┘
```

---

## 📋 Sustainability Credits Evaluated

### 🔴 SS-01 — Sewage, Flood & Rainwater Management *(Keystone | 3 pts)*
Verifies visible evidence of:
- Sewage network connection or on-site treatment plant
- Grease trap presence near kitchen/food service areas
- Rainwater management infrastructure

### 🔴 SS-02 — Ecological Assessment & Protection *(Keystone | 1 pt)*
Verifies visible evidence of:
- Ecological asset identification on site plan
- Protection measures for existing natural features

### 🟡 SS-05 — Heat Island Effect Mitigation *(Optional | 2 pts)*
Verifies visible evidence of:
- High-SRI roof/hardscape surfaces
- Vegetative cover over ≥70% of unused roof area

> **Keystone credits (SS-01, SS-02) are mandatory** — failing them flags certification risk regardless of total score.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- An OpenAI API key (GPT-4o access)

### Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd AI-Architecture-Plan-Auditor

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set your API key in .env
echo OPENAI_API_KEY=sk-... > .env

# 4. Launch the dashboard
streamlit run app.py
```

The app will open at `http://localhost:8501`. If no `.env` key is found, enter it in the sidebar — it will be saved automatically.

---

## 🗂️ Project Structure

```
AI-Architecture-Plan-Auditor/
├── app.py                              # Streamlit dashboard + session/cache logic
├── pipeline/
│   ├── image_processor.py              # GPT-4o Vision feature extraction
│   └── scorer.py                       # Mostadam rules + LLM compliance scoring
├── Mostadam_Commercial_Buildings_DC.md # Full regulatory ruleset (Markdown)
├── .audit_cache/                       # Auto-created disk cache (gitignored)
├── requirements.txt
└── architecture_overview.md            # System architecture & Mermaid diagram
```

---

## 🧠 Engineering Decisions

**Why Markdown over PDF?**  
PDFs are opaque to LLMs. Pre-converting the Mostadam standard to structured Markdown allows full-context injection with predictable token usage and no OCR artifacts.

**Why JSON-mode GPT-4o for scoring?**  
`response_format: json_object` guarantees schema compliance — the scorer never returns malformed output, making the pipeline fully deterministic and parse-safe.

**Why disk cache instead of Streamlit session state?**  
`st.session_state` is wiped on every full page reload. A local `.audit_cache/` directory survives restarts, network interruptions, and Streamlit re-initializations — critical for demos and client handovers.

**Why create the OpenAI client at call-time?**  
Module-level client instantiation captures the API key at import time — before the user enters it. Call-time instantiation ensures the live key is always used.

---

## 📄 License

This is a proprietary proof-of-concept developed for client demonstration. Not licensed for redistribution.
