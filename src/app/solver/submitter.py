# src/app/submitter.py
import httpx
import logging

logger = logging.getLogger("quiz-solver.submitter")

async def post_json(url: str, payload: dict, timeout: int = 20):
    """
    POST JSON and return parsed JSON response.
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

async def download_binary(url: str, timeout: int = 30) -> bytes:
    """
    Download binary data (PDF, etc.)
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.content
