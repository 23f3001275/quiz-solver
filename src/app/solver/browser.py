# src/app/solver/browser.py
import asyncio
from playwright.async_api import async_playwright, Browser, Page
import logging

logger = logging.getLogger("quiz-solver.browser")

class BrowserManager:
    def __init__(self):
        self._playwright = None
        self._browser: Browser | None = None
        self._lock = asyncio.Lock()

    async def start(self):
        async with self._lock:
            if self._browser is None:
                self._playwright = await async_playwright().start()
                self._browser = await self._playwright.chromium.launch(headless=True, args=["--no-sandbox"])
                logger.info("Playwright browser started")

    async def new_page(self) -> Page:
        if self._browser is None:
            await self.start()
        context = await self._browser.new_context()
        page = await context.new_page()
        return page

    async def stop(self):
        async with self._lock:
            if self._browser:
                try:
                    await self._browser.close()
                except Exception:
                    pass
                self._browser = None
            if self._playwright:
                try:
                    await self._playwright.stop()
                except Exception:
                    pass
                self._playwright = None
            logger.info("Playwright browser stopped")
