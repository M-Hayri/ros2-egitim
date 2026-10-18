#!/usr/bin/env bash
# Codespace ya da yerel devcontainer ilk kez oluşturulduğunda bir kez çalışır.
set -e

# Kullanıcının kendi terminallerinde de ROS ortamı hazır olsun.
if ! grep -q "/opt/ros/jazzy/setup.bash" "$HOME/.bashrc" 2>/dev/null; then
  echo "source /opt/ros/jazzy/setup.bash" >> "$HOME/.bashrc"
fi

# rosdep veritabanını güncelle (ağ yoksa uyar, ortamı bozma).
rosdep update --rosdistro jazzy || echo "[UYARI] rosdep update başarısız oldu; daha sonra elle çalıştırın."

echo
echo "Ortam hazır. Kontrol için:  bash scripts/ortam_kontrol.sh"
echo "Masaüstü: 'Ports' sekmesinde 6080 numaralı portu tarayıcıda açın (parola: ros)."
