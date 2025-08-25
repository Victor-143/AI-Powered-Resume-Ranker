# AI-Powered Resume Ranker (Flask + NLP)

An end-to-end mini app that ranks uploaded resumes for a given job description using SpaCy preprocessing + TF‑IDF cosine similarity + a keyword boost. Includes a simple web UI, CSV download for HR, and sample outputs.

## Quickstart

```bash
cd resume-ranker
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
# open http://localhost:5000
```

## Notes
- PDF text is extracted with PyPDF2; scanned/image-only PDFs won't yield text (use OCR if needed).
- The `alpha` slider blends cosine similarity with keyword coverage.
- Reports are cached in memory for the current app run; in production, persist to a DB or S3.
