#!/usr/bin/env bash
# CI'da devcontainer içinde çalışır: dersler/ altındaki paketleri derler ve testlerini koşar.
# Derleme çıktıları depo dışına (/tmp) yazılır; depo temiz kalır.
set -eo pipefail

# shellcheck disable=SC1091
source /opt/ros/jazzy/setup.bash

CIKTI="${CI_CIKTI:-/tmp/egitim_ci}"
mkdir -p "$CIKTI"

colcon --log-base "$CIKTI/log" build \
  --base-paths dersler \
  --build-base "$CIKTI/build" \
  --install-base "$CIKTI/install"

colcon --log-base "$CIKTI/log" test \
  --base-paths dersler \
  --build-base "$CIKTI/build" \
  --install-base "$CIKTI/install" \
  --event-handlers console_direct+

colcon test-result --test-result-base "$CIKTI/build" --verbose
