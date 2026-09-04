# CANDO

CANDO is a privacy-focused writing and document tool that improves prose quality, removes formulaic AI-style writing patterns, cleans invisible Unicode and document metadata, and works inside Microsoft Word.

## Architecture

- **Backend:** Python 3.11+, FastAPI, Pydantic v2
- **Frontend:** React 18, TypeScript, Vite, TipTap
- **Word Add-in:** Office.js, React

## Installation

### Backend Setup
1. `python -m venv .venv`
2. `.venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in values.
5. Run: `uvicorn backend.main:app --host 127.0.0.1 --port 8765 --reload`

## License
See `THIRD_PARTY_NOTICES.md`.
