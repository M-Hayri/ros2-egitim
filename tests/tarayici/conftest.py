"""Tarayıcı testleri için ortak düzen.

Derlenmiş site (`mkdocs build` çıktısı, varsayılan `site/`) yerel bir HTTP
sunucusundan verilir. Sayfanın dışarıya yaptığı istekler (Material'in Google
Fonts ve GitHub API istekleri) boş cevaplarla karşılanır; böylece testler
internetsiz de aynı sonucu verir ve hangi isteklerin yapıldığı kaydedilir.
"""

import functools
import http.server
import os
import pathlib
import threading

import pytest

KOK = pathlib.Path(__file__).resolve().parents[2]
SITE = pathlib.Path(os.environ.get("EGITIM_SITE", KOK / "site"))
EKRAN = pathlib.Path(os.environ.get("EGITIM_EKRAN", KOK / "tests" / "tarayici" / "ekran"))
KATALOG = "katki/bilesenler/"


class _SessizIsleyici(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def site_adresi():
    if not (SITE / "index.html").exists():
        pytest.fail(f"Derlenmiş site bulunamadı: {SITE}. Önce `mkdocs build --strict` çalıştır.")
    isleyici = functools.partial(_SessizIsleyici, directory=str(SITE))
    sunucu = http.server.ThreadingHTTPServer(("127.0.0.1", 0), isleyici)
    is_parcacigi = threading.Thread(target=sunucu.serve_forever, daemon=True)
    is_parcacigi.start()
    yield f"http://127.0.0.1:{sunucu.server_address[1]}/"
    sunucu.shutdown()


@pytest.fixture(scope="session")
def tarayici():
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        yield b
        b.close()


class Sayfa:
    """Bir Playwright sayfası ve onun konsol hataları ile ağ istekleri."""

    def __init__(self, page, adres):
        self.page = page
        self.adres = adres
        self.konsol_hatalari = []
        self.istekler = []
        page.on("console", lambda m: m.type == "error" and self.konsol_hatalari.append(m.text))
        page.on("pageerror", lambda e: self.konsol_hatalari.append(f"pageerror: {e}"))
        page.on("request", lambda r: self.istekler.append(r.url))

    def ac(self, yol=KATALOG):
        self.page.goto(self.adres + yol, wait_until="load")
        self.page.wait_for_selector("[data-egitim-widget][data-egitim-hazir]")
        return self


def _dis_istekleri_karsila(route):
    url = route.request.url
    if "api.github.com" in url:
        route.fulfill(status=200, content_type="application/json", body="{}")
    elif route.request.resource_type == "stylesheet":
        route.fulfill(status=200, content_type="text/css", body="")
    else:
        route.fulfill(status=204, body="")


@pytest.fixture
def sayfa_ac(tarayici, site_adresi):
    """sayfa_ac(genislik=..., tema="light"|"dark", depolama_kapali=False, hareket="reduce"|"no-preference")"""
    baglamlar = []

    def ac(genislik=1280, yukseklik=900, tema="light", depolama_kapali=False, baglam=None, hareket="reduce"):
        if baglam is None:
            baglam = tarayici.new_context(
                viewport={"width": genislik, "height": yukseklik},
                color_scheme=tema,
                reduced_motion=hareket,
            )
            baglam.route(lambda u: not u.startswith(site_adresi), _dis_istekleri_karsila)
            if depolama_kapali:
                # Çerezleri/site verisini engelleyen tarayıcılardaki davranış: erişim atar.
                baglam.add_init_script(
                    "Object.defineProperty(window, 'localStorage', {"
                    " get() { throw new DOMException('engellendi', 'SecurityError'); } });"
                )
            baglamlar.append(baglam)
        return Sayfa(baglam.new_page(), site_adresi)

    yield ac
    for b in baglamlar:
        b.close()
