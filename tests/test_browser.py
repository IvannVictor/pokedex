"""Testes de regressão da Pokédex em navegador Chromium real."""
import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def run():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                try:
                    for width in (320, 390, 768, 1440):
                        page = browser.new_page(viewport={"width": width, "height": 900})
                        errors = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.route("https://fonts.googleapis.com/**", lambda route: route.abort())
                        page.route("https://fonts.gstatic.com/**", lambda route: route.abort())
                        page.goto(f"http://127.0.0.1:{server.server_port}/index.html")
                        assert page.locator(".cartao-pokemon").count() == 10
                        assert page.locator("#botao-alterar-tema").get_attribute("aria-label")
                        assert page.locator("main#inicio").count() == 1
                        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"Overflow em {width}px"
                        assert page.locator("body").evaluate("(el) => !el.classList.contains('modo-escuro')")
                        page.locator("#botao-alterar-tema").click()
                        assert page.locator("body").evaluate("(el) => el.classList.contains('modo-escuro')")
                        assert "moon.png" in page.locator(".imagem-botao").get_attribute("src")
                        page.locator("#botao-alterar-tema").click()
                        assert page.locator("body").evaluate("(el) => !el.classList.contains('modo-escuro')")
                        page.locator("#botao-alterar-tema").focus()
                        page.keyboard.press("Enter")
                        assert page.locator("body").evaluate("(el) => el.classList.contains('modo-escuro')")
                        assert not errors, errors
                        print(f"PASS: Pokédex {width}px, tema, teclado e layout")
                        page.close()
                finally:
                    browser.close()
        finally:
            server.shutdown()


if __name__ == "__main__":
    run()
