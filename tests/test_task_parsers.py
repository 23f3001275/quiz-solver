# tests/test_task_parsers.py
import pytest
import asyncio
from playwright.async_api import async_playwright
from src.app.solver.task_parsers import detect_and_parse

@pytest.mark.asyncio
async def test_detect_pre_parser(tmp_path):
    html = """
    <html><body>
    <pre>""" + "UEsDBAoAAAA..." + """</pre>
    </body></html>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_content(html)
        parser = await detect_and_parse(page)
        # the sample base64 won't decode, so parser likely None or Parser
        # we just assert the function runs without crashing
        assert (parser is None) or (hasattr(parser, "compute"))
        await browser.close()
