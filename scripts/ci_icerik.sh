#!/usr/bin/env bash
# CI'da devcontainer içinde çalışır: sitedeki komut bloklarını (S2) ve ortam
# betiğinin iki yönlü davranışını (S3) sınar. Çıktılar ci-sonuc/ klasörüne yazılır.
set -o pipefail
cd "$(dirname "$0")/.." || exit 1
mkdir -p ci-sonuc

durum=0
bash scripts/ci_ortam_iki_yon.sh 2>&1 | tee ci-sonuc/ortam-iki-yon.txt || durum=1
python3 scripts/icerik_komutlari.py --calistir --ekransiz --rapor ci-sonuc/komutlar.json 2>&1 | tee ci-sonuc/komutlar.txt || durum=1
exit "$durum"
