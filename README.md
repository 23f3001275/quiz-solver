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
`pip install -r requirements.txt`
`playwright install`
3. Set environment variables:
   - `EXPECTED_SECRET=your_secret`
   - Optionally `HOST=0.0.0.0` and `PORT=8000`
4. Start server:
   `uvicorn src.app.main:app --host 0.0.0.0 --port 8000`
5. Test with demo:
`curl -X POST https://<your-host>/api/v1/quiz
-H "Content-Type: application/json"
-d '{"email":"you@example.com
","secret":"<your_secret>","url":"https://tds-llm-analysis.s-anand.net/demo"}
'`

## File layout
See `docs/architecture.md` for design, API and viva notes.

## License
MIT
