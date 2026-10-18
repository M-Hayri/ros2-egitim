#!/usr/bin/env bash
# CI'da devcontainer içinde çalışır: önce ortam kontrolü, sonra derleme ve testler.
# İlk hata bütün işi durdurur. Çıktılar ci-sonuc/ klasörüne de yazılır;
# iş akışı bunları Actions özetine ve notlara aktarır.
set -eo pipefail

cd "$(dirname "$0")/.."
mkdir -p ci-sonuc

# ortam_kontrol.sh ROS'u kendisi yüklemez (Ders 0.2); CI kabuğunda açıkça yüklenir.
# shellcheck disable=SC1091
source /opt/ros/jazzy/setup.bash

bash scripts/ortam_kontrol.sh 2>&1 | tee ci-sonuc/ortam.txt
bash scripts/ci_test.sh 2>&1 | tee ci-sonuc/test.txt
