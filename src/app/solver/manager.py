# src/app/solver/manager.py
import asyncio
import logging
from typing import Optional
from ..solver.browser import BrowserManager
from ..solver.task_parsers import detect_and_parse
from ..submitter import post_json

logger = logging.getLogger("quiz-solver")
logging.basicConfig(level=logging.INFO)

# Total time budget (seconds) to solve starting from receiving POST (must be < 180)
TOTAL_TIME_BUDGET = 170

async def _solve_loop(email: str, secret: str, start_url: str):
    """
    Main loop: visit start_url, parse the task, compute answer, submit, handle next URL.
    """
    start_time = asyncio.get_event_loop().time()
    remaining = lambda: TOTAL_TIME_BUDGET - (asyncio.get_event_loop().time() - start_time)

    browser_mgr = BrowserManager()
    await browser_mgr.start()

    try:
        url = start_url
        while url and remaining() > 5:  # leave small margin
            logger.info("Visiting %s (remaining %.1fs)", url, remaining())
            page = await browser_mgr.new_page()
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
            except Exception as e:
                logger.exception("Page.goto failed: %s", e)
            # Detect parser
            parser = await detect_and_parse(page)
            if parser is None:
                logger.warning("No parser detected for %s", url)
                await page.close()
                break
            # Compute answer payload
            try:
                payload = await parser.compute(email, secret, page, remaining)
            except Exception as e:
                logger.exception("Error computing answer: %s", e)
                await page.close()
                break

            # Submit
            try:
                resp = await post_json(parser.submit_url, payload, timeout=30)
                logger.info("Submit response: %s", resp)
            except Exception as e:
                logger.exception("Submit failed: %s", e)
                await page.close()
                break

            # Decide next URL
            next_url = resp.get("url")
            correct = resp.get("correct")
            if correct is True and next_url:
                url = next_url
            elif correct is False and next_url:
                # allow to move to next if server provided
                url = next_url
            else:
                # finish
                url = None

            await page.close()
    finally:
        await browser_mgr.stop()

def solve_quiz_background(email: str, secret: str, url: str):
    """
    Synchronous wrapper called by FastAPI BackgroundTasks.
    It creates an asyncio task to run the solver loop.
    """
    loop = asyncio.get_event_loop()
    # schedule the coroutine
    loop.create_task(_solve_loop(email, secret, url))
