#!/usr/bin/env python3
"""Sitedeki komut bloklarını bulur, denetler ve devcontainer içinde çalıştırır.

Her `bash`/`sh`/`shell`/`console` kod bloğunun hemen önünde bir işaret olmalı:

    <!-- test: otomatik -->                         bloğu bir terminale yazar; çıkış kodu 0 olmalı
    <!-- test: otomatik; cikis: 127; desen: command not found -->
    <!-- test: otomatik; terminal: temiz -->        aynı adlı terminal blok blok sürer (oturum)
    <!-- test: arka-plan; hazir: ros2 node list; desen: ^/turtlesim$; sure: 30 -->
                                                    kendiliğinden bitmeyen komut: arka planda başlar,
                                                    `hazir` komutu `sure` saniye içinde `desen`i
                                                    gösterirse geçer; sayfa bitince süreç kapatılır
    <!-- test: elle; neden: klavye -->              klavye/GUI ister; bloğun başlığı (title="...")
                                                    "Elle doğrulandı (kim, tarih)" ya da
                                                    "Test edilmedi" ile başlamalı

`desen` birden çok kez yazılabilir; hepsi çıktıda (stdout+stderr) bulunmalıdır (çok satırlı
düzenli ifade). Terminal, yeni açılmış bir Codespace terminalini taklit eder: temiz bir
ortamdan `bash -i` başlatılır, böylece /etc/bash.bashrc ve ~/.bashrc okunur. Blok satırları
terminale yazılır; yani blok içinde açılan bir alt kabuk sonraki satırları okur.

Kullanım:
    python3 scripts/icerik_komutlari.py --denetle            # yalnızca işaretleri denetler
    python3 scripts/icerik_komutlari.py --listele            # blokları ve elle listesini yazar
    python3 scripts/icerik_komutlari.py --calistir [--ekransiz] [--rapor dosya.json] [sayfa ...]
"""

import argparse
import json
import os
import pathlib
import queue
import re
import signal
import subprocess
import sys
import threading
import time

KOK = pathlib.Path(__file__).resolve().parents[1]
KOMUT_DILLERI = {"bash", "sh", "shell", "console"}
TURLER = {"otomatik", "arka-plan", "elle"}
ELLE_BASLIKLARI = ("Elle doğrulandı (", "Test edilmedi")
ISARET = re.compile(r"^\s*<!--\s*test:\s*(?P<govde>.*?)\s*-->\s*$")
CIT = re.compile(r"^(?P<girinti>\s*)(?P<cit>`{3,}|~{3,})\s*(?P<bilgi>.*)$")
BASLIK = re.compile(r'title="(?P<baslik>[^"]*)"')


class Blok:
    def __init__(self, sayfa, satir, dil, baslik, metin, ozellik, hata=None):
        self.sayfa = sayfa
        self.satir = satir
        self.dil = dil
        self.baslik = baslik
        self.metin = metin
        self.ozellik = ozellik  # dict: tur, desen (liste), cikis, terminal, sure, hazir, neden
        self.hata = hata

    @property
    def tur(self):
        return self.ozellik.get("tur")

    @property
    def yer(self):
        try:
            ad = self.sayfa.relative_to(KOK)
        except ValueError:
            ad = self.sayfa
        return f"{ad}:{self.satir}"


def isaret_coz(govde):
    """'otomatik; desen: a; desen: b; cikis: 1' -> sözlük."""
    parcalar = [p.strip() for p in govde.split(";") if p.strip()]
    if not parcalar:
        return {}, "boş işaret"
    oz = {"tur": parcalar[0], "desen": []}
    for parca in parcalar[1:]:
        if ":" not in parca:
            return oz, f"anlaşılmayan parça: {parca!r}"
        anahtar, deger = parca.split(":", 1)
        anahtar, deger = anahtar.strip(), deger.strip()
        if anahtar == "desen":
            oz["desen"].append(deger)
        elif anahtar in ("cikis", "sure"):
            try:
                oz[anahtar] = int(deger)
            except ValueError:
                return oz, f"{anahtar} bir tam sayı olmalı: {deger!r}"
        elif anahtar in ("terminal", "hazir", "neden"):
            oz[anahtar] = deger
        else:
            return oz, f"bilinmeyen anahtar: {anahtar!r}"
    return oz, None


def bloklari_bul(sayfa):
    satirlar = sayfa.read_text(encoding="utf-8").splitlines()
    bloklar = []
    bekleyen = None  # (satır no, gövde)
    i = 0
    while i < len(satirlar):
        satir = satirlar[i]
        m = ISARET.match(satir)
        if m:
            if bekleyen:
                bloklar.append(Blok(sayfa, bekleyen[0], None, None, "", {}, "işaretten sonra kod bloğu gelmedi"))
            bekleyen = (i + 1, m.group("govde"))
            i += 1
            continue
        c = CIT.match(satir)
        if c:
            girinti, cit, bilgi = c.group("girinti"), c.group("cit"), c.group("bilgi")
            dil = (bilgi.split()[0] if bilgi.split() else "").lstrip("{.").strip("}").lower()
            baslik_m = BASLIK.search(bilgi)
            govde = []
            j = i + 1
            while j < len(satirlar):
                kapanis = satirlar[j].strip()
                if kapanis.startswith(cit[0] * len(cit)) and kapanis.strip(cit[0]) == "":
                    break
                govde.append(satirlar[j][len(girinti):] if satirlar[j].startswith(girinti) else satirlar[j].lstrip())
                j += 1
            metin = "\n".join(govde)
            if dil in KOMUT_DILLERI:
                if bekleyen is None:
                    bloklar.append(Blok(sayfa, i + 1, dil, None, metin, {}, "işaretsiz komut bloğu"))
                else:
                    oz, hata = isaret_coz(bekleyen[1])
                    bloklar.append(
                        Blok(sayfa, i + 1, dil, baslik_m.group("baslik") if baslik_m else None, metin, oz, hata)
                    )
            elif bekleyen is not None:
                bloklar.append(Blok(sayfa, bekleyen[0], dil, None, metin, {}, f"işaret komut olmayan bir bloğa ({dil or 'dilsiz'}) bağlı"))
            bekleyen = None
            i = j + 1
            continue
        if bekleyen and satir.strip():
            bloklar.append(Blok(sayfa, bekleyen[0], None, None, "", {}, "işaretten sonra kod bloğu gelmedi"))
            bekleyen = None
        i += 1
    if bekleyen:
        bloklar.append(Blok(sayfa, bekleyen[0], None, None, "", {}, "işaretten sonra kod bloğu gelmedi"))
    return bloklar


def denetle(bloklar):
    hatalar = []
    for b in bloklar:
        if b.hata:
            hatalar.append(f"{b.yer}: {b.hata}")
            continue
        if b.tur not in TURLER:
            hatalar.append(f"{b.yer}: bilinmeyen tür {b.tur!r} (otomatik, arka-plan, elle)")
            continue
        if b.tur == "arka-plan" and not (b.ozellik.get("hazir") and b.ozellik["desen"]):
            hatalar.append(f"{b.yer}: arka-plan bloğu için 'hazir' ve 'desen' gerekli")
        if b.tur == "elle":
            if not b.ozellik.get("neden"):
                hatalar.append(f"{b.yer}: elle bloğu için 'neden' gerekli")
            if not (b.baslik and b.baslik.startswith(ELLE_BASLIKLARI)):
                hatalar.append(f'{b.yer}: elle bloğunun başlığı "Elle doğrulandı (kim, tarih)" ya da "Test edilmedi" ile başlamalı')
        elif b.baslik and b.baslik.startswith(ELLE_BASLIKLARI):
            hatalar.append(f"{b.yer}: otomatik test edilen blok elle etiketi taşıyamaz")
        for d in b.ozellik.get("desen", []):
            try:
                re.compile(d, re.M)
            except re.error as e:
                hatalar.append(f"{b.yer}: geçersiz desen {d!r}: {e}")
    return hatalar


# ---------- Çalıştırma ----------


def terminal_ortami(ekransiz):
    ortam = {
        "HOME": os.environ.get("HOME", "/root"),
        "USER": os.environ.get("USER", ""),
        "LANG": "C.UTF-8",
        "TERM": "dumb",
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    }
    if ekransiz:
        ortam["QT_QPA_PLATFORM"] = "offscreen"  # CI'da ekran yok; Qt penceresi bellekte açılır
    elif os.environ.get("DISPLAY"):
        ortam["DISPLAY"] = os.environ["DISPLAY"]
    return ortam


class Terminal:
    """Satırları stdin'den okuyan etkileşimli bir bash: bir Codespace terminali gibi."""

    sayac = 0

    def __init__(self, ortam):
        self.surec = subprocess.Popen(
            ["bash", "-i"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=ortam,
            cwd=KOK,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        self.kuyruk = queue.Queue()
        threading.Thread(target=self._oku, daemon=True).start()

    def _oku(self):
        for satir in self.surec.stdout:
            self.kuyruk.put(satir.rstrip("\n"))
        self.kuyruk.put(None)

    def yaz(self, metin, sure):
        Terminal.sayac += 1
        isaret = f"__EGITIM_SON_{Terminal.sayac}__"
        try:
            self.surec.stdin.write(metin.rstrip("\n") + "\n" + f'echo "{isaret} $?"\n')
            self.surec.stdin.flush()
        except BrokenPipeError:
            return None, ["(terminal kapanmış)"]
        cikti = []
        son = time.time() + sure
        desen = re.compile(re.escape(isaret) + r" (\d+)")
        while True:
            kalan = son - time.time()
            if kalan <= 0:
                return "zaman-asimi", cikti
            try:
                satir = self.kuyruk.get(timeout=kalan)
            except queue.Empty:
                return "zaman-asimi", cikti
            if satir is None:
                self.surec.wait(timeout=5)
                return self.surec.returncode, cikti
            m = desen.search(satir)
            if m:
                onu = satir[: m.start()]
                if onu.strip():
                    cikti.append(onu)
                return int(m.group(1)), cikti
            cikti.append(satir)

    def kapat(self):
        try:
            self.surec.stdin.write("exit\n")
            self.surec.stdin.close()
            self.surec.wait(timeout=3)
        except (BrokenPipeError, OSError, subprocess.TimeoutExpired):
            pass
        kapat_grup(self.surec)


def kapat_grup(surec):
    if surec.poll() is not None:
        return
    # Önce Ctrl+C (SIGINT): ROS node'ları bunu düzgün kapanma olarak işler.
    for isaret, bekle in ((signal.SIGINT, 5), (signal.SIGTERM, 3), (signal.SIGKILL, 2)):
        try:
            os.killpg(surec.pid, isaret)
        except ProcessLookupError:
            return
        try:
            surec.wait(timeout=bekle)
            return
        except subprocess.TimeoutExpired:
            continue


def desenleri_bul(desenler, metin):
    return [d for d in desenler if not re.search(d, metin, re.M)]


def sayfa_calistir(sayfa, bloklar, ortam, sonuclar):
    terminaller = {}
    arka = []
    try:
        for b in bloklar:
            if b.tur == "elle":
                sonuclar.append({"yer": b.yer, "tur": "elle", "durum": "elle", "neden": b.ozellik.get("neden"), "baslik": b.baslik, "metin": b.metin})
                continue
            if b.tur == "otomatik":
                ad = b.ozellik.get("terminal", "1")
                if ad not in terminaller:
                    terminaller[ad] = Terminal(ortam)
                bas = time.time()
                kod, cikti = terminaller[ad].yaz(b.metin, b.ozellik.get("sure", 90))
                metin = "\n".join(cikti)
                beklenen = b.ozellik.get("cikis", 0)
                eksik = desenleri_bul(b.ozellik["desen"], metin)
                gecti = kod == beklenen and not eksik
                sonuclar.append({
                    "yer": b.yer, "tur": "otomatik", "durum": "geçti" if gecti else "düştü",
                    "cikis": kod, "beklenen_cikis": beklenen, "eksik_desen": eksik,
                    "sure_sn": round(time.time() - bas, 1), "metin": b.metin,
                    "cikti_son": cikti[-40:],
                })
            elif b.tur == "arka-plan":
                bas = time.time()
                surec = subprocess.Popen(
                    ["bash", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    env=ortam, cwd=KOK, text=True, start_new_session=True,
                )
                surec.stdin.write(b.metin.rstrip("\n") + "\n")
                surec.stdin.close()  # komut bitince kabuk da kapansın (Ctrl+C sonrası gibi)
                kuyruk = queue.Queue()
                threading.Thread(target=lambda: [kuyruk.put(s.rstrip("\n")) for s in surec.stdout], daemon=True).start()
                arka.append(surec)
                sure = b.ozellik.get("sure", 30)
                son_cikti, eksik, hazir = "", b.ozellik["desen"], False
                while time.time() - bas < sure:
                    if surec.poll() is not None:
                        break
                    sorgu = subprocess.run(
                        ["bash", "-i", "-c", b.ozellik["hazir"]], env=ortam, cwd=KOK,
                        capture_output=True, text=True, timeout=60,
                    )
                    son_cikti = sorgu.stdout + sorgu.stderr
                    eksik = desenleri_bul(b.ozellik["desen"], son_cikti)
                    if not eksik:
                        hazir = True
                        break
                    time.sleep(1)
                surec_cikti = []
                while not kuyruk.empty():
                    surec_cikti.append(kuyruk.get())
                sonuclar.append({
                    "yer": b.yer, "tur": "arka-plan", "durum": "geçti" if hazir else "düştü",
                    "hazir_komut": b.ozellik["hazir"], "eksik_desen": [] if hazir else eksik,
                    "sure_sn": round(time.time() - bas, 1), "surec_bitti": surec.poll() is not None,
                    "metin": b.metin, "cikti_son": (surec_cikti + ["--- hazir komutu ---"] + son_cikti.splitlines())[-40:],
                })
    finally:
        for t in terminaller.values():
            t.kapat()
        for s in arka:
            kapat_grup(s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--denetle", action="store_true")
    ap.add_argument("--listele", action="store_true")
    ap.add_argument("--calistir", action="store_true")
    ap.add_argument("--ekransiz", action="store_true", help="Qt uygulamalarını ekransız (offscreen) çalıştır")
    ap.add_argument("--rapor", help="sonuçları JSON olarak yaz")
    ap.add_argument("--kok", default=str(KOK / "docs"), help="taranacak klasör (varsayılan docs/)")
    ap.add_argument("sayfalar", nargs="*")
    arg = ap.parse_args()

    if arg.sayfalar:
        sayfalar = [pathlib.Path(s).resolve() for s in arg.sayfalar]
    else:
        sayfalar = sorted(pathlib.Path(arg.kok).resolve().rglob("*.md"))
    tum = {s: bloklari_bul(s) for s in sayfalar}
    bloklar = [b for bl in tum.values() for b in bl]

    hatalar = denetle(bloklar)
    sayim = {t: sum(1 for b in bloklar if b.tur == t) for t in TURLER}
    print(f"İşaret denetimi: {len(bloklar)} komut bloğu "
          f"(otomatik {sayim['otomatik']}, arka-plan {sayim['arka-plan']}, elle {sayim['elle']}), {len(hatalar)} hata")
    for h in hatalar:
        print(f"[HATA] {h}")

    if arg.listele:
        for b in bloklar:
            ilk = b.metin.splitlines()[0] if b.metin else ""
            print(f"{b.yer}\t{b.tur}\t{b.baslik or ''}\t{ilk}")

    if hatalar:
        return 1
    if not arg.calistir:
        return 0

    sonuclar = []
    ortam = terminal_ortami(arg.ekransiz)
    for sayfa, bl in tum.items():
        if any(b.tur in ("otomatik", "arka-plan") for b in bl) or any(b.tur == "elle" for b in bl):
            sayfa_calistir(sayfa, bl, ortam, sonuclar)

    dusen = [s for s in sonuclar if s["durum"] == "düştü"]
    for s in sonuclar:
        etiket = {"geçti": "[GEÇTİ]", "düştü": "[DÜŞTÜ]", "elle": "[ELLE] "}[s["durum"]]
        ek = ""
        if s["tur"] == "otomatik":
            ek = f" çıkış={s['cikis']} (beklenen {s['beklenen_cikis']}), {s['sure_sn']} sn"
        elif s["tur"] == "arka-plan":
            ek = f" hazır komutu: {s['hazir_komut']}, {s['sure_sn']} sn"
        else:
            ek = f" ({s['neden']})"
        print(f"{etiket} {s['yer']} {s['tur']}{ek}")
        if s["durum"] == "düştü":
            if s.get("eksik_desen"):
                print(f"         bulunamayan desen: {s['eksik_desen']}")
            for satir in s.get("cikti_son", []):
                print(f"         | {satir}")
    gecen = sum(1 for s in sonuclar if s["durum"] == "geçti")
    elle = sum(1 for s in sonuclar if s["durum"] == "elle")
    print(f"İçerik komutları: {len(sonuclar)} blok, {gecen} geçti, {len(dusen)} düştü, {elle} elle")
    if arg.rapor:
        pathlib.Path(arg.rapor).write_text(json.dumps(sonuclar, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if dusen else 0


if __name__ == "__main__":
    sys.exit(main())
