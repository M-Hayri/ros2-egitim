"""Ders sayfası denetimleri (A2: S1, S7'nin bankası, S11'in otomatik kısmı, n−2 tekrar kuralı).

Kurallar sistem belgesinin 8. bölümündeki şablondan ve 18 Ekim 2026 kararlarından gelir.
ROS gerektirmez.
"""

import pathlib
import re

import pytest

KOK = pathlib.Path(__file__).resolve().parents[2]
DOCS = KOK / "docs"
SORULAR = KOK / "sorular"

BOLUMLER = [
    "Bağlam", "Kavram", "Tahmin et", "Çalıştır", "İncele", "Değiştir", "Yap",
    "Arıza laboratuvarı", "Hatırla", "Resmi doküman", "Sözlüğe eklenenler",
]
ACILIS = "Açılış: tekrar"
KAVRAM_SINIRI = 800
SNIPPET = re.compile(r'^\s*--8<--\s+"(?P<dosya>[^"]+)"\s*$', re.M)
SORU_ID = re.compile(r'data-soru-id="(?P<id>[^"]+)"')


def ders_dosyalari():
    dosyalar = []
    for yol in DOCS.glob("seviye-*/*.md"):
        m = re.fullmatch(r"(\d+)-(\d+)-.+\.md", yol.name)
        if m:
            dosyalar.append(((int(m.group(1)), int(m.group(2))), yol))
    return [yol for _, yol in sorted(dosyalar)]


DERSLER = ders_dosyalari()


def kod(yol):
    a, b = re.match(r"(\d+)-(\d+)-", yol.name).groups()
    return f"{a}.{b}"


def bolumlere_ayir(metin):
    """'## Başlık' -> gövde (kod blokları içindeki ## satırları bölüm sayılmaz)."""
    bolumler, ad, satirlar, kodda = {}, None, [], False
    for satir in metin.splitlines():
        if satir.lstrip().startswith("```"):
            kodda = not kodda
        if not kodda and satir.startswith("## "):
            if ad is not None:
                bolumler[ad] = "\n".join(satirlar)
            ad, satirlar = satir[3:].strip(), []
        elif ad is not None:
            satirlar.append(satir)
    if ad is not None:
        bolumler[ad] = "\n".join(satirlar)
    return bolumler


def duz_metin(md):
    md = re.sub(r"```.*?```", " ", md, flags=re.S)
    md = re.sub(r"<!--.*?-->", " ", md, flags=re.S)
    md = re.sub(r"<[^>]+>", " ", md)
    md = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", md)
    md = re.sub(r"[*_`#>|]", " ", md)
    return md


def kelime_say(md):
    return len(re.findall(r"[0-9A-Za-zÇĞİÖŞÜçğıöşü][0-9A-Za-zÇĞİÖŞÜçğıöşü'’.,\-]*", duz_metin(md)))


def tekrar_snippetleri(metin):
    kaplar = re.findall(r'<div class="egitim-tekrar" markdown>(.*?)</div>', metin, flags=re.S)
    return [m.group("dosya") for kap in kaplar for m in SNIPPET.finditer(kap)]


def ana_snippetler(metin):
    temiz = re.sub(r'<div class="egitim-tekrar" markdown>.*?</div>', "", metin, flags=re.S)
    return [m.group("dosya") for m in SNIPPET.finditer(temiz)]


def test_seviye_0_dersleri_var():
    assert [kod(y) for y in DERSLER][:3] == ["0.1", "0.2", "0.3"]


@pytest.mark.parametrize("yol", DERSLER, ids=kod)
def test_s1_kunye_ve_hedef(yol):
    metin = yol.read_text(encoding="utf-8")
    ilk = metin.splitlines()[0]
    assert ilk.startswith(f"# {kod(yol)} "), ilk
    assert re.search(r"^\| Tür \| Süre \| Önkoşul \|$", metin, re.M), "künye tablosu yok"
    assert re.search(r"^\| (Çekirdek|Genişletme) \| \d+ dk \| .+ \|$", metin, re.M), "künye satırı biçimsiz"
    hedef = re.search(r"^\*\*Hedef:\*\* (.+)$", metin, re.M)
    assert hedef, "**Hedef:** satırı yok"
    assert "**" in hedef.group(1), "hedefte kalın yazılmış ölçülebilir fiil yok"


@pytest.mark.parametrize("yol", DERSLER, ids=kod)
def test_s1_bolumler_sirali_ve_dolu(yol):
    bolumler = bolumlere_ayir(yol.read_text(encoding="utf-8"))
    adlar = list(bolumler)
    if adlar and adlar[0] == ACILIS:
        adlar = adlar[1:]
    assert adlar == BOLUMLER, adlar
    for ad, govde in bolumler.items():
        duz = duz_metin(govde).strip()
        assert duz or SNIPPET.search(govde), f"{ad} bölümü boş"
        for m in re.finditer(r"Bu derste (?:CI testi )?yok\.\*{0,2}\s*(.*)", govde):
            gerekce = m.group(1).strip()
            assert len(gerekce.split()) >= 3, f"{ad}: 'Bu derste yok' gerekçesiz"


@pytest.mark.parametrize("yol", DERSLER, ids=kod)
def test_s1_kavram_800_kelimeyi_gecmez(yol):
    kavram = bolumlere_ayir(yol.read_text(encoding="utf-8"))["Kavram"]
    sayi = kelime_say(kavram)
    print(f"[kelime] {kod(yol)} Kavram: {sayi}")
    assert sayi <= KAVRAM_SINIRI, f"{kod(yol)} Kavram {sayi} kelime"


@pytest.mark.parametrize("yol", DERSLER, ids=kod)
def test_s11_kavram_paragraflari_kaynakli(yol):
    """Kavram'daki her paragraf bir kaynağa bağlı ya da açıkça kaynaksız diye işaretli."""
    kavram = bolumlere_ayir(yol.read_text(encoding="utf-8"))["Kavram"]
    paragraflar = [p.strip() for p in re.split(r"\n\s*\n", kavram) if p.strip()]
    kaynaksiz = []
    for p in paragraflar:
        if p.startswith("<div") or p.startswith("<!--"):
            continue
        if "](http" in p or "(aynı sayfa)" in p or "<!-- kaynaksız:" in p:
            continue
        kaynaksiz.append(p[:70])
    assert kaynaksiz == [], kaynaksiz


@pytest.mark.parametrize("yol", DERSLER, ids=kod)
def test_s1_soru_alanlari(yol):
    metin = yol.read_text(encoding="utf-8")
    b = bolumlere_ayir(metin)
    assert 'data-tur="tahmin"' in b["Tahmin et"], "Tahmin et bölümünde tahmin sorusu yok"
    d = kod(yol).replace(".", "-")
    hatirla = [m.group("dosya") for m in SNIPPET.finditer(b["Hatırla"])]
    assert hatirla == [f"d{d}-hatirla-{i}.md" for i in (1, 2, 3)], hatirla
    assert re.search(r"https://docs\.ros\.org/en/jazzy/", b["Resmi doküman"]), "resmi doküman bağlantısı yok"
    assert "CI testi" in b["Yap"], "Yap bölümü CI testinin ne kontrol ettiğini söylemiyor"


def test_tekrar_kurali_n_eksi_2():
    """n. ders, n−2. dersin hatırla sorularından tam 2 tanesiyle açılır (karar: 18 Ekim 2026)."""
    for i, yol in enumerate(DERSLER):
        metin = yol.read_text(encoding="utf-8")
        tekrar = tekrar_snippetleri(metin)
        bolumler = bolumlere_ayir(metin)
        if i < 2:
            assert tekrar == [] and ACILIS not in bolumler, f"{kod(yol)} açılış sorusu almamalı"
            continue
        kaynak = kod(DERSLER[i - 2]).replace(".", "-")
        assert len(tekrar) == 2, f"{kod(yol)}: {tekrar}"
        assert all(re.fullmatch(rf"d{kaynak}-hatirla-[123]\.md", t) for t in tekrar), (kod(yol), tekrar)
        assert len(set(tekrar)) == 2
        assert list(bolumler)[0] == ACILIS, f"{kod(yol)}: tekrar soruları Açılış bölümünde olmalı"


def test_soru_bankasi_tutarli():
    sayfalar = list(DOCS.rglob("*.md"))
    ana, tekrar = [], []
    for s in sayfalar:
        metin = s.read_text(encoding="utf-8")
        ana += ana_snippetler(metin)
        tekrar += tekrar_snippetleri(metin)
    for dosya in sorted(SORULAR.glob("*.md")):
        metin = dosya.read_text(encoding="utf-8")
        kimlikler = SORU_ID.findall(metin)
        assert kimlikler == [dosya.stem], f"{dosya.name}: kimlik {kimlikler}, dosya adıyla aynı olmalı"
        if re.fullmatch(r"d\d+-\d+-hatirla-\d", dosya.stem):
            assert 'data-tur="hatirla"' in metin, dosya.name
        assert ana.count(dosya.name) == 1, f"{dosya.name} asıl yerinde {ana.count(dosya.name)} kez eklenmiş (1 olmalı)"
    for t in tekrar:
        assert (SORULAR / t).exists(), t


def test_soru_kimlikleri_site_genelinde_tek():
    gorulen = {}
    for s in DOCS.rglob("*.md"):
        metin = re.sub(r"```.*?```", "", s.read_text(encoding="utf-8"), flags=re.S)
        for k in SORU_ID.findall(metin):
            gorulen.setdefault(k, []).append(s.name)
        for d in ana_snippetler(metin):
            k = d[:-3]
            gorulen.setdefault(k, []).append(s.name)
    cift = {k: v for k, v in gorulen.items() if len(v) > 1}
    assert cift == {}, cift


# ---------- Soru seçenekleri: uzunluk ipucu (bağımsız inceleme, 19 Ekim 2026) ----------

UZUNLUK_ORANI = 1.5
SORU_BLOGU = re.compile(r'<div class="egitim-soru"(?P<oz>[^>]*)>(?P<govde>.*?)</div>', re.S)


def sorulari_topla():
    """(kaynak, kimlik, doğru sıra, seçenek metinleri) — banka ve sayfa içi sorular."""
    sorular = []
    for dosya in list(SORULAR.glob("*.md")) + list(DOCS.rglob("*.md")):
        metin = re.sub(r"```.*?```", "", dosya.read_text(encoding="utf-8"), flags=re.S)
        for m in SORU_BLOGU.finditer(metin):
            kimlik = re.search(r'data-soru-id="([^"]+)"', m.group("oz")).group(1)
            dogru = int(re.search(r'data-dogru="(\d+)"', m.group("oz")).group(1))
            secenekler = re.findall(r"^\d+\.\s+(.+)$", m.group("govde"), re.M)
            sorular.append((dosya.name, kimlik, dogru, [duz_metin(s).strip() for s in secenekler]))
    return sorular


SORU_LISTESI = sorulari_topla()


@pytest.mark.parametrize("kaynak,kimlik,dogru,secenekler", SORU_LISTESI, ids=[s[1] for s in SORU_LISTESI])
def test_dogru_secenek_uzunluguyla_ele_verilmiyor(kaynak, kimlik, dogru, secenekler):
    uzunluk = [len(s) for s in secenekler]
    dogru_u = uzunluk[dogru - 1]
    yanlis_en_uzun = max(u for i, u in enumerate(uzunluk) if i != dogru - 1)
    oran = dogru_u / yanlis_en_uzun
    print(f"[uzunluk] {kimlik}: doğru {dogru_u}, yanlışların en uzunu {yanlis_en_uzun}, oran {oran:.2f}")
    assert oran <= UZUNLUK_ORANI, f"{kimlik} ({kaynak}): doğru seçenek {oran:.2f} kat uzun"
