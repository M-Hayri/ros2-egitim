"""A1 çıkış kriterleri W1–W6 için tarayıcı ve dosya testleri.

Beklenen davranış koşudan ÖNCE yazıldı (18 Ekim 2026) ve sonuçlara bakılarak
değiştirilmez. Değişmesi gerekirse yeni beklenti "keşif amaçlı" diye işaretlenir.
"""

import pathlib
import re

import pytest

from conftest import EKRAN, KATALOG, KOK

PARCALAR = ["kamera", "algilama", "planlayici", "motor", "kayitci"]

# W2 beklentisi. Anahtar: çökertilen parça.
#   tek program: beş parçanın beşi "durdu", robot duruyor.
#   node grafiği: yalnızca çöken "durdu"; ondan (doğrudan ya da dolaylı) beslenenler
#   "veri-gelmiyor"; geri kalanlar ayakta ve verisi geliyor; robot, motor_surucu'ya
#   veri geldiği sürece sürer.
BEKLENEN_VERI_GELMIYOR = {
    "kamera": {"algilama", "planlayici", "motor", "kayitci"},
    "algilama": {"planlayici", "motor"},
    "planlayici": {"motor"},
    "motor": set(),
    "kayitci": set(),
}
BEKLENEN_GRAF_ROBOT_SURUYOR = {
    "kamera": "hayir",
    "algilama": "hayir",
    "planlayici": "hayir",
    "motor": "hayir",
    "kayitci": "evet",
}
AYAKTA = {"calisiyor", "veri-geliyor"}


def _durumlar(page, model):
    return page.eval_on_selector_all(
        f'[data-model="{model}"] .eg-durum-listesi li',
        "els => Object.fromEntries(els.map(e => [e.dataset.parca, e.dataset.durum]))",
    )


def _robot(page, model):
    return page.get_attribute(f'[data-model="{model}"] .eg-robot', "data-suruyor")


# ---------- W1 ----------


def test_w1_widget_markdownda_tek_satir():
    """Kod bloğu dışındaki her widget gömmesi tam olarak tek satırlık biçimde."""
    desen = re.compile(r'^<div data-egitim-widget="[a-z0-9-]+"></div>$')
    bulunan = 0
    for md in (KOK / "docs").rglob("*.md"):
        kod_blogunda = False
        for no, satir in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            if satir.lstrip().startswith("```"):
                kod_blogunda = not kod_blogunda
                continue
            if kod_blogunda or "data-egitim-widget" not in satir:
                continue
            bulunan += 1
            assert desen.match(satir.strip()), f"{md}:{no} tek satırlık gömme biçiminde değil: {satir}"
    assert bulunan >= 1, "Hiçbir sayfada widget yok"


def test_w1_widget_sayfada_kuruluyor(sayfa_ac):
    s = sayfa_ac().ac()
    kok = s.page.locator('[data-egitim-widget="tek-program-node-grafigi"]')
    assert kok.count() == 1
    assert kok.get_attribute("data-egitim-hazir") == ""
    assert s.page.locator(".eg-tng .eg-panel").count() == 2
    assert s.konsol_hatalari == []


# ---------- W2 ----------


def test_w2_baslangicta_her_sey_ayakta(sayfa_ac):
    s = sayfa_ac().ac()
    assert set(_durumlar(s.page, "tek-program").values()) == {"calisiyor"}
    graf = _durumlar(s.page, "node-grafigi")
    assert graf["kamera"] == "calisiyor"
    assert all(graf[p] == "veri-geliyor" for p in PARCALAR if p != "kamera")
    assert _robot(s.page, "tek-program") == "evet"
    assert _robot(s.page, "node-grafigi") == "evet"
    assert s.page.locator('.eg-graf-kenar[data-akiyor="evet"]').count() == 4
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("parca", PARCALAR)
def test_w2_cokertince_beklenen_parcalar_duruyor(sayfa_ac, parca):
    s = sayfa_ac().ac()
    p = s.page
    p.click(f'.eg-tng-secim button[data-parca="{parca}"]')
    p.click('button[data-eylem="cokert"]')

    tek = _durumlar(p, "tek-program")
    assert tek == {k: "durdu" for k in PARCALAR}, tek
    assert _robot(p, "tek-program") == "hayir"

    graf = _durumlar(p, "node-grafigi")
    assert graf[parca] == "durdu"
    for diger in PARCALAR:
        if diger == parca:
            continue
        if diger in BEKLENEN_VERI_GELMIYOR[parca]:
            assert graf[diger] == "veri-gelmiyor", (diger, graf)
        else:
            assert graf[diger] in AYAKTA, (diger, graf)
    assert _robot(p, "node-grafigi") == BEKLENEN_GRAF_ROBOT_SURUYOR[parca]
    # Grafikteki kutu, listedeki durumla aynı.
    for k in PARCALAR:
        g = p.locator(".eg-graf-node").nth(PARCALAR.index(k))
        assert g.get_attribute("data-durum") == graf[k]
    assert " çöktü." in p.inner_text(".eg-ozet")
    assert s.konsol_hatalari == []


def test_w2_yeniden_baslat_her_seyi_geri_getirir(sayfa_ac):
    # A2 notu: A1'deki ortak "Hepsini yeniden başlat" düğmesi S4 gereği kaldırıldı.
    # Testin amacı aynı (yeniden başlatma her şeyi geri getirir); yalnızca basılan
    # düğmeler değişti: her çöken node'un kendi düğmesi ve "Programı yeniden başlat".
    s = sayfa_ac().ac()
    p = s.page
    for parca in ["kamera", "kayitci"]:
        p.click(f'.eg-tng-secim button[data-parca="{parca}"]')
        p.click('button[data-eylem="cokert"]')
    for parca in ["kamera", "kayitci"]:
        p.click(f'button[data-yeniden="{parca}"]')
    p.click('button[data-eylem="program-yeniden"]')
    assert set(_durumlar(p, "tek-program").values()) == {"calisiyor"}
    assert "durdu" not in _durumlar(p, "node-grafigi").values()
    assert _robot(p, "node-grafigi") == "evet"
    assert s.konsol_hatalari == []


def test_w2_bilinmeyen_widget_konsola_hata_duser(sayfa_ac):
    """Yazım hatası sessiz kalmasın: test bunu yakalayabilmeli."""
    s = sayfa_ac().ac()
    s.page.evaluate(
        "() => { const d = document.createElement('div');"
        " d.setAttribute('data-egitim-widget', 'boyle-bir-sey-yok');"
        " document.querySelector('article').appendChild(d); Egitim.baslat(); }"
    )
    assert any("Bilinmeyen widget" in h for h in s.konsol_hatalari)


# ---------- W3 ----------


@pytest.mark.parametrize("tema", ["light", "dark"])
def test_w3_375_pikselde_yatay_kaydirma_yok(sayfa_ac, tema):
    s = sayfa_ac(genislik=375, yukseklik=812, tema=tema).ac()
    p = s.page

    def olc():
        return p.evaluate(
            "() => ({sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,"
            " tasan: [...document.querySelectorAll('.eg-kutu, .eg-kutu *')]"
            "   .filter(e => e.getBoundingClientRect().right > document.documentElement.clientWidth + 0.5)"
            "   .map(e => e.className.baseVal ?? e.className).slice(0, 5)})"
        )

    ilk = olc()
    assert ilk["sw"] <= ilk["cw"], ilk
    assert ilk["tasan"] == [], ilk
    # En uzun metinler ortaya çıkınca da taşmamalı.
    p.click('button[data-eylem="cokert"]')
    p.click('.egitim-soru[data-soru-id="katalog-tahmin"] button[data-secenek="1"]')
    sonra = olc()
    assert sonra["sw"] <= sonra["cw"], sonra
    assert sonra["tasan"] == [], sonra
    assert s.konsol_hatalari == []


# ---------- W4 (göz kontrolü için ekran görüntüsü + ek olarak ölçülen kontrast) ----------


def _parlaklik(rgb):
    def kanal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * kanal(r) + 0.7152 * kanal(g) + 0.0722 * kanal(b)


def _kontrast(a, b):
    la, lb = sorted([_parlaklik(a), _parlaklik(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


@pytest.mark.parametrize("tema,sema", [("light", "default"), ("dark", "slate")])
def test_w4_tema_ekran_goruntusu_ve_kontrast(sayfa_ac, tema, sema):
    EKRAN.mkdir(parents=True, exist_ok=True)
    for genislik in (1280, 375):
        s = sayfa_ac(genislik=genislik, yukseklik=900, tema=tema).ac()
        p = s.page
        assert p.get_attribute("body", "data-md-color-scheme") == sema
        # Yapışkan üst bar ve "Başa dön" düğmesi öğe görüntüsünün üstüne biner; yalnızca
        # ekran görüntüsü için gizlenir, ölçümleri etkilemez.
        p.add_style_tag(content=".md-header, .md-top { visibility: hidden !important; }")
        p.click('.eg-tng-secim button[data-parca="algilama"]')
        p.click('button[data-eylem="cokert"]')
        p.click('.egitim-soru[data-soru-id="katalog-tahmin"] button[data-secenek="2"]')
        p.click('.egitim-soru[data-soru-id="katalog-hatirla"] button[data-secenek="1"]')
        p.locator(".eg-tng").screenshot(path=str(EKRAN / f"widget-{tema}-{genislik}.png"))
        p.locator(".egitim-soru").first.screenshot(path=str(EKRAN / f"soru-dogru-{tema}-{genislik}.png"))
        p.locator(".egitim-soru").nth(1).screenshot(path=str(EKRAN / f"soru-yanlis-{tema}-{genislik}.png"))

        cifler = p.evaluate(
            """() => {
              // rgba(...) dördüncü değeri alfa: yarı saydam yazı rengi zemine karıştırılmalı.
              const rgba = s => { const n = s.match(/\\d+(\\.\\d+)?/g).map(Number); return [n[0], n[1], n[2], n.length > 3 ? n[3] : 1]; };
              const rgb = s => rgba(s).slice(0, 3);
              const zemin = e => { while (e) { const c = getComputedStyle(e).backgroundColor;
                  if (c && !c.endsWith(', 0)') && c !== 'transparent') return rgb(c); e = e.parentElement; }
                return [255, 255, 255]; };
              return [...document.querySelectorAll(
                  '.eg-durum, .eg-robot, .eg-geri-bildirim, .eg-not, .eg-etiket, .eg-secenek, .eg-parca-adi, .eg-aciklama p, .eg-lejant')]
                .filter(e => e.offsetParent !== null && e.textContent.trim())
                .map(e => { let o = 1; for (let a = e; a; a = a.parentElement) o *= +getComputedStyle(a).opacity;
                  const z = zemin(e), r = rgba(getComputedStyle(e).color), y = r.slice(0, 3);
                  o *= r[3];
                  // Opaklık ve renk alfası yazıyı zemine karıştırır: etkin renk = o*yazı + (1-o)*zemin.
                  return {ad: e.className, yazi: y.map((c, i) => o * c + (1 - o) * z[i]), zemin: z}; });
            }"""
        )
        dusuk = [
            (c["ad"], round(_kontrast(c["yazi"], c["zemin"]), 2))
            for c in cifler
            if _kontrast(c["yazi"], c["zemin"]) < 4.5
        ]
        assert cifler, "Ölçülecek metin bulunamadı"
        en_dusuk = min(_kontrast(c["yazi"], c["zemin"]) for c in cifler)
        print(f"[kontrast] {tema}/{genislik}: {len(cifler)} metin, en düşük {en_dusuk:.2f}:1")
        assert dusuk == [], f"{tema}/{genislik}: WCAG AA (4.5:1) altında kalan metinler: {dusuk}"
        assert s.konsol_hatalari == []


# ---------- W5 ----------

SORU = '.egitim-soru[data-soru-id="katalog-tahmin"]'


def test_w5_dogru_yanlis_geri_bildirim_ve_hatirlama(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    p.click(f'{SORU} button[data-secenek="1"]')
    assert p.get_attribute(SORU, "data-sonuc") == "yanlis"
    assert p.inner_text(f"{SORU} .eg-geri-bildirim").startswith("Yanlış. Doğru cevap: B.")
    assert p.get_attribute(f'{SORU} button[data-secenek="2"]', "data-sonuc") == "dogru"
    assert p.is_visible(f"{SORU} .eg-aciklama")

    p.reload(wait_until="load")
    p.wait_for_selector(f"{SORU}[data-egitim-hazir]")
    assert p.get_attribute(SORU, "data-sonuc") == "yanlis", "Cevap yenilemede hatırlanmadı"
    assert p.is_disabled(f'{SORU} button[data-secenek="1"]')

    p.click(f"{SORU} button[data-tekrar]")
    assert p.get_attribute(SORU, "data-sonuc") is None
    p.click(f'{SORU} button[data-secenek="2"]')
    assert p.inner_text(f"{SORU} .eg-geri-bildirim").startswith("Doğru.")

    p.reload(wait_until="load")
    p.wait_for_selector(f"{SORU}[data-egitim-hazir]")
    assert p.get_attribute(SORU, "data-sonuc") == "dogru"
    # Öteki soru etkilenmedi.
    assert p.get_attribute('.egitim-soru[data-soru-id="katalog-hatirla"]', "data-sonuc") is None
    assert s.konsol_hatalari == []


def test_w5_depolama_engelliyken_calisir(sayfa_ac):
    s = sayfa_ac(depolama_kapali=True).ac()
    p = s.page
    assert p.evaluate("() => { try { localStorage; return 'acik'; } catch (e) { return e.name; } }") == "SecurityError"
    p.click(f'{SORU} button[data-secenek="2"]')
    assert p.get_attribute(SORU, "data-sonuc") == "dogru"
    assert "depolaması kapalı" in p.inner_text(f"{SORU} .eg-not")
    # Widget de etkilenmiyor.
    p.click('button[data-eylem="cokert"]')
    assert _robot(p, "tek-program") == "hayir"
    p.reload(wait_until="load")
    p.wait_for_selector(f"{SORU}[data-egitim-hazir]")
    assert p.get_attribute(SORU, "data-sonuc") is None
    # Olumsuz bulgu (18 Ekim 2026): depolama engelliyken Material'in kendi betiği her
    # yüklemede yakalanmamış hata atıyor. Bizim betiğimizin hiç hata eklemediğini, aynı
    # adımları egitim.js'li ve egitim.js'siz iki sayfada koşup hata sayısını
    # karşılaştırarak gösteriyoruz. Material'in hataları eşzamansız geldiği için her
    # yüklemeden sonra ağ durulana kadar beklenir.
    def say(egitim_acik):
        t = sayfa_ac(depolama_kapali=True)
        if not egitim_acik:
            t.page.route(
                "**/assets/egitim/egitim.js",
                lambda r: r.fulfill(status=200, body="", content_type="text/javascript"),
            )
        for _ in range(2):
            t.page.goto(t.adres + KATALOG, wait_until="networkidle")
            t.page.wait_for_timeout(300)
        return t.konsol_hatalari

    bizimle, bizsiz = say(True), say(False)
    assert len(bizimle) == len(bizsiz), f"egitim.js ek hata üretti: {bizimle} ≠ {bizsiz}"


def test_w5_etkilesim_ag_istegi_yapmaz(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    p.wait_for_load_state("networkidle")
    once = len(s.istekler)
    p.click(f'{SORU} button[data-secenek="3"]')
    p.click(f"{SORU} button[data-tekrar]")
    p.click('.egitim-soru[data-soru-id="katalog-hatirla"] button[data-secenek="3"]')
    for parca in PARCALAR:
        p.click(f'.eg-tng-secim button[data-parca="{parca}"]')
        p.click('button[data-eylem="cokert"]')
    # A2 notu: ortak sıfırlama düğmesi kalktı; aynı etkileşim yeni düğmelerle yapılıyor.
    for parca in PARCALAR:
        p.click(f'button[data-yeniden="{parca}"]')
    p.click('button[data-eylem="program-yeniden"]')
    p.wait_for_timeout(500)
    assert s.istekler[once:] == []
    assert s.konsol_hatalari == []


# ---------- W6 ----------


def test_w6_tek_js_tek_css_harici_kutuphane_yok():
    klasor = KOK / "docs" / "assets" / "egitim"
    assert sorted(f.name for f in klasor.iterdir()) == ["egitim.css", "egitim.js"]
    js = (klasor / "egitim.js").read_text(encoding="utf-8")
    css = (klasor / "egitim.css").read_text(encoding="utf-8")
    for yasak in ("fetch(", "XMLHttpRequest", "import(", "import ", "sendBeacon", "WebSocket", "eval("):
        assert yasak not in js, f"egitim.js içinde yasak: {yasak}"
    adresler = set(re.findall(r"https?://[^\s\"')]+", js))
    assert adresler == {"http://www.w3.org/2000/svg"}, adresler
    assert "@import" not in css and "url(" not in css

    # Derlenmiş katalog sayfası: bizim eklediğimiz tek betik ve tek stil.
    html = (KOK / "site" / KATALOG / "index.html").read_text(encoding="utf-8")
    betikler = re.findall(r'<script[^>]+src="([^"]+)"', html)
    bizim = [b for b in betikler if "assets/javascripts/" not in b]
    assert [pathlib.PurePosixPath(b).name for b in bizim] == ["egitim.js"], betikler
    stiller = re.findall(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"', html)
    bizim_stil = [x for x in stiller if "assets/stylesheets/" not in x and "fonts.googleapis" not in x]
    assert [pathlib.PurePosixPath(x).name for x in bizim_stil] == ["egitim.css"], stiller


def test_w6_navigation_instant_kapali():
    yml = (KOK / "mkdocs.yml").read_text(encoding="utf-8")
    assert "navigation.instant" not in yml.split("features:")[1].split("palette:")[0]
