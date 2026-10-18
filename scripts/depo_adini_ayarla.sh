#!/usr/bin/env bash
# Depo sahibi ve adı belli olunca README ve mkdocs.yml'deki yer tutucuları doldurur.
# Kullanım:  bash scripts/depo_adini_ayarla.sh <sahip> <depo>
# Örnek:     bash scripts/depo_adini_ayarla.sh mavigolge ros2-egitim
set -e

if [ "$#" -ne 2 ]; then
  echo "Kullanım: bash scripts/depo_adini_ayarla.sh <sahip> <depo>"
  exit 1
fi
SAHIP="$1"
DEPO="$2"

cd "$(dirname "$0")/.."

sed -i "s#SAHIP/DEPO#${SAHIP}/${DEPO}#g; s#SAHIP.github.io/DEPO#${SAHIP}.github.io/${DEPO}#g" README.md
sed -i "s|^# repo_url: https://github.com/SAHIP/DEPO|repo_url: https://github.com/${SAHIP}/${DEPO}|; s|^# edit_uri: edit/main/docs/|edit_uri: edit/main/docs/|" mkdocs.yml

echo "Güncellendi: README.md ve mkdocs.yml (${SAHIP}/${DEPO})"
grep -n "${SAHIP}" README.md mkdocs.yml
