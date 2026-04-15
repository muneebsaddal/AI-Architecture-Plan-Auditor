# AI Architecture Plan Auditor

This project implements a Proof of Concept (PoC) for an AI-powered architectural plan evaluator. The system takes a floor plan image and a set of sustainability rules (in PDF format), extracts features and rules using AI (specifically LLMs and image processing), and then generates a sustainability score with detailed explanations based on the provided rules.

## Planned Features
- **PDF Parser**: Extract text from Mostadam sustainability rule PDFs.
- **Rule Extraction**: Use LLMs to summarize and extract key rules from the PDF.
- **Feature Extraction**: Identify rooms and layout features from floor plan images.
- **AI Scoring**: Apply extracted rules to floor plan features using GPT-4o-mini to generate scores and feedback.
- **Interactive UI**: A Streamlit-based application for easy file uploads and result visualization.
