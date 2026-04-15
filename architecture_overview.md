# AI Architecture Plan Auditor - System Architecture

This flowchart illustrates the end-to-end process of the AI Architecture Plan Auditor. It showcases how independent rule extraction and spatial vision analysis are combined to provide a verified sustainability assessment.

```mermaid
graph TD
    %% Inputs
    subgraph Inputs ["Inputs"]
        MD["Mostadam Rules (Markdown)"]
        IMG["Floor Plan / Site Plan (Image)"]
    end

    %% Rule Processing
    subgraph Rule_Processing ["Focused SS Evaluation"]
        MD --> P1["Direct Content Access<br/>(Full Context)"]
        P1 --> P2["Sustainability Criteria:<br/>- SS-01: Rainwater & Sewage<br/>- SS-02: Ecological Assessment<br/>- SS-05: Heat Island Effect"]
    end

    %% Image Processing
    subgraph Signal_Extraction ["Site Signal Extraction (Vision)"]
        IMG --> V1["Spatial Analysis<br/>(GPT-4o Vision)"]
        V1 --> V2["Detected Signals:<br/>- Drainage/Grease Traps<br/>- Vegetated Areas<br/>- Site Coverage"]
    end

    %% Logic Core
    subgraph Logic ["Compliance Engine"]
        P2 --> SC["SS Scorer<br/>(LLM Reasoning)"]
        V2 --> SC
        SC --> RL["Verify Keystone Compliance<br/>(Fail/Pass Logic)"]
    end

    %% Outputs
    subgraph Outputs ["Audit Report"]
        RL --> SCR["SS Score<br/>(Total / 6 pts)"]
        RL --> SUM["Executive Summary"]
        RL --> RT["Detailed Compliance<br/>(Methodology & Logic)"]
    end

    %% Styling
    style Inputs fill:#1e2130,stroke:#1d976c,stroke-width:2px,color:#fff
    style Rule_Processing fill:#2c3e50,stroke:#93f9b9,color:#fff
    style Signal_Extraction fill:#2c3e50,stroke:#93f9b9,color:#fff
    style Logic fill:#0b3c2c,stroke:#1d976c,stroke-width:3px,color:#fff
    style Outputs fill:#1b1b2f,stroke:#1d976c,color:#fff
```

### 🧠 Strategic Advantage for Presentation:
- **Focused Compliance**: Specifically targets high-impact Site Sustainability (SS) credits.
- **Keystone Verification**: Automatically flags missing Keystone requirements (SS-01/SS-02) which are critical for certification.
- **Markdown-Optimized**: Transitioned to Markdown for maximum token efficiency and faster analysis.
- **Transparent Scoring**: The "6-Point" system clearly separates Baseline (Keystone) from Optional performance.
