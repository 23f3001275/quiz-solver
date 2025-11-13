# Quiz Solver (FastAPI + Playwright)

Automatic quiz-solving framework for data-driven quizzes (JS-rendered pages).
Designed for the "TDS LLM Analysis" assignment.

## Features
- FastAPI server to receive quiz tasks
- Playwright headless browser to render JS pages
- Modular parsers for extracting tasks from pages
- Safe secret validation (env-based)
- Auto-submission to provided submit URLs
- Prompts stored in files for evaluation (system + user)
- Dockerfile for containerized deployment
- Basic tests and CI workflow

## Quickstart (local)
1. Clone repo
2. Create virtualenv & activate
3. `pip install -r requirements.txt`
4. `playwright install`
5. Set environment variables:
   - `EXPECTED_SECRET=your_secret`
   - Optionally `HOST=0.0.0.0` and `PORT=8000`
6. Start server:
