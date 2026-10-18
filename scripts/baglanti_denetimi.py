#!/usr/bin/env python3
"""Sitedeki dış bağlantıları denetler (A2, S9).

- https://docs.ros.org/en/jazzy/<yol>.html bağlantıları web isteğiyle DEĞİL, ros2/ros2_documentation
  deposunun jazzy dalında karşılık gelen kaynak dosyanın (source/<yol>.rst ya da .md) varlığıyla
  doğrulanır. docs.ros.org otomatik isteklere "Access Denied" döndürebildiği için.
  Dosya listesi, blob indirmeden `git ls-tree` ile alınır.
- Öteki bağlantılara HTTP isteği atılır: 2xx/3xx geçer; 403 ve 429 "doğrulanamadı" uyarısıdır
  (hata değil); başka 4xx/5xx ve bağlantı hataları hatadır.

Kullanım:
    python3 scripts/baglanti_denetimi.py [--yalniz-ros] [--rapor dosya.json]
Çıkış kodu: hata varsa 1, yalnızca uyarı varsa 0.
"""

import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

KOK = pathlib.Path(__file__).resolve().parents[1]
ROS_DOC = re.compile(r"^https://docs\.ros\.org/en/jazzy/(?P<yol>[^#?]*)")
BAGLANTI = re.compile(r"\]\((?P<url>https?://[^)\s]+)\)|href=\"(?P<href>https?://[^\"]+)\"")
DEPO = "https://github.com/ros2/ros2_documentation.git"
DAL = "jazzy"
UYARI_KODLARI = {403, 429}


def baglantilari_topla():
    bulunan = {}
    for klasor in (KOK / "docs", KOK / "sorular"):
        for dosya in sorted(klasor.rglob("*.md")):
            metin = re.sub(r"```.*?```", "", dosya.read_text(encoding="utf-8"), flags=re.S)
            for m in BAGLANTI.finditer(metin):
                url = m.group("url") or m.group("href")
                bulunan.setdefault(url, set()).add(str(dosya.relative_to(KOK)))
    return {u: sorted(s) for u, s in bulunan.items()}


def ros_kaynak_listesi():
    with tempfile.TemporaryDirectory() as gecici:
        subprocess.run(
            ["git", "clone", "-q", "--depth", "1", "--branch", DAL, "--filter=blob:none", "--no-checkout", DEPO, gecici],
            check=True, timeout=600,
        )
        commit = subprocess.run(["git", "-C", gecici, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
        dosyalar = subprocess.run(
            ["git", "-C", gecici, "ls-tree", "-r", "--name-only", "HEAD", "source"],
            capture_output=True, text=True, check=True,
        ).stdout.split()
    return commit, set(dosyalar)


def ros_yolunu_coz(yol, kaynaklar):
    yol = yol.strip("/")
    if yol in ("", "index.html"):
        adaylar = ["source/index.rst"]
    else:
        temel = yol[:-5] if yol.endswith(".html") else yol
        adaylar = [f"source/{temel}.rst", f"source/{temel}.md", f"source/{temel}/index.rst"]
    for aday in adaylar:
        if aday in kaynaklar:
            return aday
    return None


def http_dene(url):
    istek = urllib.request.Request(url, method="GET", headers={"User-Agent": "ros2-egitim-baglanti-denetimi/1.0"})
    try:
        with urllib.request.urlopen(istek, timeout=20) as yanit:
            return yanit.status, None
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:  # bağlantı hatası, zaman aşımı, TLS ...
        return None, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yalniz-ros", action="store_true", help="yalnızca docs.ros.org bağlantılarını denetle")
    ap.add_argument("--rapor")
    arg = ap.parse_args()

    baglantilar = baglantilari_topla()
    commit, kaynaklar = ros_kaynak_listesi()
    sonuclar = []
    for url, yerler in sorted(baglantilar.items()):
        m = ROS_DOC.match(url)
        if m:
            kaynak = ros_yolunu_coz(m.group("yol"), kaynaklar)
            sonuclar.append({"url": url, "yerler": yerler, "tur": "ros-kaynak",
                             "durum": "geçti" if kaynak else "hata", "ayrinti": kaynak or "kaynak dosya bulunamadı"})
            continue
        if url.startswith("https://docs.ros.org/"):
            sonuclar.append({"url": url, "yerler": yerler, "tur": "ros-kaynak", "durum": "hata",
                             "ayrinti": "docs.ros.org bağlantısı jazzy sürümüne işaret etmiyor"})
            continue
        if arg.yalniz_ros:
            continue
        kod, hata = http_dene(url)
        if kod is not None and 200 <= kod < 400:
            durum = "geçti"
        elif kod in UYARI_KODLARI:
            durum = "doğrulanamadı"
        else:
            durum = "hata"
        sonuclar.append({"url": url, "yerler": yerler, "tur": "http", "durum": durum, "ayrinti": hata or f"HTTP {kod}"})

    for s in sonuclar:
        etiket = {"geçti": "[GEÇTİ]", "doğrulanamadı": "[UYARI]", "hata": "[HATA] "}[s["durum"]]
        print(f"{etiket} {s['url']}  ({s['ayrinti']}; {', '.join(s['yerler'])})")
    sayim = {d: sum(1 for s in sonuclar if s["durum"] == d) for d in ("geçti", "doğrulanamadı", "hata")}
    print(f"Bağlantı denetimi: {len(sonuclar)} bağlantı, {sayim['geçti']} geçti, "
          f"{sayim['doğrulanamadı']} doğrulanamadı (uyarı), {sayim['hata']} hata; "
          f"ros2_documentation {DAL} @ {commit}")
    if arg.rapor:
        pathlib.Path(arg.rapor).write_text(json.dumps({"commit": commit, "sonuclar": sonuclar}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if sayim["hata"] else 0


if __name__ == "__main__":
    sys.exit(main())
