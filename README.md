# FreshCheck AI – Verify What You Read

**An AI-powered answer verification and freshness detection platform.**

FreshCheck AI helps users evaluate AI-generated answers by extracting factual claims, searching for live web evidence, and identifying information that may be outdated.

## The Problem

AI-generated answers can contain:
- Incorrect or unsupported facts.
- Outdated information presented as current.
- Claims without reliable supporting evidence.

Users need a way to check not only whether an answer is correct, but also whether it is still correct today.

## Our Solution

FreshCheck AI acts as a verification layer between AI-generated answers and users.

It analyzes an answer, extracts factual claims, searches the web for supporting evidence, and uses AI to evaluate each claim.

## Key Features

- **Automatic Claim Extraction:** Identifies factual claims from an answer.
- **Live Web Evidence:** Retrieves relevant information using Tavily.
- **AI-Powered Verification:** Uses Gemini through the Bifrost AI gateway.
- **Source Ranking:** Organizes evidence using domain-based credibility heuristics.
- **Four Verification Verdicts:**
  - Supported
  - Contradicted
  - Potentially Outdated
  - Insufficient Evidence
- **Freshness Score:** Provides an overall evidence-based freshness assessment.
- **Suggested Corrections:** Helps users understand how claims could be improved.
- **Evidence Links:** Provides links to sources for further checking.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend logic |
| Flask | Web application |
| HTML & CSS | Dashboard interface |
| Gemini | AI claim verification |
| Tavily API | Live web search |
| Bifrost | AI gateway |
| JSON | Verification report data |

## How It Works

1. User submits an AI-generated answer.
2. FreshCheck AI extracts factual claims.
3. Tavily searches for relevant web evidence.
4. Evidence is ranked using source-domain heuristics.
5. Gemini evaluates each claim against the retrieved evidence.
6. The system generates verdicts, explanations, corrections, and a freshness score.
7. Results are displayed on the dashboard.

## Project Architecture

```text
User Input
    |
    v
Flask Dashboard
    |
    v
Claim Extraction
    |
    v
Live Web Search (Tavily)
    |
    v
Evidence Ranking
    |
    v
AI Verification (Gemini via Bifrost)
    |
    v
Freshness Analysis
    |
    v
Verification Dashboard
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sagar1050/FreshCheck-AI.git
cd FreshCheck-AI
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure your own API credentials and Bifrost settings.

Do not upload API keys or other secrets to GitHub.

### 6. Start Bifrost

Start your local Bifrost instance and configure your Gemini provider and model.

### 7. Run the application

```bash
python app.py
```

Open the dashboard at:

http://127.0.0.1:5000

## Example Use Cases

- Students checking AI-generated study material.
- Researchers validating factual information.
- Developers verifying technical answers.
- Content creators checking facts before publishing.
- Businesses reviewing AI-generated reports.

## Future Scope

- Browser extension for instant answer verification.
- Public verification API.
- Verification history and downloadable reports.
- Multilingual claim verification.
- Improved source-quality evaluation.
- Enterprise verification dashboard.

## Impact

FreshCheck AI aims to improve trust in AI-generated information by combining live web evidence with AI-powered claim analysis.

**We don't just ask whether an AI answer is correct. We also ask whether it is still correct today.**

## Project Links

- **GitHub:** https://github.com/Sagar1050/FreshCheck-AI

---

**FreshCheck AI – Verify What You Read. Trust What You Verify.**