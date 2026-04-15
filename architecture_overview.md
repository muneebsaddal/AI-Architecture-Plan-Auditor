# AI Architecture Plan Auditor - System Architecture

This flowchart illustrates the end-to-end process of the AI Architecture Plan Auditor. It showcases how independent rule extraction and spatial vision analysis are combined to provide a verified sustainability assessment.

```mermaid
graph TD
    %% Inputs
    subgraph Inputs ["Inputs"]
        PDF["Mostadam Rules (PDF)"]
        IMG["Floor Plan (Image)"]
    end

    %% PDF Processing
    subgraph Rule_Extraction ["Rule Processing (AI)"]
        PDF --> P1["PDF Text Extraction<br/>(pdfplumber)"]
        P1 --> P2["Rule Summarization & <br/>Criteria Extraction<br/>(GPT-4o-mini)"]
    end

    %% Image Processing
    subgraph Signal_Extraction ["Signal Extraction (Vision)"]
        IMG --> V1["Spatial Analysis<br/>(GPT-4o Vision)"]
        V1 --> V2["Extracted Features:<br/>- Rooms & Sizes<br/>- Windows & Doors<br/>- Daylighting Signals"]
    end

    %% Logic Core
    subgraph Logic ["Compliance Engine"]
        P2 --> SC["Architecture Scorer<br/>(LLM Reasoning)"]
        V2 --> SC
        SC --> RL["Apply Rules Matrix<br/>(Daylight / Vent / Space)"]
    end

    %% Outputs
    subgraph Outputs ["Report Generation"]
        RL --> SCR["Sustainability Score<br/>(1-5 Scale)"]
        RL --> RT["Rule Traceability<br/>(Citing Mostadam Rules)"]
        RL --> SUM["Actionable Summary<br/>& UX Feedback"]
    end

    %% Styling
    style Inputs fill:#1e2130,stroke:#4facfe,stroke-width:2px,color:#fff
    style Rule_Extraction fill:#2c3e50,stroke:#00f2fe,color:#fff
    style Signal_Extraction fill:#2c3e50,stroke:#00f2fe,color:#fff
    style Logic fill:#162447,stroke:#e94560,stroke-width:3px,color:#fff
    style Outputs fill:#1b1b2f,stroke:#4facfe,color:#fff
```

### 🧠 Strategic Advantage for Presentation:
- **Scalability**: New rules (e.g., Leed, Well) can be added simply by uploading a new PDF.
- **Explainability**: Unlike a "black box," our system cites its sources.
- **Advanced Vision**: We use proprietary Vision LLMs to understand complex spatial relationships in floor plans.
