"""A2 çıkış kriteri S7: tekrar kabındaki soru dolu gelmez, kaydetmez, asıl kayda dokunmaz.

Beklentiler koşudan ÖNCE yazıldı (18 Ekim 2026).
"""

import json
import shutil
import subprocess
import sys

from conftest import KATALOG, KOK

ASIL = '.egitim-soru[data-soru-id="katalog-hatirla"]:not([data-mod="tekrar"])'
TEKRAR = '.egitim-tekrar .egitim-soru[data-soru-id="katalog-hatirla"]'
ANAHTAR = "mavigolge-egitim:v1:soru:katalog-hatirla"


def _kayit(p):
    return p.evaluate(f"() => localStorage.getItem({json.dumps(ANAHTAR)})")


def _yenile(p):
    p.reload(wait_until="load")
    p.wait_for_selector(f"{TEKRAR}[data-egitim-hazir]")


def test_s7_tekrar_dolu_gelmez(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    assert p.locator(TEKRAR).count() == 1
    assert p.get_attribute(TEKRAR, "data-mod") == "tekrar"
    assert p.inner_text(f"{TEKRAR} .eg-etiket").strip().lower() == "tekrar"

    p.click(f'{ASIL} button[data-secenek="1"]')
    _yenile(p)
    assert p.get_attribute(ASIL, "data-sonuc") == "yanlis", "asıl soru kaydını hatırlamalı"
    assert p.get_attribute(TEKRAR, "data-sonuc") is None, "tekrar sorusu dolu gelmemeli"
    assert not p.is_disabled(f'{TEKRAR} button[data-secenek="1"]')
    assert s.konsol_hatalari == []


def test_s7_tekrar_kaydetmez_ve_asil_kaydi_bozmaz(sayfa_ac):
    s = sayfa_ac().ac()
    p = s.page
    # Asıl soru hiç cevaplanmamışken tekrar cevabı yeni kayıt açmamalı.
    p.click(f'{TEKRAR} button[data-secenek="3"]')
    assert p.get_attribute(TEKRAR, "data-sonuc") == "dogru"
    assert "kaydedilmez" in p.inner_text(f"{TEKRAR} .eg-not")
    assert _kayit(p) is None

    # Asıl soru cevaplanınca kayıt açılır; tekrardaki farklı cevap ve "Tekrar dene" onu değiştirmez.
    p.click(f'{ASIL} button[data-secenek="2"]')
    once = _kayit(p)
    assert once is not None and json.loads(once)["secim"] == 2
    p.click(f"{TEKRAR} button[data-tekrar]")
    p.click(f'{TEKRAR} button[data-secenek="4"]')
    p.click(f"{TEKRAR} button[data-tekrar]")
    assert _kayit(p) == once
    _yenile(p)
    assert p.get_attribute(ASIL, "data-sonuc") == "yanlis"
    assert p.get_attribute(TEKRAR, "data-sonuc") is None
    assert s.konsol_hatalari == []


def test_s7_eksik_soru_dosyasi_derlemeyi_dusurur(tmp_path):
    """sorular/ içinde olmayan bir dosyaya başvuran sayfa, katı derlemede hata vermeli."""
    kopya = tmp_path / "depo"
    for ad in ("docs", "sorular"):
        shutil.copytree(KOK / ad, kopya / ad)
    shutil.copy(KOK / "mkdocs.yml", kopya / "mkdocs.yml")
    (kopya / "docs" / "eksik.md").write_text('# Eksik\n\n--8<-- "boyle-bir-soru-yok.md"\n', encoding="utf-8")
    sonuc = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q", "-d", str(tmp_path / "cikti")],
        cwd=kopya,
        capture_output=True,
        text=True,
    )
    cikti = sonuc.stdout + sonuc.stderr
    assert sonuc.returncode != 0, cikti
    assert "boyle-bir-soru-yok.md" in cikti, cikti

    # Karşı deneme: dosya eklenince aynı kopya derleniyor (test yalnızca eksikliği yakalıyor).
    (kopya / "sorular" / "boyle-bir-soru-yok.md").write_text("Yer tutucu.\n", encoding="utf-8")
    tamam = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q", "-d", str(tmp_path / "cikti2")],
        cwd=kopya,
        capture_output=True,
        text=True,
    )
    assert tamam.returncode == 0, tamam.stdout + tamam.stderr
