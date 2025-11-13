# Architecture

## Overview
The system receives quiz tasks via POST `/api/v1/quiz`. It validates a secret, acknowledges the request (HTTP 200), and launches an asynchronous solver that:
1. Renders the JS-heavy quiz page using Playwright.
2. Detects the quiz type and extracts instructions / submission URL.
3. Computes the answer (data scraping, PDF parsing, tables, etc.).
4. Submits the answer to the page-provided endpoint.
5. Repeats when a new URL is returned.

## Components
- FastAPI: HTTP API, validation
- Playwright: headless browser for JS rendering
- pdfplumber, PyPDF2: PDF parsing
- httpx: async HTTP client for submission & downloads

## Time Budget
- Entire solve sequence must complete within 3 minutes. We use TOTAL_TIME_BUDGET=170s to leave margin.
- Each network call uses timeouts; parser must check remaining time.

## Prompts
- `prompts/system_prompt.txt` and `prompts/user_prompt.txt` are included for the jailbreaking test.
- Keep them <=100 chars.

## Security
- SECRET set in environment variable `EXPECTED_SECRET`
- Do not log secrets or post them unintentionally.
