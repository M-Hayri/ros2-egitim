#!/usr/bin/env bash
# A2 / S3: ortam kontrol betiğini iki yönlü sınar (CI'da devcontainer içinde çalışır).
#   1) ROS yüklü yeni terminal (bash -i, açılış betikleri okunur): 7/7 yeşil, çıkış 0
#   2) Temiz kabuk (env -i bash --norc): kırmızı, ROS_DISTRO maddesi adıyla, çıkış ≠ 0
#   3) Bilgi: ROS yüklü bir kabuktan açılan düz `bash --norc` ortamı miras alır mı?
#      (Ders 0.2'deki "yalnızca bash --norc yetmezdi" cümlesinin kanıtı; eşik değil.)
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

hata=0
girintile() { while IFS= read -r satir; do printf '         | %s\n' "$satir"; done <<<"$1"; }
temiz_yol="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

cikti1=$(env -i HOME="$HOME" PATH="$temiz_yol" TERM=dumb bash -i -c 'bash scripts/ortam_kontrol.sh' 2>&1); kod1=$?
tamam1=$(grep -c '^\[TAMAM\]' <<<"$cikti1")
if [ "$kod1" -eq 0 ] && [ "$tamam1" -eq 7 ]; then
  echo "[GEÇTİ] 1) yüklü terminal: çıkış $kod1, $tamam1/7 [TAMAM]"
else
  echo "[DÜŞTÜ] 1) yüklü terminal: çıkış $kod1, $tamam1/7 [TAMAM]"; girintile "$cikti1"; hata=1
fi

cikti2=$(env -i bash --norc -c 'bash scripts/ortam_kontrol.sh' 2>&1); kod2=$?
if [ "$kod2" -ne 0 ] && grep -q '^\[HATA\]  ROS_DISTRO = jazzy$' <<<"$cikti2"; then
  echo "[GEÇTİ] 2) temiz kabuk (env -i bash --norc): çıkış $kod2, '[HATA]  ROS_DISTRO = jazzy' satırı var, $(grep -c '^\[HATA\]' <<<"$cikti2")/7 [HATA]"
else
  echo "[DÜŞTÜ] 2) temiz kabuk: çıkış $kod2"; girintile "$cikti2"; hata=1
fi

# shellcheck disable=SC1091
cikti3=$(env -i HOME="$HOME" PATH="$temiz_yol" bash -c 'source /opt/ros/jazzy/setup.bash; bash --norc -c "bash scripts/ortam_kontrol.sh"' 2>&1); kod3=$?
echo "[BİLGİ] 3) ROS yüklü kabuktan düz 'bash --norc': çıkış $kod3, $(grep -c '^\[TAMAM\]' <<<"$cikti3")/7 [TAMAM] (0 ve 7/7 ise ortam miras alınıyor demektir)"

exit "$hata"
