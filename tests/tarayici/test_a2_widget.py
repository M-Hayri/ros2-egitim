"""A2 çıkış kriterleri S4–S6: node başına yeniden başlatma, durma sebebi, özet, lejant.

Beklentiler koşudan ÖNCE yazıldı (18 Ekim 2026, kullanıcı onayı 23:34) ve sonuçlara
bakılarak değiştirilmez.
"""

import pytest

from test_bilesenler import PARCALAR, _durumlar, _kontrast, _robot

AD = {
    "kamera": "kamera",
    "algilama": "algilama",
    "planlayici": "planlayici",
    "motor": "motor_surucu",
    "kayitci": "kayitci",
}

TEK_ROBOT_KAPALI = "Robot duruyor: bütün program kapandı."
TEK_ROBOT_ACIK = "Robot sürüyor."

# S4: tek bir node çökünce node grafiğindeki robot metni.
GRAF_ROBOT_TEK_COKME = {
    "kamera": "Robot duruyor: kamera çalışmıyor, motor_surucu'ya komut gelmiyor.",
    "algilama": "Robot duruyor: algilama çalışmıyor, motor_surucu'ya komut gelmiyor.",
    "planlayici": "Robot duruyor: planlayici çalışmıyor, motor_surucu'ya komut gelmiyor.",
    "motor": "Robot duruyor: motor_surucu çalışmıyor.",
    "kayitci": "Robot sürüyor: kayitci çalışmıyor ama sürüş zincirinde değil.",
}

# S4: birden fazla node çökünce sürüş zincirinde motor_surucu'ya en yakın olan adlandırılır.
GRAF_ROBOT_COKLU_COKME = [
    (("kamera", "planlayici"), "Robot duruyor: planlayici çalışmıyor, motor_surucu'ya komut gelmiyor."),
    (("kayitci", "algilama"), "Robot duruyor: algilama çalışmıyor, motor_surucu'ya komut gelmiyor."),
    (("kamera", "motor"), "Robot duruyor: motor_surucu çalışmıyor."),
    (("kayitci", "kamera"), "Robot duruyor: kamera çalışmıyor, motor_surucu'ya komut gelmiyor."),
]

LEJANT_HAREKETLI = "Oklar: renkli ve hareketli = veri akıyor, soluk gri = veri akmıyor."
LEJANT_HAREKETSIZ = "Oklar: renkli = veri akıyor, soluk gri = veri akmıyor."


def _cokert(p, *parcalar):
    for parca in parcalar:
        p.click(f'.eg-tng-secim button[data-parca="{parca}"]')
        p.click('button[data-eylem="cokert"]')


def _robot_metni(p, model):
    return p.inner_text(f'[data-model="{model}"] .eg-robot').strip()


# ---------- S4: düğmeler ----------


def test_s4_ortak_sifirlama_yok_panel_dugmeleri_var(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    assert p.locator('button[data-eylem="sifirla"]').count() == 0
    assert p.get_by_text("Hepsini yeniden başlat").count() == 0
    # Tek programda yalnızca bütün programı yeniden başlatan tek düğme var.
    tek = p.locator('[data-model="tek-program"] button')
    assert tek.count() == 1
    assert tek.inner_text().strip() == "Programı yeniden başlat"
    # Node grafiğinde her node'un kendi düğmesi var.
    for parca in PARCALAR:
        assert p.locator(f'[data-model="node-grafigi"] button[data-yeniden="{parca}"]').count() == 1
    # Başlangıçta hiçbir şey çökmediği için hepsi devre dışı.
    assert p.is_disabled('button[data-eylem="program-yeniden"]')
    for parca in PARCALAR:
        assert p.is_disabled(f'button[data-yeniden="{parca}"]')
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("parca", PARCALAR)
def test_s4_yalnizca_coken_node_yeniden_baslatilabilir(sayfa_ac, parca):
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, parca)
    for diger in PARCALAR:
        etkin = not p.is_disabled(f'button[data-yeniden="{diger}"]')
        assert etkin == (diger == parca), (diger, etkin)
    assert not p.is_disabled('button[data-eylem="program-yeniden"]')
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("parca", PARCALAR)
def test_s4_iki_model_bagimsiz_yeniden_baslar(sayfa_ac, parca):
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, parca)

    # Node grafiğinde yalnızca çökeni yeniden başlat: grafik tamamen ayağa kalkar,
    # tek program kendi düğmesine basılana kadar kapalı kalır.
    p.click(f'button[data-yeniden="{parca}"]')
    graf = _durumlar(p, "node-grafigi")
    assert "durdu" not in graf.values() and "veri-gelmiyor" not in graf.values(), graf
    assert _robot_metni(p, "node-grafigi") == "Robot sürüyor."
    assert _durumlar(p, "tek-program") == {k: "durdu" for k in PARCALAR}
    assert _robot_metni(p, "tek-program") == TEK_ROBOT_KAPALI

    p.click('button[data-eylem="program-yeniden"]')
    assert set(_durumlar(p, "tek-program").values()) == {"calisiyor"}
    assert _robot_metni(p, "tek-program") == TEK_ROBOT_ACIK
    assert s.konsol_hatalari == []


def test_s4_tek_node_yeniden_baslatmasi_otekileri_baslatmaz(sayfa_ac):
    """İki node çökükken yalnızca birini yeniden başlatmak ötekini ayağa kaldırmamalı."""
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, "kamera", "kayitci")
    p.click('button[data-yeniden="kayitci"]')
    graf = _durumlar(p, "node-grafigi")
    assert graf["kamera"] == "durdu"
    assert graf["kayitci"] == "veri-gelmiyor"  # ayakta ama kamera hâlâ çökük
    assert not p.is_disabled('button[data-yeniden="kamera"]')
    assert p.is_disabled('button[data-yeniden="kayitci"]')
    assert s.konsol_hatalari == []


def test_s4_program_yeniden_baslatmasi_grafigi_etkilemez(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, "algilama")
    p.click('button[data-eylem="program-yeniden"]')
    assert set(_durumlar(p, "tek-program").values()) == {"calisiyor"}
    assert _durumlar(p, "node-grafigi")["algilama"] == "durdu"
    assert _robot_metni(p, "node-grafigi") == GRAF_ROBOT_TEK_COKME["algilama"]
    assert s.konsol_hatalari == []


# ---------- S4: robot metinleri ----------


def test_s4_robot_metni_baslangicta(sayfa_ac):
    s = sayfa_ac().ac()
    assert _robot_metni(s.page, "tek-program") == TEK_ROBOT_ACIK
    assert _robot_metni(s.page, "node-grafigi") == "Robot sürüyor."


@pytest.mark.parametrize("parca", PARCALAR)
def test_s4_robot_metni_tek_cokme(sayfa_ac, parca):
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, parca)
    assert _robot_metni(p, "tek-program") == TEK_ROBOT_KAPALI
    assert _robot_metni(p, "node-grafigi") == GRAF_ROBOT_TEK_COKME[parca]
    assert _robot(p, "node-grafigi") == ("evet" if parca == "kayitci" else "hayir")
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("cokenler,beklenen", GRAF_ROBOT_COKLU_COKME)
def test_s4_robot_metni_coklu_cokme(sayfa_ac, cokenler, beklenen):
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, *cokenler)
    assert _robot_metni(p, "tek-program") == TEK_ROBOT_KAPALI
    assert _robot_metni(p, "node-grafigi") == beklenen
    assert s.konsol_hatalari == []


# ---------- S4: özet ----------


@pytest.mark.parametrize("parca", PARCALAR)
def test_s4_ozet_yayilmayi_ve_tekil_yeniden_baslatmayi_soyler(sayfa_ac, parca):
    s = sayfa_ac().ac()
    p = s.page
    ad = AD[parca]
    _cokert(p, parca)
    ozet = p.inner_text(".eg-ozet")
    assert ozet.startswith(f"{ad} çöktü.")
    assert "bütün süreci kapattı" in ozet
    assert "çökme öteki süreçlere yayılmadı" in ozet
    assert f"yalnızca {ad} node'unu yeniden başlatman yeter" in ozet

    p.click(f'button[data-yeniden="{parca}"]')
    ozet = p.inner_text(".eg-ozet")
    assert ozet.startswith(f"{ad} yeniden başlatıldı")
    assert "öteki node'lar bu sırada hiç kapanmadı" in ozet
    assert "tek bir parçayı yeniden başlatmanın yolu yok" in ozet  # tek program hâlâ kapalı
    assert s.konsol_hatalari == []


# ---------- S6: lejant ----------


@pytest.mark.parametrize("hareket,beklenen", [("no-preference", LEJANT_HAREKETLI), ("reduce", LEJANT_HAREKETSIZ)])
def test_s6_lejant_metni(sayfa_ac, hareket, beklenen):
    s = sayfa_ac(hareket=hareket).ac()
    lejant = s.page.locator('[data-model="node-grafigi"] .eg-lejant')
    assert lejant.count() == 1
    assert lejant.inner_text().strip() == beklenen
    # Lejant grafiğin hemen altında.
    sira = s.page.evaluate(
        "() => [...document.querySelector('[data-model=\"node-grafigi\"]').children].map(e => e.className.baseVal ?? e.className)"
    )
    assert sira.index("eg-lejant") == sira.index("eg-graf") + 1, sira
    assert s.konsol_hatalari == []


@pytest.mark.parametrize("tema", ["light", "dark"])
def test_s6_lejant_ve_akan_ok_kontrasti(sayfa_ac, tema):
    s = sayfa_ac(tema=tema).ac()
    p = s.page
    _cokert(p, "kayitci")  # akan ve akmayan ok bir arada
    olcum = p.evaluate(
        """() => {
          const rgba = s => { const n = s.match(/\\d+(\\.\\d+)?/g).map(Number); return [n[0], n[1], n[2], n.length > 3 ? n[3] : 1]; };
          const rgb = s => rgba(s).slice(0, 3);
          const karis = (renk, z) => { const r = rgba(renk); return r.slice(0, 3).map((c, i) => r[3] * c + (1 - r[3]) * z[i]); };
          const zemin = e => { while (e) { const c = getComputedStyle(e).backgroundColor;
              if (c && !c.endsWith(', 0)') && c !== 'transparent') return rgb(c); e = e.parentElement; }
            return [255, 255, 255]; };
          const lej = document.querySelector('[data-model="node-grafigi"] .eg-lejant');
          const ok = document.querySelector('.eg-graf-kenar[data-akiyor="evet"]');
          const okStil = getComputedStyle(ok);
          return {
            lejant: {yazi: karis(getComputedStyle(lej).color, zemin(lej)), zemin: zemin(lej)},
            ok: {cizgi: karis(okStil.stroke, zemin(ok.ownerSVGElement)), opaklik: +okStil.opacity, zemin: zemin(ok.ownerSVGElement)},
          };
        }"""
    )
    lejant = _kontrast(olcum["lejant"]["yazi"], olcum["lejant"]["zemin"])
    o = olcum["ok"]["opaklik"]
    etkin = [o * c + (1 - o) * z for c, z in zip(olcum["ok"]["cizgi"], olcum["ok"]["zemin"])]
    ok = _kontrast(etkin, olcum["ok"]["zemin"])
    print(f"[kontrast] {tema}: lejant {lejant:.2f}:1, akan ok {ok:.2f}:1")
    assert lejant >= 4.5, f"lejant {lejant:.2f}:1"
    assert ok >= 3.0, f"akan ok {ok:.2f}:1"
    assert s.konsol_hatalari == []


# ---------- Bağımsız inceleme (19 Ekim 2026): "Yeniden başlat" düğmelerinin düzeni ----------


def _dugme_olcumu(p):
    return p.evaluate(
        """() => [...document.querySelectorAll('[data-model="node-grafigi"] button[data-yeniden]')].map(b => {
             const r = b.getBoundingClientRect(), panel = b.closest('.eg-panel').getBoundingClientRect();
             return {parca: b.dataset.yeniden, gorunur: getComputedStyle(b).visibility === 'visible',
                     etkin: !b.disabled, sol: Math.round(r.left), sag: Math.round(r.right),
                     genislik: Math.round(r.width), panelSag: Math.round(panel.right)};
           })"""
    )


@pytest.mark.parametrize("genislik", [1280, 375])
def test_yeniden_baslat_gorunur_ise_etkin_ve_hizali(sayfa_ac, genislik):
    s = sayfa_ac(genislik=genislik, yukseklik=900).ac()
    p = s.page
    # Başlangıç: hiçbir düğme görünmez.
    assert [d["gorunur"] for d in _dugme_olcumu(p)] == [False] * 5
    # Biri çökünce yalnızca onun düğmesi görünür ve etkin.
    _cokert(p, "algilama")
    for d in _dugme_olcumu(p):
        assert d["gorunur"] == d["etkin"] == (d["parca"] == "algilama"), d
    # Hepsi çökünce beşi de görünür; aynı sütunda, aynı genişlikte, panelin içinde.
    _cokert(p, "kamera", "planlayici", "motor", "kayitci")
    olcum = _dugme_olcumu(p)
    assert all(d["gorunur"] and d["etkin"] for d in olcum), olcum
    assert len({d["sol"] for d in olcum}) == 1, olcum
    assert len({d["genislik"] for d in olcum}) == 1, olcum
    assert all(d["sag"] <= d["panelSag"] for d in olcum), olcum
    assert s.konsol_hatalari == []


def test_ozet_birden_fazla_cokmede_hepsini_sayar(sayfa_ac):
    """Ekran görüntüsünden bulundu (19 Ekim): özet yalnızca son çökeni sayıyordu."""
    s = sayfa_ac().ac()
    p = s.page
    _cokert(p, "algilama", "kayitci")
    ozet = p.inner_text(".eg-ozet")
    assert "yalnızca kayitci durdu" not in ozet, ozet
    assert "algilama, kayitci" in ozet, ozet
    # Birden fazla çökük node varken öneri hepsini kapsamalı (tek çökmenin S4 cümlesi ayrı testte).
    assert "yalnızca çöken node'ları (algilama, kayitci) yeniden başlatman yeter" in ozet, ozet
    assert s.konsol_hatalari == []
