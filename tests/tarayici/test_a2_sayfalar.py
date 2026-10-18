"""A2: Seviye 0 sayfaları tarayıcıda (S7 gerçek sayfada, S9, S10 ekran görüntüleri)."""

import pytest

from conftest import EKRAN

SAYFALAR = [
    "seviye-0/",
    "seviye-0/0-1-ros2-neden-var/",
    "seviye-0/0-2-ortam-ve-ros2/",
    "seviye-0/0-3-turtlesim-ve-rqt/",
    "baslarken/",
    "hazir-misin/",
]


def _ad(yol):
    return yol.strip("/").replace("/", "_") or "ana"


@pytest.mark.parametrize("yol", SAYFALAR, ids=_ad)
@pytest.mark.parametrize("tema", ["light", "dark"])
def test_s9_konsol_temiz_ve_375te_kaydirma_yok(sayfa_ac, yol, tema):
    s = sayfa_ac(genislik=375, yukseklik=812, tema=tema).ac(yol, bekle=None)
    p = s.page
    p.wait_for_load_state("networkidle")
    olcum = p.evaluate("() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth})")
    assert olcum["sw"] <= olcum["cw"], olcum
    assert p.locator(".eg-hata").count() == 0, p.locator(".eg-hata").all_inner_texts()
    # Sayfadaki her soru ve widget kurulmuş olmalı.
    assert p.locator(".egitim-soru:not([data-egitim-hazir])").count() == 0
    assert p.locator("[data-egitim-widget]:not([data-egitim-hazir])").count() == 0
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("yol", SAYFALAR, ids=_ad)
def test_s10_ekran_goruntuleri(sayfa_ac, yol):
    EKRAN.mkdir(parents=True, exist_ok=True)
    for genislik, tema in ((1280, "light"), (375, "dark")):
        s = sayfa_ac(genislik=genislik, yukseklik=900, tema=tema).ac(yol, bekle=None)
        s.page.wait_for_load_state("networkidle")
        s.page.add_style_tag(content=".md-header, .md-top { visibility: hidden !important; }")
        s.page.screenshot(path=str(EKRAN / f"sayfa-{_ad(yol)}-{tema}-{genislik}.png"), full_page=True)
        assert s.konsol_hatalari == []


def test_s7_gercek_sayfada_tekrar_bos_gelir(sayfa_ac):
    """0.1'de cevaplanan soru, 0.3'ün açılışında boş gelir; 0.1'deki kayıt durur."""
    s = sayfa_ac().ac("seviye-0/0-1-ros2-neden-var/")
    p = s.page
    p.click('.egitim-soru[data-soru-id="d0-1-hatirla-1"] button[data-secenek="3"]')
    p.goto(s.adres + "seviye-0/0-3-turtlesim-ve-rqt/", wait_until="load")
    tekrar = '.egitim-tekrar .egitim-soru[data-soru-id="d0-1-hatirla-1"]'
    p.wait_for_selector(f"{tekrar}[data-egitim-hazir]")
    assert p.locator(".egitim-tekrar .egitim-soru").count() == 2
    assert p.get_attribute(tekrar, "data-sonuc") is None
    p.click(f'{tekrar} button[data-secenek="1"]')  # tekrarda yanlış cevap
    p.goto(s.adres + "seviye-0/0-1-ros2-neden-var/", wait_until="load")
    p.wait_for_selector('.egitim-soru[data-soru-id="d0-1-hatirla-1"][data-egitim-hazir]')
    assert p.get_attribute('.egitim-soru[data-soru-id="d0-1-hatirla-1"]', "data-sonuc") == "dogru"
    assert s.konsol_hatalari == []


def test_gizli_ogeler_gorunmez(sayfa_ac):
    """`hidden` niteliği taşıyan öğe (ör. cevap öncesi "Tekrar dene") ekranda görünmemeli.
    A2'de ekran görüntüsünden bulundu: .eg-dugme'nin display kuralı hidden'ı eziyordu."""
    s = sayfa_ac().ac("seviye-0/0-3-turtlesim-ve-rqt/", bekle=".egitim-soru[data-egitim-hazir]")
    p = s.page
    gorunen = p.evaluate(
        "() => [...document.querySelectorAll('.eg-kutu [hidden]')]"
        ".filter(e => getComputedStyle(e).display !== 'none').map(e => e.className)"
    )
    assert p.locator(".eg-kutu [hidden]").count() > 0
    assert gorunen == [], gorunen
