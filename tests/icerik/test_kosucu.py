"""scripts/icerik_komutlari.py için testler (S2). ROS gerektirmez; düz kabuk komutlarıyla
koşucunun hem doğruyu geçirdiğini hem de bozuğu yakaladığını gösterir."""

import json
import os
import pathlib
import subprocess
import sys
import textwrap
import time

KOK = pathlib.Path(__file__).resolve().parents[2]
KOSUCU = KOK / "scripts" / "icerik_komutlari.py"


def kos(tmp_path, metin, *ek):
    sayfa = tmp_path / "sayfa.md"
    sayfa.write_text(textwrap.dedent(metin), encoding="utf-8")
    rapor = tmp_path / "rapor.json"
    sonuc = subprocess.run(
        [sys.executable, str(KOSUCU), *ek, "--rapor", str(rapor), str(sayfa)],
        capture_output=True, text=True, timeout=180,
    )
    veri = json.loads(rapor.read_text(encoding="utf-8")) if rapor.exists() else []
    return sonuc, veri


def test_dogru_sayfa_gecer(tmp_path):
    hazir = tmp_path / "hazir.txt"
    pid = tmp_path / "pid.txt"
    sonuc, veri = kos(tmp_path, f'''
        <!-- test: otomatik; desen: ^merhaba$ -->
        ```bash
        echo merhaba
        ```

        <!-- test: otomatik; cikis: 1 -->
        ```bash
        false
        ```

        Aynı adlı terminal oturumu sürdürür:

        <!-- test: otomatik; terminal: iki -->
        ```bash
        export DENEME=42
        ```

        <!-- test: otomatik; terminal: iki; desen: ^42$ -->
        ```bash
        echo $DENEME
        ```

        <!-- test: otomatik; cikis: 127; desen: komut_yok_xyz: command not found -->
        ```bash
        komut_yok_xyz
        ```

        Blok içinde açılan alt kabuk sonraki satırları okur:

        <!-- test: otomatik; desen: ^SHLVL=2$ -->
        ```bash
        bash --norc
        echo "SHLVL=$SHLVL"
        exit
        ```

        - Liste içinde girintili blok:

            <!-- test: otomatik; desen: ^girintili$ -->
            ```bash
            echo girintili
            ```

        <!-- test: arka-plan; hazir: cat {hazir}; desen: ^hazir$; sure: 15 -->
        ```bash
        echo $$ > {pid}; sleep 1; echo hazir > {hazir}; sleep 300
        ```

        <!-- test: elle; neden: klavye -->
        ```bash title="Test edilmedi · klavye gerekir"
        ros2 run turtlesim turtle_teleop_key
        ```

        Komut olmayan bloklar işaret istemez:

        ```text
        çıktı örneği
        ```
    ''', "--calistir")
    assert sonuc.returncode == 0, sonuc.stdout + sonuc.stderr
    assert "9 blok, 8 geçti, 0 düştü, 1 elle" in sonuc.stdout, sonuc.stdout
    assert [s["durum"] for s in veri].count("geçti") == 8
    # Arka plan süreci sayfa bitince kapatılmış olmalı.
    eski_pid = int(pid.read_text())
    time.sleep(0.5)
    try:
        os.kill(eski_pid, 0)
        hala_calisiyor = True
    except ProcessLookupError:
        hala_calisiyor = False
    assert not hala_calisiyor, "arka plan süreci sayfa sonunda kapatılmadı"


def test_yanlis_cikis_kodu_duser(tmp_path):
    sonuc, veri = kos(tmp_path, '''
        <!-- test: otomatik -->
        ```bash
        exit_kodu_3() { return 3; }; exit_kodu_3
        ```
    ''', "--calistir")
    assert sonuc.returncode == 1
    assert veri[0]["durum"] == "düştü" and veri[0]["cikis"] == 3


def test_eksik_desen_duser(tmp_path):
    sonuc, veri = kos(tmp_path, '''
        <!-- test: otomatik; desen: ^beklenen$ -->
        ```bash
        echo baska
        ```
    ''', "--calistir")
    assert sonuc.returncode == 1
    assert veri[0]["eksik_desen"] == ["^beklenen$"]
    assert "bulunamayan desen" in sonuc.stdout


def test_hazir_olmayan_arka_plan_duser(tmp_path):
    sonuc, veri = kos(tmp_path, '''
        <!-- test: arka-plan; hazir: echo bekleniyor; desen: ^hazir$; sure: 3 -->
        ```bash
        sleep 300
        ```
    ''', "--calistir")
    assert sonuc.returncode == 1
    assert veri[0]["durum"] == "düştü"


def test_zaman_asimi_duser(tmp_path):
    sonuc, veri = kos(tmp_path, '''
        <!-- test: otomatik; sure: 2 -->
        ```bash
        sleep 30
        ```
    ''', "--calistir")
    assert sonuc.returncode == 1
    assert veri[0]["cikis"] == "zaman-asimi"


def test_isaretsiz_blok_denetimde_duser(tmp_path):
    sonuc, _ = kos(tmp_path, '''
        ```bash
        echo işaretsiz
        ```
    ''', "--denetle")
    assert sonuc.returncode == 1
    assert "işaretsiz komut bloğu" in sonuc.stdout


def test_basliksiz_elle_blogu_duser(tmp_path):
    sonuc, _ = kos(tmp_path, '''
        <!-- test: elle; neden: klavye -->
        ```bash
        ros2 run turtlesim turtle_teleop_key
        ```
    ''', "--denetle")
    assert sonuc.returncode == 1
    assert "elle bloğunun başlığı" in sonuc.stdout


def test_otomatik_blok_elle_etiketi_tasiyamaz(tmp_path):
    sonuc, _ = kos(tmp_path, '''
        <!-- test: otomatik -->
        ```bash title="Elle doğrulandı (Hayri, 2026-10-19)"
        echo yanlis etiket
        ```
    ''', "--denetle")
    assert sonuc.returncode == 1
    assert "elle etiketi taşıyamaz" in sonuc.stdout


def test_bilinmeyen_anahtar_duser(tmp_path):
    sonuc, _ = kos(tmp_path, '''
        <!-- test: otomatik; beklentim: x -->
        ```bash
        echo x
        ```
    ''', "--denetle")
    assert sonuc.returncode == 1
    assert "bilinmeyen anahtar" in sonuc.stdout
