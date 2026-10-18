#!/usr/bin/env bash
# Ortam kontrolü: bu betiği çalıştıran terminalde ROS 2 Jazzy ortamının hazır olup
# olmadığını denetler (Ders 0.2).
# Kullanım:  bash scripts/ortam_kontrol.sh
# Çıkış kodu: tüm zorunlu kontroller geçerse 0, biri bile düşerse 1.
#
# Betik ROS'u kendisi yüklemez (source etmez). Bilerek: çağıran terminal
# `source /opt/ros/jazzy/setup.bash` yapmadıysa kontrollerin düşmesi gerekir.
# Betik ayrı bir süreçte çalışır ve terminalin ortam değişkenlerini (PATH,
# ROS_DISTRO ...) miras alır; denetlediği şey tam olarak bu mirastır.

hata=0

kontrol() {
  local ad="$1"; shift
  if "$@" >/dev/null 2>&1; then
    echo "[TAMAM] $ad"
  else
    echo "[HATA]  $ad"
    hata=1
  fi
}

kontrol "ROS_DISTRO = jazzy"            test "${ROS_DISTRO:-}" = "jazzy"
kontrol "ros2 komutu bulunuyor"          command -v ros2
kontrol "turtlesim_node kurulu"          bash -c "ros2 pkg executables turtlesim | grep -q turtlesim_node"
kontrol "turtle_teleop_key kurulu"       bash -c "ros2 pkg executables turtlesim | grep -q turtle_teleop_key"
kontrol "rqt_gui kurulu"                 bash -c "ros2 pkg list | grep -qx rqt_gui"
kontrol "colcon bulunuyor"               command -v colcon
kontrol "rosdep bulunuyor"               command -v rosdep

# Zorunlu olmayan bilgi: grafik ekran (CI'da yoktur, bu normaldir).
if [ -n "${DISPLAY:-}" ]; then
  echo "[BİLGİ] DISPLAY=${DISPLAY} (masaüstü pencereleri buraya açılır)"
else
  echo "[BİLGİ] DISPLAY tanımlı değil (CI'da normal; Codespace'te olmamalı)"
fi

if [ "$hata" -eq 0 ]; then
  echo "Sonuç: ortam hazır."
else
  echo "Sonuç: en az bir kontrol düştü. Yukarıdaki [HATA] satırlarına bakın."
  if [ -z "${ROS_DISTRO:-}" ]; then
    echo "İpucu: bu terminalde ROS ortamı yüklenmemiş. Şunu çalıştırıp tekrar dene:"
    echo "       source /opt/ros/jazzy/setup.bash"
  fi
fi
exit "$hata"
