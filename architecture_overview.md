# AI Architecture Plan Auditor — System Architecture

End-to-end pipeline combining multimodal vision AI, regulatory knowledge injection, and structured LLM reasoning to produce evidence-based sustainability compliance verdicts from raw floor plan images.

---

## 🎯 Simplified Overview *(presentation)*

```mermaid
flowchart LR
    A(["🖼️ Floor Plan\nImage"]) --> B["👁️ Vision AI\nGPT-4o"]
    B --> C["🧮 Compliance\nScorer"]
    D(["📄 Mostadam\nRuleset"]) --> C
    C --> E(["📊 Audit\nReport"])

    style A fill:#1e2130,stroke:#1d976c,stroke-width:2px,color:#c9d1d9
    style B fill:#0b3c2c,stroke:#93f9b9,stroke-width:2px,color:#c9d1d9
    style C fill:#0b3c2c,stroke:#93f9b9,stroke-width:2px,color:#c9d1d9
    style D fill:#1e2130,stroke:#1d976c,stroke-width:2px,color:#c9d1d9
    style E fill:#1b1b2f,stroke:#4a9eff,stroke-width:2px,color:#c9d1d9
```

---

## 🔬 Detailed System Flow *(technical reference)*

```mermaid
flowchart TD
    %% ── Inputs ──────────────────────────────────────────────
    subgraph IN["📥 Inputs"]
        IMG["🖼️ Floor Plan Image\n(PNG / JPG upload)"]
        KEY["🔑 OpenAI API Key\n(sidebar → saved to .env)"]
        MD["📄 Mostadam Ruleset\n(399 KB Markdown)"]
    end

    %% ── Stage 1: Vision ──────────────────────────────────────
    subgraph VISION["👁️ Stage 1 — Visual Feature Extraction"]
        VP["image_processor.py\nGPT-4o Vision API"]
        VF["Detected Features\n🚰 Site Services\n🍳 Food Service / Grease Traps\n🌦️ Water Management\n🌳 Ecological Assets\n🔥 Heat Island Signals\n📐 Spatial Coverage"]
        IMG --> VP
        KEY --> VP
        VP -->|"max_tokens: 1000"| VF
    end

    %% ── Stage 2: Rules + Scoring ─────────────────────────────
    subgraph SCORE["🧮 Stage 2 — Compliance Scoring Engine"]
        SC["scorer.py\nGPT-4o JSON-mode"]
        RULES["Mostadam Rules\nSS-01 · SS-02 · SS-05\nInjected as full context"]
        PROMPT["Strict Evidence Prompt\n• No assumptions\n• 25% assumption cap\n• Keystone pass/fail logic\n• JSON schema enforced"]
        MD --> RULES
        RULES --> SC
        VF --> SC
        KEY --> SC
        PROMPT --> SC
    end

    %% ── Stage 3: JSON Output ─────────────────────────────────
    subgraph JSON["📦 Stage 3 — Structured Audit Output"]
        J1["summary\n3–5 sentence executive verdict"]
        J2["credits.SS-01\npoints · max · keystone_met · explanation"]
        J3["credits.SS-02\npoints · max · keystone_met · explanation"]
        J4["credits.SS-05\npoints · max · explanation"]
        J5["audit_report\nDetailed narrative ≥ 150 words"]
        SC -->|"response_format: json_object"| J1
        SC --> J2
        SC --> J3
        SC --> J4
        SC --> J5
    end

    %% ── Stage 4: Persistence ─────────────────────────────────
    subgraph CACHE["💾 Stage 4 — Disk Persistence"]
        DISK[".audit_cache/*.json\nImage bytes + result JSON\nKeyed by filename MD5"]
        RESTORE["Auto-restore on page reload\nload_latest_cache()"]
        J1 --> DISK
        J2 --> DISK
        J3 --> DISK
        J4 --> DISK
        J5 --> DISK
        DISK -->|"on fresh load"| RESTORE
    end

    %% ── Stage 5: Dashboard ───────────────────────────────────
    subgraph UI["🎨 Stage 5 — Streamlit Dashboard"]
        SCORE_CARD["🏆 Score Card\nTotal / 6 pts"]
        SUMMARY["📝 Executive Summary"]
        CARDS["📋 Credit Cards\nSS-01 · SS-02 · SS-05\nKeystone badges · Point display"]
        REPORT["📄 Detailed Audit Report\nFull narrative reasoning"]
        RESTORE --> SCORE_CARD
        J1 --> SUMMARY
        J2 --> CARDS
        J3 --> CARDS
        J4 --> CARDS
        J5 --> REPORT
    end

    %% ── Styling ──────────────────────────────────────────────
    style IN fill:#1a1f2e,stroke:#1d976c,stroke-width:2px,color:#c9d1d9
    style VISION fill:#0f2027,stroke:#93f9b9,stroke-width:2px,color:#c9d1d9
    style SCORE fill:#0b3c2c,stroke:#1d976c,stroke-width:3px,color:#c9d1d9
    style JSON fill:#1b1b2f,stroke:#4a9eff,stroke-width:2px,color:#c9d1d9
    style CACHE fill:#1e1e2e,stroke:#f7c948,stroke-width:2px,color:#c9d1d9
    style UI fill:#161b22,stroke:#1d976c,stroke-width:2px,color:#c9d1d9
```

---

## Component Responsibilities

| Component | File | Role |
|---|---|---|
| **Vision Extractor** | `pipeline/image_processor.py` | GPT-4o Vision → structured feature text |
| **Compliance Scorer** | `pipeline/scorer.py` | Rules + features → JSON audit verdict |
| **Disk Cache** | `app.py` → `.audit_cache/` | Persist results across page reloads |
| **Dashboard** | `app.py` | Render score, summary, cards, report |
| **Ruleset** | `Mostadam_Commercial_Buildings_DC.md` | Single source of grading truth |

---

## Design Principles

### 🔒 Strict Evidence-Only Scoring
The LLM prompt enforces a **25% assumption cap**. Features that cannot be visually confirmed (flood zone status, SRI values) are automatically flagged as *"Requires External Documentation"* rather than assumed compliant.

### ⚠️ Keystone-First Architecture
SS-01 and SS-02 are **Keystone credits** — mandatory prerequisites for Mostadam certification. The system surfaces keystone failures prominently with colour-coded badges before optional credits are considered.

### 📦 JSON-Mode Determinism
Using `response_format: { type: "json_object" }` on GPT-4o guarantees the scorer always returns a parsable, schema-compliant response — eliminating brittle string parsing and making the pipeline production-safe.

### 💾 Resilient State Management
Streamlit session state is ephemeral. The disk cache (`MD5-keyed JSON`) decouples audit results from the server process lifecycle, ensuring results survive restarts, network drops, and browser refreshes.

### 🔑 Late-Binding API Key
The `OpenAI` client is instantiated at **call-time** in both pipeline modules — not at module-import time. This ensures the key entered by the user in the sidebar is always the one used, with no stale-key bugs.
