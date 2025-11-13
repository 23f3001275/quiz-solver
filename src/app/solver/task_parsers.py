# src/app/solver/task_parsers.py
"""
Detects task types from the rendered page and returns a parser object with:
- submit_url (str)
- compute(email, secret, page, remaining) -> dict payload to POST

This module includes a few generic parsers:
1. JSON-in-<pre> parser (like sample)
2. Table-sum parser: finds an HTML table and sums a column named 'value'
3. PDF-instruction parser: page contains link to PDF; parser downloads & computes
"""

import re
import json
import base64
import logging
from typing import Optional, Callable, Any
from ..submitter import download_binary
import pdfplumber
import io

logger = logging.getLogger("quiz-solver.parsers")

class Parser:
    def __init__(self, submit_url: str, compute: Callable):
        self.submit_url = submit_url
        self.compute = compute

async def detect_and_parse(page) -> Optional[Parser]:
    """
    Heuristic-based detection:
    - If page contains <pre> with base64 JSON like the sample -> parse it
    - If page contains a <table> with headers -> use table parser
    - If page contains link to PDF -> return pdf parser
    """
    content = await page.content()
    # 1) Try to find <pre> with base64 encoded payload (sample pages use atob)
    pre_text = await page.eval_on_selector("pre", "el => el.innerText", strict=False)
    if pre_text:
        # Try to decode base64 segments inside
        try:
            # sample page wrapped JSON inside atob encoded chunk - try to detect base64 block
            b64_matches = re.findall(r"[A-Za-z0-9+/=\n]{40,}", pre_text)
            for m in b64_matches:
                try:
                    decoded = base64.b64decode(m).decode("utf-8", errors="ignore")
                    # find JSON object inside decoded
                    js = re.search(r"\{.*\}", decoded, flags=re.DOTALL)
                    if js:
                        parsed = json.loads(js.group(0))
                        # create a parser that posts the answer field if provided
                        submit_url = parsed.get("submit_url") or "https://example.com/submit"
                        # create compute: simply return what `answer` suggests or compute if instruction present
                        async def compute(email, secret, page, remaining):
                            # if JSON contains 'answer' return; else try numeric 'answer' or 'ans'
                            payload = {
                                "email": email,
                                "secret": secret,
                                "url": (await page.url)
                            }
                            if "answer" in parsed:
                                payload["answer"] = parsed["answer"]
                            elif "ans" in parsed:
                                payload["answer"] = parsed["ans"]
                            else:
                                payload["answer"] = parsed.get("answer_suggested", None)
                            return payload
                        return Parser(submit_url, compute)
                except Exception:
                    continue
        except Exception:
            pass

    # 2) Table parser: find first visible <table> and look for header 'value'
    has_table = await page.query_selector("table")
    if has_table:
        # compute: find column index for header 'value' (case-insensitive)
        async def compute_table(email, secret, page, remaining):
            # extract headers
            headers = await page.eval_on_selector_all("table th, table thead th", "nodes => nodes.map(n => n.innerText.trim())")
            if not headers:
                # try first row as header
                headers = await page.eval_on_selector_all("table tr:first-child td", "nodes => nodes.map(n => n.innerText.trim())")
            idx = None
            for i, h in enumerate(headers):
                if h and h.strip().lower() == "value":
                    idx = i
                    break
            if idx is None:
                # fallback: try numeric column detection
                rows = await page.eval_on_selector_all("table tr", "nodes=> nodes.map(r => Array.from(r.querySelectorAll('td')).map(td=>td.innerText.trim()))")
                total = 0.0
                for r in rows[1:]:
                    for cell in r:
                        if re.match(r"^-?\d+(\.\d+)?$", cell.replace(",", "")):
                            total += float(cell.replace(",", ""))
                payload = {"email": email, "secret": secret, "url": (await page.url), "answer": total}
                return payload
            # else sum the column
            cells = await page.eval_on_selector_all(f"table tr td:nth-child({idx+1})", "nodes => nodes.map(n => n.innerText.trim())")
            total = 0.0
            for c in cells:
                s = c.replace(",", "")
                try:
                    total += float(s)
                except Exception:
                    continue
            return {"email": email, "secret": secret, "url": (await page.url), "answer": total}
        # attempt to get submit URL from page: try data-submit or form action
        submit_url = await page.eval_on_selector("form", "f => f ? f.action : null", strict=False) or (await page.get_attribute("body", "data-submit") or "https://example.com/submit")
        return Parser(submit_url, compute_table)

    # 3) PDF link parser: look for link with .pdf
    pdf_link = await page.eval_on_selector("a[href$='.pdf']", "a => a.href", strict=False)
    if pdf_link:
        async def compute_pdf(email, secret, page, remaining):
            # download PDF
            binary = await download_binary(pdf_link)
            # parse with pdfplumber: compute sum of column 'value' on page 2 (sample)
            with pdfplumber.open(io.BytesIO(binary)) as pdf:
                # sample: take page index 1 (page 2)
                if len(pdf.pages) >= 2:
                    p = pdf.pages[1]
                else:
                    p = pdf.pages[0]
                tables = p.extract_tables()
                total = 0.0
                for tbl in tables:
                    headers = [c.strip().lower() if c else "" for c in tbl[0]]
                    if "value" in headers:
                        idx = headers.index("value")
                        for row in tbl[1:]:
                            cell = row[idx]
                            try:
                                cell = cell.replace(",", "")
                                total += float(cell)
                            except Exception:
                                continue
                return {"email": email, "secret": secret, "url": (await page.url), "answer": total}
        # Try to extract submit endpoint from page text, else fallback
        submit_url = await page.eval_on_selector("body", "b => b.getAttribute('data-submit') || null", strict=False) or "https://example.com/submit"
        return Parser(submit_url, compute_pdf)

    # otherwise: no parser found
    return None
